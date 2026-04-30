"""Combine AERITH (periodic) + SBDB (non-periodic) into one apparition scaffold.

Per spec §3, the unit of analysis is one apparition. Per the source-architecture
discussion in this session:

- AERITH is the primary scaffold for periodic comets (full historical coverage,
  rich expected/seen statuses).
- SBDB is the source for non-periodic comets in scope (AERITH only catalogs
  non-periodic comets observed since 1995).

Fragment merging: SBDB stores post-split fragments separately (e.g.,
C/1882 R1-A, R1-B, R1-C, R1-D for the Great September Comet of 1882). For
analysis purposes the parent comet is the unit, so we collapse fragments
that share a base designation, taking the earliest perihelion and
preserving fragment metadata in `merged_fragments`.
"""

from __future__ import annotations

import re
import logging
import pandas as pd

from . import config
from .source_aerith import filter_to_scope
from .source_jpl import enumerate_comets_by_perihelion
from .status_mapping import apply_status_mapping

logger = logging.getLogger(__name__)


FRAGMENT_RE = re.compile(r"^(.+?)-([A-Z])$")


def _merge_fragments(sbdb: pd.DataFrame) -> pd.DataFrame:
    """Collapse pdes like '1882 R1-A', '1882 R1-B', ... into single '1882 R1' rows.

    Strategy:
      - Group rows whose pdes shares a base (everything before '-X' fragment letter).
      - Earliest perihelion date wins.
      - Keep alphabetically-first fragment's pdes as `query_pdes` so Horizons
        ephemeris queries have a unique target.
      - Record merged fragment list in `merged_fragments`.
    """
    rows = []
    sbdb = sbdb.copy()
    sbdb["_base"] = sbdb["pdes"].apply(
        lambda d: FRAGMENT_RE.match(d).group(1) if FRAGMENT_RE.match(d) else d
    )
    for base, group in sbdb.groupby("_base"):
        if len(group) == 1:
            r = group.iloc[0].to_dict()
            r["query_pdes"] = r["pdes"]
            r["merged_fragments"] = ""
            rows.append(r)
        else:
            sorted_group = group.sort_values("pdes")
            earliest = group.sort_values("perihelion_date").iloc[0]
            merged = earliest.to_dict()
            # Display under the base designation
            merged["pdes"] = base
            merged["full_name"] = re.sub(r"-[A-Z]\b", "", str(earliest["full_name"]))
            # Use first fragment for ephemeris query (Horizons can't resolve the parent)
            merged["query_pdes"] = sorted_group.iloc[0]["pdes"]
            merged["merged_fragments"] = ",".join(sorted_group["pdes"].tolist())
            rows.append(merged)
    out = pd.DataFrame(rows).drop(columns=["_base"], errors="ignore")
    return out


def make_apparition_id(comet_id: str, year: int) -> str:
    """Deterministic apparition_id per spec §15.1.

    comet_id is the JPL/MPC primary designation with whitespace removed.
    """
    cid = comet_id.replace(" ", "").replace("/", "_")
    return f"{cid}_{year}"


def build_combined_scaffold(refresh: bool = False) -> pd.DataFrame:
    """Return the unified apparition scaffold (AERITH periodic + SBDB non-periodic)
    with status coding applied and apparition_id assigned.

    Assumes AERITH raw scrape has already been written by source_aerith.scrape_all_apparitions
    and saved at data/intermediate/aerith_apparitions_raw.csv.
    """
    ae_raw = pd.read_csv(config.DATA_INTERMEDIATE / "aerith_apparitions_raw.csv")
    ae = filter_to_scope(ae_raw)
    ae_in = ae[ae["in_scope"]].copy()

    # ------------------------------------------------------------------
    # AERITH periodic side
    # ------------------------------------------------------------------
    ae_unified = pd.DataFrame({
        "raw_status_source": "AERITH",
        "comet_id": ae_in["comet_id"].str.lstrip("0"),  # 0001P -> 1P
        "comet_name": ae_in["comet_name"],
        "designation": ae_in["designation"],
        "apparition_year": ae_in["perihelion_year"],
        "perihelion_date": ae_in["perihelion_date"],
        "discovery_date": "",
        "raw_aerith_status": ae_in["raw_aerith_status"],
        "sbdb_pdes": "",
        "sbdb_prefix": "",
        "query_pdes": ae_in["comet_id"].str.lstrip("0"),  # e.g. "1P", needs CAP suffix at query time
        "merged_fragments": "",
        "is_periodic": True,
    })

    # ------------------------------------------------------------------
    # SBDB non-periodic side
    # ------------------------------------------------------------------
    sb = enumerate_comets_by_perihelion(refresh=refresh)
    sb_nonper = sb[sb["prefix"] == "C"].copy()
    sb_in = sb_nonper[(sb_nonper["perihelion_year"] >= config.START_YEAR) &
                      (sb_nonper["perihelion_year"] <= config.END_YEAR)].copy()
    sb_merged = _merge_fragments(sb_in)
    logger.info("SBDB non-periodic: %d raw rows -> %d after fragment merge",
                len(sb_in), len(sb_merged))

    sb_unified = pd.DataFrame({
        "raw_status_source": "SBDB",
        "comet_id": sb_merged["pdes"].apply(lambda d: "C/" + d),
        "comet_name": sb_merged["full_name"].str.strip(),
        "designation": sb_merged["full_name"].str.strip(),
        "apparition_year": sb_merged["perihelion_year"],
        "perihelion_date": sb_merged["perihelion_date"],
        "discovery_date": "",
        "raw_aerith_status": "Discovered",  # synthesized: non-periodic = unexpected_seen
        "sbdb_pdes": sb_merged["pdes"],
        "sbdb_prefix": sb_merged["prefix"],
        "query_pdes": sb_merged["query_pdes"],
        "merged_fragments": sb_merged["merged_fragments"],
        "is_periodic": False,
    })

    scaffold = pd.concat([ae_unified, sb_unified], ignore_index=True)
    coded = apply_status_mapping(scaffold)

    coded["apparition_id"] = coded.apply(
        lambda r: make_apparition_id(r["comet_id"], int(r["apparition_year"])), axis=1
    )
    coded["apparition_id_source"] = "perihelion"

    dupes = coded["apparition_id"].duplicated().sum()
    if dupes:
        logger.warning("Found %d duplicate apparition_ids in scaffold", dupes)

    return coded
