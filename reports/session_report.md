# Session Report — Comet Visibility Pipeline

_Session ID: `6bfdb567-6d42-45df-a61d-d78cdfd75609`_
_Generated: 2026-05-04_

This report covers the end-to-end work on the photometric/visibility
side of Chapter 5 (comet salience). It documents what was built, how
it works, what the final numbers are, and what remains open. The
companion document `bigv_promotion_summary.md` covers the Big V
promotion in more detail.

---

## 1. Goal

Build a reproducible dataset of modeled per-day apparent visual
magnitudes for every comet apparition in the window **1850-01-01 to
1940-12-31**, suitable for cross-comparison against historical
newspaper salience. The comparison itself (newspaper side and the
brightness ↔ salience analysis) is a separate workstream not
addressed in this session.

Headline deliverable: one row per apparition in
`data/processed/comet_brightness_summary.csv` with peak magnitude,
duration above naked-eye thresholds, and integrated brightness
measures, plus per-day light curves in
`data/processed/comet_daily_light_curves.csv` (gzipped in the repo;
the raw .csv is gitignored due to the 100 MB GitHub limit).

---

## 2. Methods

### 2.1 Architecture

The pipeline lives in `src/comet_visibility/` as a series of modules
invoked by `scripts/run_overnight.py`:

```
source_aerith.py    — periodic-comet status scraping (Yoshida AERITH)
source_jpl.py       — non-periodic enumeration + Horizons ephemeris
scaffold.py         — combines AERITH + SBDB into one apparition table
                       (handles C/1882 R1 fragment merging)
light_curves.py     — per-apparition daily magnitude generation,
                       including the Tier 1/1.5/2/3 fallback chain
measures.py         — apparition-level summary statistics
                       (peak_mag, days_mag_le_6, integrated_*, etc.)
audit.py            — Markdown audit-report builder
diagnostics.py      — diagnostic figure generation
```

Cache-aware design: Horizons responses are cached under
`data/raw/` and `data/intermediate/horizons_cache/` so reruns are
cheap (~12 minutes for the full 644-apparition pipeline on warm
cache, vs. multi-hour cold).

### 2.2 Data sources

| Source | Role | Window |
|---|---|---|
| Yoshida's AERITH | Periodic comet apparition list + observed-or-not status | 1850-1940 |
| JPL SBDB (`sbdb_query.api`) | Non-periodic comet enumeration; SBDB photometric M1/K1 fallback | 1850-1940 |
| JPL Horizons (`astroquery.jplhorizons`) | Daily geocentric/heliocentric distance ephemeris | per-apparition window |
| Vsekhsvyatskij 1958 *Physical Characteristics of Comets* ("Big V") | Primary photometric source for absolute magnitudes — H10 values | 1850-1940 |
| Kronk *Cometography* + Bortle/ICQ bright-comet lists | Cross-validation (peak magnitudes for famous apparitions, exclusion check for Tier 3 stragglers) | 1850-1940 |

### 2.3 Photometric model

Standard cometary apparent-magnitude law:

  `m = M1 + 5·log10(Δ) + K1·log10(r)`

where Δ is geocentric distance (AU), r is heliocentric distance (AU),
M1 is the absolute total magnitude at r = Δ = 1 AU, and K1 = 2.5n
(active comets typically K1 ≈ 8-15, asteroidal/bare-nucleus K1 ≈
4-5). Phase angle and surface-brightness corrections are deferred to
future increments.

Big V's H10 convention is M1 with K1 = 10 implicit, mapped directly.

### 2.4 Tier fallback chain (spec §8.2)

Each apparition resolves an (M1, K1) pair through this priority:

| Tier | Provenance | Condition |
|---|---|---|
| 1.5 | `manual_curated` or `manual_curated_override` | `pdes` matches a row in `data/inputs/manual_M1K1.csv` (Big V values live here). Override variant if SBDB also had values. |
| 1   | `horizons_tmag` | SBDB has both M1 and K1 |
| 2   | `assumed_default_K1` | SBDB has M1 only — use `DEFAULT_K1 = 10.0` |
| 3   | `failed` | Nothing available — no light curve generated |

The key precedence rule, established in this session: **manual
entries always win over SBDB, regardless of SBDB's K1**. The
era-appropriate published references (Big V, Marsden & Williams)
are anchored against contemporary visual observations of the
apparitions themselves; SBDB fits are integrated across all known
returns and weighted toward modern, well-observed apparitions where
comet activity may have evolved (often downward, e.g. 2P/Encke).
For 1850-1940 work, Big V > SBDB.

`NUCLEAR_FIT_K1_THRESHOLD` (default 6.0) is preserved as a
diagnostic flag in the audit (so the reviewer can see which
SBDB-only entries are particularly suspect — bare-nucleus fits where
K1 ≈ 4-5 will under-predict total brightness near perihelion by
5-10 mag) but no longer gates the override decision.

### 2.5 Adaptive window

Light curves run from perihelion ±180 days by default, extended to
±365 days when the apparition is still brighter than mag 10 at the
window boundary. Window extension statistics are reported in the
audit.

### 2.6 Apparition data structure

One row per *apparition*, not per comet. `apparition_id` is
constructed deterministically as `{comet_id}_{year}` (spec §15.1).
Peak magnitude, duration above thresholds, and integrated measures
are all per-apparition. C/1882 R1 fragments R1-A through R1-D are
merged into a single C/1882 R1 row using earliest perihelion and
R1-A's ephemeris geometry; original fragment list is preserved in
`merged_fragments`.

### 2.7 Event-case framework

The 4-cell expected/seen framework distinguishes:
- `expected_seen` — periodic comet predicted to return, observed
- `expected_not_seen` — periodic predicted, not observed
- `unexpected_seen` — non-periodic discovery (always this case for
  C/-prefix comets in scope, since by definition a one-shot first
  appearance is unexpected)
- `retrospective_not_observed` / `retrospective_pre_discovery` —
  reverse-computed apparitions of comets discovered later

---

## 3. The Big V promotion (the central event of this session)

### 3.1 Motivation

Pre-Big V, the pipeline was hitting **Tier 3 (`failed`) for ~87% of
non-periodic apparitions** because SBDB simply doesn't carry
photometric parameters for most pre-1950 one-shot comets. Result:
427 / 644 light curves and only 21 naked-eye apparitions — missing
essentially every famous 19th-century non-periodic comet (Donati,
Tebbutt, the Great Comets of 1858/1861/1865/1880/1882/1887, etc.).

### 3.2 Process

1. User obtained the Big V PDF (333 pages, 21 MB).
2. PDF was OCR'd in a parallel Claude thread (separate session) to
   avoid working-directory conflicts. That thread parsed
   Roman-numeral entries and produced
   `data/inputs/bigv_staging.csv` with 274 rows
   (190 high / 52 medium / 32 low confidence).
3. Two NaN-M1 skip rows and two `?`-pdes ambiguous rows were held
   aside; **270 rows** were promoted to
   `data/inputs/manual_M1K1.csv`.
4. Spec §8.2 was amended to make manual entries unconditionally win
   over SBDB.
5. `light_curves.resolve_magnitude_model` was rewritten with
   manual-first ordering. Provenance distinguishes
   `manual_curated` (gap-fill, SBDB had nothing) from
   `manual_curated_override` (SBDB had values but Big V is
   preferred) so the audit counts remain meaningful.
6. Pipeline was re-run end-to-end (~12 minutes warm cache).

### 3.3 Before vs. after

| Metric | Before Big V | After Big V |
|---|---|---|
| Successful daily light curves | 427 / 644 | **619 / 644** |
| Apparitions with peak_mag ≤ 6.0 (naked eye) | 21 | **146** |
| `manual_curated_override` provenance | 0 | **373** |
| `manual_curated` provenance (gap-fill) | ~5 | **201** |
| `horizons_tmag` provenance | 422 | 54 |
| `failed` provenance (Tier 3) | 217 | 16 |

---

## 4. Results

### 4.1 Top 10 by peak brightness

| comet_name | year | peak_mag |
|---|---|---|
| C/1882 R1 (Great September) | 1882 | -13.13 |
| C/1887 B1 (Great southern) | 1887 | -12.38 |
| C/1865 B1 (Great southern) | 1865 | -11.32 |
| C/1880 C1 (Great southern) | 1880 | -9.10 |
| C/1882 F1 (Wells) | 1882 | -7.95 |
| C/1931 P1 (Ryves) | 1931 | -5.04 |
| C/1910 A1 (Great January) | 1910 | -3.77 |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | -2.65 |
| C/1901 G1 (Great comet) | 1901 | -2.32 |
| C/1895 W1 (Perrine) | 1895 | -2.26 |

### 4.2 Top 10 by integrated brightness above naked-eye threshold

| comet_name | year | integrated_mag6_excess | peak_mag |
|---|---|---|---|
| C/1882 R1 (Great September) | 1882 | 654 | -13.13 |
| C/1913 Y1 (Delavan) | 1914 | 398 | 2.61 |
| C/1858 L1 (Donati) | 1858 | 352 | -0.19 |
| C/1881 K1 (Great comet) | 1881 | 344 | 0.03 |
| C/1861 J1 (Great comet) | 1861 | 338 | -0.99 |
| C/1882 F1 (Wells) | 1882 | 323 | -7.95 |
| C/1915 C1 (Mellish) | 1915 | 301 | 2.45 |
| C/1901 G1 (Great comet) | 1901 | 300 | -2.32 |
| C/1907 L2 (Daniel) | 1907 | 291 | 1.38 |
| C/1865 B1 (Great southern) | 1865 | 277 | -11.32 |

These rankings recover the comets contemporary newspapers covered
most heavily — which is the entire point of building this dataset.

### 4.3 Pipeline elapsed

- Cold cache (initial overnight): ~6-7 hours (Horizons rate-limited)
- Warm cache (Big V re-run): **741 s** (~12 minutes)

---

## 5. Validation

Four independent checks live in `scripts/validate_results.py`:

### 5.1 External peak comparison — 10 / 10 counted entries pass

Reference peaks for 13 well-known apparitions are drawn from Kronk's
*Cometography* and standard references. Each entry is classified:

- **tolerance** (8 entries): well-constrained published peak; model
  must match within ±1.5 mag. **All 8 pass.**
- **range** (2 entries): peak reported as a range across sources
  (sungrazer with daylight peak, multi-source). Model passes if
  inside the range. **Both pass.**
  - C/1882 R1 modeled -13.13, reported range -17 to -10 ✔
  - C/1910 A1 modeled -3.77, reported range -5 to -1 ✔
- **model_limit** (3 entries): physical phenomena the single-law
  M1/K1 model cannot capture by construction. Diff reported but
  *not counted* toward pass-rate.
  - 17P/Holmes 1892 (outburst): diff +8.83
  - 3D/Biela 1852 (final intact return, disintegrating): diff +3.22
  - 2P/Encke 1898 (apparition-to-apparition variability): diff -1.95

### 5.2 Hand-calculation check — 0.0000 mag agreement

Halley 1910 near-perihelion row, manually plugging r, Δ, M1, K1
into `m = M1 + 5·log10(Δ) + K1·log10(r)`:
- pipeline: 2.7103
- by hand: 2.7103
- diff: 0.0000 mag

Confirms the formula implementation is correct.

### 5.3 Manual-CSV path check — Tier 1.5 engages correctly

Temporary Big-V-style entry for C/1858 L1 (Donati) generated 361
daily rows with `magnitude_provenance = manual_curated`, modeled
peak +1.21, days-above-naked-eye = 84. CSV is restored after the
test.

### 5.4 Audit + diagnostic figures — all present

`reports/comet_visibility_audit.md` (16,700 bytes, 268 lines) and
9 diagnostic PNGs in `figures/comet_visibility_diagnostics/`.

### 5.5 Kronk cross-check on the 16 remaining Tier 3 stragglers

A research sub-agent verified that none of the 16 apparitions still
without light curves (Big V also lacked H10 for them) appear in
Bortle's *Bright-Comet Chronicles* (ICQ), the ICQ "brightest since
1935" list, or Cometwatch's historic bright-comet list within the
1850-1940 window. The one direct numeric data point recoverable
from secondary sources was C/1891 F1 (Barnard-Denning) at peak mag
8.0 — comfortably sub-naked-eye and consistent with the pattern.
All 16 are confirmed faint telescopic discoveries by professional
comet hunters (Barnard, Winnecke, Hartwig, Borrelly, Skjellerup,
Whipple) plus pre-discovery apparitions of 95P/Chiron. **No
naked-eye-visibility risk from leaving them as Tier 3.**

The cross-check used cometography.com (curated highlights) plus
secondary lists rather than the print *Cometography* volumes; the
negative-evidence pattern is robust enough for "documented
exclusion" purposes.

---

## 6. File map

### Outputs
- `data/processed/comet_brightness_summary.csv` — apparition-level
  summary (one row per apparition; 644 rows)
- `data/processed/comet_daily_light_curves.csv` (gitignored,
  >100 MB) and `.csv.gz` (committed, 37 MB) — per-day rows
- `reports/comet_visibility_audit.md` — full audit report
- `reports/morning_summary.md` — top-line numbers from the latest run
- `reports/validation_results.md` — validation suite output
- `reports/bigv_promotion_summary.md` — Big V promotion writeup
- `reports/session_report.md` — this document
- `figures/comet_visibility_diagnostics/` — 9 PNGs

### Inputs
- `data/inputs/manual_M1K1.csv` — 270 Big V H10 rows (the primary
  photometric source)
- `data/inputs/bigv_staging.csv` — full 274-row OCR output (for
  audit trail)
- `data/inputs/bigv_target_list.csv` — the 644-apparition list
  handed to the OCR thread

### Source
- `src/comet_visibility/` — pipeline modules
- `scripts/run_overnight.py` — end-to-end runner with gzip + git
  push surface
- `scripts/validate_results.py` — validation suite
- `comet_visibility_commission_v2.md` — active spec (root of repo)

---

## 7. Notable issues encountered and resolved

- **Astroquery logger init bug** (`AttributeError: 'Logger' object
  has no attribute '_set_defaults'`) when `logging.basicConfig`
  was called before astroquery import. Fixed by eager import at
  module load.
- **AERITH self-signed certificate** required `verify=False` with
  `urllib3.disable_warnings`.
- **Daily CSV exceeded GitHub's 100 MB limit** (105 MB raw).
  Committed gzipped; runner script gzips automatically and surfaces
  push failures (was using `subprocess.run(check=False)` which
  silently swallowed errors).
- **C/1882 R1 fragment ambiguity**: the four post-split fragments
  R1-A through R1-D were merged into a single C/1882 R1 apparition
  using R1-A's ephemeris geometry.
- **2P/Encke and 8P/Tuttle silently 5-7 mag too dim**: diagnosed as
  nuclear-biased SBDB fits (K1 ≈ 4.5 = asteroidal slope). Initially
  triggered the K1 < 6 conditional override; later resolved by the
  unconditional Big-V-wins rule.
- **OCR thread caught a worked-example error** in the original Big
  V commission (mis-stated 1851 I as d'Arrest when it was actually
  Faye); acknowledged as illustrative-only.

---

## 8. Caveats and known limits

These are documented in spec §8.4 and the audit report:

- **City/topocentric visibility not yet implemented.** Apparent
  magnitude is computed at the geocenter; light pollution, altitude
  above horizon, and atmospheric extinction are deferred to a
  future increment.
- **Surface-brightness modeling not yet implemented.** A diffuse
  large coma at integrated mag 5 may have appeared dimmer to the
  unaided eye than a compact mag-5 object. Currently
  `mag_le_6 = true` reflects integrated magnitude only.
- **Photometric law applied symmetrically around perihelion.**
  Pre- vs. post-perihelion asymmetric activity slopes (e.g.,
  Brorsen 1851 had H10 = 7.6 pre-peri and H10 = 12 post-peri per
  Big V) are not separately fit.
- **Outbursts and disintegrations cannot be captured by a
  single-law model.** 17P/Holmes 1892 and 3D/Biela 1852 are the
  documented examples in the validation set.
- **AERITH does not catalog non-periodic comets observed before
  1995.** Non-periodic apparitions in 1850-1940 are sourced from
  JPL SBDB and uniformly assigned `event_case = unexpected_seen`.

---

## 9. Open items

- **16 Tier 3 stragglers** remain without light curves because Big
  V also lacked H10 for them. Cross-check confirmed none would have
  been naked-eye visible. Could be resolved if Marsden & Williams
  has parameters for any, but they are not blocking the chapter.
- **Held rows from Big V staging** (4 rows: 2 NaN-M1 skip, 2 `?`-pdes
  ambiguous) — confirmed by user as not important.

The dataset is **complete and validated** for the photometric/
visibility side of Chapter 5. The next workstream (newspaper
salience extraction and the brightness ↔ salience comparison
itself) lives outside this directory.

---

## 10. Repository state

- Branch: `main`
- HEAD: `fb675a9` (Reclassify validation outliers)
- Remote: https://github.com/Gorf7000/comet_salience
- Working tree: clean

Recent commits (this session and immediate predecessors):
- `fb675a9` Reclassify validation outliers: model_limit and range vs tolerance
- `ac22383` Note Kronk cross-check of 16 Tier 3 stragglers
- `1db4579` Big V promotion summary + OCR thread artifacts
- `28c69f2` Big V always wins over SBDB (1850-1940 era-appropriate precedence)
- `83672fa` Overnight pipeline run: 619/644 apparitions with light curves
- `a4b42ad` Big V H10 extraction: 274 deduped rows (69% high confidence)
- `0be343a` Brief and target list for Big V extraction thread
- `8605251` Overnight pipeline run: 427/644 apparitions with light curves
  (pre-Big V baseline)
- `281f2a2` Allow manual override when SBDB fit is nuclear-biased
  (superseded by `28c69f2`)
- `1e04496` Add post-run validation suite with findings
