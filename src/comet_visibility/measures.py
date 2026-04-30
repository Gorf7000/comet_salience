"""Brightness-duration measures per spec §9.

Two parallel families:
  - Magnitude-threshold (mag <= 6): integrated and spectacle-weighted excess.
  - Flux/apparent-brightness proxy: linearised, threshold-relative, and
    spectacle-weighted.

We never compute or report raw `magnitude × duration` — the spec is explicit
that this measure is misleading because magnitude is logarithmic and reversed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config


def add_daily_measures(daily: pd.DataFrame) -> pd.DataFrame:
    """Per spec §9, add daily-row measure columns to a light-curve frame."""
    out = daily.copy()
    m = pd.to_numeric(out["apparent_mag"], errors="coerce")
    thresh = config.NAKED_EYE_MAG_THRESHOLD
    excess = (thresh - m).clip(lower=0)
    out["mag6_excess"] = excess
    out["mag6_excess_squared"] = excess ** 2
    out["mag_le_6"] = m <= thresh
    out["flux_proxy"] = 10.0 ** (-0.4 * m)
    out["relative_flux_mag6"] = 10.0 ** (-0.4 * (m - thresh))
    out["visible_relative_flux_mag6"] = np.where(m <= thresh, out["relative_flux_mag6"], 0.0)
    out["visible_relative_flux_mag6_squared"] = out["visible_relative_flux_mag6"] ** 2
    return out


def summarize_apparition(daily: pd.DataFrame) -> dict:
    """Per spec §9, summarize an apparition-level light curve into measures."""
    if daily is None or daily.empty:
        return {
            "peak_mag": None, "date_peak_mag": None,
            "days_mag_le_6": 0,
            "integrated_mag6_excess": 0.0, "spectacle_mag6_excess": 0.0,
            "peak_flux_proxy": 0.0, "integrated_flux_proxy": 0.0,
            "integrated_visible_relative_flux_mag6": 0.0,
            "spectacle_visible_relative_flux_mag6": 0.0,
        }
    m = pd.to_numeric(daily["apparent_mag"], errors="coerce")
    valid = daily[m.notna()].copy()
    valid["apparent_mag"] = m[m.notna()]
    if valid.empty:
        return summarize_apparition(pd.DataFrame())

    peak_idx = valid["apparent_mag"].idxmin()
    peak_row = valid.loc[peak_idx]
    return {
        "peak_mag": float(peak_row["apparent_mag"]),
        "date_peak_mag": str(peak_row.get("date") or peak_row.get("date_str") or ""),
        "days_mag_le_6": int(valid["mag_le_6"].sum()),
        "integrated_mag6_excess": float(valid["mag6_excess"].sum()),
        "spectacle_mag6_excess": float(valid["mag6_excess_squared"].sum()),
        "peak_flux_proxy": float(valid["flux_proxy"].max()),
        "integrated_flux_proxy": float(valid["flux_proxy"].sum()),
        "integrated_visible_relative_flux_mag6": float(valid["visible_relative_flux_mag6"].sum()),
        "spectacle_visible_relative_flux_mag6": float(valid["visible_relative_flux_mag6_squared"].sum()),
    }


def assign_main_sample_flags(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Per spec §11, set main_sample_candidate / exclude_from_main_sample / exclusion_reason."""
    out = summary_df.copy()
    pm = pd.to_numeric(out.get("peak_mag"), errors="coerce")
    failed = out.get("failed_light_curve", pd.Series(False, index=out.index)).astype(bool)
    case = out.get("event_case", pd.Series("", index=out.index))

    main_candidate = (pm <= config.NAKED_EYE_MAG_THRESHOLD) & (~failed) \
                     & (case != "future_return") & (case != "retrospective_not_observed")

    out["main_sample_candidate"] = main_candidate.fillna(False)
    excl = []
    for i, row in out.iterrows():
        reasons = []
        if pd.notna(row.get("peak_mag")) and row["peak_mag"] > config.NAKED_EYE_MAG_THRESHOLD:
            reasons.append("peak magnitude fainter than 6")
        if row.get("failed_light_curve"):
            reasons.append("no usable light curve")
        if row.get("event_case") == "future_return":
            reasons.append("future return")
        if row.get("event_case") == "retrospective_not_observed":
            reasons.append("retrospective non-observation")
        excl.append("; ".join(reasons))
    out["exclude_from_main_sample"] = ~out["main_sample_candidate"]
    out["exclusion_reason"] = excl
    return out
