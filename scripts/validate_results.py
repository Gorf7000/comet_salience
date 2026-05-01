"""End-to-end validation of pipeline outputs.

Runs four independent checks and writes findings to reports/validation_results.md:

  1. Modeled peak magnitudes vs hand-curated published peak magnitudes for
     well-known periodic comets.
  2. Hand calculation: take one daily row, plug r, Δ, M1, K1 into the
     formula by hand, confirm apparent_mag matches.
  3. Manual M1/K1 CSV path: add a temporary entry, confirm Tier 1.5
     provenance applies and a light curve is generated.
  4. Spot-check the audit report and confirm diagnostic figures rendered.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Eager imports first (avoid astropy logger init bug)
from src.comet_visibility import config, measures
from src.comet_visibility.light_curves import (compute_magnitude,
                                                generate_for_apparition,
                                                resolve_magnitude_model,
                                                _load_manual_M1K1)
from src.comet_visibility.scaffold import build_combined_scaffold
from src.comet_visibility.source_jpl import lookup_sbdb, extract_M1_K1

import logging
import math
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.getLogger("astropy").setLevel(logging.ERROR)
logging.getLogger("astroquery").setLevel(logging.ERROR)


# ----------------------------------------------------------------------
# Reference peak magnitudes for periodic comet apparitions in scope.
# Sources: Kronk's Cometography (cited by year+comet), Marsden & Williams,
# IAU Minor Planet Center records. Values are approximate observed visual peak.
# When a range is published I take the midpoint. These are sanity-check
# benchmarks — agreement to within ~1 magnitude is good for an M1/K1 single
# power-law model.
# ----------------------------------------------------------------------
REFERENCE_PEAKS = [
    # (comet_id, apparition_year, observed_peak_mag, source/notes)
    ("1P",  1910, 0.0,  "Halley 1910; Kronk: peak ~0, briefly -0.5 in early May"),
    ("109P", 1862, 2.0, "Swift-Tuttle 1862 discovery; Kronk: peak ~+2"),
    ("12P", 1884, 3.0,  "Pons-Brooks 1884; Kronk: peak +3 to +3.5"),
    ("2P",  1898, 6.0,  "Encke 1898; mid-range estimate, Encke varies +5 to +7"),
    ("3D",  1852, 5.0,  "Biela 1852 final intact return; Kronk: peak ~+5"),
    ("5D",  1879, 6.0,  "Brorsen 1879; Kronk: peak ~+5 to +6"),
    ("23P", 1919, 5.0,  "Brorsen-Metcalf 1919; Kronk: peak ~+5"),
    ("8P",  1858, 7.0,  "Tuttle 1858 discovery; Kronk: peak ~+7"),
    ("17P", 1892, 5.0,  "Holmes 1892; famous outburst, peak ~+5 (M1/K1 model will not capture)"),
    # Famous non-periodics that should now be in the dataset post-Big V promotion
    ("C/1858 L1", 1858, -1.0, "Donati 1858; widely reported peak ~-1"),
    ("C/1861 J1", 1861,  0.0, "Tebbutt 1861; widely reported peak ~0"),
    ("C/1882 R1", 1882, -10.0, "Great September Comet 1882; sungrazer, peak ~-17 in daylight (single-law model will under-predict)"),
    ("C/1910 A1", 1910, -1.0, "Great January Comet 1910; widely reported peak ~-1 to -5"),
]


def check1_external_peaks(summary: pd.DataFrame) -> tuple[list[str], pd.DataFrame]:
    """External-magnitude sanity check."""
    rows = []
    for cid, year, observed, note in REFERENCE_PEAKS:
        sm = summary[(summary["comet_id"] == cid) & (summary["apparition_year"] == year)]
        if sm.empty:
            rows.append({"comet_id": cid, "year": year, "observed_peak": observed,
                         "modeled_peak": None, "diff": None, "ok": False, "notes": "MISSING from summary"})
            continue
        modeled = pd.to_numeric(sm["peak_mag"], errors="coerce").iloc[0]
        if pd.isna(modeled):
            rows.append({"comet_id": cid, "year": year, "observed_peak": observed,
                         "modeled_peak": None, "diff": None, "ok": False, "notes": f"no model ({note})"})
            continue
        diff = float(modeled) - observed
        ok = abs(diff) <= 1.5
        rows.append({"comet_id": cid, "year": year, "observed_peak": observed,
                     "modeled_peak": float(modeled), "diff": diff, "ok": ok, "notes": note})
    df = pd.DataFrame(rows)
    msgs = []
    pass_count = df["ok"].sum()
    msgs.append(f"External-peak check: {pass_count}/{len(df)} within ±1.5 mag of observed.")
    misses = df[~df["ok"]]
    if not misses.empty:
        for _, r in misses.iterrows():
            msgs.append(f"  - {r['comet_id']} {r['year']}: observed {r['observed_peak']:+.1f}, "
                        f"modeled {r['modeled_peak']!r}, diff {r['diff']!r} — {r['notes']}")
    return msgs, df


def check2_hand_calc(daily: pd.DataFrame) -> list[str]:
    """Hand-calculate magnitude for a Tier-1-or-1.5 row and confirm match.

    After Big V promotion most periodic comets get their M1/K1 from the manual
    CSV (provenance=manual_curated_override). Pick whatever path Halley 1910
    is on now; whichever (M1, K1) was used, the formula has to match.
    """
    msgs = []
    halley = daily[daily["apparition_id"] == "1P_1910"]
    if halley.empty:
        return ["Hand-calc skipped: no 1P_1910 rows"]
    halley = halley.copy()
    halley["dfp"] = pd.to_numeric(halley["days_from_perihelion"], errors="coerce").abs()
    near_peri = halley.sort_values("dfp").iloc[0]
    r = float(near_peri["heliocentric_distance_au"])
    delta = float(near_peri["geocentric_distance_au"])
    pipeline_mag = float(near_peri["apparent_mag"])
    provenance = near_peri["magnitude_model_provenance"]

    # Determine which (M1, K1) the pipeline used.
    if provenance == "manual_curated_override" or provenance == "manual_curated":
        manual = _load_manual_M1K1()
        entry = manual.get("1P")
        if entry is None:
            return [f"Hand-calc skipped: 1P provenance is {provenance} but no manual entry"]
        M1, K1 = entry["M1"], entry["K1"]
        source_desc = f"manual_M1K1.csv (provenance={provenance})"
    else:
        payload = lookup_sbdb("1P")
        M1, K1 = extract_M1_K1(payload)
        source_desc = f"SBDB lookup (provenance={provenance})"

    by_hand = M1 + 5 * math.log10(delta) + K1 * math.log10(r)
    diff = pipeline_mag - by_hand

    msgs.append(f"Hand-calc on 1P_1910 near-perihelion row ({source_desc}):")
    msgs.append(f"  date={near_peri['date']}, days_from_perihelion={near_peri['days_from_perihelion']}")
    msgs.append(f"  r={r:.6f} AU, Δ={delta:.6f} AU")
    msgs.append(f"  SBDB M1={M1}, K1={K1}")
    msgs.append(f"  pipeline apparent_mag = {pipeline_mag:.4f}")
    msgs.append(f"  hand calc m = {M1} + 5·log10({delta:.4f}) + {K1}·log10({r:.4f}) = {by_hand:.4f}")
    msgs.append(f"  diff = {diff:+.4f} mag")
    if abs(diff) < 0.1:
        msgs.append(f"  RESULT: agreement within 0.1 mag — Tier 1 formula path is consistent.")
    else:
        msgs.append(f"  RESULT: discrepancy > 0.1 mag. Horizons may use a slightly different "
                    f"phase function or include additional corrections.")
    return msgs


def check3_manual_csv() -> list[str]:
    """Add a temporary manual M1/K1 row, regenerate one Tier 3 apparition, confirm Tier 1.5."""
    msgs = []
    csv_path = config.DATA_INPUTS / "manual_M1K1.csv"
    backup = csv_path.read_text(encoding="utf-8")

    try:
        # Pick a known Tier 3: C/1858 L1 (Donati). Use a Vsekhsvyatskij-style H10.
        # H10 = 4.7 corresponds to M1=4.7 with K1=10 (n=4).
        test_row = "1858 L1,4.7,10.0,Vsekhsvyatskij 1958 (test entry),validation_check_3"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("pdes,M1,K1,source_citation,notes\n")
            f.write(test_row + "\n")

        # Clear lru_cache so the new CSV gets read
        _load_manual_M1K1.cache_clear()

        scaffold = build_combined_scaffold()
        donati = scaffold[(scaffold["comet_id"] == "C/1858 L1") & (scaffold["apparition_year"] == 1858)]
        if donati.empty:
            return ["Manual-CSV check FAILED: no C/1858 L1 1858 row in scaffold"]

        daily, meta = generate_for_apparition(donati.iloc[0])
        msgs.append(f"Manual-CSV check on C/1858 L1 with Vsekhsvyatskij M1=4.7, K1=10:")
        msgs.append(f"  magnitude_provenance = {meta['magnitude_provenance']}")
        msgs.append(f"  manual_curated_source_citation = {meta['manual_curated_source_citation']!r}")
        if daily is not None:
            sm = measures.add_daily_measures(daily)
            summary = measures.summarize_apparition(sm)
            msgs.append(f"  generated daily rows: {len(daily)}")
            msgs.append(f"  modeled peak_mag = {summary['peak_mag']:.2f} (observed peak ~-1)")
            msgs.append(f"  days_mag_le_6 = {summary['days_mag_le_6']}")
            msgs.append(f"  integrated_mag6_excess = {summary['integrated_mag6_excess']:.1f}")
        else:
            msgs.append(f"  RESULT: light curve generation FAILED")
            msgs.append(f"  audit_notes: {meta.get('audit_notes')}")
        if meta["magnitude_provenance"] == "manual_curated":
            msgs.append(f"  RESULT: Tier 1.5 path engaged correctly.")
        else:
            msgs.append(f"  RESULT: Tier 1.5 NOT engaged (got {meta['magnitude_provenance']}).")
    finally:
        csv_path.write_text(backup, encoding="utf-8")
        _load_manual_M1K1.cache_clear()
    return msgs


def check4_artifacts() -> list[str]:
    """Eyeball the audit report + confirm diagnostic figures exist."""
    msgs = []
    audit = config.REPORTS / "comet_visibility_audit.md"
    msgs.append(f"Audit report: {audit}")
    if audit.exists():
        size = audit.stat().st_size
        text = audit.read_text(encoding="utf-8")
        msgs.append(f"  size: {size} bytes, {text.count(chr(10))} lines")
        msgs.append(f"  contains 'Manual M1/K1 candidates': {'Manual M1/K1 candidates' in text}")
        msgs.append(f"  contains 'Tier 3 non-periodic candidates: ': {'Tier 3 non-periodic candidates: ' in text}")
        msgs.append(f"  contains 'Validation failures': {'Validation failures' in text}")
    else:
        msgs.append(f"  MISSING")

    fig_dir = config.FIGURES
    expected_figs = ["01_peak_mag_histogram.png", "02_peak_vs_duration.png",
                     "03_integrated_vs_spectacle_mag.png", "04_mag_vs_flux_families.png",
                     "05_event_case_counts.png", "06_main_sample_candidate.png",
                     "07a_top_by_integrated_mag.png", "07b_top_by_spectacle_mag.png",
                     "07c_top_by_flux.png"]
    msgs.append(f"\nDiagnostic figures in {fig_dir}:")
    for f in expected_figs:
        p = fig_dir / f
        if p.exists():
            msgs.append(f"  OK   {f} ({p.stat().st_size} bytes)")
        else:
            msgs.append(f"  MISS {f}")
    return msgs


def main():
    summary = pd.read_csv(config.DATA_PROCESSED / "comet_brightness_summary.csv")
    daily = pd.read_csv(config.DATA_PROCESSED / "comet_daily_light_curves.csv")

    out = config.REPORTS / "validation_results.md"
    lines = []
    lines.append(f"# Validation Results")
    lines.append(f"_Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_")
    lines.append("")
    lines.append("Four independent checks: external-peak comparison, hand calculation,")
    lines.append("manual-CSV path test, and artifact inspection. Designed to be readable")
    lines.append("in 5 minutes and to surface issues that the pipeline's internal")
    lines.append("validation does not catch.")
    lines.append("")

    # Check 1
    lines.append("## 1. External peak-magnitude comparison")
    lines.append("")
    msgs, ext_df = check1_external_peaks(summary)
    for m in msgs:
        lines.append(m)
    lines.append("")
    lines.append("Detailed comparison table:")
    lines.append("")
    lines.append("| comet_id | year | observed peak | modeled peak | diff | within ±1.5? | notes |")
    lines.append("|---|---|---|---|---|---|---|")
    for _, r in ext_df.iterrows():
        modeled = f"{r['modeled_peak']:.2f}" if r['modeled_peak'] is not None else "_(missing)_"
        diff = f"{r['diff']:+.2f}" if r['diff'] is not None else "—"
        ok = "yes" if r['ok'] else "**no**"
        lines.append(f"| {r['comet_id']} | {r['year']} | {r['observed_peak']:+.1f} | {modeled} | {diff} | {ok} | {r['notes']} |")
    lines.append("")

    # Check 2
    lines.append("## 2. Hand calculation of magnitude formula")
    lines.append("")
    for m in check2_hand_calc(daily):
        lines.append(m)
    lines.append("")

    # Check 3
    lines.append("## 3. Manual M1/K1 CSV path (Tier 1.5)")
    lines.append("")
    for m in check3_manual_csv():
        lines.append(m)
    lines.append("")

    # Check 4
    lines.append("## 4. Audit report + diagnostic figures")
    lines.append("")
    for m in check4_artifacts():
        lines.append(m)
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
