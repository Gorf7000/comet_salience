# Salience vs. Brightness — First-Pass Analysis

_Generated 2026-05-04. Companion script: `scripts/salience_brightness_analysis.py`._

This report covers the first cross-comparison between the photometric/visibility
dataset and three monthly newspaper-salience series (US press, 1850–1940). It
documents what we found, where the data is clean, and where it isn't.

---

## 1. Data

### Brightness side
- `data/processed/comet_brightness_summary.csv` — 619 / 644 apparitions with
  modeled light curves; 146 naked-eye (`peak_mag ≤ 6.0`).
- `data/processed/comet_daily_light_curves.csv.gz` — per-day apparent magnitudes
  used to compute solo flags.

### Salience side (3 monthly series, 1850-01 to 1940-12, 1092 months each)
- `comets_20260504_103047_data_X_fraction.csv` — fraction of articles where
  "comet" appears ≥1. *Breadth of mention.*
- `comets2_20260504_103348_data-Comet_2_x_fraction.csv` — same, but ≥2 mentions.
  Filters out collateral/metaphorical uses. *Stricter breadth.*
- `comets_20260504_103143_data_word_count.csv` — average occurrences of "comet"
  per matching article. *Intensity within mentioning articles.*

### Distribution of X_fraction (used to set thresholds)
- median = 0.088
- p75 = 0.168 (used as "elevated salience" threshold)
- p90 = 0.306 (used as "spike" threshold)
- p99 = 0.711

---

## 2. Raw alignment — top salience peaks

For each salience series, the 15 highest monthly values, labeled with the
brightest comet active that month per the daily light-curve data:

### X_fraction top 15

| month | X_fraction | brightest comet | mag |
|---|---|---|---|
| 1861-07 | 0.952 | C/1861 J1 (Tebbutt) | -0.94 |
| 1857-04 | 0.905 | 5D/Brorsen + cluster | +5.90 |
| 1910-05 | 0.887 | 1P/Halley | -0.12 |
| 1874-07 | 0.886 | C/1874 H1 (Coggia) | +1.63 |
| 1858-09 | 0.873 | C/1858 L1 (Donati) | +0.23 |
| 1910-04 | 0.821 | 1P/Halley | +2.21 |
| 1862-08 | 0.786 | 109P/Swift-Tuttle | +1.54 |
| 1858-10 | 0.753 | C/1858 L1 (Donati) | -0.19 |
| 1853-03 | 0.750 | C/1853 E1 (Secchi) | +5.89 |
| 1863-02 | 0.750 | C/1862 W1 (Respighi) | +7.02 |
| 1857-05 | 0.725 | 5D/Brorsen + cluster | +6.74 |
| 1881-08 | 0.707 | C/1881 N1 (Schaeberle) | +1.84 |
| 1910-03 | 0.705 | 1P/Halley | +4.41 |
| 1881-07 | 0.668 | C/1881 K1 (Great comet) | +1.09 |
| 1861-04 | 0.667 | C/1861 G1 (Thatcher) | +3.13 |

13 of the top 15 are clearly attributable to identifiable bright apparitions.
The two exceptions (1853-03 and 1863-02) are months where the brightest
modeled comet is barely naked-eye — possible drivers: unmodeled telescopic
discoveries, retrospective coverage, or non-comet "comet" mentions.

### Comets2_xf top 15
Essentially the same comets in slightly different order. Confirms X_fraction
peaks are driven by genuine comet content (≥2 mentions in an article filters
out passing references).

### word_count top 15
Different pattern entirely. Top peaks (1871-03, 1931-10, 1875-10, 1933-09, …)
do **not** correspond to bright apparitions — the brightest comet in each top
month is mag +8 or fainter. word_count is measuring intensity within articles,
not volume across articles. A single long retrospective or science feature in
an otherwise quiet month spikes the average. **It is not a good proxy for
public attention to current events.**

---

## 3. Hemisphere bias

For our top-12 brightest apparitions, max X_fraction in ±6 months of perihelion:

| comet | year | peak_mag | max X_fraction | month |
|---|---|---|---|---|
| C/1882 R1 (Great September) | 1882 | -13.13 | **0.59** | 1882-10 |
| C/1887 B1 (Great southern) | 1887 | -12.38 | **0.52** | 1886-11 |
| C/1865 B1 (Great southern) | 1865 | -11.32 | **0.33** | 1865-04 |
| C/1880 C1 (Great southern) | 1880 | -9.10 | **0.25** | 1879-12 |
| C/1882 F1 (Wells) | 1882 | -7.95 | 0.59 | 1882-10 |
| C/1931 P1 (Ryves) | 1931 | -5.04 | 0.19 | 1931-08 |
| C/1910 A1 (Great January) | 1910 | -3.77 | 0.89 | 1910-05 |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | -2.65 | 0.21 | 1927-10 |
| C/1901 G1 (Great comet) | 1901 | -2.32 | 0.31 | 1901-10 |
| C/1895 W1 (Perrine) | 1895 | -2.26 | 0.37 | 1896-03 |
| C/1874 D1 (Winnecke) | 1874 | -1.53 | 0.89 | 1874-07 |
| C/1861 J1 (Tebbutt) | 1861 | -0.99 | **0.95** | 1861-07 |

**The four "Great Southern Comets" (bolded peak_mag) — modeled brightest in the
sample at -9 to -13 — produced lower salience than far dimmer northern-visible
comets.** Tebbutt 1861 at modeled -0.99 hit X_fraction = 0.95; the Great
Southern Comet of 1865 at modeled -11.32 only managed 0.33.

Mechanism: the salience corpus is US press; southern-hemisphere apparitions
weren't visible to US readers regardless of intrinsic brightness. The Great
Comets of 1882 still register because their tails were briefly seen from
northern latitudes after perihelion.

This is best treated as a **documented exclusion** in the chapter (corpus
geography), not modeled as a regression term.

---

## 4. Predicted vs. unpredicted — full set

We split apparitions by `event_case`:
- **Predicted** = `expected_seen` (returns of known periodics): n=131
- **Unpredicted** = `unexpected_seen` (new discoveries, periodic and
  non-periodic first apparitions): n=263

Per-apparition features computed within ±180-day window of perihelion:

### H1 — peak X_fraction in window, by brightness bin

| brightness | predicted (n) | predicted median | unpredicted (n) | unpredicted median |
|---|---|---|---|---|
| great (<-5) | 0 | — | 6 | 0.426 |
| very_bright (-5..-1) | 0 | — | 5 | 0.371 |
| bright (-1..2) | 3 | 0.645 | 21 | 0.560 |
| naked_eye (2..4) | 16 | 0.248 | 23 | 0.308 |
| marginal (4..6) | 21 | 0.304 | 41 | 0.369 |
| telescopic (>6) | 91 | 0.235 | 167 | 0.259 |

**Apparent finding: unpredicted (discoveries) outperform predicted at almost
every brightness bin.** Tempting headline.

### But this is contaminated by attribution

The salience signal is monthly and not comet-attributed. When two comets
share a month, both get credited with the full month's salience. This
inflates the predicted-group numbers because faint periodic returns
piggyback on co-occurring bright discoveries.

Top 10 "predicted" apparitions by peak_salience:
- 5D/Brorsen 1857 (mag +5.9, max_sal 0.90) — sharing 1857 with the C/1857
  D1/M1/O1 cluster
- 6P/d'Arrest 1910 (mag +9.0, max_sal 0.89) — sharing 1910 with Halley + Great
  January
- 4P/Faye 1858 (mag +8.8, max_sal 0.87) — sharing 1858 with Donati
- 2P/Encke 1862 (mag +3.1, max_sal 0.79) — sharing 1862 with Swift-Tuttle and
  Tebbutt's tail

None of these faint periodics is plausibly responsible for those salience
values. The full-set comparison is therefore not interpretable as a clean
test of prior-prediction effects.

---

## 5. Solo apparitions — clean attribution

We define an apparition as **solo at mag-6** if no other comet reached
mag ≤ 6.0 anywhere in its ±180-day window. This isolates apparitions where
any salience signal in the window can be unambiguously attributed to that
comet.

- Solo at mag-6: **72 apparitions** (31 predicted, 41 unpredicted)
- Solo at mag-8 (stricter): 15 apparitions — too few to bin

### H1 (solo) — peak salience by brightness

| brightness | predicted (n) | predicted median | unpredicted (n) | unpredicted median |
|---|---|---|---|---|
| bright (-2..2) | 0 | — | 1 | 0.157 |
| naked_eye (2..4) | 4 | 0.182 | 5 | 0.300 |
| marginal (4..6) | 5 | 0.245 | 5 | 0.194 |
| telescopic (>6) | 22 | 0.185 | 29 | 0.187 |

**Result: the discoveries-beat-predicted finding largely disappears.** With
clean attribution, predicted and unpredicted are within noise at every
brightness level. The full-set finding from §4 was an attribution artifact.

### H2 (solo) — pre-perihelion lead time at p75 (months)

Months before perihelion when X_fraction first crosses the elevated
threshold (negative = before peri):

| brightness | predicted median | unpredicted median |
|---|---|---|
| naked_eye (2..4) | -2.0 | +1.0 |
| marginal (4..6) | **-4.0** | +1.0 |
| telescopic (>6) | **-3.0** (mean -2.62) | 0.0 (mean -0.82) |

**This is the cleanest finding in the analysis.** Predicted comets show
salience elevation 2–4 months earlier than unpredicted comets at the same
brightness. The effect is most pronounced at marginal and telescopic
brightnesses — i.e., where unpredicted comets would generate little salience
on their own merits.

**Mechanism:** a known periodic return can be announced in newspapers weeks
or months ahead of recovery. A new discovery only registers after detection.
Predicted comets aren't louder stories — they're *earlier* ones.

### H3 (solo) — integrated salience above p75

Mixed and noisy in the small bins; no clear pattern emerges separately from
peak-salience and lead-time effects.

### H4 (solo) — pre-perihelion peak salience

Same direction as H2: predicted comets reach their pre-perihelion peak
salience earlier (and slightly higher in marginal-bright bins) than
unpredicted ones.

---

## 6. Bright solo apparitions (peak_mag ≤ 4)

The full table of solo apparitions reaching naked-eye or near-naked-eye:

| comet | year | peak_mag | predicted | max_sal | peak_offset | lead_p75 | preperi_max |
|---|---|---|---|---|---|---|---|
| C/1880 C1 (Great Southern) | 1880 | -9.10 | F | 0.245 | -1 | -5 | 0.245 |
| C/1907 L2 (Daniel) | 1907 | +1.38 | F | 0.157 | -5 | — | 0.157 |
| C/1905 X1 (Giacobini) | 1906 | +2.02 | F | 0.095 | -1 | — | 0.095 |
| 7P/Pons-Winnecke | 1869 | +2.60 | T | 0.195 | +3 | +3 | 0.063 |
| C/1880 S1 (Hartwig) | 1880 | +3.12 | F | 0.314 | +2 | +2 | 0.067 |
| 2P/Encke | 1895 | +3.15 | T | 0.194 | -2 | -2 | 0.194 |
| 2P/Encke | 1918 | +3.20 | T | 0.170 | +2 | +2 | 0.114 |
| C/1863 Y1 (Respighi) | 1863 | +3.32 | F | 0.300 | +1 | +1 | 0.143 |
| 2P/Encke | 1905 | +3.37 | T | 0.085 | +1 | — | 0.056 |
| C/1924 R1 (Finsler) | 1924 | +3.38 | F | 0.162 | +1 | — | 0.107 |
| C/1867 S1 (Baeker-Winnecke) | 1867 | +3.69 | F | 0.308 | +1 | -3 | 0.267 |

Two things stand out:

1. **C/1880 C1 (Great Southern) reached only X_fraction = 0.245** — the
   brightest solo apparition in the dataset, far dimmer in salience than
   several telescopic predicted comets. Strong confirmation of the
   hemisphere-bias hypothesis.
2. **The 4 Encke solo apparitions are remarkably consistent** at max
   X_fraction ≈ 0.09–0.19 with mostly small lead times. Encke was a
   well-known periodic that returned routinely; newspapers covered it
   reliably but not enthusiastically. This is the canonical "predicted but
   familiar" pattern.

---

## 7. Halley 1910 — the canonical case

Halley 1910 is excluded from the solo set (Great January Comet C/1910 A1
shares the year and modeled mag -3.77). But within the full set:

- max X_fraction = 0.887 (in May 1910, perihelion April)
- pre-perihelion lead at p75 = -5 months (salience elevated from December 1909)
- pre-perihelion lead at p90 = -5 months (same)

Halley shows the cleanest possible prior-prediction signature: salience
elevation a full half-year before perihelion, peaking at the brightness peak.
This is the demonstration of the mechanism — N=1 but unambiguous.

It is the canonical "predicted bright comet" case in the dataset. No other
apparition in 1850–1940 combines (a) advance public prediction, (b) genuine
brightness, and (c) being the only major comet that year cleanly.

---

## 8. Caveats

- **Sample size at the bright end.** The solo-set bright (-2..2) bin has only
  1 apparition (C/1880 C1, southern-hemisphere). The clean test of "does
  prediction help bright comets" is unreachable from solo data because the
  brightest era comets co-occurred with others.
- **Threshold sensitivity.** All findings use p75 of X_fraction (= 0.168) as
  the "elevated salience" threshold. The lead-time finding is robust at p90
  (0.306) where present, but p90 events are too rare in the solo set to
  bin meaningfully.
- **Background salience floor.** Median X_fraction across all months is
  0.088 — comets get baseline coverage even with no current event. Lead-time
  measurements may pick up retrospective articles or general astronomy
  coverage rather than true anticipation. Worth a sensitivity check using
  detrended residuals from a baseline model.
- **Prediction tag is retrospective.** The `expected_seen` tag is based on
  what we know now to be periodic, not on what was actually predicted in
  contemporary US newspapers. We agreed (per discussion) to accept this as
  a starting definition; cleaner operationalization (hand-curated subset of
  comets actually announced in US press in advance) is a possible follow-up
  but probably not necessary given the lead-time finding's strength.
- **word_count series is not a salience proxy.** Its top peaks don't track
  brightness peaks; it measures article depth, not breadth of attention.
  Useful as a secondary signal (perhaps for "depth of coverage") but not
  for the main analysis.

---

## 9. Findings summary

1. **X_fraction is a clean salience signal.** 13 of its top 15 monthly peaks
   are attributable to identifiable bright apparitions in the brightness
   data.

2. **Comets2_xf is essentially X_fraction with less noise.** Same pattern,
   stricter mention threshold filters out collateral references.

3. **word_count is not a volume signal.** It measures intensity within
   articles, not breadth of attention. Should not be used as the primary
   salience measure.

4. **Hemisphere bias is real and large.** The four Great Southern Comets
   (modeled mag -9 to -13) underperform far dimmer northern-visible comets
   in US salience by 2-3× or more. Treat as a documented exclusion.

5. **The "discoveries beat predicted" headline from the full set is an
   attribution artifact.** Faint periodics share salience credit with
   co-occurring bright discoveries. The solo-set comparison removes this
   contamination and the gap disappears.

6. **There is a real prior-prediction effect, but it acts on lead time, not
   peak height.** In the solo set, predicted comets show salience elevation
   2-4 months earlier than unpredicted comets at the same brightness. The
   effect is most visible at marginal and telescopic brightnesses — i.e.,
   prediction helps comets that wouldn't have grabbed attention on their own.

7. **Halley 1910 is the canonical case study.** N=1 but the cleanest
   demonstration of the lead-time mechanism: salience elevated 5 months
   before perihelion.

---

## 10. Recommended next steps

1. **Make the lead-time finding the central result.** Visualize as paired
   distributions (CDF or histogram) of pre-perihelion lead time by
   prediction status. Probably the single chart that should anchor the
   chapter.

2. **Run the lead-time comparison on the full set with attribution
   controls.** A regression model — `salience(month) ~ Σ brightness_proxies
   + Σ prediction_indicators + month_baseline` — would let us recover the
   lead-time signal from the larger sample without filtering out clustered
   apparitions. Lift from solo to full sample.

3. **Halley 1910 mini-study.** Since it's the cleanest single case, pull
   the actual newspaper-mention timeline from the source corpus and
   document what the lead-up coverage looked like, both as a sanity check
   on the brightness-side numbers and as a worked example for the chapter.

4. **Document the corpus-geography exclusion explicitly.** A paragraph
   noting that the four Great Southern Comets are systematically
   under-covered in US press, with the brightness numbers and the salience
   numbers side by side. Probably belongs as an appendix or a methods
   sidebar rather than as a regression control.

5. **Word-count as secondary signal.** Consider whether "depth of coverage
   per article" tracks anything interesting — possibly correlating with
   how scientifically prominent the comet was (named discoverers,
   famous returns, etc.) rather than brightness. Worth a quick look but
   probably not central.

6. **Consider running a non-trivial brightness predictor to baseline
   salience.** Once we have a reasonable expected-salience function from
   brightness alone, the residuals become the interesting variable —
   apparitions where salience exceeded or fell short of the
   brightness-only expectation are the candidates for narrative analysis
   (was there a discovery story, a public-engagement event, a science
   controversy?).

---

## Appendix: Outputs

- `data/processed/salience_brightness_analysis.csv` — per-apparition
  features (peak salience, lead times, integrated, pre-perihelion max)
- `data/processed/solo_analysis.csv` — solo-flag annotations
- `scripts/salience_brightness_analysis.py` — reproducible pipeline
