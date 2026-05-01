# Morning Summary  (run 2026-05-01 16:56 UTC)

Pipeline elapsed: **741 s**

## Run summary

- Total apparitions in scope: **644**
- Successful daily light curves: **619**
- Apparitions with peak_mag <= 6.0: **146**
- Daily light-curve rows: **223459**

## Magnitude provenance breakdown

- manual_curated_override: 373
- manual_curated: 201
- horizons_tmag: 54
- failed: 16

## event_case breakdown

- unexpected_seen: 280
- expected_not_seen: 211
- expected_seen: 131
- retrospective_not_observed: 16
- retrospective_pre_discovery: 6

## Top 10 apparitions by peak brightness

| comet_name | year | peak_mag | days <= 6 | event_case | provenance |
|---|---|---|---|---|---|
| C/1882 R1 (Great September comet) | 1882 | -13.13 | 185 | unexpected_seen | manual_curated |
| C/1887 B1 (Great southern comet) | 1887 | -12.38 | 62 | unexpected_seen | manual_curated |
| C/1865 B1 (Great southern comet) | 1865 | -11.32 | 77 | unexpected_seen | manual_curated |
| C/1880 C1 (Great southern comet) | 1880 | -9.10 | 50 | unexpected_seen | manual_curated |
| C/1882 F1 (Wells) | 1882 | -7.95 | 90 | unexpected_seen | manual_curated |
| C/1931 P1 (Ryves) | 1931 | -5.04 | 39 | unexpected_seen | manual_curated |
| C/1910 A1 (Great January comet) | 1910 | -3.77 | 53 | unexpected_seen | manual_curated |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | -2.65 | 65 | unexpected_seen | manual_curated |
| C/1901 G1 (Great comet) | 1901 | -2.32 | 86 | unexpected_seen | manual_curated |
| C/1895 W1 (Perrine) | 1895 | -2.26 | 60 | unexpected_seen | manual_curated |

## Top 10 by integrated_mag6_excess

| comet_name | year | integrated_mag6_excess | peak_mag | event_case |
|---|---|---|---|---|
| C/1882 R1 (Great September comet) | 1882 | 654 | -13.13 | unexpected_seen |
| C/1913 Y1 (Delavan) | 1914 | 398 | 2.61 | unexpected_seen |
| C/1858 L1 (Donati) | 1858 | 352 | -0.19 | unexpected_seen |
| C/1881 K1 (Great comet) | 1881 | 344 | 0.03 | unexpected_seen |
| C/1861 J1 (Great comet) | 1861 | 338 | -0.99 | unexpected_seen |
| C/1882 F1 (Wells) | 1882 | 323 | -7.95 | unexpected_seen |
| C/1915 C1 (Mellish) | 1915 | 301 | 2.45 | unexpected_seen |
| C/1901 G1 (Great comet) | 1901 | 300 | -2.32 | unexpected_seen |
| C/1907 L2 (Daniel) | 1907 | 291 | 1.38 | unexpected_seen |
| C/1865 B1 (Great southern comet) | 1865 | 277 | -11.32 | unexpected_seen |

## Top 10 by spectacle_mag6_excess

| comet_name | year | spectacle_mag6_excess | peak_mag | event_case |
|---|---|---|---|---|
| C/1882 R1 (Great September comet) | 1882 | 4.33e+03 | -13.13 | unexpected_seen |
| C/1882 F1 (Wells) | 1882 | 2e+03 | -7.95 | unexpected_seen |
| C/1865 B1 (Great southern comet) | 1865 | 1.87e+03 | -11.32 | unexpected_seen |
| C/1901 G1 (Great comet) | 1901 | 1.61e+03 | -2.32 | unexpected_seen |
| C/1858 L1 (Donati) | 1858 | 1.52e+03 | -0.19 | unexpected_seen |
| C/1861 J1 (Great comet) | 1861 | 1.42e+03 | -0.99 | unexpected_seen |
| C/1881 K1 (Great comet) | 1881 | 1.39e+03 | 0.03 | unexpected_seen |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | 1.21e+03 | -2.65 | unexpected_seen |
| C/1887 B1 (Great southern comet) | 1887 | 1.19e+03 | -12.38 | unexpected_seen |
| C/1895 W1 (Perrine) | 1895 | 1.12e+03 | -2.26 | unexpected_seen |

## Top 10 by integrated_visible_relative_flux_mag6

| comet_name | year | integrated_visible_relative_flux_mag6 | peak_mag | event_case |
|---|---|---|---|---|
| C/1882 R1 (Great September comet) | 1882 | 4.87e+07 | -13.13 | unexpected_seen |
| C/1887 B1 (Great southern comet) | 1887 | 2.25e+07 | -12.38 | unexpected_seen |
| C/1865 B1 (Great southern comet) | 1865 | 8.76e+06 | -11.32 | unexpected_seen |
| C/1880 C1 (Great southern comet) | 1880 | 1.11e+06 | -9.10 | unexpected_seen |
| C/1882 F1 (Wells) | 1882 | 5.89e+05 | -7.95 | unexpected_seen |
| C/1931 P1 (Ryves) | 1931 | 5.12e+04 | -5.04 | unexpected_seen |
| C/1910 A1 (Great January comet) | 1910 | 3.41e+04 | -3.77 | unexpected_seen |
| C/1901 G1 (Great comet) | 1901 | 2.27e+04 | -2.32 | unexpected_seen |
| C/1927 X1 (Skjellerup-Maristany) | 1927 | 1.98e+04 | -2.65 | unexpected_seen |
| C/1895 W1 (Perrine) | 1895 | 1.51e+04 | -2.26 | unexpected_seen |

## Validation findings

_No validation issues._

## What's next

- Review the audit report at `reports/comet_visibility_audit.md`.
- Inspect the diagnostic plots in `figures/comet_visibility_diagnostics/`.
- The audit's **Manual M1/K1 candidates** section lists the Tier 3
  non-periodic apparitions awaiting M1/K1 entry. Add rows to
  `data/inputs/manual_M1K1.csv` and re-run; cached Horizons responses
  make incremental reruns cheap.