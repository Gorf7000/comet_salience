# Commission: Build a Comet Apparition Brightness and Visibility-Opportunity Dataset, 1850–1940

## 0. Purpose

Build a reproducible Python pipeline that creates an apparition-level comet brightness dataset for use in a later Chapter 5 newspaper salience analysis.

This commission is **not** asking for newspaper analysis yet. It is also **not** asking for city-level or topocentric visibility modeling yet. The immediate goal is to generate a defensible comet apparition scaffold and daily geocentric apparent-magnitude light curves, then summarize each apparition using brightness-duration and spectacle measures.

The underlying research question for this increment is:

> For comet apparitions between 1850 and 1940, how bright did each apparition become, for how long did it remain plausibly naked-eye relevant, and how should that brightness-duration opportunity be summarized for later comparison with newspaper coverage?

The larger Chapter 5 logic is that comet salience will later be compared across expectation and visibility. This increment only builds the comet-side visibility/brightness information.

---

## 1. Core Requirements

Produce a pipeline that:

1. Builds or ingests an **apparition-level comet scaffold** for comet apparitions from **1850 through 1940**.
2. Preserves source-based apparition status information, especially AERITH/Yoshida status categories.
3. Derives traceable `expected` and `seen` Boolean fields from the raw status where possible.
4. Generates daily modeled apparent-magnitude light curves for each apparition where data are available.
5. Computes both:
   - magnitude-threshold brightness-duration measures; and
   - flux/apparent-brightness proxy measures.
6. Flags, but does not prematurely delete, boundary cases such as faint/telescopic apparitions, retrospective pre-discovery appearances, and ambiguous source records.
7. Produces clean processed CSV outputs, diagnostic plots, and an audit report documenting missing data, ambiguous identifiers, failed source matches, exclusions, and assumptions.

The pipeline should be designed so that a later increment can add city-level/topocentric visibility modeling for New York, Chicago, New Orleans, and San Francisco. Do not implement that city layer in this run.

---

## 2. Non-Goals for This Increment

Do **not** perform any of the following in this run:

1. Do not analyze newspapers.
2. Do not compute newspaper salience, article counts, event windows, baselines, or keyword frequencies.
3. Do not implement city-specific visibility for New York, Chicago, New Orleans, or San Francisco.
4. Do not model twilight, altitude, moonlight, horizon effects, local weather, or sky brightness.
5. Do not create a final historical interpretation of comet salience.
6. Do not collapse ambiguous historical cases into clean categories without preserving raw source evidence.
7. Do not create a category like `major_public_prediction_event`; that bakes interpretive conclusions into the dataset.
8. Do not apply hand-curated photometric overrides or special-case treatment for individually famous apparitions. Treat all apparitions through the same pipeline rules; let outliers emerge from the data.

This increment should produce the astronomical/apparition brightness dataset only.

---

## 3. Conceptual Model

The unit of analysis is:

```text
one comet apparition / return / appearance
```

not simply one comet.

This matters because a comet can have multiple historical statuses across different apparitions:

- first discovery;
- known or anticipated return;
- missed return;
- lost comet;
- recovered comet;
- retrospective pre-discovery appearance.

The final dataset must therefore be organized at the **apparition level**.

The basic historical-event logic is:

```text
expected = true / false
seen = true / false
```

These fields produce four conceptual cases:

| Expected? | Seen? | Event case |
|---|---|---|
| true | true | expected_seen |
| true | false | expected_not_seen |
| false | true | unexpected_seen |
| false | false | unexpected_not_seen |

For later analysis, the main contrast will probably be:

```text
expected_seen vs. unexpected_seen
```

But for this increment, keep all cases that can be responsibly represented in the data. Use flags and audit notes rather than premature deletion.

---

## 4. Source Architecture

Use multiple sources, but keep their roles distinct. Do not let one source silently override another without recording the conflict.

### 4.1 AERITH / Seiichi Yoshida

Use AERITH/Yoshida as the **primary apparition scaffold and historical-status source**.

Main uses:

- apparition list;
- raw apparition status;
- expected/seen coding scaffold;
- discovery vs. appeared vs. not-observed logic;
- retrospective pre-discovery cases.

Preserve raw AERITH status values exactly as source fields where possible.

Important raw status categories include:

```text
Discovered
Appeared
Not observed
Appeared before discovery
Not observed before discovery
Returns in the future
```

Do not collapse `Appeared before discovery` into ordinary `Appeared` or ordinary `Discovered`. It should remain traceable as a separate retrospective category.

### 4.2 JPL Horizons / JPL SBDB

Use JPL Horizons / SBDB as the main source for:

- object identifiers;
- orbital/ephemeris data;
- daily apparent magnitude where available or computable;
- heliocentric and geocentric distances if useful;
- comet photometric parameters (`M1`, `K1`) where available;
- perihelion dates and designation cross-checks.

The pipeline may use `astroquery.jplhorizons`, direct Horizons API calls, or another reproducible JPL-based method. Cache all API responses locally.

### 4.3 Minor Planet Center

Use MPC as a cross-check source for:

- official comet designations;
- identity matching;
- alternate names;
- object/discovery metadata where useful.

Do not use MPC as the primary source for expectation/seen status unless AERITH is unavailable or ambiguous.

### 4.4 Secondary Audit Sources

Use sources such as COBS, ICQ-style observations, Kronk, Marsden & Williams, or other cometography references only as **audit/cross-check sources**, especially for important or ambiguous cases.

Main uses:

- resolving ambiguous identifiers;
- checking historically important outliers;
- validating suspicious light curves;
- resolving major disagreements between AERITH and JPL/MPC metadata.

These sources are not required to be fully automated if that would take disproportionate effort. Manual audit notes are acceptable, provided they are documented.

---

## 5. Date and Scope Rules

### 5.1 Time Range

Target apparitions:

```text
1850-01-01 through 1940-12-31
```

The apparition should be included if its relevant apparition/perihelion/discovery/appearance falls within this range.

If an apparition straddles the boundary, preserve it and flag it for review rather than silently excluding it.

### 5.2 Relevance Scope

The intended main sample is:

```text
1850–1940 comet apparitions with plausible naked-eye relevance
```

However, do not overfilter during initial collection. Prefer this workflow:

```text
collect candidate apparition records broadly
attempt light-curve generation
compute peak magnitude and summary measures
flag main_sample_candidate based on brightness/public relevance
preserve fainter or failed cases with exclusion_reason / audit notes
```

This lets later analysis explain what was excluded and why.

### 5.3 Default Light-Curve Window

Use the following default date window for modeled light curves:

```text
perihelion_date - 180 days through perihelion_date + 180 days
```

If no perihelion date is available but a discovery date is available:

```text
discovery_date - 180 days through discovery_date + 180 days
```

If neither perihelion date nor discovery date is available:

```text
mark no_light_curve_window = true
skip light-curve generation
write the issue to the audit report
```

### 5.4 Adaptive Window Extension

The ±180-day window is coarse. Implement an optional adaptive extension rule:

1. Generate the default ±180-day light curve.
2. If `mag <= 6` occurs within 14 days of either boundary, extend that side by 30 days.
3. Repeat until either:
   - no threshold-relevant brightness occurs near the boundary; or
   - a hard maximum of ±365 days from perihelion is reached.

Record whether the window was extended:

```text
window_extended = true / false
window_extension_reason
window_start
window_end
```

---

## 6. Status Coding Rules

Create the following fields:

```text
raw_status_source
raw_aerith_status
expected
seen
event_case
status_mapping_confidence
status_notes
manual_review_status
```

### 6.1 Default AERITH Mapping

Use this first-pass mapping:

| Raw AERITH status | expected | seen | event_case | Notes |
|---|---:|---:|---|---|
| Discovered | false | true | unexpected_seen | newly discovered apparition |
| Appeared | true | true | expected_seen | known/anticipated return observed |
| Not observed | true | false | expected_not_seen | expected/lost/missed return |
| Appeared before discovery | null | true | retrospective_pre_discovery | preserve separately |
| Not observed before discovery | null | false | retrospective_not_observed | likely exclude from main sample |
| Returns in the future | null | null | future_return | exclude from 1850–1940 analysis unless historically relevant due to source error |

Use `null` rather than forcing historical expectation where the source status is retrospective.

### 6.2 Traceability Requirement

Every derived `expected`, `seen`, and `event_case` value must be traceable to:

1. raw status;
2. mapping rule;
3. source basis;
4. optional manual override note.

If the code cannot confidently map a case, set:

```text
manual_review_status = true
status_mapping_confidence = low
```

and preserve the row.

---

## 7. Reserved (Outliers and Exceptions — Out of Scope)

A section on outlier handling and per-comet exceptions was considered and removed. Per-apparition special-casing (Halley, Biela, etc.) is out of scope for this increment. All apparitions pass through the same pipeline rules; outliers are surfaced via audit flags rather than handled by name.

This section number is preserved to keep downstream numbering stable.

---

## 8. Daily Light-Curve Generation

For each apparition with usable identifiers and date windows, generate a daily light curve.

Required fields for daily light-curve output:

```text
apparition_id
comet_id
comet_name
designation
source_object_id
date
julian_date
perihelion_date
days_from_perihelion
apparent_mag
mag_source_or_method
magnitude_model_provenance
heliocentric_distance_au
geocentric_distance_au
phase_angle_deg
raw_ephemeris_source
orbit_condition_code
orbit_data_arc_days
light_curve_quality_flag
light_curve_notes
```

If some ephemeris columns are unavailable, preserve the light curve if `apparent_mag` is available. If `apparent_mag` is unavailable, record failure in the audit report.

### 8.1 Magnitude Quality

Comet magnitudes can be uncertain. Add quality fields:

```text
magnitude_model_available
magnitude_model_parameters_available
observed_magnitude_available
magnitude_quality
magnitude_notes
```

Use simple labels:

```text
high
medium
low
failed
```

The goal is not to solve historical comet photometry perfectly, but to make uncertainty visible.

### 8.2 Magnitude Model Fallback

The standard photometric law for total comet visual apparent magnitude is:

```text
m = M1 + 5 * log10(geocentric_distance_au) + K1 * log10(heliocentric_distance_au)
```

where `M1` is the absolute total magnitude (at r = Δ = 1 AU) and `K1` is the activity slope. Typical active comets have `K1 ≈ 10` (equivalent to n = 4); inactive/asteroidal bodies have `K1 ≈ 5`. JPL Horizons returns the result of this law as `T-mag` when SBDB stores both parameters.

For apparitions where Horizons does not return a usable T-mag, apply the following tiered fallback:

| Tier | Provenance tag | Condition | Action |
|---|---|---|---|
| 1 | `horizons_tmag` | Horizons returns T-mag | Use it directly |
| 1.5 | `manual_curated` | Apparition's `pdes` matches a row in `data/inputs/manual_M1K1.csv` | Use the (M1, K1) from the curated CSV |
| 2 | `assumed_default_K1` | SBDB has `M1` but not `K1` | Compute manually using `DEFAULT_K1` |
| 3 | `failed` | Neither `M1` nor `K1` available, and no manual entry | Skip light curve; set `missing_magnitude_model = true` and `failed_light_curve = true` |

Each daily light-curve row must record `magnitude_model_provenance` with one of: `horizons_tmag`, `manual_curated`, `assumed_default_K1`, `failed`.

The curated CSV (Tier 1.5) exists to fill SBDB gaps for historically observed comets that JPL has not parameterized — typically pre-1950 non-periodic comets. Required columns: `pdes`, `M1`, `K1`, `source_citation`, `notes`. The `source_citation` must reference a published photometric reference (e.g., Vsekhsvyatskij 1958, Marsden & Williams *Catalogue of Cometary Magnitudes*) and is recorded per daily row in `manual_curated_source_citation`.

**Tier precedence is strict and SBDB wins on conflict.** If a `pdes` exists in both SBDB (Tier 1 or 2) and the manual CSV, SBDB takes precedence and the audit report records the conflict. The manual CSV is for filling gaps, not overriding existing JPL values.

Configuration:

```python
DEFAULT_K1 = 10.0   # active-comet activity slope, equivalent to n = 4
```

Rules:

1. **Total magnitudes only.** Use `M1`/`K1` (total). Do not substitute `M2`/`K2` (nuclear) when total parameters are missing — nuclear magnitudes systematically underestimate naked-eye visibility. Record presence/absence of `M2`/`K2` in the audit report but do not use them in the light curve.
2. **Symmetric law.** Apply the photometric law symmetrically around perihelion. Do not attempt to fit pre- vs. post-perihelion asymmetric activity slopes. Record `photometric_law = symmetric` in the audit report.
3. **No manual overrides.** Do not apply hand-curated `M1`/`K1` values for famous or boundary-case apparitions. If Horizons T-mag disagrees with documented historical accounts for a specific apparition, log the discrepancy in the audit report and leave the value unchanged.
4. **No fabricated values.** Tier 3 apparitions get no light curve. They appear in the apparition summary table with `failed_light_curve = true` and `missing_magnitude_model = true`.

`magnitude_quality` labels (from §8.1) map to tier and fit quality as follows:

| magnitude_quality | Typical tier and parameter quality |
|---|---|
| high | Tier 1 with both `M1` and `K1` fit from a well-observed apparition |
| medium | Tier 1 with sparse or single-branch fit, OR Tier 2 (default `K1` applied) |
| low | Tier 2 where `M1` itself is suspicious (e.g., extrapolated from a single apparition of a lost comet) |
| failed | Tier 3 |

### 8.3 Orbit Quality

Where Horizons exposes an orbit-uncertainty indicator (e.g., `condition_code`, `data_arc_in_days`, or equivalent), record it on each daily light-curve row:

```text
orbit_condition_code
orbit_data_arc_days
orbit_quality_notes
```

Do not propagate orbital uncertainty into the magnitude calculation. The goal is to make orbit quality visible alongside magnitude quality, not to model uncertainty propagation.

---

## 9. Brightness-Duration Measures

Compute two parallel measure families from the daily apparent-magnitude curve.

Do **not** compute or report raw `magnitude × duration`. Magnitude is logarithmic and reversed, so that measure is misleading.

### 9.1 Magnitude-Threshold Family

Use magnitude 6 as the default naked-eye threshold.

For each daily row:

```text
mag6_excess = max(6 - apparent_mag, 0)
mag6_excess_squared = mag6_excess ** 2
mag_le_6 = apparent_mag <= 6
```

For each apparition:

```text
peak_mag = minimum apparent_mag
date_peak_mag = date of minimum apparent_mag
days_mag_le_6 = count(days where apparent_mag <= 6)
integrated_mag6_excess = sum(mag6_excess)
spectacle_mag6_excess = sum(mag6_excess_squared)
```

Interpretation:

- `integrated_mag6_excess` captures brightness-duration opportunity above naked-eye threshold.
- `spectacle_mag6_excess` privileges short periods of exceptional brightness over long periods of marginal visibility. The squared form is an exploratory weighting choice, not a derivation; later analysis may revisit the exponent.

Examples:

```text
10 days at mag 5 → 10 × (6 - 5) = 10
5 days at mag 2  → 5 × (6 - 2) = 20
```

Spectacle version:

```text
30 days at mag 5.5 → 30 × (0.5^2) = 7.5
7 days at mag 2    → 7 × (4^2) = 112
```

### 9.2 Flux / Apparent-Brightness Proxy Family

Also compute a linearized brightness proxy from magnitude.

For each daily row:

```text
flux_proxy = 10 ** (-0.4 * apparent_mag)
relative_flux_mag6 = 10 ** (-0.4 * (apparent_mag - 6))
visible_relative_flux_mag6 = relative_flux_mag6 if apparent_mag <= 6 else 0
visible_relative_flux_mag6_squared = visible_relative_flux_mag6 ** 2
```

For each apparition:

```text
peak_flux_proxy = max(flux_proxy)
integrated_flux_proxy = sum(flux_proxy)
integrated_visible_relative_flux_mag6 = sum(visible_relative_flux_mag6)
spectacle_visible_relative_flux_mag6 = sum(visible_relative_flux_mag6_squared)
```

Interpretation:

- `relative_flux_mag6` places magnitude 6 at 1 threshold unit.
- brighter-than-threshold days accumulate more strongly because flux is linearized.
- the squared version provides a spectacle-weighted flux proxy.

Keep both the magnitude-excess family and the flux family. Later newspaper analysis can test which produces the clearer signal.

---

## 10. Apparition-Level Summary Output

Create one apparition-level summary table with at least the following fields.

### 10.1 Identity and Source Fields

```text
apparition_id
comet_id
comet_name
designation
alternate_designations
apparition_year
perihelion_date
discovery_date
window_start
window_end
window_extended
raw_status_source
raw_aerith_status
source_notes
```

### 10.2 Expected/Seen Fields

```text
expected
seen
event_case
status_mapping_confidence
status_notes
manual_review_status
retrospective_pre_discovery_case
```

### 10.3 Brightness Fields

```text
peak_mag
date_peak_mag
days_mag_le_6
integrated_mag6_excess
spectacle_mag6_excess
peak_flux_proxy
integrated_flux_proxy
integrated_visible_relative_flux_mag6
spectacle_visible_relative_flux_mag6
```

### 10.4 Quality and Inclusion Fields

```text
magnitude_quality
light_curve_quality_flag
main_sample_candidate
exclude_from_main_sample
exclusion_reason
faint_or_telescopic_only
ambiguous_status
ambiguous_identifier
failed_horizons_match
failed_light_curve
missing_magnitude_model
audit_notes
```

---

## 11. Main-Sample Candidate Logic

Do not permanently delete non-main-sample records from the processed output.

Set:

```text
main_sample_candidate = true
```

when:

```text
peak_mag <= 6
AND failed_light_curve = false
AND event_case is not future_return
AND event_case is not retrospective_not_observed
```

Set:

```text
exclude_from_main_sample = true
```

only when a clear reason applies.

Possible exclusion reasons:

```text
peak magnitude fainter than 6
no usable light curve
future return
retrospective non-observation
ambiguous identity
outside date range
no usable date window
```

Keep all rows in the summary table unless the record is a duplicate or demonstrably erroneous.

---

## 12. Diagnostics and Plots

Produce diagnostic figures, not interpretive chapter graphics yet.

Required diagnostic plots:

1. Histogram of `peak_mag`.
2. Scatterplot: `peak_mag` vs. `days_mag_le_6`.
3. Scatterplot: `integrated_mag6_excess` vs. `spectacle_mag6_excess`.
4. Scatterplot: `integrated_mag6_excess` vs. `integrated_visible_relative_flux_mag6`.
5. Count of apparitions by `event_case`.
6. Count of apparitions by `main_sample_candidate`.
7. Light-curve plots for top N apparitions by:
   - `integrated_mag6_excess`;
   - `spectacle_mag6_excess`;
   - `integrated_visible_relative_flux_mag6`.

Store plots in:

```text
figures/comet_visibility_diagnostics/
```

Do not overinterpret these figures. They are QA and exploratory tools.

---

## 13. Audit Report

Create a Markdown audit report:

```text
reports/comet_visibility_audit.md
```

The audit report should include:

1. Number of raw apparition records collected.
2. Number within 1850–1940.
3. Number successfully matched to ephemeris/light-curve source.
4. Number with failed Horizons/JPL match.
5. Number with missing perihelion date and missing discovery date.
6. Number with successful apparent-magnitude curves.
7. Number with `peak_mag <= 6`.
8. Number of `main_sample_candidate = true` records.
9. Counts by `event_case`.
10. Counts by `magnitude_model_provenance` (`horizons_tmag` / `assumed_default_K1` / `failed`).
11. Counts by `magnitude_quality` (`high` / `medium` / `low` / `failed`).
12. Counts of apparitions with `M2`/`K2` parameters present in SBDB but unused (per §8.2).
13. Adaptive-window statistics: number of apparitions where the ±180-day window was extended, and number that hit the ±365-day cap.
14. List of ambiguous identifiers.
15. List of ambiguous statuses.
16. List of rows requiring manual review.
17. List of boundary cases surfaced by audit flags (faint/telescopic, retrospective, etc.).
18. Summary of magnitude-quality labels.
19. Any API failures, missing data, or assumptions.

The audit report should also include the following caveats explicitly:

- City/topocentric visibility is not implemented in this increment.
- `mag_le_6 = true` reflects integrated magnitude only. A large diffuse comet at integrated mag 5 may have appeared dimmer to the eye than a compact comet at the same magnitude. Surface-brightness modeling is deferred to the city-visibility increment.
- The photometric law is applied symmetrically around perihelion (`photometric_law = symmetric`). Pre- vs. post-perihelion asymmetric activity slopes are not fit.
- No hand-curated `M1`/`K1` overrides have been applied for any apparition.

---

## 14. Required File Outputs

Use this directory structure unless the existing project already has a better convention.

```text
data/
  raw/
    comet_sources/
  intermediate/
    aerith_apparitions_raw.csv
    comet_identifier_matches.csv
    horizons_cache_index.csv
  processed/
    comet_apparitions_coded.csv
    comet_daily_light_curves.csv
    comet_brightness_summary.csv

figures/
  comet_visibility_diagnostics/

reports/
  comet_visibility_audit.md

notebooks/
  comet_visibility_pipeline.ipynb

src/
  comet_visibility/
    __init__.py
    config.py
    source_aerith.py
    source_jpl.py
    source_mpc.py
    status_mapping.py
    light_curves.py
    measures.py
    diagnostics.py
    audit.py
    pipeline.py
```

Minimum required final outputs:

```text
data/processed/comet_apparitions_coded.csv
data/processed/comet_daily_light_curves.csv
data/processed/comet_brightness_summary.csv
reports/comet_visibility_audit.md
notebooks/comet_visibility_pipeline.ipynb
```

---

## 15. Reproducibility Requirements

The pipeline must be rerunnable.

Requirements:

1. Put parameters in a config file or clearly marked config section.
2. Cache all remote-source responses.
3. Never silently overwrite raw downloaded/source data.
4. Never auto-invalidate the remote-query cache. Cache invalidation must be triggered manually (e.g., a `--refresh-cache` flag or explicit deletion of cache files). Reruns against an unchanged cache must produce byte-identical processed outputs.
5. Log failed source requests.
6. Preserve raw status values and raw identifiers.
7. Preserve manual-review flags.
8. Document all assumptions in the audit report.
9. Use deterministic output file names.
10. Include enough comments/docstrings that a future coding session can extend the pipeline.

Suggested config values:

```python
START_DATE = "1850-01-01"
END_DATE = "1940-12-31"
DEFAULT_WINDOW_DAYS = 180
MAX_WINDOW_DAYS = 365
WINDOW_EXTENSION_STEP_DAYS = 30
WINDOW_EXTENSION_BOUNDARY_DAYS = 14
NAKED_EYE_MAG_THRESHOLD = 6.0
DEFAULT_K1 = 10.0
CACHE_REMOTE_QUERIES = True
IMPLEMENT_CITY_VISIBILITY = False
```

### 15.1 Apparition ID Construction

`apparition_id` must be deterministic across pipeline reruns. Construct as:

```text
apparition_id = f"{comet_id}_{perihelion_year}"
```

where `comet_id` is the JPL/MPC primary designation with whitespace removed. For apparitions sharing the same `(comet_id, perihelion_year)` (rare but possible for short-period comets with two perihelia in one calendar year), append `_a`, `_b`, … in chronological order of perihelion.

For apparitions without a perihelion date, fall back to:

```text
apparition_id = f"{comet_id}_d{discovery_year}"
```

with the `_d` prefix marking discovery-date-derived IDs. Record which form was used in `apparition_id_source` (`perihelion` / `discovery`).

---

## 16. Failure Behavior

If the code cannot retrieve or compute something, it should not fabricate values.

Use explicit failure columns:

```text
failed_horizons_match
failed_light_curve
missing_perihelion_date
missing_discovery_date
missing_magnitude_model
manual_review_status
audit_notes
```

Examples:

- If an AERITH apparition cannot be matched to JPL/Horizons, preserve the row and set `failed_horizons_match = true`.
- If a JPL match exists but no magnitude is available (Tier 3, per §8.2), preserve the row and set `failed_light_curve = true` and `missing_magnitude_model = true`.
- If the status cannot be mapped cleanly, preserve the raw status and set `manual_review_status = true`.
- If a record appears duplicated, write it to the audit report before dropping or merging.

No invented values. No silent exclusions.

---

## 17. Implementation Notes

### 17.1 Suggested Python Stack

Use standard scientific Python tools where possible:

```text
pandas
numpy
matplotlib
requests
astroquery
astropy
python-dateutil
pathlib
```

Pin versions in `requirements.txt` (or equivalent). The `astroquery.jplhorizons` interface has changed shape across versions and an unpinned environment will silently break reruns.

Do not use `ace_tools`.

### 17.2 Notebook and Script Both Required

Provide both:

1. a notebook for inspection and handoff:

```text
notebooks/comet_visibility_pipeline.ipynb
```

2. a script/module pipeline that can be rerun:

```text
src/comet_visibility/pipeline.py
```

The notebook can call the same functions used by the script. Avoid notebook-only logic.

### 17.3 Dataframe Display

In the notebook, show:

1. first 20 rows of the apparition scaffold;
2. rows requiring manual review;
3. brightest apparitions by `peak_mag`;
4. top apparitions by `integrated_mag6_excess`;
5. top apparitions by `spectacle_mag6_excess`;
6. top apparitions by `integrated_visible_relative_flux_mag6`;
7. summary counts by `event_case`.

---

## 18. Validation Checks

Implement validation checks before writing final outputs.

Required checks:

1. `apparition_id` is unique in apparition-level tables.
2. Every daily light-curve row has an `apparition_id` that appears in the apparition scaffold.
3. Every apparition summary row has exactly one `apparition_id`.
4. `peak_mag` equals the minimum `apparent_mag` in the daily table for that apparition.
5. `days_mag_le_6` equals count of daily rows where `apparent_mag <= 6`.
6. `integrated_mag6_excess` equals sum of daily `mag6_excess`.
7. `spectacle_mag6_excess` equals sum of daily `mag6_excess_squared`.
8. `main_sample_candidate` is not true when `failed_light_curve = true`.
9. Retrospective statuses are not forced into ordinary expected/unexpected cases without manual notes.
10. No rows with missing key dates are used for light-curve generation unless a documented fallback window exists.
11. Every daily light-curve row has a non-null `magnitude_model_provenance` value drawn from the allowed set.
12. No daily light-curve rows exist where `magnitude_model_provenance = failed` (Tier 3 apparitions must produce no daily rows).

Write validation failures to the audit report and, where serious, stop the pipeline before final export.

---

## 19. Expected Final Summary

At the end of the notebook and audit report, provide a concise run summary:

```text
Raw apparition records collected: N
Records in 1850–1940 scope: N
Successfully matched to ephemeris source: N
Successful daily light curves: N
Main-sample candidates, peak_mag <= 6: N
Manual-review records: N
Failed/ambiguous records: N
Magnitude provenance breakdown: horizons_tmag=N, assumed_default_K1=N, failed=N
```

Then show the top 10 apparitions by:

```text
peak brightness
integrated_mag6_excess
spectacle_mag6_excess
integrated_visible_relative_flux_mag6
```

Do not interpret these historically yet. Label them as diagnostic rankings.

---

## 20. Handoff Note for Future Increment

This pipeline should be designed so the next increment can add local observing geometry.

Future city-level visibility increment will likely add:

```text
reference cities:
    New York City
    Chicago
    New Orleans
    San Francisco

nightly/topocentric variables:
    altitude
    azimuth
    twilight state
    solar elongation
    moon altitude / phase / separation
    local limiting magnitude
    diffuse comet penalty
    effective comet magnitude
    visibility_margin
```

Future visibility-margin formula:

```text
visibility_margin = local_limiting_mag - effective_comet_mag
```

where:

```text
effective_comet_mag = apparent_comet_mag + diffuse_comet_penalty
```

Do not implement this in the present run. Just keep IDs, dates, and light-curve outputs organized so this layer can be attached later.

---

## 21. Final Instruction to Coding Agent

Build the smallest robust pipeline that satisfies the above. Prioritize traceability over completeness. If a source is hard to scrape, blocked, inconsistent, or ambiguous, document that problem and produce a partial but honest dataset rather than inventing or silently filling values.

The successful result is not a perfect historical comet catalog. The successful result is a reproducible, auditable, apparition-level brightness dataset that can later be joined to newspaper salience measures.
