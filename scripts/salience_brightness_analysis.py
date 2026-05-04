"""Salience vs. brightness analysis for the comet visibility chapter.

Loads three monthly newspaper-salience series (US press, 1850-1940) and the
pipeline's per-apparition brightness summary, then:

  1. Identifies the top peaks in each salience series and labels each peak with
     the brightest comet in the sky that month (raw alignment view).
  2. Computes per-apparition salience features (peak X_fraction, lead time,
     integrated above threshold) within ±180-day windows around perihelion.
  3. Flags "solo apparitions" — those with no other naked-eye comet (mag ≤ 6.0)
     in the apparition window. The solo subset gives clean attribution.
  4. Compares predicted (event_case = expected_seen) vs. unpredicted
     (event_case = unexpected_seen) apparitions across brightness bins, on both
     the full set and the solo subset.

Outputs:
  data/processed/salience_brightness_analysis.csv  (per-apparition features)
  data/processed/solo_analysis.csv                  (solo-flag features)

Companion report: reports/salience_brightness_analysis.md
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd

from src.comet_visibility import config


SALIENCE_FILES = {
    "X_fraction": config.DATA_INPUTS / "comets_20260504_103047_data_X_fraction.csv",
    "word_count": config.DATA_INPUTS / "comets_20260504_103143_data_word_count.csv",
    "Comets2_xf": config.DATA_INPUTS / "comets2_20260504_103348_data-Comet_2_x_fraction.csv",
}

WINDOW_DAYS = 180


def load_salience() -> dict[str, pd.DataFrame]:
    """Load the three monthly salience series, return dict keyed by short name."""
    out = {}
    for name, path in SALIENCE_FILES.items():
        df = pd.read_csv(path, parse_dates=["time_point"])
        df = df[["time_point", "value"]].rename(
            columns={"time_point": "month", "value": name})
        df["month"] = df["month"].dt.to_period("M").dt.to_timestamp()
        out[name] = df
    return out


def per_apparition_features(brightness: pd.DataFrame,
                             salience: pd.DataFrame,
                             value_col: str,
                             elevated_thresh: float,
                             spike_thresh: float) -> pd.DataFrame:
    """Compute per-apparition salience features within ±WINDOW_DAYS of perihelion."""
    feats = []
    for _, row in brightness.iterrows():
        peri = row["perihelion_date"]
        win = salience[(salience["month"] >= peri - pd.Timedelta(days=WINDOW_DAYS)) &
                       (salience["month"] <= peri + pd.Timedelta(days=WINDOW_DAYS))].copy()
        if win.empty:
            feats.append({"max_salience": np.nan, "peak_month_offset": np.nan,
                          "integ_above_p75": np.nan, "lead_time_p75": np.nan,
                          "lead_time_p90": np.nan, "preperi_max": np.nan})
            continue
        win["offset_months"] = ((win["month"].dt.year - peri.year) * 12 +
                                 (win["month"].dt.month - peri.month))
        pk_idx = win[value_col].idxmax()
        pk_off = win.loc[pk_idx, "offset_months"]
        pk_val = win.loc[pk_idx, value_col]
        integ = (win[value_col] - elevated_thresh).clip(lower=0).sum()
        lt75 = (win[win[value_col] >= elevated_thresh]["offset_months"].min()
                if (win[value_col] >= elevated_thresh).any() else np.nan)
        lt90 = (win[win[value_col] >= spike_thresh]["offset_months"].min()
                if (win[value_col] >= spike_thresh).any() else np.nan)
        preperi = (win[win["offset_months"] < 0][value_col].max()
                   if (win["offset_months"] < 0).any() else np.nan)
        feats.append({"max_salience": pk_val, "peak_month_offset": pk_off,
                      "integ_above_p75": integ, "lead_time_p75": lt75,
                      "lead_time_p90": lt90, "preperi_max": preperi})
    return pd.DataFrame(feats)


def compute_solo_flags(brightness: pd.DataFrame,
                        daily: pd.DataFrame,
                        cutoffs: tuple[float, ...] = (6.0, 8.0)) -> pd.DataFrame:
    """For each apparition, find the brightest competing comet in the window."""
    daily = daily.dropna(subset=["apparent_mag"]).copy()
    daily["mag"] = pd.to_numeric(daily["apparent_mag"], errors="coerce")
    out = []
    for _, row in brightness.iterrows():
        peri = row["perihelion_date"]
        aid = row["apparition_id"]
        win = daily[(daily["date"] >= peri - pd.Timedelta(days=WINDOW_DAYS)) &
                    (daily["date"] <= peri + pd.Timedelta(days=WINDOW_DAYS)) &
                    (daily["apparition_id"] != aid)]
        comp_min = float(win["mag"].min()) if not win.empty else float("inf")
        rec = {"comet_id": row["comet_id"], "comet_name": row["comet_name"],
               "apparition_id": aid, "apparition_year": row["apparition_year"],
               "perihelion_date": peri, "peak_mag_n": row["peak_mag_n"],
               "predicted": row["predicted"], "event_case": row["event_case"],
               "competing_min_mag": comp_min}
        for c in cutoffs:
            rec[f"solo_at_mag{int(c)}"] = comp_min > c
        out.append(rec)
    return pd.DataFrame(out)


def main():
    salience = load_salience()
    xf = salience["X_fraction"]
    elevated = xf["X_fraction"].quantile(0.75)
    spike = xf["X_fraction"].quantile(0.90)
    print(f"X_fraction p75={elevated:.3f}  p90={spike:.3f}")

    brightness = pd.read_csv(config.DATA_PROCESSED / "comet_brightness_summary.csv",
                              parse_dates=["perihelion_date"])
    brightness["peak_mag_n"] = pd.to_numeric(brightness["peak_mag"], errors="coerce")
    brightness = brightness.dropna(subset=["peak_mag_n", "perihelion_date"]).copy()
    brightness = brightness[brightness["event_case"].isin(
        ["expected_seen", "unexpected_seen"])]
    brightness["predicted"] = brightness["event_case"] == "expected_seen"
    print(f"Apparitions in scope: {len(brightness)} "
          f"({brightness['predicted'].sum()} predicted, "
          f"{(~brightness['predicted']).sum()} unpredicted)")

    feats = per_apparition_features(brightness, xf, "X_fraction", elevated, spike)
    keep = ["comet_id", "comet_name", "apparition_id", "apparition_year",
            "perihelion_date", "peak_mag_n", "predicted", "event_case"]
    ana = pd.concat([brightness[keep].reset_index(drop=True),
                      feats.reset_index(drop=True)], axis=1)
    ana_path = config.DATA_PROCESSED / "salience_brightness_analysis.csv"
    ana.to_csv(ana_path, index=False)
    print(f"Wrote {ana_path}")

    print("Computing solo flags (loading daily light curves)...")
    daily = pd.read_csv(config.DATA_PROCESSED / "comet_daily_light_curves.csv.gz",
                        parse_dates=["date"],
                        usecols=["comet_id", "apparition_id", "date", "apparent_mag"])
    solo = compute_solo_flags(brightness, daily)
    solo_path = config.DATA_PROCESSED / "solo_analysis.csv"
    solo.to_csv(solo_path, index=False)
    print(f"Wrote {solo_path}")
    print(f"Solo at mag 6 cutoff: {solo['solo_at_mag6'].sum()} "
          f"({solo[solo['solo_at_mag6']]['predicted'].sum()} predicted, "
          f"{solo[solo['solo_at_mag6'] & ~solo['predicted']].shape[0]} unpredicted)")


if __name__ == "__main__":
    main()
