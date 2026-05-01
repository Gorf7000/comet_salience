"""Daily light-curve generation per spec §8.

Implements the four-tier magnitude-model fallback (spec §8.2):

    Tier 1   (horizons_tmag)        Horizons T-mag from SBDB-stored M1/K1
    Tier 1.5 (manual_curated)       (M1, K1) from data/raw/comet_sources/manual_M1K1.csv
    Tier 2   (assumed_default_K1)   SBDB M1 only; K1 = config.DEFAULT_K1
    Tier 3   (failed)               No magnitude model; row dropped, summary marks failure

Adaptive window extension per spec §5.4.
"""

from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from . import config
from .source_jpl import (extract_M1_K1, horizons_id_for, lookup_sbdb,
                         query_horizons_daily)

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Tier 1.5: manual curated CSV
# ----------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_manual_M1K1() -> dict[str, dict]:
    """Load the manual M1/K1 CSV. Returns dict keyed by pdes (with whitespace
    preserved as in SBDB), value is dict with keys M1, K1, source_citation, notes.
    """
    path = config.DATA_INPUTS / "manual_M1K1.csv"
    if not path.exists():
        return {}
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return {}
    out = {}
    for _, r in df.iterrows():
        if pd.notna(r.get("pdes")) and pd.notna(r.get("M1")) and pd.notna(r.get("K1")):
            out[str(r["pdes"]).strip()] = {
                "M1": float(r["M1"]),
                "K1": float(r["K1"]),
                "source_citation": str(r.get("source_citation", "")),
                "notes": str(r.get("notes", "")),
            }
    logger.info("Loaded %d manual M1/K1 entries from %s", len(out), path.name)
    return out


# ----------------------------------------------------------------------
# Magnitude-model resolution (Tier 1 / 1.5 / 2 / 3)
# ----------------------------------------------------------------------

@dataclass
class MagModel:
    M1: float | None
    K1: float | None
    # 'horizons_tmag' | 'manual_curated' | 'manual_curated_override'
    # | 'assumed_default_K1' | 'failed'
    provenance: str
    source_citation: str = ""
    sbdb_M1: float | None = None    # what SBDB stored, regardless of which we use
    sbdb_K1: float | None = None
    sbdb_M2: float | None = None    # for audit: presence of nuclear params
    sbdb_K2: float | None = None
    conflict_with_sbdb: bool = False  # for audit if manual entry overlaps SBDB
    sbdb_nuclear_biased: bool = False  # SBDB K1 below NUCLEAR_FIT_K1_THRESHOLD


def resolve_magnitude_model(query_pdes: str, sbdb_pdes: str = "") -> MagModel:
    """Determine which tier applies for an apparition's magnitude model.

    query_pdes is the SBDB pdes for non-periodic, or e.g. "1P" for periodic.
    """
    # SBDB lookup (always done — needed for both Tier 1 path and conflict detection)
    payload = lookup_sbdb(sbdb_pdes or query_pdes)
    sbdb_M1, sbdb_K1 = extract_M1_K1(payload)
    M2 = K2 = None
    if payload:
        for entry in payload.get("phys_par") or []:
            try:
                v = float(entry.get("value"))
            except (TypeError, ValueError):
                continue
            if entry.get("name") == "M2":
                M2 = v
            elif entry.get("name") == "K2":
                K2 = v

    manual = _load_manual_M1K1()
    manual_entry = manual.get((sbdb_pdes or query_pdes).strip())

    sbdb_nuclear = (sbdb_K1 is not None
                    and sbdb_K1 < config.NUCLEAR_FIT_K1_THRESHOLD)

    # Tier 1: SBDB has both M1 and K1 with an active-coma slope.
    # Spec §8.2 rule 3: SBDB wins on conflict — except where SBDB looks
    # nuclear-biased (K1 < threshold), in which case manual overrides.
    if sbdb_M1 is not None and sbdb_K1 is not None and not sbdb_nuclear:
        conflict = manual_entry is not None
        return MagModel(M1=sbdb_M1, K1=sbdb_K1,
                        provenance="horizons_tmag",
                        sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                        sbdb_M2=M2, sbdb_K2=K2,
                        conflict_with_sbdb=conflict,
                        sbdb_nuclear_biased=False)

    # Tier 1.5 override: SBDB has values but they're nuclear-biased,
    # and a manual entry exists. Manual wins; provenance tagged distinctly.
    if sbdb_nuclear and manual_entry is not None:
        return MagModel(M1=manual_entry["M1"], K1=manual_entry["K1"],
                        provenance="manual_curated_override",
                        source_citation=manual_entry["source_citation"],
                        sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                        sbdb_M2=M2, sbdb_K2=K2,
                        sbdb_nuclear_biased=True)

    # SBDB nuclear-biased but no manual entry: stuck with SBDB but flagged.
    if sbdb_M1 is not None and sbdb_K1 is not None and sbdb_nuclear:
        return MagModel(M1=sbdb_M1, K1=sbdb_K1,
                        provenance="horizons_tmag",
                        sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                        sbdb_M2=M2, sbdb_K2=K2,
                        sbdb_nuclear_biased=True)

    # Tier 1.5 gap-fill: SBDB has nothing usable, manual entry exists.
    if manual_entry is not None:
        return MagModel(M1=manual_entry["M1"], K1=manual_entry["K1"],
                        provenance="manual_curated",
                        source_citation=manual_entry["source_citation"],
                        sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                        sbdb_M2=M2, sbdb_K2=K2)

    # Tier 2: SBDB has M1 only
    if sbdb_M1 is not None:
        return MagModel(M1=sbdb_M1, K1=config.DEFAULT_K1,
                        provenance="assumed_default_K1",
                        sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                        sbdb_M2=M2, sbdb_K2=K2)

    # Tier 3: nothing usable
    return MagModel(M1=None, K1=None, provenance="failed",
                    sbdb_M1=sbdb_M1, sbdb_K1=sbdb_K1,
                    sbdb_M2=M2, sbdb_K2=K2)


def compute_magnitude(r_au: float, delta_au: float, M1: float, K1: float) -> float:
    """Standard total comet visual magnitude law: m = M1 + 5 log10(Δ) + K1 log10(r)."""
    if r_au <= 0 or delta_au <= 0:
        return float("nan")
    return M1 + 5.0 * math.log10(delta_au) + K1 * math.log10(r_au)


# ----------------------------------------------------------------------
# Window construction & adaptive extension
# ----------------------------------------------------------------------

def initial_window(perihelion_date: str | None, discovery_date: str | None
                   ) -> tuple[str, str, str]:
    """Per spec §5.3: ±DEFAULT_WINDOW_DAYS around perihelion or discovery.

    Returns (start_iso, end_iso, anchor_kind) where anchor_kind is
    'perihelion' or 'discovery'. Raises ValueError if neither date present.
    """
    anchor = None
    kind = None
    for d, k in [(perihelion_date, "perihelion"), (discovery_date, "discovery")]:
        if d and isinstance(d, str) and re.match(r"\d{4}-\d{2}-\d{2}", d):
            anchor = datetime.fromisoformat(d[:10])
            kind = k
            break
    if anchor is None:
        raise ValueError("no usable anchor date")
    start = anchor - timedelta(days=config.DEFAULT_WINDOW_DAYS)
    end = anchor + timedelta(days=config.DEFAULT_WINDOW_DAYS)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), kind


def adaptive_extend(daily: pd.DataFrame, anchor_date: str,
                    cur_start: str, cur_end: str) -> tuple[str, str, bool, str]:
    """Per spec §5.4: extend window if mag<=6 occurs near boundary.

    Returns (new_start, new_end, was_extended, reason).
    """
    if "apparent_mag" not in daily.columns:
        return cur_start, cur_end, False, ""
    valid = daily.dropna(subset=["apparent_mag"]).copy()
    if valid.empty:
        return cur_start, cur_end, False, ""
    valid["date"] = pd.to_datetime(valid["date"])
    anchor = datetime.fromisoformat(anchor_date)

    s = datetime.fromisoformat(cur_start)
    e = datetime.fromisoformat(cur_end)
    extended = False
    reasons = []

    # Check whether mag<=6 occurs within boundary window
    near_start = valid[valid["date"] <= s + timedelta(days=config.WINDOW_EXTENSION_BOUNDARY_DAYS)]
    near_end = valid[valid["date"] >= e - timedelta(days=config.WINDOW_EXTENSION_BOUNDARY_DAYS)]

    if (near_start["apparent_mag"] <= config.NAKED_EYE_MAG_THRESHOLD).any():
        proposed = s - timedelta(days=config.WINDOW_EXTENSION_STEP_DAYS)
        max_back = anchor - timedelta(days=config.MAX_WINDOW_DAYS)
        if proposed >= max_back:
            s = proposed
            extended = True
            reasons.append("extended pre-perihelion (boundary mag<=6)")
        else:
            s = max_back
            extended = True
            reasons.append("extended pre-perihelion to MAX_WINDOW cap")
    if (near_end["apparent_mag"] <= config.NAKED_EYE_MAG_THRESHOLD).any():
        proposed = e + timedelta(days=config.WINDOW_EXTENSION_STEP_DAYS)
        max_fwd = anchor + timedelta(days=config.MAX_WINDOW_DAYS)
        if proposed <= max_fwd:
            e = proposed
            extended = True
            reasons.append("extended post-perihelion (boundary mag<=6)")
        else:
            e = max_fwd
            extended = True
            reasons.append("extended post-perihelion to MAX_WINDOW cap")

    return s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"), extended, "; ".join(reasons)


# ----------------------------------------------------------------------
# Build daily light curve for one apparition
# ----------------------------------------------------------------------

def _normalize_horizons_columns(eph: pd.DataFrame) -> pd.DataFrame:
    """Standardize Horizons output column names. Keep the originals too for audit."""
    out = eph.copy()
    out.columns = [str(c) for c in out.columns]
    rename_map = {}
    for src, tgt in [("datetime_str", "date_str"), ("r", "heliocentric_distance_au"),
                     ("delta", "geocentric_distance_au"), ("alpha", "phase_angle_deg")]:
        if src in out.columns:
            rename_map[src] = tgt
    out = out.rename(columns=rename_map)
    if "date_str" in out.columns:
        out["date"] = pd.to_datetime(out["date_str"], errors="coerce").dt.date
    return out


def generate_for_apparition(row: pd.Series, refresh: bool = False) -> tuple[pd.DataFrame | None, dict]:
    """Generate a daily light curve for a single apparition row from the scaffold.

    Returns (daily_df or None, meta_dict). meta_dict carries window info,
    magnitude provenance, and failure reasons for the apparition summary.
    """
    apparition_id = row["apparition_id"]
    meta = {
        "apparition_id": apparition_id,
        "window_start": "", "window_end": "", "window_extended": False,
        "window_extension_reason": "",
        "magnitude_provenance": "failed",
        "manual_curated_source_citation": "",
        "failed_horizons_match": False,
        "failed_light_curve": False,
        "missing_magnitude_model": False,
        "missing_perihelion_date": not bool(row.get("perihelion_date")),
        "no_light_curve_window": False,
        "audit_notes": "",
        "magnitude_quality": "failed",
        "sbdb_M1": None, "sbdb_K1": None,
        "sbdb_M2_present": False, "sbdb_K2_present": False,
        "manual_sbdb_conflict": False,
        "sbdb_nuclear_biased": False,
    }

    try:
        win_start, win_end, anchor_kind = initial_window(
            row.get("perihelion_date"), row.get("discovery_date")
        )
    except ValueError:
        meta["no_light_curve_window"] = True
        meta["failed_light_curve"] = True
        meta["audit_notes"] = "no usable anchor date"
        return None, meta
    anchor_date = row["perihelion_date"][:10] if anchor_kind == "perihelion" else row["discovery_date"][:10]
    meta["window_start"], meta["window_end"] = win_start, win_end

    # Resolve magnitude model first — Tier 3 short-circuits without Horizons
    sbdb_pdes = row.get("sbdb_pdes") or row.get("query_pdes")
    mag_model = resolve_magnitude_model(row["query_pdes"], sbdb_pdes)
    meta["magnitude_provenance"] = mag_model.provenance
    meta["manual_curated_source_citation"] = mag_model.source_citation
    meta["sbdb_M1"] = mag_model.sbdb_M1
    meta["sbdb_K1"] = mag_model.sbdb_K1
    meta["sbdb_M2_present"] = mag_model.sbdb_M2 is not None
    meta["sbdb_K2_present"] = mag_model.sbdb_K2 is not None
    meta["manual_sbdb_conflict"] = mag_model.conflict_with_sbdb
    meta["sbdb_nuclear_biased"] = mag_model.sbdb_nuclear_biased

    if mag_model.provenance == "failed":
        meta["missing_magnitude_model"] = True
        meta["failed_light_curve"] = True
        meta["audit_notes"] = "no SBDB M1/K1 and no manual entry"
        return None, meta

    # Quality label
    if mag_model.provenance == "horizons_tmag":
        meta["magnitude_quality"] = "low" if mag_model.sbdb_nuclear_biased else "high"
    elif mag_model.provenance in ("manual_curated", "manual_curated_override",
                                   "assumed_default_K1"):
        meta["magnitude_quality"] = "medium"

    # Build Horizons id and query
    prefix = row.get("sbdb_prefix") or ("P" if row.get("is_periodic") else "C")
    hid = horizons_id_for(row["query_pdes"], int(row["apparition_year"]), prefix)
    cache_key = f"{apparition_id}__{win_start}_{win_end}"
    eph = query_horizons_daily(hid, win_start, win_end, cache_key, refresh=refresh)
    if eph is None or len(eph) == 0:
        meta["failed_horizons_match"] = True
        meta["failed_light_curve"] = True
        meta["audit_notes"] = f"horizons query failed for {hid}"
        return None, meta

    eph = _normalize_horizons_columns(eph)

    # Build apparent_mag column per tier
    daily = eph.copy()
    if mag_model.provenance == "horizons_tmag" and "Tmag" in daily.columns:
        daily["apparent_mag"] = pd.to_numeric(daily["Tmag"], errors="coerce")
    else:
        # Tier 1.5 or Tier 2: compute from r and Δ using mag_model.M1, mag_model.K1
        r = pd.to_numeric(daily.get("heliocentric_distance_au"), errors="coerce")
        d = pd.to_numeric(daily.get("geocentric_distance_au"), errors="coerce")
        with np.errstate(invalid="ignore", divide="ignore"):
            daily["apparent_mag"] = (
                mag_model.M1
                + 5.0 * np.log10(d.where(d > 0))
                + mag_model.K1 * np.log10(r.where(r > 0))
            )

    # Drop rows with no usable mag — but only if zero useful rows result, mark fail
    if daily["apparent_mag"].notna().sum() == 0:
        meta["failed_light_curve"] = True
        meta["audit_notes"] = "horizons returned rows but apparent_mag all NaN"
        return None, meta

    # Adaptive window extension
    new_start, new_end, extended, reason = adaptive_extend(daily, anchor_date, win_start, win_end)
    if extended:
        meta["window_extended"] = True
        meta["window_extension_reason"] = reason
        # Re-query with extended window
        cache_key2 = f"{apparition_id}__{new_start}_{new_end}"
        eph2 = query_horizons_daily(hid, new_start, new_end, cache_key2, refresh=refresh)
        if eph2 is not None and len(eph2) > len(eph):
            eph2 = _normalize_horizons_columns(eph2)
            daily = eph2.copy()
            if mag_model.provenance == "horizons_tmag" and "Tmag" in daily.columns:
                daily["apparent_mag"] = pd.to_numeric(daily["Tmag"], errors="coerce")
            else:
                r = pd.to_numeric(daily.get("heliocentric_distance_au"), errors="coerce")
                d = pd.to_numeric(daily.get("geocentric_distance_au"), errors="coerce")
                with np.errstate(invalid="ignore", divide="ignore"):
                    daily["apparent_mag"] = (
                        mag_model.M1
                        + 5.0 * np.log10(d.where(d > 0))
                        + mag_model.K1 * np.log10(r.where(r > 0))
                    )
            meta["window_start"], meta["window_end"] = new_start, new_end

    # Decorate with apparition-level fields per spec §8
    daily["apparition_id"] = apparition_id
    daily["comet_id"] = row["comet_id"]
    daily["comet_name"] = row["comet_name"]
    daily["designation"] = row["designation"]
    daily["source_object_id"] = row["query_pdes"]
    daily["perihelion_date"] = row.get("perihelion_date") or ""
    if daily["perihelion_date"].iloc[0]:
        peri_dt = pd.to_datetime(daily["perihelion_date"].iloc[0])
        daily["days_from_perihelion"] = (
            pd.to_datetime(daily["date"]) - peri_dt
        ).dt.days
    else:
        daily["days_from_perihelion"] = pd.NA
    daily["magnitude_model_provenance"] = mag_model.provenance
    daily["manual_curated_source_citation"] = mag_model.source_citation
    daily["raw_ephemeris_source"] = "JPL Horizons"
    daily["light_curve_quality_flag"] = meta["magnitude_quality"]

    return daily, meta
