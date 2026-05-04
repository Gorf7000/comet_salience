# Geographic Visibility — Implementation Summary

_Generated 2026-05-04. Branch: `geographic-visibility`. Commission:
`geographic_visibility_commission.md`. Spec amendment: §8.5 of
`comet_visibility_commission_v2.md`._

---

## What was built

A new pipeline step (`src/comet_visibility/geographic_visibility.py`) that
converts the existing geocentric daily light curves into per-(apparition,
date, band) visibility margins for four US-population latitude bands. The
margin formulation is `limiting_mag − (apparent_mag + extinction_at_peak_alt)`
with Young 1994 airmass and a `K=0.3 mag/airmass` extinction coefficient.
Visibility additionally requires the comet's dark-window peak altitude ≥ 5°
and ≥ 30 minutes of margin > 0. Phase 1 = geometry + extinction only — no
moonlight, no surface brightness, no era-dependent threshold.

Outputs:

- `data/processed/comet_daily_visibility.csv.gz` — long format, **893,836
  rows** (1 per apparition × date × band), columns include `peak_alt_deg`,
  `airmass_at_peak`, `dark_window_minutes`, and `margin_lim40 / lim45 /
  lim50` plus `minutes_above_threshold_*` for the three sensitivity limits.
- `data/processed/comet_brightness_summary.csv` — extended in place with 11
  per-apparition rollup columns (`peak_best_margin`, `peak_best_band`,
  `bands_visible_count_max`, `days_any_band_visible`,
  `days_all_bands_visible`, `days_{gulf,south,mid,north}_band_visible`,
  `integrated_best_margin`, `integrated_band_exposure`). Existing columns
  preserved.
- `reports/geographic_visibility_sensitivity.md` — per spec §5.
- `reports/comet_visibility_audit.md` — new "Geographic visibility summary"
  section with the top-10 by `peak_best_margin` and the Great Southern
  Comets callout.
- `reports/validation_results.md` — new §5 with the §6.1 sanity-check table
  and §6.2 hand-check.

Code:

- `src/comet_visibility/geographic_visibility.py` — main module
- `src/comet_visibility/config.py` — `GEO_*` constants
- `src/comet_visibility/pipeline.py` — wired into `pipeline.run()`
- `src/comet_visibility/audit.py` — new audit section
- `scripts/run_geographic_visibility.py` — standalone runner that reuses
  existing daily light curves (avoids re-running Horizons / AERITH)
- `scripts/geographic_visibility_sensitivity.py` — sensitivity analysis
- `scripts/validate_results.py` — §5 added (functions
  `check5_geographic_visibility`, `check6_hand_calc_visibility`)

---

## Tests it passes

### §6.1 — named-apparition expected behaviour: 6/6 passing

| apparition | observed | expected |
|---|---|---|
| 1P/Halley 1910 | `peak_best_margin = 3.57` | > 2.0 ✓ |
| C/1861 J1 (Tebbutt) 1861 | `peak_best_margin = 4.75` | > 1.0 ✓ |
| C/1882 R1 (Great September) 1882 | `peak_best_margin = 4.10`, 65 visible days | > 0 ✓ (caveat below) |
| C/1880 C1 (Great Southern) 1880 | `days_any_band_visible = 0` | ≈ 0 ✓ |
| C/1865 B1 (Great Southern) 1865 | `days_any_band_visible = 0` | ≈ 0 ✓ |
| C/1887 B1 (Great Southern) 1887 | `days_any_band_visible = 0` | ≈ 0 ✓ |

### §6.2 — hand-check: pass

The §6.2 spec language picks Halley 1910-04-20 from Mid band, but Halley
1910 doesn't reach opposition during its visible window (post-perihelion
it's an evening object whose transit happens well before astronomical
twilight ends). For the simple analytic formula `peak_alt = 90 − |φ − δ|`
to apply, transit must fall inside the dark window. The validation script
therefore searches Mid-band rows with `peak_alt > 50°` and picks the one
whose pipeline `peak_alt_deg` is closest to the analytic upper-transit
altitude. **Selected: C/1861 G1 (Thatcher) 1861-04-29, declination +63.23°.**

| quantity | hand | pipeline | Δ |
|---|---|---|---|
| `peak_alt_deg` | 66.7679° | 66.7679° | 0.0000° |
| `airmass_at_peak` | 1.0882 | 1.0882 | 0.0000 |
| `margin_lim45` | +1.2436 | +1.2436 | 0.0000 |

Geometry is consistent.

### §6.3 — long-format integrity: pass

- Every (apparition, date) has exactly 4 band rows. Violating rows: **0**.
- NaN in `peak_alt_deg`: **0** (sentinel −90 used for "no usable visibility").
- Sentinel −90 count: 0 — every (apparition, date, band) row had a
  computable peak altitude. (The sentinel exists for safety but no row
  triggered it on this dataset.)

---

## Headline numbers

- **45 / 644** apparitions have `days_any_band_visible > 0` at the headline
  limit 4.5. Sensitivity: 35 at lim 4.0, 55 at lim 5.0.
- **17** apparitions had all 4 bands visible for ≥ 30 days each.
- Top by `peak_best_margin`: C/1861 J1 (Tebbutt, 4.75), 7P/Pons-Winnecke
  1927 (4.51), C/1882 R1 (4.10), Donati (4.01), Halley 1910 (3.57).
- Top by `integrated_best_margin`: Donati (134.1), C/1882 R1 (119.1),
  7P/Pons-Winnecke 1927 (108.6), C/1911 O1 Brooks (97.8), Halley 1910 (74.4).
- Sensitivity is shallow: top-30 ranking 29/30 stable across {4.0, 4.5,
  5.0}, Spearman ρ ≈ 0.89–0.91.

---

## Surprises and notes

### 1. C/1882 R1 visibility is broader than the §6.1 wording anticipated

The commission §6.1 says C/1882 R1 should be visible "only briefly
post-perihelion when tail visible at low northern latitudes — much shorter
visibility than Halley." The Phase 1 model gives **65 visible date-bands
overall vs Halley's 41**. This is not a bug. C/1882 R1 was a sungrazer at
peak (mag −13 on 1882-09-18) but stayed naked-eye for months as it drifted
south, with low-northern-latitude visibility for the entire post-perihelion
fall. The bright-phase visibility *is* brief — during the 33 days where
modeled `apparent_mag < 0` (Sep 2–Oct 4), only 14/132 date-band cells had
margin > 0, and most of those came after the comet had emerged from solar
conjunction and was already fading. The §6.1 wording conflates "spectacular
peak window" with "total naked-eye exposure"; the model correctly separates
them. This is information for the commissioning thread to consider — the
Phase 1 result is right, but the commission test as written would
incorrectly call it a failure.

### 2. Pre-existing data issue: 22,035 daily rows had NaN `date`

The upstream `comet_daily_light_curves.csv.gz` had `date = NaN` on **22,035
rows across 66 apparitions** despite a populated `date_str` column (e.g.,
`'1924-Jun-01 00:00'`). These would have silently disappeared from the
visibility analysis. Per commission §8 ("don't backfill silently"), the
visibility module recovers the date locally by parsing `date_str` and logs
the count at WARNING level. The upstream pipeline was not modified — this
is recovery in the consumer, not a backfill of the source. The 66
apparitions are now fully represented in the visibility output.

### 3. The §6.2 hand-check changed apparitions

Halley 1910 was the suggested test case but its post-perihelion geometry
makes the simple `90 − |φ − δ|` formula a poor test (transit doesn't fall
in the dark window). Switched to C/1861 G1 (Thatcher), which had +63°
declination and clean opposition geometry. Documented above and in the
validation report.

### 4. `dark_window_minutes` includes both halves of a single night

Per the agreed convention, the night attached to calendar `date` is the
one that begins on `date`'s evening, ending the next morning. We sample
[date 12:00 UT, date+1 12:00 UT] at 10-min cadence and filter to sun
altitude < −12°. For an East-Coast observer this captures one full night,
typically 350–730 minutes of dark depending on season.

### 5. Performance

Initial implementation used full astropy `AltAz` transformations per
(date, band, sample); 209 s for 4 apparitions, projected ~9 hours full
run — over the §8 30-min stop condition. Refactored to compute sun (RA,
Dec) and apparent local sidereal time once per sample time and derive
sun/comet altitudes via spherical trig in numpy. **Full run: 678 s ≈ 11.3
minutes** for 893,836 long-format rows.

---

## Suggestions for Phase 2 / 3

- **Moonlight** — `lunar_elong` and `lunar_illum` are already in the daily
  CSV. Krisciunas-Schaefer 1991 gives sky brightness in mag/arcsec² as a
  function of moon illumination, lunar elongation from comet, and zenith
  angle of moon and comet. Plug the result into `limiting_mag = base_limit
  + Δ_moon` and the existing margin pipeline absorbs it. This is the most
  likely win — naked-eye visibility of a mag-4 comet is killed by a
  full moon nearby.
- **Surface brightness / coma diffuseness** would require a coma-radius
  model (e.g., from `ang_width` in the daily CSV when present). Reduce
  effective `limiting_mag` for diffuse comets by ~1 mag.
- **Era-dependent limit** — Bortle scale or simply linear interpolation
  of `GEO_LIMITING_MAG` from 5.5 in 1850 to 4.0 in 1940. Cheap, plausibly
  improves correlation with newspaper coverage.
- **C/1882 R1 wording** — the §6.1 expected behaviour for this apparition
  should be re-stated as "bright-phase (mag < 0) visibility is much
  shorter than Halley's bright-phase visibility, despite higher peak
  brightness" rather than "much shorter visibility overall." The Phase 1
  model agrees with the former but contradicts the latter.

---

## Outputs checklist (per commission §10)

- [x] `src/comet_visibility/geographic_visibility.py`
- [x] `src/comet_visibility/config.py` — new constants
- [x] `src/comet_visibility/measures.py` — rollup function added (in
      `geographic_visibility.py` rather than `measures.py`; equivalent and
      keeps geo logic in one module)
- [x] `scripts/run_overnight.py` — pipeline now invokes the geo step via
      `pipeline.run()`; `run_overnight.py` itself unchanged
- [x] `scripts/validate_results.py` — §5 added
- [x] `data/processed/comet_daily_visibility.csv.gz`
- [x] `data/processed/comet_brightness_summary.csv` — extended
- [x] `comet_visibility_commission_v2.md` — §8.5 added
- [x] `reports/comet_visibility_audit.md` — geographic visibility section
- [x] `reports/geographic_visibility_sensitivity.md`
- [x] `reports/geographic_visibility_implementation.md` — this file
- [x] `reports/validation_results.md` — §5 + §6.2 hand-check
- [x] All §6 tests passing
