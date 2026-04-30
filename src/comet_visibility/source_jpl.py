"""JPL SBDB and Horizons sources.

Two roles:

1. **Enumeration of non-periodic comets** in the spec date range. AERITH
   does not catalog historical non-periodic ("C/...") comets, so SBDB
   is the primary source for that population. All such comets get the
   AERITH-equivalent status "Discovered" (=> event_case unexpected_seen),
   since by definition a one-shot first appearance is unexpected.

2. **Per-apparition lookups**: SBDB photometric parameters (M1, K1) and
   Horizons daily ephemerides (T-mag, distances). These feed the
   light-curve generator (spec §8) and the Tier 1/2/3 magnitude-model
   fallback (spec §8.2).

All responses cached locally per spec §15.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

import pandas as pd
import requests
from astropy.time import Time

from . import config

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# SBDB enumeration (bulk query)
# ----------------------------------------------------------------------

def _sbdb_query_cache_path(start_jd: float, end_jd: float) -> Path:
    return config.SBDB_CACHE / f"query_tp_{start_jd:.1f}_{end_jd:.1f}.json"


def enumerate_comets_by_perihelion(
    start_date: str = config.START_DATE,
    end_date: str = config.END_DATE,
    refresh: bool = False,
) -> pd.DataFrame:
    """Enumerate all comets in SBDB whose representative perihelion (tp) falls
    inside [start_date, end_date].

    Note: for periodic comets, SBDB stores one representative epoch — so a
    multi-apparition periodic comet returns at most one row here, and that row
    may or may not fall inside the date window. Periodic apparitions are
    handled by the AERITH source module instead. This enumeration is primarily
    used to capture non-periodic comets.

    Returns one row per SBDB record.
    """
    start_jd = Time(start_date).jd
    end_jd = Time(end_date).jd + 1.0  # inclusive end

    cache = _sbdb_query_cache_path(start_jd, end_jd)
    if cache.exists() and not refresh and config.CACHE_REMOTE_QUERIES:
        data = json.loads(cache.read_text(encoding="utf-8"))
    else:
        params = {
            "fields": "full_name,name,pdes,prefix,kind,epoch,e,a,q,tp,producer",
            "sb-kind": "c",
            "sb-cdata": json.dumps({"AND": [f"tp|GE|{start_jd}", f"tp|LE|{end_jd}"]}),
            "full-prec": "1",
        }
        logger.info("SBDB query: comets with tp in [%s, %s]", start_date, end_date)
        r = requests.get(config.SBDB_QUERY_API, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        cache.write_text(json.dumps(data), encoding="utf-8")

    cols = data["fields"]
    df = pd.DataFrame(data["data"], columns=cols)
    # Compute ISO perihelion date from tp (JD)
    df["tp"] = pd.to_numeric(df["tp"], errors="coerce")
    df["perihelion_date"] = df["tp"].apply(
        lambda jd: Time(jd, format="jd").iso[:10] if pd.notnull(jd) else None
    )
    df["perihelion_year"] = pd.to_datetime(df["perihelion_date"], errors="coerce").dt.year
    return df


# ----------------------------------------------------------------------
# SBDB single-comet lookup (for M1/K1)
# ----------------------------------------------------------------------

def _sbdb_lookup_cache_path(designation: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", designation)
    return config.SBDB_CACHE / f"lookup_{safe}.json"


def lookup_sbdb(designation: str, refresh: bool = False) -> dict:
    """Single-comet SBDB lookup. Returns the full JSON payload (or {} on fail).

    Used to extract M1/K1 photometric parameters per spec §8.2 Tier 1/2 logic.
    """
    cache = _sbdb_lookup_cache_path(designation)
    if cache.exists() and not refresh and config.CACHE_REMOTE_QUERIES:
        return json.loads(cache.read_text(encoding="utf-8"))
    params = {"sstr": designation, "phys-par": "1", "full-prec": "1"}
    logger.debug("SBDB lookup: %s", designation)
    try:
        r = requests.get(config.SBDB_LOOKUP_API, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        logger.warning("SBDB lookup failed for %s: %s", designation, e)
        return {}
    cache.write_text(json.dumps(data), encoding="utf-8")
    time.sleep(config.HTTP_THROTTLE_SEC)
    return data


def extract_M1_K1(sbdb_payload: dict) -> tuple[float | None, float | None]:
    """Pull (M1, K1) from a SBDB lookup payload, or (None, None) if absent.

    SBDB physics parameters list is at payload['phys_par']; each entry has
    'name' and 'value'. We want 'M1' (total magnitude) and 'K1' (slope).
    """
    if not sbdb_payload:
        return None, None
    phys = sbdb_payload.get("phys_par") or []
    M1 = K1 = None
    for entry in phys:
        nm = entry.get("name")
        try:
            val = float(entry.get("value"))
        except (TypeError, ValueError):
            continue
        if nm == "M1":
            M1 = val
        elif nm == "K1":
            K1 = val
    return M1, K1


# ----------------------------------------------------------------------
# Horizons daily ephemeris
# ----------------------------------------------------------------------

def _horizons_cache_path(comet_id: str, perihelion_year: int, start: str, end: str) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9]", "", comet_id)
    return config.HORIZONS_CACHE / f"{safe_id}_{perihelion_year}_{start}_{end}.csv"


def horizons_id_for(comet_id: str, perihelion_year: int, prefix: str | None) -> str:
    """Construct the Horizons id string that resolves a single apparition.

    For periodic comets we use 'DES=NP;CAP<YYYY+1;' to pick the closest
    apparition prior to year+1. For non-periodic, the designation alone
    (e.g., 'C/1858 L1') uniquely identifies the comet.
    """
    if prefix in ("P", "D"):
        return f"DES={comet_id};CAP<{perihelion_year + 1};"
    return f"DES={comet_id};"


def query_horizons_daily(
    horizons_id: str,
    start_date: str,
    end_date: str,
    cache_key: str,
    refresh: bool = False,
) -> pd.DataFrame | None:
    """Query Horizons for a daily ephemeris over [start_date, end_date].

    Returns a DataFrame with at minimum: datetime_str, r, delta, Tmag, Nmag,
    alpha (phase angle). Returns None on failure.
    """
    cache = config.HORIZONS_CACHE / f"{cache_key}.csv"
    if cache.exists() and not refresh and config.CACHE_REMOTE_QUERIES:
        return pd.read_csv(cache)

    from astroquery.jplhorizons import Horizons
    try:
        obj = Horizons(
            id=horizons_id,
            location=config.HORIZONS_OBSERVER_LOC,
            epochs={"start": start_date, "stop": end_date, "step": "1d"},
            id_type=None,
        )
        eph = obj.ephemerides()
    except Exception as e:
        logger.warning("Horizons query failed for %s [%s..%s]: %s",
                       horizons_id, start_date, end_date, e)
        return None

    df = eph.to_pandas()
    df.to_csv(cache, index=False)
    time.sleep(config.HTTP_THROTTLE_SEC)
    return df
