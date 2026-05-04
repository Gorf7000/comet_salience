"""Geographic visibility — Phase 1 (geometry + extinction).

Per spec §8.5. For each (apparition, date, band) computes a margin in
magnitudes that captures whether the comet was plausibly naked-eye visible
from US observers in that latitude band on that date:

    margin = limiting_mag - (apparent_mag + extinction_at_peak_alt)

where extinction_at_peak_alt = K * (airmass - 1) using the Young 1994
plane-parallel airmass approximation. Visibility additionally requires
peak altitude > GEO_MIN_ALT_DEG and at least GEO_MIN_VISIBLE_MINUTES of
margin > 0 within the dark window (sun altitude < GEO_DARK_SUN_ALT_DEG).

Phase 1 deferrals (NOT modeled here): moonlight / sky brightness,
surface-brightness / coma diffuseness, era-dependent limiting magnitude,
population weighting.

Performance: comet altitude is computed via direct spherical trig in
numpy (sin(alt) = sin δ sin φ + cos δ cos φ cos HA) using astropy only
for sun positions and apparent sidereal time, both cached per unique
date. This keeps the full ~130M point evaluation under a few minutes.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, get_sun
from astropy.time import Time
from astropy.utils.exceptions import AstropyWarning

from . import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------------

def airmass_young94(alt_deg: np.ndarray | float) -> np.ndarray:
    """Young (1994) plane-parallel airmass with horizon-safe denominator.

        X = 1 / (sin h + 0.025 * exp(-11 * sin h))

    Returns +inf if alt <= 0 (below horizon, undefined).
    """
    alt = np.asarray(alt_deg, dtype=float)
    sa = np.sin(np.radians(alt))
    out = np.where(
        alt > 0.0,
        1.0 / (sa + 0.025 * np.exp(-11.0 * sa)),
        np.inf,
    )
    return out


def comet_alt_from_ha(ra_deg: float, dec_deg: float,
                      lst_deg: np.ndarray, lat_deg: float) -> np.ndarray:
    """Spherical-trig altitude of a fixed (ra, dec) at one observer over an
    array of local apparent sidereal times. All inputs in degrees.
    """
    ha_r = np.radians(lst_deg - ra_deg)
    dec_r = np.radians(dec_deg)
    lat_r = np.radians(lat_deg)
    sin_alt = (np.sin(dec_r) * np.sin(lat_r)
               + np.cos(dec_r) * np.cos(lat_r) * np.cos(ha_r))
    sin_alt = np.clip(sin_alt, -1.0, 1.0)
    return np.degrees(np.arcsin(sin_alt))


# ---------------------------------------------------------------------------
# Per-date precomputation (shared across apparitions)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _NightGrid:
    """Sample-time grid for one calendar date, plus per-band dark masks.

    The grid covers the night that BEGINS on the calendar date `date_str`
    for an East-Coast observer: 24 h starting at date 12:00 UT (≈ NYC
    07:00 local) running to date+1 12:00 UT (next day's late morning).
    The dark window (sun_alt < cutoff) inside this grid is one full night.
    """
    date_str: str
    times_jd: np.ndarray              # shape (N,), Julian dates (TT)
    lst_deg: np.ndarray               # shape (N,), apparent LST at NYC longitude
    sun_alt_per_band: dict[str, np.ndarray]  # band_name -> (N,) sun altitude °


def _build_master_grid_for_dates(dates: list[str], bands: list[dict]) -> dict[str, _NightGrid]:
    """Vectorised precomputation of LST and sun altitudes for many dates.

    Returns a dict date_str -> _NightGrid. Sun positions and LST are
    computed once per sample time (independent of observer); per-band sun
    altitude is then derived by spherical trig in plain numpy. This
    avoids one full astropy frame transformation per band.
    """
    samples_per_night = int(round(24 * 60 / config.GEO_NIGHT_SAMPLE_MINUTES))
    sample_offsets_min = np.arange(samples_per_night, dtype=float) * config.GEO_NIGHT_SAMPLE_MINUTES

    n = len(dates)
    base_times = Time([d + "T12:00:00" for d in dates], scale="utc", format="isot")
    grid_jd = (base_times.jd[:, None]
               + (sample_offsets_min / 1440.0)[None, :]).reshape(-1)
    grid_times = Time(grid_jd, scale="utc", format="jd")

    nyc_lon = config.GEO_OBSERVER_LON_DEG * u.deg

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", AstropyWarning)
        # Local apparent sidereal time at NYC longitude — depends on time
        # and longitude only, identical across bands.
        lst_all = grid_times.sidereal_time("apparent", longitude=nyc_lon).deg
        # Sun (RA, Dec) in GCRS / apparent — this is geocentric, not yet
        # rotated to a horizon frame. Same for all observers.
        sun = get_sun(grid_times)
        sun_ra = sun.ra.deg
        sun_dec = sun.dec.deg

    # Per-band sun altitude via spherical trig in numpy. The helper
    # broadcasts elementwise when ra/dec are arrays matching lst.
    sun_alt_by_band: dict[str, np.ndarray] = {
        b["name"]: comet_alt_from_ha(sun_ra, sun_dec, lst_all, b["lat"])
        for b in bands
    }

    out: dict[str, _NightGrid] = {}
    for i, d in enumerate(dates):
        sl = slice(i * samples_per_night, (i + 1) * samples_per_night)
        out[d] = _NightGrid(
            date_str=d,
            times_jd=grid_jd[sl],
            lst_deg=lst_all[sl],
            sun_alt_per_band={b["name"]: sun_alt_by_band[b["name"]][sl] for b in bands},
        )
    return out


# ---------------------------------------------------------------------------
# Per-(apparition, date, band) margin computation
# ---------------------------------------------------------------------------

def _compute_one(
    ra_app: float, dec_app: float, apparent_mag: float,
    grid: _NightGrid, band: dict,
    limits: tuple[float, ...],
) -> dict:
    """Compute the visibility record for one (apparition_date_row, band).

    Returns a dict matching the long-format output schema (one entry per
    limit produces a per-limit margin/minutes triple suffixed with the
    integer milli-mag of the limit, e.g. "_lim40", "_lim45", "_lim50").
    """
    sun_alt = grid.sun_alt_per_band[band["name"]]
    dark_mask = sun_alt < config.GEO_DARK_SUN_ALT_DEG
    n_dark = int(dark_mask.sum())
    dark_window_minutes = n_dark * config.GEO_NIGHT_SAMPLE_MINUTES

    rec: dict = {
        "band_name": band["name"],
        "band_lat": band["lat"],
        "dark_window_minutes": dark_window_minutes,
    }

    if n_dark == 0 or not np.isfinite(ra_app) or not np.isfinite(dec_app):
        rec["peak_alt_deg"] = -90.0
        rec["airmass_at_peak"] = np.inf
        for lim in limits:
            tag = _lim_tag(lim)
            if not np.isfinite(apparent_mag):
                rec[f"margin_{tag}"] = np.nan
            else:
                rec[f"margin_{tag}"] = -np.inf
            rec[f"minutes_above_threshold_{tag}"] = 0
        return rec

    # Comet altitude across the dark window
    lst_dark = grid.lst_deg[dark_mask]
    alt_samples = comet_alt_from_ha(ra_app, dec_app, lst_dark, band["lat"])
    peak_alt = float(np.max(alt_samples))
    rec["peak_alt_deg"] = peak_alt
    rec["airmass_at_peak"] = float(airmass_young94(peak_alt))

    # NaN apparent_mag: report NaN margins and skip threshold counting
    if not np.isfinite(apparent_mag):
        for lim in limits:
            tag = _lim_tag(lim)
            rec[f"margin_{tag}"] = np.nan
            rec[f"minutes_above_threshold_{tag}"] = 0
        return rec

    # Per-sample airmass (above-horizon); below horizon -> inf -> infinite extinction
    am_samples = airmass_young94(alt_samples)
    ext_samples = config.GEO_EXTINCTION_K * (am_samples - 1.0)
    # mark samples below MIN_ALT as effectively invisible
    below_min = alt_samples < config.GEO_MIN_ALT_DEG
    ext_samples = np.where(below_min, np.inf, ext_samples)

    peak_below_min = peak_alt < config.GEO_MIN_ALT_DEG
    ext_at_peak = (np.inf if peak_below_min
                   else config.GEO_EXTINCTION_K * (rec["airmass_at_peak"] - 1.0))

    for lim in limits:
        tag = _lim_tag(lim)
        # Per-sample margin to determine minutes_above_threshold
        margin_samples = lim - apparent_mag - ext_samples
        n_above = int(np.sum(margin_samples > 0))
        minutes_above = n_above * config.GEO_NIGHT_SAMPLE_MINUTES
        rec[f"minutes_above_threshold_{tag}"] = minutes_above

        if peak_below_min or minutes_above < config.GEO_MIN_VISIBLE_MINUTES:
            rec[f"margin_{tag}"] = -np.inf
        else:
            rec[f"margin_{tag}"] = float(lim - apparent_mag - ext_at_peak)
    return rec


def _lim_tag(lim: float) -> str:
    """4.5 -> 'lim45', 4.0 -> 'lim40', 5.0 -> 'lim50'."""
    return f"lim{int(round(lim * 10)):02d}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_visibility(daily: pd.DataFrame,
                       bands: list[dict] | None = None,
                       limits: tuple[float, ...] = config.GEO_LIMITING_MAG_SENSITIVITY,
                       chunk_dates: int = 500,
                       ) -> pd.DataFrame:
    """Per-(apparition, date, band) visibility margins.

    Parameters
    ----------
    daily
        Daily light-curve DataFrame with columns including `apparition_id`,
        `date` (YYYY-MM-DD string), `RA_app`, `DEC_app`, `apparent_mag`.
    bands
        Latitude bands. Defaults to `config.GEO_VISIBILITY_BANDS`.
    limits
        Limiting magnitudes to evaluate in parallel. Defaults to the
        sensitivity sweep (4.0, 4.5, 5.0).
    chunk_dates
        Number of unique dates to precompute per batch (memory–CPU balance).

    Returns
    -------
    DataFrame with one row per (apparition_id, date, band) and columns:
        apparition_id, date, band_name, band_lat,
        peak_alt_deg, airmass_at_peak, dark_window_minutes,
        margin_lim40, margin_lim45, margin_lim50,
        minutes_above_threshold_lim40, ..._lim45, ..._lim50
    """
    if bands is None:
        bands = config.GEO_VISIBILITY_BANDS

    # Normalise inputs. The upstream daily CSV has a known issue: 66
    # apparitions (~22K rows) have NaN in `date` despite a populated
    # `date_str` like '1924-Jun-01 00:00'. We recover here so those
    # apparitions remain in the visibility analysis; the count is logged
    # for surfacing in the implementation summary.
    cols_in = ["apparition_id", "date", "RA_app", "DEC_app", "apparent_mag"]
    if "date_str" in daily.columns:
        cols_in = ["apparition_id", "date", "date_str", "RA_app", "DEC_app", "apparent_mag"]
    df = daily[cols_in].copy()
    if "date_str" in df.columns:
        missing = df["date"].isna()
        n_missing = int(missing.sum())
        if n_missing:
            recovered = pd.to_datetime(df.loc[missing, "date_str"], errors="coerce").dt.strftime("%Y-%m-%d")
            df.loc[missing, "date"] = recovered
            n_apps_affected = df.loc[missing, "apparition_id"].nunique()
            logger.warning(
                "Recovered %d daily rows (%d apparitions) where `date` was NaN "
                "by parsing `date_str`; surface in implementation summary.",
                n_missing, n_apps_affected,
            )
        df = df.drop(columns=["date_str"])
    df = df[df["date"].notna()].copy()
    df["date"] = df["date"].astype(str)
    df["RA_app"] = pd.to_numeric(df["RA_app"], errors="coerce")
    df["DEC_app"] = pd.to_numeric(df["DEC_app"], errors="coerce")
    df["apparent_mag"] = pd.to_numeric(df["apparent_mag"], errors="coerce")

    unique_dates = sorted(df["date"].unique())
    logger.info(
        "Geographic visibility: %d rows over %d unique dates × %d bands × %d limits",
        len(df), len(unique_dates), len(bands), len(limits),
    )

    out_records: list[dict] = []

    for chunk_start in range(0, len(unique_dates), chunk_dates):
        chunk = unique_dates[chunk_start: chunk_start + chunk_dates]
        grids = _build_master_grid_for_dates(chunk, bands)
        chunk_set = set(chunk)
        sub = df[df["date"].isin(chunk_set)]

        for row in sub.itertuples(index=False):
            grid = grids[row.date]
            for band in bands:
                rec = _compute_one(
                    row.RA_app, row.DEC_app, row.apparent_mag,
                    grid, band, limits,
                )
                rec["apparition_id"] = row.apparition_id
                rec["date"] = row.date
                out_records.append(rec)

        if (chunk_start // chunk_dates) % 5 == 0:
            logger.info("  geographic visibility progress: %d / %d dates",
                        min(chunk_start + chunk_dates, len(unique_dates)),
                        len(unique_dates))

    out = pd.DataFrame.from_records(out_records)
    cols_first = ["apparition_id", "date", "band_name", "band_lat",
                  "peak_alt_deg", "airmass_at_peak", "dark_window_minutes"]
    margin_cols = [c for c in out.columns if c.startswith("margin_")]
    minutes_cols = [c for c in out.columns if c.startswith("minutes_above_threshold_")]
    return out[cols_first + margin_cols + minutes_cols]


# ---------------------------------------------------------------------------
# Apparition-level rollup
# ---------------------------------------------------------------------------

def summarize_apparition_visibility(visibility: pd.DataFrame,
                                    headline_limit: float = config.GEO_LIMITING_MAG,
                                    bands: list[dict] | None = None,
                                    ) -> pd.DataFrame:
    """Roll up the long-format visibility table to per-apparition columns.

    Uses the headline limiting-mag (default 4.5) for the headline rollup
    columns. Sensitivity-limit results live alongside in the long file
    and are summarised by `summarize_apparition_visibility_at_limits`.
    """
    if bands is None:
        bands = config.GEO_VISIBILITY_BANDS
    band_names = [b["name"] for b in bands]
    margin_col = f"margin_{_lim_tag(headline_limit)}"

    df = visibility.copy()
    # Treat -inf and NaN as "not visible"; keep NaN apart for diagnostics.
    margin = df[margin_col]
    visible = (margin > 0).fillna(False)
    df["_visible"] = visible
    df["_margin_pos"] = margin.where(visible, 0.0)

    records: list[dict] = []
    for app_id, g in df.groupby("apparition_id"):
        per_date_band = g.pivot_table(
            index="date", columns="band_name", values="_visible", aggfunc="any",
        ).reindex(columns=band_names, fill_value=False)
        per_date_band_margin = g.pivot_table(
            index="date", columns="band_name", values="_margin_pos", aggfunc="max",
        ).reindex(columns=band_names, fill_value=0.0)

        bands_count_per_date = per_date_band.sum(axis=1)
        any_band_visible = bands_count_per_date > 0
        all_band_visible = bands_count_per_date == len(band_names)
        best_margin_per_date = per_date_band_margin.max(axis=1)

        # Peak across this apparition's (date, band) — find max within g
        g_pos = g[g["_visible"]]
        if not g_pos.empty:
            peak_idx = g_pos[margin_col].idxmax()
            peak_best_margin = float(g_pos.loc[peak_idx, margin_col])
            peak_best_band = str(g_pos.loc[peak_idx, "band_name"])
        else:
            peak_best_margin = float("-inf")
            peak_best_band = ""

        rec = {
            "apparition_id": app_id,
            "peak_best_margin": peak_best_margin,
            "peak_best_band": peak_best_band,
            "bands_visible_count_max": int(bands_count_per_date.max()) if len(g) else 0,
            "days_any_band_visible": int(any_band_visible.sum()),
            "days_all_bands_visible": int(all_band_visible.sum()),
            "integrated_best_margin": float(best_margin_per_date.sum()),
            "integrated_band_exposure": float(per_date_band_margin.values.sum()),
        }
        for bname in band_names:
            rec[f"days_{bname.lower()}_band_visible"] = int(per_date_band[bname].sum())
        records.append(rec)
    return pd.DataFrame(records)


def run_pipeline_step(daily: pd.DataFrame,
                      summary: pd.DataFrame,
                      daily_out_path=None,
                      ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pipeline step: compute geographic visibility, write daily long file,
    roll up to per-apparition columns, and merge into the summary frame.

    Returns (visibility_long, summary_with_geo_columns).
    """
    if daily_out_path is None:
        daily_out_path = config.GEO_DAILY_OUTPUT
    logger.info("Geographic visibility step: computing margins")
    visibility = compute_visibility(daily)

    logger.info("Geographic visibility: writing %d rows -> %s",
                len(visibility), daily_out_path)
    visibility.to_csv(daily_out_path, index=False, compression="infer")

    rollup = summarize_apparition_visibility(visibility)

    # Drop any prior geo-rollup columns so re-runs are idempotent
    geo_cols = [c for c in rollup.columns if c != "apparition_id"]
    summary_clean = summary.drop(columns=[c for c in geo_cols if c in summary.columns])
    summary_with_geo = summary_clean.merge(rollup, on="apparition_id", how="left")

    logger.info("Geographic visibility: appended %d columns to summary", len(geo_cols))
    return visibility, summary_with_geo


def summarize_apparition_visibility_at_limits(
        visibility: pd.DataFrame,
        limits: tuple[float, ...] = config.GEO_LIMITING_MAG_SENSITIVITY,
        bands: list[dict] | None = None,
) -> pd.DataFrame:
    """For sensitivity reporting: per-apparition rollup at each limit.

    Returns a DataFrame keyed by (apparition_id, limit) with peak_best_margin,
    days_any_band_visible, integrated_best_margin.
    """
    if bands is None:
        bands = config.GEO_VISIBILITY_BANDS
    band_names = [b["name"] for b in bands]

    out_rows: list[dict] = []
    for lim in limits:
        margin_col = f"margin_{_lim_tag(lim)}"
        sub = visibility[["apparition_id", "date", "band_name", margin_col]].copy()
        sub["_visible"] = (sub[margin_col] > 0).fillna(False)
        sub["_margin_pos"] = sub[margin_col].where(sub["_visible"], 0.0)

        for app_id, g in sub.groupby("apparition_id"):
            per_date_band_margin = g.pivot_table(
                index="date", columns="band_name", values="_margin_pos", aggfunc="max",
            ).reindex(columns=band_names, fill_value=0.0)
            best_margin_per_date = per_date_band_margin.max(axis=1)
            visible_per_date = best_margin_per_date > 0

            finite_pos = sub.loc[g.index, margin_col].where(g["_visible"])
            peak = float(finite_pos.max()) if finite_pos.notna().any() else float("-inf")

            out_rows.append({
                "apparition_id": app_id,
                "limit": lim,
                "peak_best_margin": peak,
                "days_any_band_visible": int(visible_per_date.sum()),
                "integrated_best_margin": float(best_margin_per_date.sum()),
            })
    return pd.DataFrame(out_rows)
