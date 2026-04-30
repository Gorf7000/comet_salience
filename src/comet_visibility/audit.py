"""Audit report builder per spec §13."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from . import config


def write_audit_report(scaffold: pd.DataFrame, summary: pd.DataFrame,
                       daily: pd.DataFrame, validation_failures: list[str]) -> Path:
    """Write the Markdown audit report. Returns the path written."""
    path = config.REPORTS / "comet_visibility_audit.md"
    lines: list[str] = []

    def add(s: str = ""):
        lines.append(s)

    add(f"# Comet Visibility Audit Report")
    add(f"_Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_")
    add()
    add("## Summary counts")
    add()
    add(f"- Raw apparition records collected: {len(scaffold)}")
    in_scope = scaffold[(scaffold['apparition_year'] >= config.START_YEAR) &
                        (scaffold['apparition_year'] <= config.END_YEAR)]
    add(f"- Records in 1850–1940 scope: {len(in_scope)}")
    add(f"- Records by raw_status_source: " +
        ", ".join(f"{k}={v}" for k, v in scaffold['raw_status_source'].value_counts().items()))
    add()

    matched = summary[~summary.get('failed_horizons_match', False).fillna(False).astype(bool)]
    add(f"- Successfully matched to ephemeris source: {len(matched)}")
    add(f"- Failed Horizons/JPL match: {summary.get('failed_horizons_match', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add(f"- Missing perihelion date: {summary.get('missing_perihelion_date', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add(f"- No usable light-curve window: {summary.get('no_light_curve_window', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add(f"- Successful daily light curves: {summary.get('failed_light_curve', pd.Series(dtype=bool)).fillna(False).astype(bool).eq(False).sum()}")
    pm = pd.to_numeric(summary.get('peak_mag'), errors='coerce')
    add(f"- peak_mag <= {config.NAKED_EYE_MAG_THRESHOLD}: {(pm <= config.NAKED_EYE_MAG_THRESHOLD).sum()}")
    add(f"- main_sample_candidate = true: {summary.get('main_sample_candidate', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add()

    add("## Counts by event_case")
    add()
    if 'event_case' in summary.columns:
        for k, v in summary['event_case'].value_counts().items():
            add(f"- {k}: {v}")
    add()

    add("## Magnitude model provenance (per apparition)")
    add()
    if 'magnitude_provenance' in summary.columns:
        for k, v in summary['magnitude_provenance'].value_counts().items():
            add(f"- {k}: {v}")
    add()

    add("## Magnitude quality (per apparition)")
    add()
    if 'magnitude_quality' in summary.columns:
        for k, v in summary['magnitude_quality'].value_counts().items():
            add(f"- {k}: {v}")
    add()

    add("## Adaptive window statistics")
    add()
    we = summary.get('window_extended', pd.Series(dtype=bool)).fillna(False).astype(bool)
    add(f"- Apparitions with extended window: {we.sum()}")
    if 'window_extension_reason' in summary.columns:
        capped = summary['window_extension_reason'].astype(str).str.contains("MAX_WINDOW cap").sum()
        add(f"- Apparitions hitting MAX_WINDOW cap: {capped}")
    add()

    add("## SBDB nuclear (M2/K2) parameters present but unused")
    add()
    add(f"- Apparitions with M2 stored in SBDB but unused per §8.2: "
        f"{summary.get('sbdb_M2_present', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add(f"- Apparitions with K2 stored in SBDB but unused: "
        f"{summary.get('sbdb_K2_present', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add()

    add("## Manual / SBDB conflicts")
    add()
    add(f"- Apparitions where manual M1/K1 entry was overridden by SBDB (per spec §8.2): "
        f"{summary.get('manual_sbdb_conflict', pd.Series(dtype=bool)).fillna(False).astype(bool).sum()}")
    add()

    add("## Manual M1/K1 candidates (Tier 3 non-periodics)")
    add()
    add("These non-periodic apparitions in scope have no SBDB photometric parameters")
    add("and produced no light curve. They are candidates for manual entry into")
    add("`data/raw/comet_sources/manual_M1K1.csv`. Sorted by perihelion year then")
    add("alphabetical by designation. Adding rows here and re-running the pipeline")
    add("will generate light curves for those apparitions.")
    add()
    candidates = summary[(summary.get('failed_light_curve', False).fillna(False).astype(bool)) &
                          (summary.get('magnitude_provenance', '') == 'failed') &
                          (summary['raw_status_source'] == 'SBDB')].copy()
    candidates = candidates.sort_values(['apparition_year', 'comet_name'])
    add(f"Total Tier 3 non-periodic candidates: **{len(candidates)}**")
    add()
    add("| pdes | comet_name | perihelion_date |")
    add("|---|---|---|")
    for _, row in candidates.iterrows():
        pdes = row.get('sbdb_pdes', '') or ''
        nm = str(row.get('comet_name', ''))[:60]
        peri = str(row.get('perihelion_date', ''))[:10]
        add(f"| {pdes} | {nm} | {peri} |")
    add()

    add("## Caveats")
    add()
    add("- City/topocentric visibility is not implemented in this increment.")
    add("- `mag_le_6 = true` reflects integrated magnitude only. A large diffuse")
    add("  comet at integrated mag 5 may have appeared dimmer to the eye than a")
    add("  compact comet at the same magnitude. Surface-brightness modeling is")
    add("  deferred to the city-visibility increment.")
    add("- The photometric law is applied symmetrically around perihelion")
    add("  (`photometric_law = symmetric`). Pre- vs. post-perihelion asymmetric")
    add("  activity slopes are not fit.")
    add("- No hand-curated `M1`/`K1` overrides have been applied; the manual CSV")
    add("  only fills SBDB gaps (Tier 1.5), and SBDB takes precedence on conflict.")
    add("- AERITH does not catalog non-periodic comets observed before 1995.")
    add("  Non-periodic apparitions in 1850–1940 are sourced from JPL SBDB and")
    add("  uniformly assigned `event_case = unexpected_seen` (synthetic AERITH")
    add("  status `Discovered`), since by definition a one-shot first appearance")
    add("  is unexpected.")
    add("- C/1882 R1 (Great September Comet) post-split fragments R1-A through R1-D")
    add("  are merged into a single apparition row using the earliest perihelion")
    add("  and R1-A's geometry for ephemeris. Original fragment list is preserved")
    add("  in the `merged_fragments` field.")
    add()

    add("## Validation failures")
    add()
    if not validation_failures:
        add("_None._")
    else:
        for v in validation_failures:
            add(f"- {v}")
    add()

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
