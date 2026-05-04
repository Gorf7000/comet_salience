# Geographic visibility — sensitivity to limiting magnitude
_Generated 2026-05-04 17:25 UTC per spec §5._

Phase 1 of geographic visibility uses a constant limiting magnitude. The headline output uses **4.5** (urban-naked-eye threshold). This report compares the per-apparition rollup at three values {4.0, 4.5, 5.0}, computed from a single geometry pass that stores per-sample margins for all three.

## 1. "Ever visible" apparition counts

How many apparitions have at least one date with `margin > 0` from any band, at each limit:

| limit | n apparitions ever visible |
|---|---|
| 4.0 | 35 |
| 4.5 | 45 |
| 5.0 | 55 |

## 2. Top-30 stability (rank by `integrated_best_margin`)

- Spearman ρ(lim 4.5, lim 4.0) = **0.8889**
- Spearman ρ(lim 4.5, lim 5.0) = **0.9116**
- Top-30 overlap (lim 4.5 ↔ lim 4.0): **29 / 30**
- Top-30 overlap (lim 4.5 ↔ lim 5.0): **29 / 30**

**Verdict:** ranking of the top spectacular apparitions is stable across the limit range. The choice of 4.5 vs 4.0/5.0 changes the depth of integrated visibility but not which comets dominate.

## 3. Per-apparition `peak_best_margin` shift

`peak_best_margin` is `limit − apparent_mag − extinction_at_peak_alt` for the best (date, band) — so a +0.5 mag change in `limit` lifts peak by exactly +0.5 mag wherever the dark-window-minimum and altitude rules still admit the same row. Differences in the dataset arise only when a different (date, band) wins at a different limit.

- Δ(peak_best_margin: lim 4.5 − lim 4.0): median 0.500, mean 0.500, max abs 0.500
- Δ(peak_best_margin: lim 5.0 − lim 4.5): median 0.500, mean 0.502, max abs 0.578

Almost-exactly +0.5 medians confirm the additive shift; outliers come from apparitions that gained/lost a peak (date, band) when the limit moved.

## 4. Top-30 list at the headline limit (4.5)

| rank | apparition | comet | peak_mag | int. margin (4.0) | int. margin (4.5) | int. margin (5.0) | days visible (4.5) |
|---|---|---|---|---|---|---|---|
| 1 | C_1858L1_1858 | C/1858 L1 (Donati) | -0.19 | 108.1 | 134.1 | 163.8 | 51 |
| 2 | C_1882R1_1882 | C/1882 R1 (Great September comet) | -13.13 | 86.0 | 119.1 | 157.5 | 65 |
| 3 | 7P_1927 | 7P/Pons-Winnecke | -0.04 | 84.2 | 108.6 | 137.7 | 52 |
| 4 | C_1911O1_1911 | C/1911 O1 (Brooks) | +1.51 | 65.3 | 97.8 | 135.5 | 68 |
| 5 | C_1907L2_1907 | C/1907 L2 (Daniel) | +1.38 | 66.4 | 95.2 | 128.0 | 57 |
| 6 | 109P_1862 | 109P/Swift-Tuttle | +1.54 | 56.7 | 79.7 | 106.9 | 49 |
| 7 | 1P_1910 | 1P/Halley | -0.12 | 53.0 | 74.4 | 96.7 | 41 |
| 8 | C_1913Y1_1914 | C/1913 Y1 (Delavan) | +2.61 | 36.4 | 73.4 | 128.3 | 78 |
| 9 | C_1861J1_1861 | C/1861 J1 (Great comet) | -0.99 | 54.8 | 69.1 | 85.7 | 31 |
| 10 | C_1881K1_1881 | C/1881 K1 (Great comet) | +0.03 | 51.6 | 68.5 | 88.2 | 36 |
| 11 | 7P_1921 | 7P/Pons-Winnecke | +2.72 | 33.5 | 58.4 | 89.9 | 56 |
| 12 | C_1881N1_1881 | C/1881 N1 (Schaeberle) | +1.84 | 34.4 | 52.7 | 73.9 | 38 |
| 13 | 7P_1939 | 7P/Pons-Winnecke | +2.40 | 29.9 | 48.2 | 70.6 | 41 |
| 14 | C_1882F1_1882 | C/1882 F1 (Wells) | -7.95 | 31.5 | 44.2 | 67.6 | 28 |
| 15 | C_1861G1_1861 | C/1861 G1 (Thatcher) | +2.72 | 24.9 | 42.4 | 62.8 | 37 |
| 16 | 7P_1892 | 7P/Pons-Winnecke | +1.78 | 16.8 | 39.3 | 68.1 | 48 |
| 17 | 12P_1884 | 12P/Pons-Brooks | +3.01 | 17.6 | 37.4 | 62.0 | 43 |
| 18 | C_1857Q1_1857 | C/1857 Q1 (Klinkerfues) | +2.97 | 13.2 | 31.4 | 52.6 | 38 |
| 19 | C_1892E1_1892 | C/1892 E1 (Swift) | +3.45 | 6.8 | 30.6 | 64.8 | 57 |
| 20 | C_1864N1_1864 | C/1864 N1 (Tempel) | +0.60 | 19.9 | 29.5 | 41.4 | 21 |
| 21 | C_1860M1_1860 | C/1860 M1 (Great comet) | +0.15 | 17.0 | 27.7 | 39.1 | 20 |
| 22 | C_1911S3_1911 | C/1911 S3 (Beljawsky) | -0.21 | 19.0 | 26.9 | 36.1 | 15 |
| 23 | C_1903M1_1903 | C/1903 M1 (Borrelly) | +1.84 | 3.4 | 23.4 | 45.2 | 40 |
| 24 | 7P_1869 | 7P/Pons-Winnecke | +2.60 | 4.2 | 21.8 | 47.9 | 39 |
| 25 | C_1874H1_1874 | C/1874 H1 (Coggia) | +1.63 | 10.8 | 20.7 | 33.1 | 22 |
| 26 | C_1853G1_1853 | C/1853 G1 (Schweizer) | +0.31 | 13.8 | 20.0 | 31.4 | 13 |
| 27 | C_1895W1_1895 | C/1895 W1 (Perrine) | -2.26 | 11.4 | 17.1 | 23.9 | 12 |
| 28 | C_1899E1_1899 | C/1899 E1 (Swift) | +1.06 | 3.2 | 15.6 | 34.2 | 30 |
| 29 | C_1886T1_1886 | C/1886 T1 (Barnard-Hartwig) | +3.17 | 3.6 | 14.8 | 34.0 | 25 |
| 30 | C_1885X1_1886 | C/1885 X1 (Fabry) | +2.03 | 5.1 | 14.2 | 25.8 | 20 |
