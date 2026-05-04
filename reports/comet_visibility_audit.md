# Comet Visibility Audit Report
_Generated 2026-05-04 17:27 UTC_

## Summary counts

- Raw apparition records collected: 644
- Records in 1850–1940 scope: 644
- Records by raw_status_source: AERITH=413, SBDB=231

- Successfully matched to ephemeris source: 635
- Failed Horizons/JPL match: 9
- Missing perihelion date: 0
- No usable light-curve window: 0
- Successful daily light curves: 619
- peak_mag <= 6.0: 146
- main_sample_candidate = true: 146

## Counts by event_case

- unexpected_seen: 280
- expected_not_seen: 211
- expected_seen: 131
- retrospective_not_observed: 16
- retrospective_pre_discovery: 6

## Magnitude model provenance (per apparition)

- manual_curated_override: 373
- manual_curated: 201
- horizons_tmag: 54
- failed: 16

## Magnitude quality (per apparition)

- medium: 574
- high: 36
- low: 18
- failed: 16

## Adaptive window statistics

- Apparitions with extended window: 0
- Apparitions hitting MAX_WINDOW cap: 0

## SBDB nuclear (M2/K2) parameters present but unused

- Apparitions with M2 stored in SBDB but unused per §8.2: 126
- Apparitions with K2 stored in SBDB but unused: 126

## Manual / SBDB conflicts

- Manual gap-fill entries (provenance = `manual_curated`, SBDB had nothing): 201
- Manual override entries (provenance = `manual_curated_override`, SBDB had values but manual is preferred per spec §8.2): 373

## Nuclear-biased SBDB fits (K1 below threshold)

SBDB sometimes stores (M1, K1) values that look like nuclear/asteroidal
photometry rather than total cometary magnitude — typically a low K1 value
(< 6.0, where active comae have K1 ~ 8-15).
Apparitions in this state will systematically underestimate peak brightness
by 5-10 magnitudes near perihelion. Add a row to `data/inputs/manual_M1K1.csv`
to override with values from a published reference; the override engages
automatically (provenance = `manual_curated_override`).

Total apparitions affected: **146** (across 21 unique comets if any)

| comet_id | year | sbdb_M1 | sbdb_K1 | provenance | peak_mag | event_case |
|---|---|---|---|---|---|---|
| 10P | 1873 | 14.70 | 4.50 | manual_curated_override | 9.57 | unexpected_seen |
| 10P | 1878 | 14.70 | 4.50 | manual_curated_override | 9.90 | expected_seen |
| 10P | 1883 | 14.70 | 4.50 | manual_curated_override | 11.82 | expected_not_seen |
| 10P | 1889 | 14.70 | 4.50 | manual_curated_override | 12.22 | expected_not_seen |
| 10P | 1894 | 14.70 | 4.50 | manual_curated_override | 11.57 | expected_seen |
| 10P | 1899 | 14.70 | 4.50 | manual_curated_override | 8.39 | expected_seen |
| 10P | 1904 | 14.70 | 4.50 | manual_curated_override | 11.85 | expected_seen |
| 10P | 1910 | 14.70 | 4.50 | manual_curated_override | 12.11 | expected_not_seen |
| 10P | 1915 | 14.70 | 4.50 | manual_curated_override | 11.61 | expected_seen |
| 10P | 1920 | 14.70 | 4.50 | manual_curated_override | 10.21 | expected_seen |
| 10P | 1925 | 14.70 | 4.50 | manual_curated_override | 7.83 | expected_seen |
| 10P | 1930 | 14.70 | 4.50 | manual_curated_override | 10.78 | expected_seen |
| 10P | 1935 | 14.70 | 4.50 | manual_curated_override | 11.91 | expected_not_seen |
| 14P | 1884 | 15.60 | 4.50 | manual_curated_override | 9.63 | unexpected_seen |
| 14P | 1891 | 15.60 | 4.50 | manual_curated_override | 9.72 | expected_seen |
| 14P | 1898 | 15.60 | 4.50 | manual_curated_override | 11.44 | expected_seen |
| 14P | 1905 | 15.60 | 4.50 | manual_curated_override | 12.06 | expected_not_seen |
| 14P | 1912 | 15.60 | 4.50 | manual_curated_override | 11.86 | expected_seen |
| 14P | 1918 | 15.60 | 4.50 | manual_curated_override | 10.44 | expected_seen |
| 14P | 1925 | 15.60 | 4.50 | manual_curated_override | 12.80 | expected_seen |
| 14P | 1934 | 15.60 | 4.50 | manual_curated_override | 13.84 | expected_seen |
| 26P | 1853 | 16.50 | 5.50 | manual_curated_override | 12.33 | retrospective_not_observed |
| 26P | 1858 | 16.50 | 5.50 | manual_curated_override | 12.29 | retrospective_not_observed |
| 26P | 1863 | 16.50 | 5.50 | manual_curated_override | 12.25 | retrospective_not_observed |
| 26P | 1868 | 16.50 | 5.50 | manual_curated_override | 12.22 | retrospective_not_observed |
| 26P | 1873 | 16.50 | 5.50 | manual_curated_override | 12.07 | retrospective_not_observed |
| 26P | 1878 | 16.50 | 5.50 | manual_curated_override | 11.52 | retrospective_not_observed |
| 26P | 1883 | 16.50 | 5.50 | manual_curated_override | 10.75 | retrospective_not_observed |
| 26P | 1888 | 16.50 | 5.50 | manual_curated_override | 12.05 | retrospective_not_observed |
| 26P | 1892 | 16.50 | 5.50 | manual_curated_override | 12.53 | retrospective_not_observed |
| 26P | 1897 | 16.50 | 5.50 | manual_curated_override | 12.49 | retrospective_not_observed |
| 26P | 1902 | 16.50 | 5.50 | manual_curated_override | 11.17 | retrospective_pre_discovery |
| 26P | 1907 | 16.50 | 5.50 | manual_curated_override | 10.89 | retrospective_not_observed |
| 26P | 1912 | 16.50 | 5.50 | manual_curated_override | 10.72 | retrospective_not_observed |
| 26P | 1917 | 16.50 | 5.50 | manual_curated_override | 10.22 | retrospective_not_observed |
| 26P | 1922 | 16.50 | 5.50 | manual_curated_override | 9.47 | unexpected_seen |
| 26P | 1927 | 16.50 | 5.50 | manual_curated_override | 8.82 | expected_seen |
| 26P | 1932 | 16.50 | 5.50 | manual_curated_override | 9.30 | expected_seen |
| 26P | 1937 | 16.50 | 5.50 | manual_curated_override | 10.31 | expected_seen |
| 289P | 1850 | 22.00 | 4.50 | horizons_tmag | 18.81 | expected_not_seen |
| 289P | 1856 | 22.00 | 4.50 | horizons_tmag | 22.86 | expected_not_seen |
| 289P | 1861 | 22.00 | 4.50 | horizons_tmag | 23.22 | expected_not_seen |
| 289P | 1866 | 22.00 | 4.50 | horizons_tmag | 16.00 | expected_not_seen |
| 289P | 1872 | 22.00 | 4.50 | horizons_tmag | 22.47 | expected_not_seen |
| 289P | 1877 | 22.00 | 4.50 | horizons_tmag | 23.27 | expected_not_seen |
| 289P | 1882 | 22.00 | 4.50 | horizons_tmag | 22.82 | expected_not_seen |
| 289P | 1887 | 22.00 | 4.50 | horizons_tmag | 19.98 | expected_not_seen |
| 289P | 1893 | 22.00 | 4.50 | horizons_tmag | 21.34 | expected_not_seen |
| 289P | 1898 | 22.00 | 4.50 | horizons_tmag | 23.16 | expected_not_seen |
| 289P | 1903 | 22.00 | 4.50 | horizons_tmag | 22.29 | expected_not_seen |
| 289P | 1909 | 22.00 | 4.50 | horizons_tmag | 23.22 | expected_not_seen |
| 289P | 1914 | 22.00 | 4.50 | horizons_tmag | 22.55 | expected_not_seen |
| 289P | 1919 | 22.00 | 4.50 | horizons_tmag | 15.00 | expected_not_seen |
| 289P | 1925 | 22.00 | 4.50 | horizons_tmag | 22.51 | expected_not_seen |
| 289P | 1930 | 22.00 | 4.50 | horizons_tmag | 23.29 | expected_not_seen |
| 289P | 1935 | 22.00 | 4.50 | horizons_tmag | 22.80 | expected_not_seen |
| 289P | 1940 | 22.00 | 4.50 | horizons_tmag | 19.25 | expected_not_seen |
| 28P | 1913 | 13.20 | 4.50 | manual_curated_override | 10.87 | unexpected_seen |
| 28P | 1931 | 13.20 | 4.50 | manual_curated_override | 13.81 | expected_seen |
| 29P | 1908 | 10.10 | 4.50 | manual_curated_override | 15.66 | retrospective_pre_discovery |
| 29P | 1925 | 10.10 | 4.50 | manual_curated_override | 15.64 | unexpected_seen |
| 2P | 1852 | 15.60 | 4.50 | manual_curated_override | 3.12 | expected_seen |
| 2P | 1855 | 15.60 | 4.50 | manual_curated_override | 4.39 | expected_seen |
| 2P | 1858 | 15.60 | 4.50 | manual_curated_override | 4.49 | expected_seen |
| 2P | 1862 | 15.60 | 4.50 | manual_curated_override | 3.13 | expected_seen |
| 2P | 1865 | 15.60 | 4.50 | manual_curated_override | 4.08 | expected_seen |
| 2P | 1868 | 15.60 | 4.50 | manual_curated_override | 4.55 | expected_seen |
| 2P | 1871 | 15.60 | 4.50 | manual_curated_override | 3.49 | expected_seen |
| 2P | 1875 | 15.60 | 4.50 | manual_curated_override | 3.34 | expected_seen |
| 2P | 1878 | 15.60 | 4.50 | manual_curated_override | 4.50 | expected_seen |
| 2P | 1881 | 15.60 | 4.50 | manual_curated_override | 4.26 | expected_seen |
| 2P | 1885 | 15.60 | 4.50 | manual_curated_override | 3.13 | expected_seen |
| 2P | 1888 | 15.60 | 4.50 | manual_curated_override | 4.45 | expected_seen |
| 2P | 1891 | 15.60 | 4.50 | manual_curated_override | 4.50 | expected_seen |
| 2P | 1895 | 15.60 | 4.50 | manual_curated_override | 3.15 | expected_seen |
| 2P | 1898 | 15.60 | 4.50 | manual_curated_override | 4.05 | expected_seen |
| 2P | 1901 | 15.60 | 4.50 | manual_curated_override | 4.67 | expected_seen |
| 2P | 1905 | 15.60 | 4.50 | manual_curated_override | 3.37 | expected_seen |
| 2P | 1908 | 15.60 | 4.50 | manual_curated_override | 3.63 | expected_seen |
| 2P | 1911 | 15.60 | 4.50 | manual_curated_override | 4.63 | expected_seen |
| 2P | 1914 | 15.60 | 4.50 | manual_curated_override | 3.95 | expected_seen |
| 2P | 1918 | 15.60 | 4.50 | manual_curated_override | 3.20 | expected_seen |
| 2P | 1921 | 15.60 | 4.50 | manual_curated_override | 4.51 | expected_seen |
| 2P | 1924 | 15.60 | 4.50 | manual_curated_override | 4.40 | expected_seen |
| 2P | 1928 | 15.60 | 4.50 | manual_curated_override | 3.02 | expected_seen |
| 2P | 1931 | 15.60 | 4.50 | manual_curated_override | 4.00 | expected_seen |
| 2P | 1934 | 15.60 | 4.50 | manual_curated_override | 4.53 | expected_seen |
| 2P | 1937 | 15.60 | 4.50 | manual_curated_override | 3.54 | expected_seen |
| 33P | 1909 | 15.50 | 4.50 | manual_curated_override | 9.03 | unexpected_seen |
| 33P | 1916 | 15.50 | 4.50 | manual_curated_override | 12.92 | expected_not_seen |
| 33P | 1923 | 15.50 | 4.50 | manual_curated_override | 13.40 | expected_not_seen |
| 33P | 1930 | 15.50 | 4.50 | manual_curated_override | 13.05 | expected_not_seen |
| 33P | 1937 | 15.50 | 4.50 | manual_curated_override | 11.45 | expected_seen |
| 41P | 1858 | 16.90 | 4.50 | manual_curated_override | 10.17 | unexpected_seen |
| 41P | 1863 | 16.90 | 4.50 | manual_curated_override | 13.39 | expected_not_seen |
| 41P | 1869 | 16.90 | 4.50 | manual_curated_override | 12.79 | expected_not_seen |
| 41P | 1874 | 16.90 | 4.50 | manual_curated_override | 10.80 | expected_not_seen |
| 41P | 1879 | 16.90 | 4.50 | manual_curated_override | 13.47 | expected_not_seen |
| 41P | 1885 | 16.90 | 4.50 | manual_curated_override | 12.45 | expected_not_seen |
| 41P | 1890 | 16.90 | 4.50 | manual_curated_override | 12.23 | expected_not_seen |
| 41P | 1896 | 16.90 | 4.50 | manual_curated_override | 12.47 | expected_not_seen |
| 41P | 1901 | 16.90 | 4.50 | manual_curated_override | 13.86 | expected_not_seen |
| 41P | 1907 | 16.90 | 4.50 | manual_curated_override | 11.61 | expected_seen |
| 41P | 1912 | 16.90 | 4.50 | manual_curated_override | 13.15 | expected_not_seen |
| 41P | 1918 | 16.90 | 4.50 | manual_curated_override | 12.67 | expected_not_seen |
| 41P | 1924 | 16.90 | 4.50 | manual_curated_override | 12.78 | expected_not_seen |
| 41P | 1929 | 16.90 | 4.50 | manual_curated_override | 12.32 | expected_not_seen |
| 41P | 1934 | 16.90 | 4.50 | manual_curated_override | 13.05 | expected_not_seen |
| 41P | 1940 | 16.90 | 4.50 | manual_curated_override | 11.52 | expected_not_seen |
| 42P | 1929 | 16.60 | 4.50 | manual_curated_override | 14.06 | unexpected_seen |
| 42P | 1940 | 16.60 | 4.50 | manual_curated_override | 14.69 | expected_not_seen |
| 69P | 1916 | 17.30 | 4.50 | manual_curated_override | 9.85 | unexpected_seen |
| 69P | 1922 | 17.30 | 4.50 | manual_curated_override | 12.72 | expected_not_seen |
| 69P | 1928 | 17.30 | 4.50 | manual_curated_override | 12.28 | expected_not_seen |
| 69P | 1935 | 17.30 | 4.50 | manual_curated_override | 12.88 | expected_not_seen |
| 7P | 1852 | 16.00 | 4.50 | manual_curated_override | 6.32 | retrospective_not_observed |
| 7P | 1858 | 16.00 | 4.50 | manual_curated_override | 5.00 | unexpected_seen |
| 7P | 1863 | 16.00 | 4.50 | manual_curated_override | 6.86 | expected_not_seen |
| 7P | 1869 | 16.00 | 4.50 | manual_curated_override | 2.60 | expected_seen |
| 7P | 1875 | 16.00 | 4.50 | manual_curated_override | 6.77 | expected_seen |
| 7P | 1880 | 16.00 | 4.50 | manual_curated_override | 7.24 | expected_not_seen |
| 7P | 1886 | 16.00 | 4.50 | manual_curated_override | 6.26 | expected_seen |
| 7P | 1892 | 16.00 | 4.50 | manual_curated_override | 1.78 | expected_seen |
| 7P | 1898 | 16.00 | 4.50 | manual_curated_override | 7.18 | expected_seen |
| 7P | 1904 | 16.00 | 4.50 | manual_curated_override | 7.80 | expected_not_seen |
| 7P | 1909 | 16.00 | 4.50 | manual_curated_override | 7.63 | expected_seen |
| 7P | 1915 | 16.00 | 4.50 | manual_curated_override | 6.83 | expected_seen |
| 7P | 1921 | 16.00 | 4.50 | manual_curated_override | 2.72 | expected_seen |
| 7P | 1927 | 16.00 | 4.50 | manual_curated_override | -0.04 | expected_seen |
| 7P | 1933 | 16.00 | 4.50 | manual_curated_override | 5.89 | expected_seen |
| 7P | 1939 | 16.00 | 4.50 | manual_curated_override | 2.40 | expected_seen |
| 8P | 1858 | 14.60 | 4.50 | manual_curated_override | 7.56 | unexpected_seen |
| 8P | 1871 | 14.60 | 4.50 | manual_curated_override | 7.14 | expected_seen |
| 8P | 1885 | 14.60 | 4.50 | manual_curated_override | 9.07 | expected_seen |
| 8P | 1899 | 14.60 | 4.50 | manual_curated_override | 9.03 | expected_seen |
| 8P | 1912 | 14.60 | 4.50 | manual_curated_override | 8.31 | expected_seen |
| 8P | 1926 | 14.60 | 4.50 | manual_curated_override | 9.05 | expected_seen |
| 8P | 1939 | 14.60 | 4.50 | manual_curated_override | 7.95 | expected_seen |
| C/1898 R1 | 1898 | 7.50 | 4.50 | manual_curated_override | 3.98 | unexpected_seen |
| C/1913 Y1 | 1914 | 4.80 | 4.25 | manual_curated_override | 2.61 | unexpected_seen |
| C/1914 F1 | 1914 | 11.10 | 4.50 | manual_curated_override | 8.71 | unexpected_seen |
| C/1915 C1 | 1915 | 7.70 | 4.50 | manual_curated_override | 2.45 | unexpected_seen |
| C/1931 O1 | 1931 | 5.70 | 4.75 | manual_curated_override | 4.88 | unexpected_seen |
| C/1932 M1 | 1932 | 11.10 | 4.50 | manual_curated_override | 12.76 | unexpected_seen |
| C/1932 M2 | 1932 | 6.10 | 4.50 | manual_curated_override | 8.88 | unexpected_seen |
| C/1939 H1 | 1939 | 6.00 | 4.50 | manual_curated_override | 3.59 | unexpected_seen |

## Manual M1/K1 candidates (Tier 3 non-periodics)

These non-periodic apparitions in scope have no SBDB photometric parameters
and produced no light curve. They are candidates for manual entry into
`data/raw/comet_sources/manual_M1K1.csv`. Sorted by perihelion year then
alphabetical by designation. Adding rows here and re-running the pipeline
will generate light curves for those apparitions.

Total Tier 3 non-periodic candidates: **15**

| pdes | comet_name | perihelion_date |
|---|---|---|
| 1851 U1 | C/1851 U1 (Brorsen) | 1851-10-01 |
| 1863 G2 | C/1863 G2 (Respighi) | 1863-04-21 |
| 1864 O1 | C/1864 O1 (Donati-Toussaint) | 1864-10-11 |
| 1864 X1 | C/1864 X1 (Baeker) | 1864-12-22 |
| 1870 K1 | C/1870 K1 (Winnecke) | 1870-07-14 |
| 1877 G1 | C/1877 G1 (Winnecke) | 1877-04-18 |
| 1879 Q2 | C/1879 Q2 (Hartwig) | 1879-08-29 |
| 1881 S1 | C/1881 S1 (Barnard) | 1881-09-14 |
| 1891 F1 | C/1891 F1 (Barnard-Denning) | 1891-04-28 |
| 1896 G1 | C/1896 G1 (Swift) | 1896-04-18 |
| 1909 L1 | C/1909 L1 (Borrelly-Daniel) | 1909-06-05 |
| 1918 L1 | C/1918 L1 (Reid) | 1918-06-06 |
| 1919 Y1 | C/1919 Y1 (Skjellerup) | 1920-01-03 |
| 1940 O1 | C/1940 O1 (Whipple-Paraskevopoulos) | 1940-10-08 |
| 1940 S1 | C/1940 S1 (Okabayasi-Honda) | 1940-08-15 |

## Geographic visibility summary (Phase 1)

Per spec §8.5. Visibility margins computed at four US-population latitude
bands (Gulf 30°N, South 35°N, Mid 40°N, North 45°N) at limiting mag 4.5,
geometry + atmospheric extinction only (no moonlight, no surface brightness,
no era-dependent threshold).

- Apparitions with `days_any_band_visible > 0`: 45 / 644
- Apparitions with all 4 bands visible for ≥ 30 days: 17
- Median `days_any_band_visible` (among ever-visible): 25

### Top 10 apparitions by `peak_best_margin`

| rank | apparition | comet | peak_mag (geocentric) | peak_best_band | peak_best_margin | days_any_band_visible |
|---|---|---|---|---|---|---|
| 1 | C_1861J1_1861 | C/1861 J1 (Great comet) | -0.99 | North | 4.75 | 31 |
| 2 | 7P_1927 | 7P/Pons-Winnecke | -0.04 | Gulf | 4.51 | 52 |
| 3 | C_1882R1_1882 | C/1882 R1 (Great September comet) | -13.13 | Gulf | 4.10 | 65 |
| 4 | C_1858L1_1858 | C/1858 L1 (Donati) | -0.19 | South | 4.01 | 51 |
| 5 | 1P_1910 | 1P/Halley | -0.12 | Gulf | 3.57 | 41 |
| 6 | C_1881K1_1881 | C/1881 K1 (Great comet) | +0.03 | North | 3.41 | 36 |
| 7 | C_1882F1_1882 | C/1882 F1 (Wells) | -7.95 | North | 3.24 | 28 |
| 8 | C_1864N1_1864 | C/1864 N1 (Tempel) | +0.60 | Gulf | 3.19 | 21 |
| 9 | C_1853G1_1853 | C/1853 G1 (Schweizer) | +0.31 | Gulf | 3.14 | 13 |
| 10 | 109P_1862 | 109P/Swift-Tuttle | +1.54 | Gulf | 2.91 | 49 |

### Great Southern Comets — geocentric brightness vs US visibility

These four comets have spectacular geocentric peak magnitudes (−9 to −13)
but were below the horizon for US observers during their bright phase.
This is the central motivation for the geographic-visibility model.

| apparition | comet | peak_mag (geocentric) | peak_best_margin (US) | days_any_band_visible |
|---|---|---|---|---|
| C_1865B1_1865 | C/1865 B1 (Great southern comet) | -11.32 | −∞ (never visible) | 0 |
| C_1880C1_1880 | C/1880 C1 (Great southern comet) | -9.10 | −∞ (never visible) | 0 |
| C_1882R1_1882 | C/1882 R1 (Great September comet) | -13.13 | 4.10 | 65 |
| C_1887B1_1887 | C/1887 B1 (Great southern comet) | -12.38 | −∞ (never visible) | 0 |

Note: C/1882 R1 has `days_any_band_visible > 0` because the comet
remained naked-eye for months as it moved north then south. During its
brightest phase (mag < 0), however, it was largely below the US horizon
at solar conjunction — see `reports/geographic_visibility_implementation.md`.

## Caveats

- City/topocentric visibility is not implemented in this increment.
- `mag_le_6 = true` reflects integrated magnitude only. A large diffuse
  comet at integrated mag 5 may have appeared dimmer to the eye than a
  compact comet at the same magnitude. Surface-brightness modeling is
  deferred to the city-visibility increment.
- The photometric law is applied symmetrically around perihelion
  (`photometric_law = symmetric`). Pre- vs. post-perihelion asymmetric
  activity slopes are not fit.
- No hand-curated `M1`/`K1` overrides have been applied; the manual CSV
  only fills SBDB gaps (Tier 1.5), and SBDB takes precedence on conflict.
- AERITH does not catalog non-periodic comets observed before 1995.
  Non-periodic apparitions in 1850–1940 are sourced from JPL SBDB and
  uniformly assigned `event_case = unexpected_seen` (synthetic AERITH
  status `Discovered`), since by definition a one-shot first appearance
  is unexpected.
- C/1882 R1 (Great September Comet) post-split fragments R1-A through R1-D
  are merged into a single apparition row using the earliest perihelion
  and R1-A's geometry for ephemeris. Original fragment list is preserved
  in the `merged_fragments` field.

## Validation failures

_None._
