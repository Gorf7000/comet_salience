# Morning Summary  (run 2026-04-30 23:24 UTC)

Pipeline elapsed: **1837 s**

## Run summary

- Total apparitions in scope: **644**
- Successful daily light curves: **427**
- Apparitions with peak_mag <= 6.0: **21**
- Daily light-curve rows: **154147**

## Magnitude provenance breakdown

- horizons_tmag: 427
- failed: 217

## event_case breakdown

- unexpected_seen: 280
- expected_not_seen: 211
- expected_seen: 131
- retrospective_not_observed: 16
- retrospective_pre_discovery: 6

## Top 10 apparitions by peak brightness

| comet_name | year | peak_mag | days <= 6 | event_case | provenance |
|---|---|---|---|---|---|
| C/1917 F1 (Mellish) | 1917 | -1.00 | 25 | unexpected_seen | horizons_tmag |
| 1P/Halley | 1910 | 1.00 | 79 | expected_seen | horizons_tmag |
| 109P/Swift-Tuttle | 1862 | 1.97 | 75 | unexpected_seen | horizons_tmag |
| 12P/Pons-Brooks | 1884 | 2.60 | 89 | expected_seen | horizons_tmag |
| 3D/Biela | 1886 | 3.56 | 100 | expected_not_seen | horizons_tmag |
| 3D/Biela | 1866 | 3.71 | 99 | expected_not_seen | horizons_tmag |
| C/1939 H1 (Jurlof-Achmarof-Hassel) | 1939 | 3.97 | 47 | unexpected_seen | horizons_tmag |
| 5D/Brorsen | 1901 | 4.00 | 48 | expected_not_seen | horizons_tmag |
| 5D/Brorsen | 1912 | 4.00 | 49 | expected_not_seen | horizons_tmag |
| 5D/Brorsen | 1928 | 4.00 | 49 | expected_not_seen | horizons_tmag |

## Top 10 by integrated_mag6_excess

| comet_name | year | integrated_mag6_excess | peak_mag | event_case |
|---|---|---|---|---|
| 12P/Pons-Brooks | 1884 | 182 | 2.60 | expected_seen |
| 1P/Halley | 1910 | 172 | 1.00 | expected_seen |
| 109P/Swift-Tuttle | 1862 | 157 | 1.97 | unexpected_seen |
| 3D/Biela | 1886 | 149 | 3.56 | expected_not_seen |
| 3D/Biela | 1866 | 138 | 3.71 | expected_not_seen |
| 3D/Biela | 1938 | 98.6 | 4.14 | expected_not_seen |
| C/1917 F1 (Mellish) | 1917 | 88.8 | -1.00 | unexpected_seen |
| 3D/Biela | 1905 | 87.6 | 4.21 | expected_not_seen |
| 23P/Brorsen-Metcalf | 1919 | 70 | 4.30 | expected_seen |
| 5D/Brorsen | 1928 | 61.7 | 4.00 | expected_not_seen |

## Top 10 by spectacle_mag6_excess

| comet_name | year | spectacle_mag6_excess | peak_mag | event_case |
|---|---|---|---|---|
| 1P/Halley | 1910 | 531 | 1.00 | expected_seen |
| 12P/Pons-Brooks | 1884 | 475 | 2.60 | expected_seen |
| 109P/Swift-Tuttle | 1862 | 446 | 1.97 | unexpected_seen |
| C/1917 F1 (Mellish) | 1917 | 438 | -1.00 | unexpected_seen |
| 3D/Biela | 1886 | 280 | 3.56 | expected_not_seen |
| 3D/Biela | 1866 | 244 | 3.71 | expected_not_seen |
| 3D/Biela | 1938 | 143 | 4.14 | expected_not_seen |
| 3D/Biela | 1905 | 121 | 4.21 | expected_not_seen |
| 5D/Brorsen | 1928 | 101 | 4.00 | expected_not_seen |
| 5D/Brorsen | 1912 | 94.6 | 4.00 | expected_not_seen |

## Top 10 by integrated_visible_relative_flux_mag6

| comet_name | year | integrated_visible_relative_flux_mag6 | peak_mag | event_case |
|---|---|---|---|---|
| C/1917 F1 (Mellish) | 1917 | 3.27e+03 | -1.00 | unexpected_seen |
| 1P/Halley | 1910 | 1.42e+03 | 1.00 | expected_seen |
| 109P/Swift-Tuttle | 1862 | 931 | 1.97 | unexpected_seen |
| 12P/Pons-Brooks | 1884 | 879 | 2.60 | expected_seen |
| 3D/Biela | 1886 | 489 | 3.56 | expected_not_seen |
| 3D/Biela | 1866 | 435 | 3.71 | expected_not_seen |
| 3D/Biela | 1938 | 280 | 4.14 | expected_not_seen |
| 3D/Biela | 1905 | 247 | 4.21 | expected_not_seen |
| 5D/Brorsen | 1928 | 189 | 4.00 | expected_not_seen |
| 23P/Brorsen-Metcalf | 1919 | 188 | 4.30 | expected_seen |

## Validation findings

_No validation issues._

## What's next

- Review the audit report at `reports/comet_visibility_audit.md`.
- Inspect the diagnostic plots in `figures/comet_visibility_diagnostics/`.
- The audit's **Manual M1/K1 candidates** section lists the Tier 3
  non-periodic apparitions awaiting M1/K1 entry. Add rows to
  `data/inputs/manual_M1K1.csv` and re-run; cached Horizons responses
  make incremental reruns cheap.