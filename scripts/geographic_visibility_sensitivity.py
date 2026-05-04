"""Sensitivity report for geographic visibility limiting magnitudes.

Per spec §5: compares peak_best_margin, days_any_band_visible, and the
top-30 ranking by integrated_best_margin across the three sensitivity
limit values {4.0, 4.5, 5.0}. Headline output uses 4.5; this report
documents how the picture changes if we'd picked 4.0 or 5.0 instead.

Writes reports/geographic_visibility_sensitivity.md.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import warnings
warnings.filterwarnings("ignore")

import pandas as pd

from src.comet_visibility import config, geographic_visibility


def _rank_corr(a: pd.Series, b: pd.Series) -> float:
    """Spearman ρ between two parallel rank series."""
    return a.corr(b, method="spearman")


def main() -> None:
    visibility = pd.read_csv(config.GEO_DAILY_OUTPUT, low_memory=False)
    summary = pd.read_csv(config.DATA_PROCESSED / "comet_brightness_summary.csv",
                          low_memory=False)

    sens = geographic_visibility.summarize_apparition_visibility_at_limits(visibility)
    # Pivot to one row per apparition with three lim columns each.
    pivot = sens.pivot(index="apparition_id", columns="limit",
                       values=["peak_best_margin", "days_any_band_visible",
                               "integrated_best_margin"])
    pivot.columns = [f"{m}_lim{int(round(l*10))}" for m, l in pivot.columns]
    pivot = pivot.merge(summary[["apparition_id", "comet_name", "peak_mag"]],
                        on="apparition_id", how="left").reset_index(drop=True)

    # Top-30 by integrated_best_margin at each limit
    top30 = {}
    for lim in (4.0, 4.5, 5.0):
        col = f"integrated_best_margin_lim{int(round(lim*10))}"
        top30[lim] = (pivot.nlargest(30, col)
                      .reset_index(drop=True)["apparition_id"].tolist())

    # Rank correlations on integrated_best_margin
    rho_45_40 = _rank_corr(pivot["integrated_best_margin_lim45"],
                           pivot["integrated_best_margin_lim40"])
    rho_45_50 = _rank_corr(pivot["integrated_best_margin_lim45"],
                           pivot["integrated_best_margin_lim50"])

    # Top-30 set overlap
    set_45 = set(top30[4.5]); set_40 = set(top30[4.0]); set_50 = set(top30[5.0])
    overlap_45_40 = len(set_45 & set_40)
    overlap_45_50 = len(set_45 & set_50)

    # "Ever visible" counts
    ever_vis = {lim: int((pivot[f"days_any_band_visible_lim{int(round(lim*10))}"] > 0).sum())
                for lim in (4.0, 4.5, 5.0)}

    out = config.REPORTS / "geographic_visibility_sensitivity.md"
    L: list[str] = []
    L.append("# Geographic visibility — sensitivity to limiting magnitude")
    L.append(f"_Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} per spec §5._")
    L.append("")
    L.append("Phase 1 of geographic visibility uses a constant limiting magnitude. "
             "The headline output uses **4.5** (urban-naked-eye threshold). This "
             "report compares the per-apparition rollup at three values "
             "{4.0, 4.5, 5.0}, computed from a single geometry pass that stores "
             "per-sample margins for all three.")
    L.append("")

    L.append("## 1. \"Ever visible\" apparition counts")
    L.append("")
    L.append("How many apparitions have at least one date with `margin > 0` from "
             "any band, at each limit:")
    L.append("")
    L.append("| limit | n apparitions ever visible |")
    L.append("|---|---|")
    for lim in (4.0, 4.5, 5.0):
        L.append(f"| {lim:.1f} | {ever_vis[lim]} |")
    L.append("")

    L.append("## 2. Top-30 stability (rank by `integrated_best_margin`)")
    L.append("")
    L.append(f"- Spearman ρ(lim 4.5, lim 4.0) = **{rho_45_40:.4f}**")
    L.append(f"- Spearman ρ(lim 4.5, lim 5.0) = **{rho_45_50:.4f}**")
    L.append(f"- Top-30 overlap (lim 4.5 ↔ lim 4.0): **{overlap_45_40} / 30**")
    L.append(f"- Top-30 overlap (lim 4.5 ↔ lim 5.0): **{overlap_45_50} / 30**")
    L.append("")
    if overlap_45_40 >= 27 and overlap_45_50 >= 27:
        L.append("**Verdict:** ranking of the top spectacular apparitions is stable "
                 "across the limit range. The choice of 4.5 vs 4.0/5.0 changes the "
                 "depth of integrated visibility but not which comets dominate.")
    else:
        L.append("**Verdict:** ranking shifts more than expected; investigate which "
                 "marginal comets cross the threshold and at what limit.")
    L.append("")

    L.append("## 3. Per-apparition `peak_best_margin` shift")
    L.append("")
    L.append("`peak_best_margin` is `limit − apparent_mag − extinction_at_peak_alt` for "
             "the best (date, band) — so a +0.5 mag change in `limit` lifts peak by "
             "exactly +0.5 mag wherever the dark-window-minimum and altitude rules "
             "still admit the same row. Differences in the dataset arise only when a "
             "different (date, band) wins at a different limit.")
    L.append("")
    delta_45_40 = pivot["peak_best_margin_lim45"] - pivot["peak_best_margin_lim40"]
    delta_50_45 = pivot["peak_best_margin_lim50"] - pivot["peak_best_margin_lim45"]
    finite_45_40 = delta_45_40[delta_45_40.notna() & (delta_45_40 != float("inf"))
                               & (delta_45_40 != float("-inf"))]
    finite_50_45 = delta_50_45[delta_50_45.notna() & (delta_50_45 != float("inf"))
                               & (delta_50_45 != float("-inf"))]
    L.append(f"- Δ(peak_best_margin: lim 4.5 − lim 4.0): "
             f"median {finite_45_40.median():.3f}, "
             f"mean {finite_45_40.mean():.3f}, "
             f"max abs {finite_45_40.abs().max():.3f}")
    L.append(f"- Δ(peak_best_margin: lim 5.0 − lim 4.5): "
             f"median {finite_50_45.median():.3f}, "
             f"mean {finite_50_45.mean():.3f}, "
             f"max abs {finite_50_45.abs().max():.3f}")
    L.append("")
    L.append("Almost-exactly +0.5 medians confirm the additive shift; outliers come "
             "from apparitions that gained/lost a peak (date, band) when the limit "
             "moved.")
    L.append("")

    L.append("## 4. Top-30 list at the headline limit (4.5)")
    L.append("")
    headline = pivot.nlargest(30, "integrated_best_margin_lim45")[
        ["apparition_id", "comet_name", "peak_mag",
         "integrated_best_margin_lim40", "integrated_best_margin_lim45",
         "integrated_best_margin_lim50",
         "days_any_band_visible_lim45"]
    ].reset_index(drop=True)
    L.append("| rank | apparition | comet | peak_mag | int. margin (4.0) | int. margin (4.5) | int. margin (5.0) | days visible (4.5) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for i, r in headline.iterrows():
        L.append(f"| {i+1} | {r['apparition_id']} | {r['comet_name']} | "
                 f"{r['peak_mag']:+.2f} | "
                 f"{r['integrated_best_margin_lim40']:.1f} | "
                 f"{r['integrated_best_margin_lim45']:.1f} | "
                 f"{r['integrated_best_margin_lim50']:.1f} | "
                 f"{int(r['days_any_band_visible_lim45'])} |")
    L.append("")

    out.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
