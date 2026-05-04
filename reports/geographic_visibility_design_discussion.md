# Geographic Visibility — Design Discussion

_Drafted 2026-05-04. **Discussion document, not a finalized spec.** Captures
the open design questions for adding a geographic-visibility model to the
pipeline. To be reviewed and decided._

---

## 1. Why we're doing this

The salience analysis (`reports/salience_brightness_analysis.md`) surfaced
a clear problem: the four "Great Southern Comets" (modeled mag −9 to −13)
produced very low US newspaper salience because they didn't rise above
the horizon for US observers during their bright phases. The current
pipeline computes geocentric apparent magnitude only, which doesn't
capture this.

Adding a geographic-visibility model converts the "Great Southern Comets
are a documented exclusion" caveat into a real explanation, and produces
a brightness input that's actually relevant to US press coverage.

---

## 2. The starting proposal (from a parallel LLM thread)

Use a four-city basket — **New York, New Orleans, Chicago, San Francisco** —
to compute a nightly city-level visibility margin:

```
night_city_margin = local_limiting_mag - effective_comet_mag
```

where `effective_comet_mag` includes modeled apparent magnitude plus
penalties for altitude/extinction, twilight, moonlight, and (eventually)
surface brightness.

Aggregate per night:
- `best_margin = max(city margins)` — anyone could see it
- `visible_city_count = count where margin > 0` — geographic breadth
- `mean_positive_margin` — depth where visible

Aggregate per apparition:
- `peak_best_margin`
- `days_any_city_visible`, `days_2plus_cities_visible`, etc.
- `max_visible_city_count`
- `integrated_best_margin = sum(max(best_margin, 0))`
- `integrated_city_exposure = sum over nights and cities of max(margin, 0)`

**Explicit don'ts:** don't collapse to mean magnitude (it's reversed and
logarithmic); don't use median (it can erase regional visibility with
only 4 cities).

---

## 3. Evaluation of the starting proposal

### Strong agreement

- **Don't use mean magnitude.** Right call. The question "could anyone in
  US press geography see it" is a max/threshold question, not a
  central-tendency one.
- **The margin formulation is the right unit.** `limiting_mag − effective_mag`
  is directly interpretable in magnitudes.
- **Best-city for "anywhere visible" + city-count or city-exposure for "how
  broadly."** Two questions, two measures.
- **Drop the median.** Even more strongly than the proposal says.

### Where I'd push back / refine

- **The "effective_comet_mag = mag + penalties" framing flattens different
  physics.** Atmospheric extinction adds to comet brightness (dims it).
  Twilight and moonlight raise the *sky brightness* (raise the limiting
  magnitude). They act differently. Cleaner formulation:

  `margin = (limiting_mag − sky_brightness_penalty) − (apparent_mag + extinction)`

  Conflating works for first pass but breaks down when we want to ask "is
  this comet swamped by twilight or by extinction?"

- **Twilight handling is critical and underspecified.** Many great comets
  (sungrazers, near-perihelion bright comets) are only visible at twilight.
  A naive "dark sky" cutoff at sun altitude < −18° would zero out C/1882
  R1. Recommend nautical twilight (sun < −12°) as the dark-sky cutoff,
  with explicit acknowledgment that "twilight comets" need separate
  treatment if we ever care about sungrazer visibility.

- **No "minimum visibility window per night."** A comet visible for 5
  minutes between sunset and comet-set isn't really "visible that night"
  in any historically meaningful sense. Recommend requiring margin > 0
  for at least ~30 minutes during the dark window before counting it.

- **"local_limiting_mag" needs a value.** Urban naked-eye limit varied
  dramatically across our window — pre-electric (1850-1880) urban skies
  were probably ~5–5.5 mag (gas lighting + coal smoke), electrified
  urban (1900-1940) closer to 3.5–4.0. Recommend: pick a single value
  (4.5) for the headline analysis, do a sensitivity check at 4.0 and 5.0
  to confirm rankings are stable. Era-dependent limits are a possible
  refinement but probably second-order.

### What's missing

- **Computational design.** (Originally flagged as a concern. Turned out
  not to be — see §4.)
- **Integration with existing measures.** The new geographic measures
  should *coexist* with the current `peak_mag`, `integrated_mag6_excess`,
  etc., not replace them. Lets us compare modeled-brightness vs.
  geographic-affordance residuals as an additional analysis dimension.

---

## 4. The size question (resolved)

Original concern: 4 cities × hourly geometry samples could blow up to ~10M
rows.

Resolution: not actually a concern.

- **The RA/Dec is already there.** Daily light-curve rows have `RA`,
  `DEC`, `RA_app`, `DEC_app`, `lunar_elong`, `lunar_illum`, solar `elong`,
  `phase_angle_deg`. Horizons gave us all the celestial geometry; it just
  gave it geocentrically (`airmass = 999`, `AZ/EL = NaN` because no
  observer was specified). We have everything to compute per-observer
  alt/az ourselves.
- **No new Horizons queries.** The geographic computation is local.
- **No hourly stepping needed.** Comet max altitude on a given night is
  analytic: `max_alt = 90° − |φ − δ|` at meridian transit. Combined with
  a dark-window check, it's one closed-form computation per (apparition,
  day, observer).
- **Storage:** ~226K daily rows × 4 stations = ~900K computations. Wide
  format adds ~16 columns to the daily CSV (~50–55 MB gzipped, under
  GitHub's 100 MB limit). Long format is ~120 MB raw / ~45 MB gzipped.
  Either fine.
- **Compute:** vectorized via astropy/numpy, probably 30s–2min total.

---

## 5. The latitude-band observation

Looking at the 4-city basket more carefully:

| city | lat | visibility behavior |
|---|---|---|
| New Orleans | 30.0°N | southern station |
| San Francisco | 37.8°N | northern station |
| New York | 40.7°N | northern station |
| Chicago | 41.9°N | northern station |

Three of four cities cluster within ~4° of latitude. **For Phase 1
(geometry + extinction), longitude doesn't affect *whether* a comet is
visible from a given station — only *when* in the night.** At apparition
timescales (months) that just shifts visible nights by hours; same
comets visible, same number of nights, essentially same margin.

Consequence: NYC, Chicago, and SF will compute nearly identical
visibility for almost every comet. The proposed `days_N_cities_visible`
metric is bimodal — values are mostly 0, 1, 3, or 4. There's almost no
genuine "exactly 2 cities visible" case, because if it's visible at any
northern station it's visible at all three. The "city count" is really a
2-bit measure (north band yes/no, south band yes/no) wearing a 5-bit
costume.

**Two cleaner alternatives within the city framework:**

- **A1 — Keep 4 cities, replace city-count with explicit two-band
  metrics.** Headline = `peak_best_margin`. Breadth = `north_band_visible`
  (any of NYC/Chicago/SF) and `south_band_visible` (New Orleans). Drop
  `days_N_cities_visible` as misleading. Cities remain interpretive
  anchor for chapter narrative.
- **A2 — Use 2-3 latitude bands directly, drop the city framing.**
  Simpler model, loses some interpretability ("visible from 30°N" doesn't
  have the same flavor as "visible from New Orleans").

---

## 6. The population-weighted alternative

The 4-city basket is a sparse proxy for "where the US press audience
was." With actual population data we can do better. Three implementation
tiers:

### Tier A — Decadal Census center-of-population

- One representative US observer per decade, shifting position as US
  population center migrates west and slightly north
- 22-row table (1850-1940 by decade) — Census Bureau publishes this
- Visibility margin computed at one latitude per decade
- Loses everything about latitude *spread* — gives you "the median
  voter's view" but doesn't distinguish "visible to half the population"
  from "visible to all"
- **Best for:** sanity check, baseline comparison, simplest possible
  implementation

### Tier B — State-level Census population, binned to latitude (IPUMS NHGIS)

- For each decade, derive `population_fraction(latitude_bin)` from state
  populations + state latitude centroids (or distribute state population
  across its latitude range as a refinement)
- ~25 latitude bins × 10 decades = ~250-row derived table
- Headline metric becomes: **fraction of US population for whom margin > 0**
  on a given night
- Apparition-level: `peak_pop_fraction_visible`,
  `days_>50pct_pop_visible`, `integrated_pop_exposure`
- Tractable work: download NHGIS state population tables, join to state
  latitude centroids, bin
- **Best for:** defensible quantitative model that maps directly to "how
  much of the press audience could see this"

### Tier C — Fang & Jawitz gridded population (1 km × decadal)

- Maximum rigor: continuous spatial population field
- Reduce to latitude distribution per decade by integrating across
  longitude
- Real download + GeoTIFF processing work; probably half a day of
  implementation
- Output is essentially the same as Tier B (population fraction per
  latitude bin per decade) but built from a more principled spatial
  reconstruction
- **Best for:** if the chapter wants the strongest methodological
  grounding, or if longitude analysis becomes interesting in Phase 2

---

## 7. Tradeoffs to think about

The choice between city basket, latitude bands, and population-weighting
hinges on what we want the model to *mean* and how much methodological
weight we want it to carry.

| approach | what it measures | strength | weakness |
|---|---|---|---|
| 4-city basket (as proposed) | "visible from these 4 places" | concrete, interpretable | latitude redundancy, misleading city count |
| 4-city, two-band metrics (A1) | "visible from N or S band" | honest about underlying physics | still arbitrary city selection |
| Latitude bands (A2) | "visible at 30/40°N" | clean, parsimonious | loses geographic interpretability |
| Tier A — pop center | "visible to median voter" | trivial to implement | no distribution information |
| Tier B — pop-binned | "visible to X% of US pop" | maps to press audience | one-time NHGIS data prep |
| Tier C — gridded | "visible to X% of US pop, fully spatial" | maximum rigor | implementation cost |

### Things to weigh

- **What is the chapter's quantitative center of gravity?** If the
  visibility model is a piece of context in a salience-driven chapter,
  Tier A or B is plenty. If geographic visibility is the central
  methodological contribution, Tier C earns its keep.
- **Other model uncertainties dominate.** Limiting magnitude (4.5 vs
  5.0), extinction coefficient (urban vs rural, era-dependent), surface
  brightness (deferred entirely) — all have larger uncertainty than the
  weighting scheme. Going Tier B → Tier C tightens an estimate that's
  already noisy from these other sources.
- **The latitude shift over 1850-1940 was modest.** US population
  moved primarily west, secondarily north, but the latitude
  distribution didn't shift as dramatically as the longitude
  distribution. Tier A (single weighted point) might be closer to Tier
  B than intuition suggests.
- **City framing is good for narrative.** "Visible from New York and
  Chicago but not from New Orleans" is the kind of sentence a humanities
  reader can engage with. Population-fraction metrics are quantitatively
  superior but rhetorically thinner. The city basket can survive as a
  *companion* to whatever quantitative model we build, used in narrative
  passages, even if the headline numbers come from a different scheme.

---

## 8. Other open design questions

These apply regardless of which spatial scheme we pick:

- **Limiting magnitude.** 4.5 default; sensitivity check at 4.0 and 5.0.
  Era-dependent (gas-era vs electric-era) is a possible refinement.
- **Dark-window definition.** Sun altitude < −12° (nautical twilight)
  default, allowing some twilight comet visibility. Stricter sun < −18°
  (astronomical twilight) zeros out sungrazers.
- **Minimum visibility window per night.** Recommend ~30 minutes of
  margin > 0 during the dark window to count the night as visible.
- **Extinction coefficient.** k = 0.3 mag/airmass standard. Could vary
  by era.
- **Storage.** Separate `data/processed/comet_daily_visibility.csv.gz`
  joined to existing daily light curves on `(apparition_id, date)` —
  cleaner cache invalidation. Or fold into the existing daily CSV — keeps
  everything monolithic. I lean separate.
- **Apparition-level summary fields** go into `comet_brightness_summary.csv`
  alongside existing measures, where the salience analysis joins them.
- **Phase 2 (moonlight) and Phase 3 (surface brightness)** are deferred
  but should be planned so the data structure accommodates them without
  rework.

---

## 9. Recommended decisions to make

1. **Spatial scheme.** 4-city (with two-band metrics), explicit latitude
   bands, Tier A pop center, Tier B pop-binned, or Tier C gridded?
2. **Whether to keep the city basket as a narrative companion** even if
   the quantitative model uses a different scheme.
3. **Limiting magnitude** value and whether to make it era-dependent.
4. **Dark-window definition** and **minimum visibility window per night**.
5. **Storage layout** (separate visibility file vs fold into daily CSV).

Once these are decided, the implementation itself is small (~half a day
to a day) and the chapter gets a real geographic-visibility input.

---

## 10. Claude's working recommendation

Tier B (state-population-binned latitude distribution) as the
quantitative model, with the 4-city basket retained as a narrative
companion. Limiting magnitude 4.5 with sensitivity at 4.0/5.0. Nautical
twilight (sun < −12°) as the dark window. 30-minute minimum visibility
window. Separate visibility CSV joined on `(apparition_id, date)`.

This gives us:
- A defensible population-weighted metric for the headline analysis
- City-named visibility ("visible from NYC, not New Orleans") for the
  chapter narrative
- Clean physics separation (extinction vs sky brightness, both modeled
  per latitude)
- A small derived dataset (state-population-by-decade, latitude-binned)
  that's easy to inspect, version, and reproduce
- Coexistence with existing measures so cross-comparison stays possible
- Room to add Phase 2 (moonlight) and Phase 3 (surface brightness)
  without rework

But this is a recommendation, not a decision. Surface this, sit with it,
push back where the framing doesn't match what you want the chapter to
do.
