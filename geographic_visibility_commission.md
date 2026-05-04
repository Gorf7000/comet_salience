# Geographic Visibility — Implementation Commission

_Issued 2026-05-04. Working branch: `geographic-visibility`._

This commission asks you to add a geographic visibility model to the comet
visibility pipeline. The model converts geocentric apparent magnitude into
per-observer-band visibility margins, so the chapter's salience analysis
can use a brightness input that actually reflects what US observers could
see.

The work is **bounded and self-contained**: inputs already exist in the
pipeline output, no new Horizons queries are needed, no upstream module
schemas change. Read this commission end-to-end before you start.

---

## 1. Context — what already exists

The pipeline computes daily geocentric apparent magnitudes for ~619
comet apparitions in 1850-1940. Outputs:

- `data/processed/comet_daily_light_curves.csv.gz` — one row per
  (apparition, date) with columns including `RA`, `DEC`, `RA_app`,
  `DEC_app`, `apparent_mag`, `lunar_elong`, `lunar_illum`, `elong`
  (solar elongation), `phase_angle_deg`, `apparition_id`, `date`,
  `comet_id`, `comet_name`, `perihelion_date`. Geocentric — `AZ/EL` are
  NaN, `airmass` = 999 (Horizons sentinels for "no observer specified").
- `data/processed/comet_brightness_summary.csv` — one row per apparition
  with `peak_mag`, `days_mag_le_6`, `integrated_mag6_excess`,
  `event_case`, etc.
- `comet_visibility_commission_v2.md` — the active spec.
- `reports/salience_brightness_analysis.md` — the reason we're adding
  this. The four "Great Southern Comets" (modeled mag −9 to −13) have
  near-zero US salience because they didn't rise above the horizon for
  US observers. The current geocentric model can't see this.

You can read everything in those files for full context.

---

## 2. What you're building

A new pipeline step that, for each (apparition, date), computes
visibility margins at four US latitude bands. The output is a new daily
CSV plus new columns appended to the brightness summary. The existing
geocentric measures are preserved — the new measures coexist with them
so cross-comparison stays possible.

### 2.1 The four bands

```python
BANDS = [
    ("Gulf",  30.0, "New Orleans"),
    ("South", 35.0, "Memphis"),
    ("Mid",   40.0, "New York"),
    ("North", 45.0, "Minneapolis"),
]
```

Even 5° intervals across the US population belt. The latitude is what
the model uses; the city name is the human-readable label. Longitude is
not needed for Phase 1.

### 2.2 The visibility margin formulation

For each (apparition, date, band), compute:

```
margin = limiting_mag - (apparent_mag + extinction_at_peak_alt)
```

with `extinction_at_peak_alt = k * airmass(peak_alt) - k`, so the
extinction penalty is zero at zenith and grows toward the horizon. (`k`
is the extinction coefficient.)

`margin > 0` means the comet was plausibly naked-eye visible from that
band on that night. Larger margin = brighter relative to threshold.

Use a **simple plane-parallel airmass approximation** with a
secant-altitude form that doesn't blow up near the horizon:

```
airmass = 1 / (sin(alt) + 0.025 * exp(-11 * sin(alt)))
```

(this is the Young 1994 formula; standard reference). For altitude < 5°,
treat the comet as not visible (margin = -infinity), regardless of
airmass — the comet is too low for atmospheric refraction to be reliable.

### 2.3 The dark window

The comet is "visible" only when the sun is below the horizon enough to
darken the sky:

- **Dark window** = times when sun altitude < −12° (nautical twilight).
- The comet's max altitude during the dark window is what counts. If
  the comet's transit is during daylight, find its max altitude during
  the dark window instead (which will be at the start or end of the
  window).
- **Minimum visibility window:** require at least 30 minutes of
  margin > 0 during the dark window before the night counts as visible.

For computational efficiency, you can **sample the night at, say, 5 or
10-minute intervals** and find the max altitude / minutes-of-visibility
numerically. Don't try to solve the geometry analytically — astropy is
fast enough for this scale.

### 2.4 What's deferred

Phase 1 = geometry + extinction only. Explicitly NOT in scope:

- **Moonlight / lunar sky brightness** — `lunar_elong` and `lunar_illum`
  are in the daily CSV but ignore them for Phase 1. Phase 2 will add a
  Krisciunas-Schaefer 1991 sky-brightness model.
- **Surface brightness / coma diffuseness** — Phase 3.
- **Era-dependent limiting magnitude** — Phase 1 uses a constant value.
- **Population weighting** — Phase 1 uses unweighted bands. Population
  weighting (Tier B from `reports/geographic_visibility_design_discussion.md`)
  is a possible follow-on but not part of this commission.

If you find yourself wanting to add any of these to "improve" the
result, **stop and don't**. They're deferred deliberately.

---

## 3. Configuration

Add to `src/comet_visibility/config.py`:

```python
# Geographic visibility (Phase 1: geometry + extinction)
GEO_VISIBILITY_BANDS = [
    {"name": "Gulf",  "lat": 30.0, "city": "New Orleans"},
    {"name": "South", "lat": 35.0, "city": "Memphis"},
    {"name": "Mid",   "lat": 40.0, "city": "New York"},
    {"name": "North", "lat": 45.0, "city": "Minneapolis"},
]
GEO_LIMITING_MAG = 4.5            # urban-naked-eye threshold
GEO_EXTINCTION_K = 0.3            # mag per airmass (standard)
GEO_DARK_SUN_ALT_DEG = -12.0      # nautical twilight cutoff
GEO_MIN_ALT_DEG = 5.0             # below this altitude, treat as invisible
GEO_MIN_VISIBLE_MINUTES = 30      # margin > 0 must persist this long to count
GEO_NIGHT_SAMPLE_MINUTES = 10     # within-night sampling cadence
```

---

## 4. Implementation

### 4.1 New module: `src/comet_visibility/geographic_visibility.py`

Function signature suggestion:

```python
def compute_visibility(daily: pd.DataFrame,
                       limiting_mag: float = config.GEO_LIMITING_MAG,
                       bands: list[dict] = None) -> pd.DataFrame:
    """Per-(apparition, date, band) visibility margins.

    Returns long-format DataFrame with columns:
        apparition_id, date, band_name, band_lat,
        peak_alt_deg, airmass_at_peak, dark_window_minutes,
        minutes_above_threshold, margin
    """
```

Use `astropy.coordinates.SkyCoord` + `AltAz` + `EarthLocation` for the
geometry. For each (apparition, date, band):

1. Build an EarthLocation at (band_lat, longitude=0, height=0). Longitude
   doesn't matter for Phase 1 — same comet position vs same observer
   latitude gives same alt/az regardless of longitude (they just shift
   in time). Use longitude=0 for simplicity.
2. Sample the 24-hour period centered on the date at
   `GEO_NIGHT_SAMPLE_MINUTES` intervals.
3. For each sample: compute sun altitude (astropy
   `get_sun().transform_to(AltAz)`) and comet altitude (using the
   stored `RA_app` and `DEC_app`).
4. Filter to samples where sun_alt < `GEO_DARK_SUN_ALT_DEG`.
5. From those samples: `peak_alt = max(comet_alt)`,
   `dark_window_minutes = len(samples) * GEO_NIGHT_SAMPLE_MINUTES`.
6. Apply extinction at `peak_alt`, compute `margin`.
7. Compute `minutes_above_threshold` = number of dark-window samples
   where the comet's `apparent_mag + extinction(sample_alt)` would be
   less than `limiting_mag`, scaled by `GEO_NIGHT_SAMPLE_MINUTES`.
8. If `peak_alt < GEO_MIN_ALT_DEG` or
   `minutes_above_threshold < GEO_MIN_VISIBLE_MINUTES`,
   set `margin = -inf`.

**Vectorize aggressively.** astropy alt/az is fast in batch — process
all dates and bands at once if memory allows, or chunk by apparition.
Estimate: ~226K dates × 4 bands × ~144 night samples = ~130M alt/az
computations. astropy can do this in a few minutes if vectorized; will
take an hour+ if you loop. Test on a small subset first.

**Cache the per-(date, band) sun-altitude samples** — sun position is
not comet-dependent, so once per (date, band) is enough across all
apparitions.

### 4.2 Apparition-level rollup

Add to `src/comet_visibility/measures.py` (or a new function in the
new module — your call) a function that takes the long-format
visibility table and produces per-apparition columns:

- `peak_best_margin` — max over (date, band) of margin (only counting
  margin > 0 entries; -inf if never visible)
- `peak_best_band` — which band achieved peak_best_margin
- `bands_visible_count_max` — max number of bands simultaneously visible
  on a single night
- `days_any_band_visible` — count of dates where any band had margin > 0
- `days_all_bands_visible` — count of dates where all 4 bands had margin > 0
- `days_north_band_visible` — count for "North" band specifically
- `days_south_band_visible` — count for "Gulf" band specifically (use
  these two as the explicit two-latitude-band metrics)
- `integrated_best_margin` — sum over dates of max(0, best_margin_that_date)
- `integrated_band_exposure` — sum over (date, band) of
  max(0, margin_for_band_that_date) — units of band-day-magnitudes

Append these as new columns to `data/processed/comet_brightness_summary.csv`.
**Do not remove existing columns.**

### 4.3 Pipeline integration

Modify `scripts/run_overnight.py` to call the new visibility step
after the daily light curves are written. The new step reads the daily
CSV, computes visibility, writes the daily visibility CSV, then triggers
the apparition-level rollup which appends columns to the brightness
summary.

The new daily file goes to:
`data/processed/comet_daily_visibility.csv.gz`

Long format (one row per apparition × date × band) is recommended over
wide — easier to filter, easier to extend later, easier to inspect.

---

## 5. Sensitivity checks

Run the full visibility computation **three times** with
`limiting_mag` ∈ {4.0, 4.5, 5.0} and produce a brief comparison
in `reports/geographic_visibility_sensitivity.md`:

- For each apparition, what is `peak_best_margin` at the three
  limiting-mag values?
- Does the rank order of `integrated_best_margin` change between the
  three? Pick top-30 and see if the order is stable.
- Does the count of "ever visible" apparitions change dramatically?
  (`days_any_band_visible > 0`)

Use the 4.5 result for the headline output. The other two are
sensitivity-check only — write them to separate files
(`*_lim4.0.csv` etc.) or compute on the fly for the comparison report.

---

## 6. Validation tests it must pass

Add to `scripts/validate_results.py` a new section "5. Geographic
visibility checks" with these tests:

### 6.1 Sanity-check Halley 1910 vs C/1882 R1

| comet | apparition | expected behavior |
|---|---|---|
| 1P/Halley | 1910 | `peak_best_margin > 2.0` (well-visible from all bands; modeled peak −0.12, ~+30° declination during peak) |
| C/1861 J1 (Tebbutt) | 1861 | `peak_best_margin > 1.0`, mostly visible from all bands |
| C/1882 R1 (Great September) | 1882 | `peak_best_margin > 0` only briefly post-perihelion when tail visible at low northern latitudes — much shorter visibility than Halley despite higher modeled brightness. **This is the central southern-comet test.**
| C/1880 C1 (Great Southern) | 1880 | low or zero `days_any_band_visible` despite modeled peak −9.10. Confirms hemisphere bias. |
| C/1865 B1 (Great Southern) | 1865 | low or zero `days_any_band_visible`. |
| C/1887 B1 (Great Southern) | 1887 | low or zero `days_any_band_visible`. |

If any of these comes out wrong (e.g., C/1880 C1 visible from all bands
for 60+ days), there's a bug. Investigate before reporting done.

### 6.2 Hand-check one row

Pick one (apparition, date, band) — e.g., Halley on 1910-04-20 from the
Mid band — and hand-compute:
- comet RA/Dec at that date (from the daily CSV — already there)
- expected peak altitude (= 90 − |40 − comet_dec|, modulo dark window)
- airmass at that altitude
- margin
- compare to the pipeline output, document in
  `reports/validation_results.md`

### 6.3 Long format integrity

Confirm: for each (apparition, date) in the daily light curves, there
are exactly 4 rows in the visibility CSV (one per band). No nulls in
`peak_alt_deg` (use −90 if never above horizon during the day; use
NaN only for "could not compute" errors).

---

## 7. Documentation deliverables

When done, produce:

1. **Updated spec.** Add §8.5 "Geographic visibility" to
   `comet_visibility_commission_v2.md` documenting the four bands, the
   margin formula, the dark-window definition, the limiting-mag value,
   and what's deferred to Phase 2/3.
2. **Audit report addition.** `reports/comet_visibility_audit.md` should
   gain a "Geographic visibility summary" section: count of apparitions
   with `days_any_band_visible > 0`, count of "fully visible" (all 4
   bands many days), top-10 by `peak_best_margin`, and a callout box for
   the Great Southern Comets showing how their visibility numbers compare
   to their geocentric brightness.
3. **Sensitivity report.** `reports/geographic_visibility_sensitivity.md`
   per §5 above.
4. **Implementation summary.**
   `reports/geographic_visibility_implementation.md` — what was built,
   what tests it passes, any surprises encountered, suggestions for
   Phase 2/3.

Update `reports/session_report.md` and `reports/bigv_promotion_summary.md`
only if the existing content becomes inaccurate. Don't rewrite them
just because something new was added.

---

## 8. Stop conditions — when to ask, not assume

Stop and ask the issuing thread (via the user) if:

- You discover a substantial issue with the existing daily light curves
  that affects what you're building (e.g., RA_app values are missing for
  a chunk of apparitions). Don't try to backfill silently.
- A validation test fails in a way you can't diagnose in 30 minutes of
  investigation.
- You find yourself wanting to change the spec (e.g., "actually 5 bands
  would be better"). The bands and the parameter values were the result
  of explicit design discussion — don't relitigate them.
- You want to add a Phase 2/3 feature "while you're in there." Don't.
  Note it as a follow-on in the implementation summary.
- The full pipeline rerun runtime exceeds 30 minutes — there's probably
  a vectorization issue worth diagnosing.

---

## 9. Workflow

1. Branch is `geographic-visibility` — already created via worktree.
2. Read this commission, then skim the existing files referenced in §1.
3. Write code, run on a small subset (one or two apparitions) to verify
   geometry, then on the full set.
4. Run the validation tests in §6. Don't proceed if §6.1 fails.
5. Run the sensitivity checks in §5.
6. Write the docs in §7.
7. Commit incrementally with descriptive messages. Suggested commit
   sequence:
   - "Add geographic visibility config and module skeleton"
   - "Implement per-(apparition, date, band) margin computation"
   - "Add apparition-level rollup of visibility measures"
   - "Run full pipeline; produce daily visibility CSV"
   - "Add validation tests for geographic visibility"
   - "Sensitivity check across limiting_mag {4.0, 4.5, 5.0}"
   - "Spec §8.5 amendment + audit report addition"
   - "Implementation summary"
8. Push to `geographic-visibility` branch. Do NOT merge to main yourself
   — the issuing thread will review and merge.

---

## 10. Outputs summary (acceptance checklist)

When you report done, the following should exist on the
`geographic-visibility` branch:

- [ ] `src/comet_visibility/geographic_visibility.py` — main module
- [ ] `src/comet_visibility/config.py` — new config constants added
- [ ] `src/comet_visibility/measures.py` (or equivalent) — apparition rollup
- [ ] `scripts/run_overnight.py` — new step integrated
- [ ] `scripts/validate_results.py` — §5 added with tests
- [ ] `data/processed/comet_daily_visibility.csv.gz` — long-format daily
- [ ] `data/processed/comet_brightness_summary.csv` — extended with new
      apparition-level columns; existing columns preserved
- [ ] `comet_visibility_commission_v2.md` — §8.5 added
- [ ] `reports/comet_visibility_audit.md` — geographic visibility section
- [ ] `reports/geographic_visibility_sensitivity.md`
- [ ] `reports/geographic_visibility_implementation.md`
- [ ] `reports/validation_results.md` — updated with §5 results,
      including hand-check from §6.2
- [ ] All tests in §6 passing

If something on the list isn't there, explain why in the
implementation summary.
