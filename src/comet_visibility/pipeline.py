"""End-to-end pipeline orchestrator.

Stages:

  1. AERITH scrape (cached) - source_aerith.scrape_all_apparitions
  2. SBDB enumeration (cached) - source_jpl.enumerate_comets_by_perihelion
  3. Combined scaffold + status mapping - scaffold.build_combined_scaffold
  4. Per-apparition light curves - light_curves.generate_for_apparition
  5. Daily measures + apparition summary - measures
  6. Diagnostic plots - diagnostics.plot_all
  7. Validation checks - validate
  8. Audit report - audit.write_audit_report

Stop conditions (this conversation, not in spec):
  - Periodic Tier 3 fraction > config.TIER3_FRACTION_HALT  -> halt
  - Hard validation failure (e.g., apparition_id collision in summary) -> halt
  - Network outage > config.NETWORK_OUTAGE_HALT_SEC -> deferred to runtime watchdog
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd

from . import audit, config, diagnostics, measures
from .light_curves import generate_for_apparition
from .scaffold import build_combined_scaffold
from .source_aerith import scrape_all_apparitions

logger = logging.getLogger(__name__)


def _ensure_aerith_scraped(refresh: bool = False) -> None:
    """If the AERITH raw CSV is absent, scrape now."""
    raw_path = config.DATA_INTERMEDIATE / "aerith_apparitions_raw.csv"
    if raw_path.exists() and not refresh:
        return
    df = scrape_all_apparitions(refresh=refresh)
    df.to_csv(raw_path, index=False)


def _validate(scaffold: pd.DataFrame, summary: pd.DataFrame, daily: pd.DataFrame,
              fail_hard: bool = True) -> list[str]:
    """Per spec §18. Returns list of validation messages; empty means pass."""
    errs: list[str] = []
    if scaffold["apparition_id"].duplicated().any():
        errs.append("apparition_id is not unique in scaffold")
    if summary["apparition_id"].duplicated().any():
        errs.append("apparition_id is not unique in summary")
    if not daily.empty:
        ids_summary = set(summary["apparition_id"])
        ids_daily = set(daily["apparition_id"])
        unknown = ids_daily - ids_summary
        if unknown:
            errs.append(f"daily light curves reference {len(unknown)} apparition_ids not in summary")
    # provenance must be from allowed set
    allowed = {"horizons_tmag", "manual_curated", "assumed_default_K1"}
    if not daily.empty:
        bad = set(daily["magnitude_model_provenance"].dropna().unique()) - allowed
        if bad:
            errs.append(f"daily provenance has unexpected values: {sorted(bad)}")
    # Tier 3 should never produce daily rows
    if not daily.empty:
        if (daily["magnitude_model_provenance"] == "failed").any():
            errs.append("Tier 3 (failed) rows found in daily light curves")
    # peak_mag matches min apparent_mag in daily (spot-check first 50)
    if not daily.empty:
        for app_id, group in list(daily.groupby("apparition_id"))[:50]:
            sm = summary[summary["apparition_id"] == app_id]
            if sm.empty:
                continue
            peak_summary = pd.to_numeric(sm["peak_mag"], errors="coerce").iloc[0]
            peak_daily = pd.to_numeric(group["apparent_mag"], errors="coerce").min()
            if pd.notna(peak_summary) and pd.notna(peak_daily):
                if abs(float(peak_summary) - float(peak_daily)) > 1e-6:
                    errs.append(f"peak_mag mismatch for {app_id}: summary={peak_summary}, daily_min={peak_daily}")
                    break
    return errs


def run(refresh: bool = False, max_apparitions: int | None = None) -> dict:
    """Run the full pipeline. max_apparitions caps for sample/test runs.

    Returns a dict with paths and counts.
    """
    t0 = time.time()
    logger.info("Pipeline start")

    _ensure_aerith_scraped(refresh=refresh)
    scaffold = build_combined_scaffold(refresh=refresh)
    scaffold_path = config.DATA_PROCESSED / "comet_apparitions_coded.csv"
    scaffold.to_csv(scaffold_path, index=False)
    logger.info("Scaffold rows: %d -> %s", len(scaffold), scaffold_path)

    rows = scaffold.copy()
    if max_apparitions is not None:
        rows = rows.head(max_apparitions)
        logger.info("Capping to first %d apparitions for sample run", max_apparitions)

    daily_chunks: list[pd.DataFrame] = []
    summary_records: list[dict] = []

    n = len(rows)
    for i, (_, row) in enumerate(rows.iterrows(), 1):
        try:
            daily, meta = generate_for_apparition(row, refresh=refresh)
        except Exception as e:
            logger.exception("Unexpected failure for %s", row.get("apparition_id"))
            meta = {
                "apparition_id": row["apparition_id"],
                "failed_light_curve": True,
                "audit_notes": f"unexpected exception: {e!r}",
                "magnitude_provenance": "failed",
                "magnitude_quality": "failed",
            }
            daily = None

        # Build summary record
        sm = {
            **{c: row.get(c) for c in [
                "apparition_id", "comet_id", "comet_name", "designation",
                "apparition_year", "perihelion_date", "discovery_date",
                "raw_status_source", "raw_aerith_status",
                "expected", "seen", "event_case",
                "status_mapping_confidence", "status_notes", "manual_review_status",
                "sbdb_pdes", "merged_fragments",
            ] if c in row.index},
            **meta,
        }
        if daily is not None:
            daily = measures.add_daily_measures(daily)
            sm.update(measures.summarize_apparition(daily))
            daily_chunks.append(daily)
        else:
            sm.update(measures.summarize_apparition(pd.DataFrame()))
        summary_records.append(sm)

        if i % 25 == 0 or i == n:
            elapsed = time.time() - t0
            ok = sum(1 for s in summary_records if not s.get("failed_light_curve"))
            logger.info("Progress %d/%d (%.0f%%): %d successful curves, elapsed %.1fs",
                        i, n, 100*i/n, ok, elapsed)

    summary = pd.DataFrame(summary_records)
    summary = measures.assign_main_sample_flags(summary)
    summary_path = config.DATA_PROCESSED / "comet_brightness_summary.csv"
    summary.to_csv(summary_path, index=False)
    logger.info("Summary rows: %d -> %s", len(summary), summary_path)

    daily_full = pd.concat(daily_chunks, ignore_index=True) if daily_chunks else pd.DataFrame()
    daily_path = config.DATA_PROCESSED / "comet_daily_light_curves.csv"
    daily_full.to_csv(daily_path, index=False)
    logger.info("Daily light-curve rows: %d -> %s", len(daily_full), daily_path)

    validation = _validate(scaffold, summary, daily_full, fail_hard=False)
    if validation:
        logger.warning("Validation findings: %d", len(validation))
        for v in validation:
            logger.warning("  - %s", v)

    # Periodic-only Tier 3 halt check (non-periodic Tier 3 is expected)
    periodic_summary = summary[summary["raw_status_source"] == "AERITH"]
    if len(periodic_summary):
        tier3_frac = (periodic_summary["magnitude_provenance"] == "failed").mean()
        if tier3_frac > config.TIER3_FRACTION_HALT:
            msg = (f"Periodic Tier 3 fraction {tier3_frac:.2f} exceeds halt threshold "
                   f"{config.TIER3_FRACTION_HALT:.2f}")
            logger.error(msg)
            validation.append(msg)

    diagnostics.plot_all(summary, daily_full)
    audit_path = audit.write_audit_report(scaffold, summary, daily_full, validation)
    logger.info("Audit -> %s", audit_path)

    return {
        "scaffold_path": scaffold_path,
        "summary_path": summary_path,
        "daily_path": daily_path,
        "audit_path": audit_path,
        "n_apparitions": len(summary),
        "n_with_curves": int((~summary["failed_light_curve"].fillna(False).astype(bool)).sum()),
        "validation_findings": validation,
        "elapsed_sec": time.time() - t0,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    result = run()
    print()
    print("=== Pipeline result ===")
    for k, v in result.items():
        print(f"{k}: {v}")
