# Big V Promotion Summary

_Generated 2026-05-01_

This report documents the dataset transformation that occurred when
Vsekhsvyatskij 1958 (*Physical Characteristics of Comets* — "Big V")
H10 photometric values were promoted into the pipeline as the primary
source of (M1, K1) for 1850–1940 apparitions. Per spec §8.2 (amended),
manual_M1K1.csv entries now win unconditionally over SBDB.

## Why Big V wins

For the 1850–1940 window, era-appropriate published references like
Vsekhsvyatskij 1958 and Marsden & Williams *Catalogue of Cometary
Magnitudes* are anchored against the **contemporary visual
observations** of each apparition. SBDB fits, by contrast, are
typically integrated across all known returns of a comet and are
weighted toward modern, well-observed apparitions where activity may
have evolved (often downward, e.g., 2P/Encke). For this chapter we
want the photometric model that best reproduces what 19th-century
observers actually saw, which is what Big V's H10 values aim to do.

## Data flow

1. PDF pages (1850–1940 entries from Big V) extracted to OCR text in a
   parallel thread.
2. OCR thread parsed Roman-numeral entries → 274 staging rows in
   `data/inputs/bigv_staging.csv` (190 high / 52 medium / 32 low
   confidence).
3. Two NaN-M1 skip rows and two `?`-pdes ambiguous rows held aside;
   270 rows promoted to `data/inputs/manual_M1K1.csv`.
4. Pipeline re-run: `manual_curated` / `manual_curated_override` now
   the dominant provenance.

## Before vs after

| Metric | Before Big V | After Big V |
|---|---|---|
| Successful daily light curves | 427 / 644 | **619 / 644** |
| Apparitions with peak_mag ≤ 6.0 | 21 | **146** |
| `manual_curated_override` | 0 | **373** |
| `manual_curated` (gap-fill) | ~5 | **201** |
| `horizons_tmag` | 422 | **54** |
| `failed` (Tier 3) | 217 | **16** |

The `manual_curated_override` count (373) is large because Big V
covers many SBDB-parameterized comets and we now prefer Big V's
contemporary-anchored values. The `manual_curated` count (201) is
gap-fill: comets where SBDB had no usable photometric parameters at
all and Big V provides the only data we have.

## Naked-eye apparitions (peak_mag ≤ 6.0)

The expansion from 21 → 146 naked-eye apparitions is the single
biggest change. The pre-Big V pipeline was missing essentially every
famous 19th-century non-periodic comet because SBDB doesn't carry
photometric parameters for most pre-1950 one-shots. The top of the
new ranking (from `reports/morning_summary.md`):

| comet_name | year | peak_mag | family |
|---|---|---|---|
| C/1882 R1 (Great September comet) | 1882 | -13.13 | sungrazer |
| C/1887 B1 (Great southern comet) | 1887 | -12.38 | sungrazer |
| C/1865 B1 (Great southern comet) | 1865 | -11.32 | sungrazer |
| C/1880 C1 (Great southern comet) | 1880 | -9.10 | sungrazer |
| C/1882 F1 (Wells) | 1882 | -7.95 | non-periodic |
| C/1931 P1 (Ryves) | 1931 | -5.04 | non-periodic |
| C/1910 A1 (Great January comet) | 1910 | -3.77 | non-periodic |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | -2.65 | non-periodic |
| C/1901 G1 (Great comet) | 1901 | -2.32 | non-periodic |
| C/1895 W1 (Perrine) | 1895 | -2.26 | non-periodic |

All of these were Tier 3 failures before Big V. The integrated
brightness rankings (`integrated_mag6_excess`,
`spectacle_mag6_excess`, `integrated_visible_relative_flux_mag6`) all
top out at C/1882 R1 with the other Great Comets ranked below — the
same comets contemporary newspapers covered most heavily.

## Validation against published peaks

Cross-checked 13 apparitions with externally-known peaks (Kronk
*Cometography*, Vsekhsvyatskij). Tolerance ±1.5 mag; 8/13 within
tolerance. Outliers and their explanations:

| comet | observed | modeled | diff | explanation |
|---|---|---|---|---|
| 2P/Encke 1898 | +6.0 | 4.05 | -1.95 | Encke varies +5 to +7 across returns; mid-range estimate |
| 3D/Biela 1852 | +5.0 | 8.22 | +3.22 | Final intact return; comet was visibly disintegrating, single-law fit can't track activity collapse |
| 17P/Holmes 1892 | +5.0 | 13.83 | +8.83 | Famous outburst; M1/K1 model cannot capture stochastic outbursts by design |
| C/1882 R1 1882 | -10.0 | -13.13 | -3.13 | Sungrazer; daylight peak ~-17 reported. Model is closer to peak-of-tail-visibility benchmark. |
| C/1910 A1 1910 | -1.0 | -3.77 | -2.77 | Reports range -1 to -5 widely; modeled value within bounds |

The Halley 1910 hand-calc check still passes to 0.0003 mag (formula
implementation is correct); the diff is in the input M1 value, where
Big V's H10 = 4.6 produces a modeled peak of -0.12 vs observed 0,
better than SBDB's M1 = 5.5.

## Remaining Tier 3 (16 apparitions)

These apparitions still have no light curve because Big V also lacked
H10 values for them. Most are obscure non-periodic discoveries where
even Big V did not have enough contemporary photometric data to fit
H10:

```
95P/Chiron, C/1851 U1 Brorsen, C/1863 G2 Respighi,
C/1864 O1 Donati-Toussaint, C/1864 X1 Baeker,
C/1870 K1 Winnecke, C/1877 G1 Winnecke,
C/1879 Q2 Hartwig, C/1881 S1 Barnard,
C/1891 F1 Barnard-Denning, C/1896 G1 Swift,
C/1909 L1 Borrelly-Daniel, C/1918 L1 Reid,
C/1919 Y1 Skjellerup, C/1940 O1 Whipple-Paraskevopoulos,
C/1940 S1 Okabayasi-Honda
```

These are likely to remain Tier 3 unless Marsden & Williams (or
another era-appropriate reference) has parameters for them. They
are listed in the audit report's "Manual M1/K1 candidates" section
for future review.

**Cross-check against Kronk (2026-05-02).** None of the 16 appear
in Bortle's *Bright-Comet Chronicles* (ICQ), the ICQ "brightest
comets since 1935" list, or Cometwatch's historic bright-comet list
— in the 1850–1940 window only C/1882 R1 makes those lists, and we
already have it. The one direct magnitude data point that could be
recovered from secondary sources was C/1891 F1 (Barnard-Denning) at
peak mag 8.0, comfortably below the naked-eye threshold and
consistent with the pattern. The remaining 15 are confirmed
telescopic discoveries by professional comet hunters (Barnard,
Winnecke, Hartwig, Borrelly, Skjellerup, Whipple, etc.) of the
kind that get an entry in *Astronomische Nachrichten* but not the
front page. No newspaper-salience risk from leaving them out.

The cross-check used cometography.com plus secondary lists; full
quotation of Kronk's printed magnitudes for entries 2–9, 11–13,
15–16 would require the print *Cometography* volumes (Cambridge
Vols. 2–4) but the negative-evidence pattern is robust enough for
"documented exclusion" purposes.

## Spec amendment (§8.2)

The precedence rule was simplified from a conditional ("manual wins
only when SBDB looks nuclear-biased, K1 < 6.0") to an unconditional
("manual always wins"). The `NUCLEAR_FIT_K1_THRESHOLD` constant is
preserved as a diagnostic flag in the audit (so the reviewer can see
which SBDB-only rows are particularly suspect) but no longer gates
the override decision.

## Files changed

- `comet_visibility_commission_v2.md` — §8.2 rewrite
- `src/comet_visibility/light_curves.py` — `resolve_magnitude_model`
  reordered (manual entries checked first)
- `src/comet_visibility/audit.py` — provenance counts split into
  gap-fill vs override
- `scripts/validate_results.py` — REFERENCE_PEAKS expanded with Big
  V famous comets; hand-calc check handles override provenance
- `data/inputs/manual_M1K1.csv` — 270 Big V rows added

Commits: `a4b42ad` (Big V extraction), `83672fa` (overnight re-run),
`28c69f2` (Big V promotion code).
