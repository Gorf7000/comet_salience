"""Overnight pipeline runner.

Executes the full pipeline, writes a morning_summary.md, then commits
processed outputs + report to git and pushes to origin.

Usage:
    python scripts/run_overnight.py
"""

from __future__ import annotations

import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    log_path = ROOT / "reports" / "overnight_run.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    sh = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh.setFormatter(fmt); sh.setFormatter(fmt)

    # Configure root logger AFTER importing astropy-using modules
    from src.comet_visibility import config, pipeline

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(fh); root.addHandler(sh)
    logging.getLogger("astropy").setLevel(logging.WARNING)
    logging.getLogger("astroquery").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    t0 = time.time()
    logging.info("Overnight pipeline start at %s", datetime.utcnow().isoformat())
    try:
        result = pipeline.run()
    except Exception:
        logging.exception("Pipeline crashed")
        raise

    elapsed = time.time() - t0
    logging.info("Pipeline complete in %.1fs", elapsed)

    # ------------------------------------------------------------------
    # Morning summary
    # ------------------------------------------------------------------
    import pandas as pd
    summary = pd.read_csv(result["summary_path"])
    daily = pd.read_csv(result["daily_path"]) if Path(result["daily_path"]).stat().st_size > 0 else pd.DataFrame()
    pm = pd.to_numeric(summary["peak_mag"], errors="coerce")

    morning = ROOT / "reports" / "morning_summary.md"
    lines = []
    lines.append(f"# Morning Summary  (run {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})")
    lines.append("")
    lines.append(f"Pipeline elapsed: **{elapsed:.0f} s**")
    lines.append("")
    lines.append("## Run summary")
    lines.append("")
    lines.append(f"- Total apparitions in scope: **{result['n_apparitions']}**")
    lines.append(f"- Successful daily light curves: **{result['n_with_curves']}**")
    lines.append(f"- Apparitions with peak_mag <= {config.NAKED_EYE_MAG_THRESHOLD}: "
                 f"**{(pm <= config.NAKED_EYE_MAG_THRESHOLD).sum()}**")
    lines.append(f"- Daily light-curve rows: **{len(daily)}**")
    lines.append("")
    lines.append("## Magnitude provenance breakdown")
    lines.append("")
    for k, v in summary["magnitude_provenance"].value_counts().items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## event_case breakdown")
    lines.append("")
    for k, v in summary["event_case"].value_counts().items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Top 10 apparitions by peak brightness")
    lines.append("")
    top_peak = summary.dropna(subset=["peak_mag"]).sort_values("peak_mag").head(10)
    lines.append("| comet_name | year | peak_mag | days <= 6 | event_case | provenance |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in top_peak.iterrows():
        lines.append(
            f"| {str(r['comet_name'])[:35]} | {int(r['apparition_year'])} | "
            f"{r['peak_mag']:.2f} | {int(r.get('days_mag_le_6', 0))} | {r['event_case']} | "
            f"{r['magnitude_provenance']} |"
        )
    lines.append("")

    for measure, label in [
        ("integrated_mag6_excess", "Top 10 by integrated_mag6_excess"),
        ("spectacle_mag6_excess", "Top 10 by spectacle_mag6_excess"),
        ("integrated_visible_relative_flux_mag6", "Top 10 by integrated_visible_relative_flux_mag6"),
    ]:
        lines.append(f"## {label}")
        lines.append("")
        top = summary.dropna(subset=[measure]).sort_values(measure, ascending=False).head(10)
        lines.append(f"| comet_name | year | {measure} | peak_mag | event_case |")
        lines.append("|---|---|---|---|---|")
        for _, r in top.iterrows():
            lines.append(
                f"| {str(r['comet_name'])[:35]} | {int(r['apparition_year'])} | "
                f"{float(r[measure]):.3g} | {pd.to_numeric(r['peak_mag'], errors='coerce'):.2f} | "
                f"{r['event_case']} |"
            )
        lines.append("")

    lines.append("## Validation findings")
    lines.append("")
    if not result["validation_findings"]:
        lines.append("_No validation issues._")
    else:
        for f in result["validation_findings"]:
            lines.append(f"- {f}")
    lines.append("")
    lines.append("## What's next")
    lines.append("")
    lines.append("- Review the audit report at `reports/comet_visibility_audit.md`.")
    lines.append("- Inspect the diagnostic plots in `figures/comet_visibility_diagnostics/`.")
    lines.append("- The audit's **Manual M1/K1 candidates** section lists the Tier 3")
    lines.append("  non-periodic apparitions awaiting M1/K1 entry. Add rows to")
    lines.append("  `data/inputs/manual_M1K1.csv` and re-run; cached Horizons responses")
    lines.append("  make incremental reruns cheap.")
    morning.write_text("\n".join(lines), encoding="utf-8")
    logging.info("Wrote morning summary -> %s", morning)

    # ------------------------------------------------------------------
    # Git commit + push
    # ------------------------------------------------------------------
    files_to_commit = [
        "data/processed/comet_apparitions_coded.csv",
        "data/processed/comet_brightness_summary.csv",
        "data/processed/comet_daily_light_curves.csv",
        "data/intermediate/aerith_apparitions_raw.csv",
        "reports/comet_visibility_audit.md",
        "reports/morning_summary.md",
        "reports/overnight_run.log",
        "figures/comet_visibility_diagnostics/",
    ]
    env_extras = ["-c", "user.email=grfaith@gmail.com", "-c", "user.name=Gorf7000"]
    add_cmd = ["git", "-C", str(ROOT)] + env_extras + ["add"] + files_to_commit
    subprocess.run(add_cmd, check=False)
    msg = (f"Overnight pipeline run: {result['n_with_curves']}/{result['n_apparitions']} "
           f"apparitions with light curves\n\n"
           f"Elapsed: {elapsed:.0f}s. Validation findings: {len(result['validation_findings'])}.\n"
           f"\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>")
    subprocess.run(["git", "-C", str(ROOT)] + env_extras + ["commit", "-m", msg], check=False)
    subprocess.run(["git", "-C", str(ROOT), "push"], check=False)
    logging.info("Git push complete")


if __name__ == "__main__":
    main()
