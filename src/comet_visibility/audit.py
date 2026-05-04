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
    add(f"- Manual gap-fill entries (provenance = `manual_curated`, SBDB had nothing): "
        f"{(summary.get('magnitude_provenance', pd.Series(dtype=str)) == 'manual_curated').sum()}")
    add(f"- Manual override entries (provenance = `manual_curated_override`, "
        f"SBDB had values but manual is preferred per spec §8.2): "
        f"{(summary.get('magnitude_provenance', pd.Series(dtype=str)) == 'manual_curated_override').sum()}")
    add()

    add("## Nuclear-biased SBDB fits (K1 below threshold)")
    add()
    add(f"SBDB sometimes stores (M1, K1) values that look like nuclear/asteroidal")
    add(f"photometry rather than total cometary magnitude — typically a low K1 value")
    add(f"(< {config.NUCLEAR_FIT_K1_THRESHOLD}, where active comae have K1 ~ 8-15).")
    add(f"Apparitions in this state will systematically underestimate peak brightness")
    add(f"by 5-10 magnitudes near perihelion. Add a row to `data/inputs/manual_M1K1.csv`")
    add(f"to override with values from a published reference; the override engages")
    add(f"automatically (provenance = `manual_curated_override`).")
    add()
    nuclear = summary[summary.get("sbdb_nuclear_biased", False).fillna(False).astype(bool)].copy()
    nuclear = nuclear.sort_values(["comet_id", "apparition_year"])
    add(f"Total apparitions affected: **{len(nuclear)}** "
        f"(across {nuclear['comet_id'].nunique()} unique comets if any)")
    add()
    if not nuclear.empty:
        add("| comet_id | year | sbdb_M1 | sbdb_K1 | provenance | peak_mag | event_case |")
        add("|---|---|---|---|---|---|---|")
        for _, row in nuclear.iterrows():
            sm1 = row.get("sbdb_M1")
            sk1 = row.get("sbdb_K1")
            sm1s = f"{sm1:.2f}" if pd.notna(sm1) else "-"
            sk1s = f"{sk1:.2f}" if pd.notna(sk1) else "-"
            pm = pd.to_numeric(row.get("peak_mag"), errors="coerce")
            pms = f"{pm:.2f}" if pd.notna(pm) else "-"
            add(f"| {row['comet_id']} | {int(row['apparition_year'])} | {sm1s} | {sk1s} | "
                f"{row.get('magnitude_provenance')} | {pms} | {row.get('event_case')} |")
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

    add("## Geographic visibility summary (Phase 1)")
    add()
    add("Per spec §8.5. Visibility margins computed at four US-population latitude")
    add("bands (Gulf 30°N, South 35°N, Mid 40°N, North 45°N) at limiting mag 4.5,")
    add("geometry + atmospheric extinction only (no moonlight, no surface brightness,")
    add("no era-dependent threshold).")
    add()
    geo_cols_present = "peak_best_margin" in summary.columns
    if geo_cols_present:
        sm = summary.copy()
        pbm = pd.to_numeric(sm.get("peak_best_margin"), errors="coerce")
        dabv = pd.to_numeric(sm.get("days_any_band_visible"), errors="coerce").fillna(0)
        ibm = pd.to_numeric(sm.get("integrated_best_margin"), errors="coerce").fillna(0)
        ever_visible = sm[dabv > 0]
        full_visible = sm[(dabv >= 30) & (pd.to_numeric(sm.get("days_all_bands_visible"), errors="coerce").fillna(0) >= 30)]
        add(f"- Apparitions with `days_any_band_visible > 0`: {len(ever_visible)} / {len(sm)}")
        add(f"- Apparitions with all 4 bands visible for ≥ 30 days: {len(full_visible)}")
        add(f"- Median `days_any_band_visible` (among ever-visible): "
            f"{int(dabv[dabv > 0].median()) if (dabv > 0).any() else 0}")
        add()
        add("### Top 10 apparitions by `peak_best_margin`")
        add()
        add("| rank | apparition | comet | peak_mag (geocentric) | peak_best_band | peak_best_margin | days_any_band_visible |")
        add("|---|---|---|---|---|---|---|")
        top10 = sm.assign(_p=pbm).nlargest(10, "_p")
        for i, (_, r) in enumerate(top10.iterrows(), 1):
            pm_val = pd.to_numeric(r.get("peak_mag"), errors="coerce")
            pm_s = f"{float(pm_val):+.2f}" if pd.notna(pm_val) else "—"
            pbm_v = pd.to_numeric(r.get("peak_best_margin"), errors="coerce")
            pbm_s = f"{float(pbm_v):.2f}" if pd.notna(pbm_v) else "—"
            dabv_v = int(pd.to_numeric(r.get("days_any_band_visible"), errors="coerce") or 0)
            add(f"| {i} | {r.get('apparition_id', '')} | {r.get('comet_name', '')} | "
                f"{pm_s} | {r.get('peak_best_band', '')} | {pbm_s} | {dabv_v} |")
        add()
        add("### Great Southern Comets — geocentric brightness vs US visibility")
        add()
        add("These four comets have spectacular geocentric peak magnitudes (−9 to −13)")
        add("but were below the horizon for US observers during their bright phase.")
        add("This is the central motivation for the geographic-visibility model.")
        add()
        add("| apparition | comet | peak_mag (geocentric) | peak_best_margin (US) | days_any_band_visible |")
        add("|---|---|---|---|---|")
        for app_id in ("C_1865B1_1865", "C_1880C1_1880", "C_1882R1_1882", "C_1887B1_1887"):
            row = sm[sm["apparition_id"] == app_id]
            if row.empty:
                add(f"| {app_id} | _missing_ | — | — | — |")
                continue
            r = row.iloc[0]
            pm_val = pd.to_numeric(r.get("peak_mag"), errors="coerce")
            pm_s = f"{float(pm_val):+.2f}" if pd.notna(pm_val) else "—"
            pbm_v = pd.to_numeric(r.get("peak_best_margin"), errors="coerce")
            pbm_s = f"{float(pbm_v):.2f}" if (pd.notna(pbm_v) and pbm_v != float("-inf")) else "−∞ (never visible)"
            dabv_v = int(pd.to_numeric(r.get("days_any_band_visible"), errors="coerce") or 0)
            add(f"| {app_id} | {r.get('comet_name', '')} | {pm_s} | {pbm_s} | {dabv_v} |")
        add()
        add("Note: C/1882 R1 has `days_any_band_visible > 0` because the comet")
        add("remained naked-eye for months as it moved north then south. During its")
        add("brightest phase (mag < 0), however, it was largely below the US horizon")
        add("at solar conjunction — see `reports/geographic_visibility_implementation.md`.")
    else:
        add("_Geographic visibility columns not yet present in summary._")
        add("Run `scripts/run_geographic_visibility.py` to populate.")
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
