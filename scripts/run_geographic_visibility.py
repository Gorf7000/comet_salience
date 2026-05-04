"""Standalone runner for the geographic-visibility pipeline step.

Reuses the already-computed daily light curves and brightness summary,
computes per-(apparition, date, band) visibility margins, writes the
long-format daily CSV, and appends per-apparition rollup columns to the
brightness summary in place. Avoids re-running the upstream Horizons /
AERITH stages.

Usage:
    python scripts/run_geographic_visibility.py
"""

from __future__ import annotations

import logging
import sys
import time
import warnings
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    # Import astropy-using module first; astropy mutates logging on import.
    from src.comet_visibility import config, geographic_visibility

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("astropy").setLevel(logging.WARNING)
    logging.getLogger("erfa").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")

    daily_path = config.DATA_PROCESSED / "comet_daily_light_curves.csv.gz"
    summary_path = config.DATA_PROCESSED / "comet_brightness_summary.csv"

    if not daily_path.exists():
        raise SystemExit(f"Missing input: {daily_path}")
    if not summary_path.exists():
        raise SystemExit(f"Missing input: {summary_path}")

    logging.info("Loading daily light curves <- %s", daily_path)
    daily = pd.read_csv(daily_path, low_memory=False)
    logging.info("Loaded %d daily rows over %d apparitions",
                 len(daily), daily["apparition_id"].nunique())

    logging.info("Loading brightness summary <- %s", summary_path)
    summary = pd.read_csv(summary_path, low_memory=False)

    t0 = time.time()
    visibility, summary_with_geo = geographic_visibility.run_pipeline_step(
        daily, summary,
    )
    summary_with_geo.to_csv(summary_path, index=False)
    elapsed = time.time() - t0

    logging.info("Geographic visibility step complete in %.1fs", elapsed)
    logging.info("  long-format daily -> %s (%d rows)",
                 config.GEO_DAILY_OUTPUT, len(visibility))
    logging.info("  summary updated   -> %s (%d cols)",
                 summary_path, summary_with_geo.shape[1])


if __name__ == "__main__":
    main()
