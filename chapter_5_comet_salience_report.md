# Chapter 5 Comet Salience Plan

## 1. Chapter 5 Frame: Salience

Chapter 5 is organized around **salience**: the conditions under which astronomical events become available to public attention.

The completed eclipse case established the first half of the chapter logic:

> **Eclipses show salience shaped by spatial accessibility.**

For eclipses, the working question was: **Where could the event be seen?**

The comet case extends the chapter by shifting from spatial accessibility to temporal and observational availability:

> **Comets show salience shaped by how an object becomes visible, expected, noticed, or missed over time.**

The current chapter-level pairing is therefore:

| Case | Salience mechanism |
|---|---|
| Eclipses | Spatial accessibility and visibility |
| Comets | Temporal availability, perceptual visibility, and expectation |

The larger claim to test is that salience is not simply a function of astronomical occurrence or intrinsic importance. It depends on the conditions under which an event becomes publicly available.

---

## 2. Completed Eclipse Case

The eclipse case used central eclipses only:

- Total
- Annular
- Hybrid

Eclipse locations were binned as:

- United States
- Europe
- Near-United States
- Near-Europe
- Remote land
- Ocean

The result showed a strong accessibility gradient:

> **United States > Europe / Near regions > Remote land > Ocean**

Interpretation:

> Eclipse salience tracks accessibility and visibility. Events available to familiar publics or familiar geographies generate more newspaper attention than remote or oceanic events.

This creates the baseline for the comet case.

---

## 3. Comet Case: Core Question

The comet case asks:

> How do the ability to see a comet and the expectation of seeing it relate to newspaper coverage, both individually and together?

Earlier formulation:

> Does salience attach more to prediction or discovery?

Refined formulation:

> How do **expectation** and **visibility affordance** shape the temporal morphology of comet coverage?

This avoids reducing the question to a simple binary of “predicted vs discovered.” The real interest is how expectation and perceptual availability interact.

---

## 4. Unit of Analysis

The unit of analysis should be:

```text
one comet apparition / return / appearance
```

Not simply “one comet.”

This matters because the same comet can pass through multiple historical statuses:

- first discovery
- known return
- missed return
- lost comet
- recovered comet
- retrospectively identified pre-discovery appearance

So the dataset should be organized at the **apparition level**, not only at the comet-identity level.

---

## 5. Expected × Seen: Main Event Logic

The simplified event structure uses two boolean flags:

```text
expected = true / false
seen = true / false
```

These produce a four-cell structure:

| | **Seen** | **Not seen** |
|---|---|---|
| **Expected** | Known / anticipated return | Missed or lost predicted return |
| **Not expected** | Newly discovered apparition | Ignore |

The main comparison is between the two visible cells:

```text
expected + seen
vs.
not expected + seen
```

In prose:

> **known/anticipated return vs. newly discovered apparition**

The side case is:

```text
expected + not seen
```

This captures missed or lost returns. These may be useful for controls or side discussions, but they should not drive the main comparison unless there is a specific reason.

The ignored case is:

```text
not expected + not seen
```

This category is analytically irrelevant for newspaper salience because there was neither expectation nor observation.

---

## 6. AERITH / Yoshida as Source Scaffold

Use **Seiichi Yoshida’s AERITH comet catalog** as the first-pass scaffold for comet appearances.

AERITH status markers should be preserved as raw audit fields:

```text
Discovered
Appeared
Not observed
Appeared before discovery
Not observed before discovery
Returns in the future
```

Approximate mapping into the Expected × Seen framework:

| AERITH status | Interpretation |
|---|---|
| Discovered | not expected + seen |
| Appeared | expected + seen |
| Not observed | expected + not seen |
| Appeared before discovery | physically seen/appeared, but not historically known as that comet at the time |
| Not observed before discovery | retrospective non-observation; likely exclude |
| Returns in the future | exclude |

Important rule:

> **“Appeared before discovery” should remain its own filter category. It should not be collapsed into ordinary “Appeared” or “Discovered.”**

Reason:

> It indicates retrospective orbital reconstruction, not necessarily historical expectation or public availability at the time.

---

## 7. Categories Not to Use as Main Analytic Categories

The following distinctions may still be useful as metadata, but should not drive the main analysis:

```text
periodic vs non-periodic
major_public_prediction_event
weeks_mag_le_6 as the central visibility variable
```

### Periodic vs non-periodic

This distinction is astronomically meaningful but analytically messy. A comet can be periodic in orbital terms without being publicly expected, and some periodic-orbit comets were observed only once.

For Chapter 5, the better distinction is historical/event-structural:

```text
expected + seen
vs.
not expected + seen
```

### major_public_prediction_event

This category is too squishy at the catalog-building stage. It risks imposing a newspaper-derived judgment before the newspaper analysis has been done.

Instead, Halley should simply be coded according to the same source variables, then handled through sensitivity analysis.

### weeks_mag_le_6

This is useful as a rough legacy measure, but it is too crude as the central visibility measure because it treats marginal visibility and spectacular visibility too similarly.

---

## 8. Main Inclusion Logic

The comet sample should be curated, not comprehensive.

Main sample:

```text
pre-1940 comet apparitions
AND historically relevant AERITH/status information
AND plausibly public-visible
```

Earlier simple filter:

```text
estimated_peak_mag <= 6
```

But this should now be treated as only a screening proxy, not the final visibility measure.

Avoid the faint-comet swamp:

> Do not include every telescopic, specialist, or barely observed comet simply because it appears in a periodic-comet catalog.

A comet like 41P is a warning case. It is historically interesting, but its pre-1940 apparitions were faint/telescopic and probably not useful for the main public salience comparison.

---

## 9. Visibility: From Magnitude Threshold to Affordance

The earlier visibility idea was:

```text
weeks_mag_le_6 = number of weeks the comet was brighter than apparent magnitude 6
```

That is too crude because apparent magnitude alone does not determine practical visibility.

A comet may be formally bright enough for the naked eye but still difficult to see because of:

- low altitude
- twilight
- small solar elongation
- moonlight
- haze / horizon conditions
- diffuse appearance
- weak surface brightness
- lack of tail or condensation

The revised concept is:

> **naked-eye visibility opportunity as public affordance**

Visibility should measure not merely whether a comet crossed a photometric threshold, but how strongly it invited ordinary perception.

---

## 10. Nightly Visibility Margin

Replace crude `weeks_mag_le_6` with a nightly **visibility margin**:

```text
visibility_margin = local_limiting_mag - effective_comet_mag
```

Where:

```text
effective_comet_mag = apparent_comet_mag + diffuse_comet_penalty
```

Interpretation:

| Visibility margin | Meaning |
|---:|---|
| < 0 | probably not naked-eye visible |
| 0 | threshold visibility |
| > 0 | naked-eye visibility opportunity |
| larger positive value | easier / more conspicuous visibility |

This should not be normalized to a 0–1 score. Magnitude already has a meaningful scale, and the margin itself is interpretable.

---

## 11. Affordance and Spectacle

The visibility framework should distinguish **affordance** from **spectacle**.

### Affordance

Affordance means:

> The sky made the comet available to ordinary perception.

A basic event-level measure:

```text
integrated_visibility_affordance = sum(max(visibility_margin, 0))
```

This captures total accumulated naked-eye visibility opportunity.

### Spectacle

Spectacle means:

> The sky made the comet difficult to ignore.

A spectacle-weighted measure:

```text
spectacle_affordance = sum(max(visibility_margin, 0)^2)
```

This intentionally weights brilliance more heavily than mere duration.

Example:

```text
30 days at margin +0.5 → 30 × 0.25 = 7.5
7 days at margin +2.0  → 7 × 4.00 = 28
```

This captures the intuition that one week of huge brilliance may matter more for salience than two months of barely visible threshold presence.

---

## 12. Event-Level Visibility Measures

For each apparition, derive:

```text
peak_visibility_margin
```

Maximum nightly visibility margin. This captures maximum spectacle potential.

```text
days_margin_gt_0
```

Number of days with positive naked-eye visibility opportunity.

```text
days_margin_gt_1
```

Number of days with more robust naked-eye visibility.

```text
integrated_visibility_affordance = sum(max(margin, 0))
```

Accumulated visibility opportunity.

```text
spectacle_affordance = sum(max(margin, 0)^2)
```

Brightness-weighted visibility opportunity.

Optional communication variable:

```text
duration_bin = short / medium / long
```

But `duration_bin` should be derived from the visibility-margin outputs and treated as a communication aid, not the core measure.

---

## 13. Observation Windows

For each comet apparition, a nightly visibility score requires a reference location or set of locations.

Possible approaches:

1. Use one representative northern U.S. location.
2. Use a small set of major newspaper/public locations, such as New York, Boston, Chicago, and San Francisco.
3. Use a location-weighted approach only if needed later.

For now, the likely best choice is a simple reference-location method, because Chapter 5 prioritizes interpretability over astronomical precision.

For each comet/date/location:

```text
1. Estimate best observing interval for the night.
2. Estimate local limiting magnitude for that interval.
3. Get apparent comet magnitude.
4. Apply diffuse/comet penalty.
5. Compute nightly visibility_margin.
6. Keep maximum nightly visibility_margin.
```

---

## 14. Relationship to Planet Visibility

This visibility framework should be preserved because it may transfer well to planet visibility.

For planets, the framework becomes cleaner because there is no diffuse-comet penalty. The core factors would be:

- apparent magnitude
- altitude
- elongation
- twilight
- moonlight
- observing window

Potential planet variables:

```text
peak_visibility_margin
nights_margin_gt_0
integrated_visibility_affordance
spectacle_affordance
```

This may be especially useful for Mars, Venus, Jupiter, or other planet-visibility cases later in the dissertation.

---

## 15. Newspaper Salience Measures

Newspaper salience should be measured separately from sky visibility.

For each apparition, compute:

```text
peak newspaper rate
```

The maximum newspaper coverage rate during the event window.

```text
salience_duration_above_baseline
```

How long coverage stays elevated above baseline.

```text
integrated_newspaper_lift
```

Total accumulated coverage elevation over the event window.

```text
pre_event_lift
```

Coverage elevation before peak visibility, perihelion, recovery, or discovery.

```text
anticipatory_share
```

Share of total coverage occurring before the observational event point.

```text
post_event_tail
```

Persistence of coverage after peak visibility or discovery.

---

## 16. Salience Morphology

The newspaper signal can be decomposed into several forms:

| Signal | Meaning | Most relevant cases |
|---|---|---|
| Prediction elevation | Coverage rises before strong visibility because the comet is expected | expected + seen; expected + not seen |
| Observation lift | Coverage rises when the comet is visible, recovered, discovered, or reported seen | expected + seen; not expected + seen |
| Discovery spike | Sharp post-discovery burst with little/no anticipatory ramp | not expected + seen |
| Spectacle amplification | Coverage rises disproportionately when visibility margin is high | brilliant comets |
| Persistence / tail | Coverage continues after peak visibility | major events, Halley-type cases |
| Missed-return attention | Coverage generated by expectation despite nonappearance | expected + not seen |
| Integrated salience | Total coverage over the whole event window | all comparable cases |

Compressed formulation:

> Comet salience can be decomposed into anticipatory attention, observational response, spectacle amplification, and persistence.

---

## 17. Conceptual Model

The conceptual model is:

```text
news salience ≈ f(visibility) + g(expectation) + h(visibility, expectation)
```

Meaning:

> Newspaper coverage may depend on how visible the comet was, whether it was expected, and whether visibility mattered differently when the comet was expected.

If translated into a simple regression-like form, the interaction version would be:

```text
salience = β0 + β1V + β2E + β3(V × E)
```

Where:

```text
V = visibility affordance
E = expectation, coded 0 or 1
```

But the multiplication symbol should not be overinterpreted. The interaction means:

> Expected and unexpected comets may have different visibility-to-salience relationships.

In prose:

> The analysis asks whether visibility and expectation each increase salience, and whether expectation changes the way visibility is converted into newspaper attention.

---

## 18. Better Model Family

Because neither salience nor visibility is a single thing, different outcomes should be matched with different visibility measures.

Possible pairings:

```text
peak_rate ~ spectacle_affordance + expectation + spectacle_affordance × expectation
```

```text
integrated_lift ~ integrated_visibility_affordance + expectation + integrated_visibility_affordance × expectation
```

```text
salience_duration ~ days_margin_gt_0 + expectation + days_margin_gt_0 × expectation
```

```text
anticipatory_share ~ expectation + predicted_visibility
```

Important caution:

> Unexpected comets cannot have true anticipatory coverage before discovery, so `anticipatory_share` is structurally tied to expectation and should not be treated exactly like peak rate or integrated lift.

Given the likely small curated sample, this may work better as labeled visual comparison and case analysis than as formal regression.

---

## 19. Expected Patterns to Test

These are hypotheses, not assumptions.

### Expected + seen

Known or anticipated returns may show:

- prediction elevation
- broader anticipatory coverage
- longer salience duration
- higher integrated lift
- possible observation lift near visibility or recovery

### Not expected + seen

Newly discovered apparitions may show:

- little or no anticipatory coverage
- sharp discovery spike
- strong dependence on spectacle
- shorter salience duration unless visibility is exceptional

### Expected + not seen

Missed or lost returns may show:

- prediction elevation
- little or no observation lift
- possible disappointment, uncertainty, or scientific follow-up

### Retrospective pre-discovery appearance

These should generally be separated from the main comparison because they were not historically known as that comet at the time.

---

## 20. Halley

Halley should not be assigned a special catalog category such as `major_public_prediction_event`.

Instead:

```text
expected = true
seen = true
```

Then treat it analytically as:

```text
outlier_candidate = true
```

The plan:

1. Run/visualize the comparison with Halley included.
2. Run/visualize the comparison with Halley excluded.
3. If Halley dominates the expected-return category, discuss it as an extreme case rather than letting it define the entire pattern.

Halley is likely important because it combines:

- expectation
- historical fame
- naked-eye visibility
- long cultural memory
- spectacle
- possible anxiety/fear/public curiosity

But those properties should emerge from the analysis rather than being imposed prematurely.

---

## 21. Biela

Biela is a boundary case.

It belongs conceptually with:

```text
expected + not seen
```

or with a side discussion of:

```text
prediction without ordinary visible appearance
```

Biela is useful because it shows that expectation itself can generate salience, even when visibility fails, is weak, or becomes entangled with loss/recovery narratives.

But Biela should not drive the main comparison unless the relevant apparition was plausibly public-visible.

Possible role:

> Biela as a side case showing prediction and missed expectation, not as a main visible-comet event.

---

## 22. 41P and the Faint-Comet Problem

41P illustrates why the sample cannot simply include all periodic comets discovered before 1940.

It has historically interesting statuses, including discovery, rediscovery, missed predictions, and later recovery. But for the pre-1940 period it appears to have been faint/telescopic rather than a public naked-eye object.

Use 41P as a methodological warning:

> A comet can be historically important to orbital astronomy without being useful for public salience analysis.

This supports the need for a visibility/affordance filter.

---

## 23. Working Dataset Fields

Recommended event-level fields:

```text
comet_id
comet_name
apparition_year
perihelion_date
discovery_date
AERITH_status
expected
seen
event_case
retrospective_pre_discovery_flag
source_basis
include_main_sample
exclusion_reason
```

Visibility fields:

```text
peak_mag
reference_location
nightly_visibility_margin_series
peak_visibility_margin
days_margin_gt_0
days_margin_gt_1
integrated_visibility_affordance
spectacle_affordance
visibility_confidence
visibility_notes
```

Newspaper fields:

```text
query_terms
window_start
window_end
peak_newspaper_rate
integrated_newspaper_lift
salience_duration_above_baseline
pre_event_lift
observation_lift
discovery_spike
post_event_tail
anticipatory_share
```

Flags:

```text
halley_outlier_candidate
biela_boundary_case
faint_or_telescopic_only
retrospective_case
missed_return_case
```

---

## 24. Practical Workflow

### Step 1: Build comet apparition scaffold

Start from Yoshida / AERITH.

Pull relevant apparition records and preserve AERITH status.

### Step 2: Convert to Expected × Seen

Map each apparition to:

```text
expected = true / false
seen = true / false
```

Then derive:

```text
expected_seen
expected_not_seen
unexpected_seen
unexpected_not_seen
```

### Step 3: Apply visibility/public relevance filter

Exclude purely telescopic/faint specialist objects from the main sample.

Preserve exclusions with reasons.

### Step 4: Compute visibility affordance

For each included apparition:

```text
nightly visibility_margin
peak_visibility_margin
days_margin_gt_0
days_margin_gt_1
integrated_visibility_affordance
spectacle_affordance
```

### Step 5: Build newspaper windows

Define event windows around discovery, perihelion, recovery, or predicted visibility depending on event case.

Keep windows standardized enough to avoid baking the result into the design.

### Step 6: Measure salience morphology

Compute:

```text
prediction elevation
observation lift
discovery spike
spectacle amplification
persistence / tail
integrated lift
```

### Step 7: Compare cases

Primary comparison:

```text
expected + seen
vs.
not expected + seen
```

Secondary cases:

```text
expected + not seen
retrospective pre-discovery appearances
Halley included/excluded
```

---

## 25. Chapter Payoff

The comet case should let Chapter 5 move beyond a simple event-response model.

The goal is to show:

> Comet salience depends not merely on astronomical brightness, but on the relationship between expectation and perceptual availability.

Or, more compactly:

> Visibility creates affordance; expectation structures attention; spectacle amplifies response.

This complements the eclipse result:

> Eclipses show public salience filtered by where an event could be seen. Comets show public salience filtered by how, when, and with what degree of expectation an object became visible.

The reusable methodological contribution is the visibility-affordance framework:

```text
visibility_margin = local_limiting_mag - effective_object_mag
```

with event-level summaries:

```text
peak_visibility_margin
integrated_visibility_affordance
spectacle_affordance
days_margin_gt_0
```

This can later be adapted to planets, where the same structure may work even better because planetary visibility is less complicated by diffuse morphology.

-----------------------

Additional user notes.

For viewing locations, use Chicago, NYC, New Orleans, and San Fran as four bounding cities.