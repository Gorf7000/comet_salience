"""Diagnostic plots per spec §12. QA/exploratory only — not chapter graphics."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config

logger = logging.getLogger(__name__)


def _save(fig, name: str):
    out = config.FIGURES / name
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    logger.info("saved %s", out)


def plot_all(summary: pd.DataFrame, daily: pd.DataFrame, top_n: int = 10):
    """Generate the diagnostic plot set required by spec §12."""
    config.FIGURES.mkdir(parents=True, exist_ok=True)
    s = summary.copy()
    s = s[pd.to_numeric(s["peak_mag"], errors="coerce").notna()]

    # 1. Peak mag histogram
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(s["peak_mag"].astype(float), bins=30, edgecolor="black")
    ax.axvline(config.NAKED_EYE_MAG_THRESHOLD, color="red", linestyle="--",
               label=f"mag {config.NAKED_EYE_MAG_THRESHOLD}")
    ax.set_xlabel("peak apparent magnitude")
    ax.set_ylabel("apparitions")
    ax.set_title("Distribution of peak apparent magnitude (1850–1940)")
    ax.invert_xaxis()
    ax.legend()
    _save(fig, "01_peak_mag_histogram.png")

    # 2. peak_mag vs days_mag_le_6
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(s["peak_mag"], s["days_mag_le_6"], alpha=0.6)
    ax.set_xlabel("peak apparent magnitude")
    ax.set_ylabel("days mag <= 6")
    ax.invert_xaxis()
    ax.set_title("Peak magnitude vs naked-eye duration")
    _save(fig, "02_peak_vs_duration.png")

    # 3. integrated_mag6_excess vs spectacle_mag6_excess
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(s["integrated_mag6_excess"], s["spectacle_mag6_excess"], alpha=0.6)
    ax.set_xlabel("integrated mag6_excess")
    ax.set_ylabel("spectacle mag6_excess (squared)")
    ax.set_title("Integrated vs spectacle (magnitude family)")
    _save(fig, "03_integrated_vs_spectacle_mag.png")

    # 4. integrated_mag6_excess vs integrated_visible_relative_flux_mag6
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(s["integrated_mag6_excess"],
               s["integrated_visible_relative_flux_mag6"], alpha=0.6)
    ax.set_xlabel("integrated mag6_excess")
    ax.set_ylabel("integrated visible relative flux (mag6 unit)")
    ax.set_title("Magnitude-excess vs flux-proxy families")
    _save(fig, "04_mag_vs_flux_families.png")

    # 5. event_case counts
    if "event_case" in summary.columns:
        fig, ax = plt.subplots(figsize=(7, 4))
        summary["event_case"].value_counts().plot(kind="bar", ax=ax)
        ax.set_ylabel("apparitions")
        ax.set_title("Apparitions by event_case (1850–1940)")
        plt.xticks(rotation=30, ha="right")
        _save(fig, "05_event_case_counts.png")

    # 6. main_sample_candidate counts
    if "main_sample_candidate" in summary.columns:
        fig, ax = plt.subplots(figsize=(5, 4))
        summary["main_sample_candidate"].value_counts().plot(kind="bar", ax=ax)
        ax.set_ylabel("apparitions")
        ax.set_title("Main-sample candidate flag")
        _save(fig, "06_main_sample_candidate.png")

    # 7. Top-N light curves (by integrated_mag6_excess and spectacle and flux)
    for measure, fname in [
        ("integrated_mag6_excess", "07a_top_by_integrated_mag.png"),
        ("spectacle_mag6_excess", "07b_top_by_spectacle_mag.png"),
        ("integrated_visible_relative_flux_mag6", "07c_top_by_flux.png"),
    ]:
        if measure not in s.columns:
            continue
        top = s.sort_values(measure, ascending=False).head(top_n)
        fig, ax = plt.subplots(figsize=(10, 6))
        for _, row in top.iterrows():
            apparition_id = row["apparition_id"]
            curve = daily[daily["apparition_id"] == apparition_id]
            if curve.empty:
                continue
            x = pd.to_numeric(curve["days_from_perihelion"], errors="coerce")
            y = pd.to_numeric(curve["apparent_mag"], errors="coerce")
            ax.plot(x, y, alpha=0.7,
                    label=f'{row["comet_name"][:25]} ({int(row["apparition_year"])}) peak={row["peak_mag"]:.1f}')
        ax.axhline(config.NAKED_EYE_MAG_THRESHOLD, color="red", linestyle="--", alpha=0.4)
        ax.invert_yaxis()
        ax.set_xlabel("days from perihelion")
        ax.set_ylabel("apparent magnitude")
        ax.set_title(f"Top {top_n} apparitions by {measure}")
        ax.legend(fontsize=7, loc="lower right")
        _save(fig, fname)
