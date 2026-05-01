# Comet Visibility Audit Report
_Generated 2026-05-01 13:52 UTC_

## Summary counts

- Raw apparition records collected: 644
- Records in 1850–1940 scope: 644
- Records by raw_status_source: AERITH=413, SBDB=231

- Successfully matched to ephemeris source: 644
- Failed Horizons/JPL match: 0
- Missing perihelion date: 0
- No usable light-curve window: 0
- Successful daily light curves: 427
- peak_mag <= 6.0: 21
- main_sample_candidate = true: 21

## Counts by event_case

- unexpected_seen: 280
- expected_not_seen: 211
- expected_seen: 131
- retrospective_not_observed: 16
- retrospective_pre_discovery: 6

## Magnitude model provenance (per apparition)

- horizons_tmag: 427
- failed: 217

## Magnitude quality (per apparition)

- high: 281
- failed: 217
- low: 146

## Adaptive window statistics

- Apparitions with extended window: 0
- Apparitions hitting MAX_WINDOW cap: 0

## SBDB nuclear (M2/K2) parameters present but unused

- Apparitions with M2 stored in SBDB but unused per §8.2: 126
- Apparitions with K2 stored in SBDB but unused: 126

## Manual / SBDB conflicts

- Apparitions where manual M1/K1 entry was overridden by SBDB (active-coma SBDB fit takes precedence): 0
- Apparitions where manual entry overrides nuclear-biased SBDB fit (K1 < 6.0, manual wins): 0

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
| 10P | 1873 | 14.70 | 4.50 | horizons_tmag | 14.42 | unexpected_seen |
| 10P | 1878 | 14.70 | 4.50 | horizons_tmag | 14.74 | expected_seen |
| 10P | 1883 | 14.70 | 4.50 | horizons_tmag | 16.70 | expected_not_seen |
| 10P | 1889 | 14.70 | 4.50 | horizons_tmag | 17.11 | expected_not_seen |
| 10P | 1894 | 14.70 | 4.50 | horizons_tmag | 16.44 | expected_seen |
| 10P | 1899 | 14.70 | 4.50 | horizons_tmag | 13.21 | expected_seen |
| 10P | 1904 | 14.70 | 4.50 | horizons_tmag | 16.64 | expected_seen |
| 10P | 1910 | 14.70 | 4.50 | horizons_tmag | 17.05 | expected_not_seen |
| 10P | 1915 | 14.70 | 4.50 | horizons_tmag | 16.54 | expected_seen |
| 10P | 1920 | 14.70 | 4.50 | horizons_tmag | 15.12 | expected_seen |
| 10P | 1925 | 14.70 | 4.50 | horizons_tmag | 12.77 | expected_seen |
| 10P | 1930 | 14.70 | 4.50 | horizons_tmag | 15.69 | expected_seen |
| 10P | 1935 | 14.70 | 4.50 | horizons_tmag | 16.83 | expected_not_seen |
| 14P | 1884 | 15.60 | 4.50 | horizons_tmag | 16.08 | unexpected_seen |
| 14P | 1891 | 15.60 | 4.50 | horizons_tmag | 16.11 | expected_seen |
| 14P | 1898 | 15.60 | 4.50 | horizons_tmag | 17.73 | expected_seen |
| 14P | 1905 | 15.60 | 4.50 | horizons_tmag | 18.54 | expected_not_seen |
| 14P | 1912 | 15.60 | 4.50 | horizons_tmag | 18.32 | expected_seen |
| 14P | 1918 | 15.60 | 4.50 | horizons_tmag | 16.80 | expected_seen |
| 14P | 1925 | 15.60 | 4.50 | horizons_tmag | 18.26 | expected_seen |
| 14P | 1934 | 15.60 | 4.50 | horizons_tmag | 19.04 | expected_seen |
| 26P | 1853 | 16.50 | 5.50 | horizons_tmag | 16.70 | retrospective_not_observed |
| 26P | 1858 | 16.50 | 5.50 | horizons_tmag | 16.66 | retrospective_not_observed |
| 26P | 1863 | 16.50 | 5.50 | horizons_tmag | 16.62 | retrospective_not_observed |
| 26P | 1868 | 16.50 | 5.50 | horizons_tmag | 16.58 | retrospective_not_observed |
| 26P | 1873 | 16.50 | 5.50 | horizons_tmag | 16.38 | retrospective_not_observed |
| 26P | 1878 | 16.50 | 5.50 | horizons_tmag | 15.80 | retrospective_not_observed |
| 26P | 1883 | 16.50 | 5.50 | horizons_tmag | 15.10 | retrospective_not_observed |
| 26P | 1888 | 16.50 | 5.50 | horizons_tmag | 16.56 | retrospective_not_observed |
| 26P | 1892 | 16.50 | 5.50 | horizons_tmag | 17.05 | retrospective_not_observed |
| 26P | 1897 | 16.50 | 5.50 | horizons_tmag | 17.00 | retrospective_not_observed |
| 26P | 1902 | 16.50 | 5.50 | horizons_tmag | 15.60 | retrospective_pre_discovery |
| 26P | 1907 | 16.50 | 5.50 | horizons_tmag | 15.01 | retrospective_not_observed |
| 26P | 1912 | 16.50 | 5.50 | horizons_tmag | 14.83 | retrospective_not_observed |
| 26P | 1917 | 16.50 | 5.50 | horizons_tmag | 14.31 | retrospective_not_observed |
| 26P | 1922 | 16.50 | 5.50 | horizons_tmag | 13.57 | unexpected_seen |
| 26P | 1927 | 16.50 | 5.50 | horizons_tmag | 12.93 | expected_seen |
| 26P | 1932 | 16.50 | 5.50 | horizons_tmag | 13.38 | expected_seen |
| 26P | 1937 | 16.50 | 5.50 | horizons_tmag | 14.39 | expected_seen |
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
| 28P | 1913 | 13.20 | 4.50 | horizons_tmag | 12.75 | unexpected_seen |
| 28P | 1931 | 13.20 | 4.50 | horizons_tmag | 15.68 | expected_seen |
| 29P | 1908 | 10.10 | 4.50 | horizons_tmag | 16.69 | retrospective_pre_discovery |
| 29P | 1925 | 10.10 | 4.50 | horizons_tmag | 16.68 | unexpected_seen |
| 2P | 1852 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1855 | 15.60 | 4.50 | horizons_tmag | 13.83 | expected_seen |
| 2P | 1858 | 15.60 | 4.50 | horizons_tmag | 13.93 | expected_seen |
| 2P | 1862 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1865 | 15.60 | 4.50 | horizons_tmag | 12.84 | expected_seen |
| 2P | 1868 | 15.60 | 4.50 | horizons_tmag | 14.07 | expected_seen |
| 2P | 1871 | 15.60 | 4.50 | horizons_tmag | 12.86 | expected_seen |
| 2P | 1875 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1878 | 15.60 | 4.50 | horizons_tmag | 14.00 | expected_seen |
| 2P | 1881 | 15.60 | 4.50 | horizons_tmag | 13.61 | expected_seen |
| 2P | 1885 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1888 | 15.60 | 4.50 | horizons_tmag | 13.85 | expected_seen |
| 2P | 1891 | 15.60 | 4.50 | horizons_tmag | 13.94 | expected_seen |
| 2P | 1895 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1898 | 15.60 | 4.50 | horizons_tmag | 12.69 | expected_seen |
| 2P | 1901 | 15.60 | 4.50 | horizons_tmag | 14.13 | expected_seen |
| 2P | 1905 | 15.60 | 4.50 | horizons_tmag | 12.95 | expected_seen |
| 2P | 1908 | 15.60 | 4.50 | horizons_tmag | 12.94 | expected_seen |
| 2P | 1911 | 15.60 | 4.50 | horizons_tmag | 14.12 | expected_seen |
| 2P | 1914 | 15.60 | 4.50 | horizons_tmag | 12.71 | expected_seen |
| 2P | 1918 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1921 | 15.60 | 4.50 | horizons_tmag | 13.95 | expected_seen |
| 2P | 1924 | 15.60 | 4.50 | horizons_tmag | 13.82 | expected_seen |
| 2P | 1928 | 15.60 | 4.50 | horizons_tmag | 13.00 | expected_seen |
| 2P | 1931 | 15.60 | 4.50 | horizons_tmag | 12.92 | expected_seen |
| 2P | 1934 | 15.60 | 4.50 | horizons_tmag | 14.06 | expected_seen |
| 2P | 1937 | 15.60 | 4.50 | horizons_tmag | 12.65 | expected_seen |
| 33P | 1909 | 15.50 | 4.50 | horizons_tmag | 14.26 | unexpected_seen |
| 33P | 1916 | 15.50 | 4.50 | horizons_tmag | 17.86 | expected_not_seen |
| 33P | 1923 | 15.50 | 4.50 | horizons_tmag | 18.37 | expected_not_seen |
| 33P | 1930 | 15.50 | 4.50 | horizons_tmag | 17.99 | expected_not_seen |
| 33P | 1937 | 15.50 | 4.50 | horizons_tmag | 16.27 | expected_seen |
| 41P | 1858 | 16.90 | 4.50 | horizons_tmag | 15.45 | unexpected_seen |
| 41P | 1863 | 16.90 | 4.50 | horizons_tmag | 18.68 | expected_not_seen |
| 41P | 1869 | 16.90 | 4.50 | horizons_tmag | 18.08 | expected_not_seen |
| 41P | 1874 | 16.90 | 4.50 | horizons_tmag | 16.10 | expected_not_seen |
| 41P | 1879 | 16.90 | 4.50 | horizons_tmag | 18.75 | expected_not_seen |
| 41P | 1885 | 16.90 | 4.50 | horizons_tmag | 17.71 | expected_not_seen |
| 41P | 1890 | 16.90 | 4.50 | horizons_tmag | 17.49 | expected_not_seen |
| 41P | 1896 | 16.90 | 4.50 | horizons_tmag | 17.61 | expected_not_seen |
| 41P | 1901 | 16.90 | 4.50 | horizons_tmag | 19.00 | expected_not_seen |
| 41P | 1907 | 16.90 | 4.50 | horizons_tmag | 16.84 | expected_seen |
| 41P | 1912 | 16.90 | 4.50 | horizons_tmag | 18.39 | expected_not_seen |
| 41P | 1918 | 16.90 | 4.50 | horizons_tmag | 17.98 | expected_not_seen |
| 41P | 1924 | 16.90 | 4.50 | horizons_tmag | 18.10 | expected_not_seen |
| 41P | 1929 | 16.90 | 4.50 | horizons_tmag | 17.66 | expected_not_seen |
| 41P | 1934 | 16.90 | 4.50 | horizons_tmag | 18.39 | expected_not_seen |
| 41P | 1940 | 16.90 | 4.50 | horizons_tmag | 16.85 | expected_not_seen |
| 42P | 1929 | 16.60 | 4.50 | horizons_tmag | 18.14 | unexpected_seen |
| 42P | 1940 | 16.60 | 4.50 | horizons_tmag | 18.63 | expected_not_seen |
| 69P | 1916 | 17.30 | 4.50 | horizons_tmag | 17.26 | unexpected_seen |
| 69P | 1922 | 17.30 | 4.50 | horizons_tmag | 20.15 | expected_not_seen |
| 69P | 1928 | 17.30 | 4.50 | horizons_tmag | 19.06 | expected_not_seen |
| 69P | 1935 | 17.30 | 4.50 | horizons_tmag | 19.52 | expected_not_seen |
| 7P | 1852 | 16.00 | 4.50 | horizons_tmag | 16.12 | retrospective_not_observed |
| 7P | 1858 | 16.00 | 4.50 | horizons_tmag | 14.56 | unexpected_seen |
| 7P | 1863 | 16.00 | 4.50 | horizons_tmag | 16.65 | expected_not_seen |
| 7P | 1869 | 16.00 | 4.50 | horizons_tmag | 12.00 | expected_seen |
| 7P | 1875 | 16.00 | 4.50 | horizons_tmag | 16.39 | expected_seen |
| 7P | 1880 | 16.00 | 4.50 | horizons_tmag | 16.88 | expected_not_seen |
| 7P | 1886 | 16.00 | 4.50 | horizons_tmag | 15.69 | expected_seen |
| 7P | 1892 | 16.00 | 4.50 | horizons_tmag | 11.00 | expected_seen |
| 7P | 1898 | 16.00 | 4.50 | horizons_tmag | 16.55 | expected_seen |
| 7P | 1904 | 16.00 | 4.50 | horizons_tmag | 17.19 | expected_not_seen |
| 7P | 1909 | 16.00 | 4.50 | horizons_tmag | 16.89 | expected_seen |
| 7P | 1915 | 16.00 | 4.50 | horizons_tmag | 16.08 | expected_seen |
| 7P | 1921 | 16.00 | 4.50 | horizons_tmag | 11.83 | expected_seen |
| 7P | 1927 | 16.00 | 4.50 | horizons_tmag | 9.06 | expected_seen |
| 7P | 1933 | 16.00 | 4.50 | horizons_tmag | 14.86 | expected_seen |
| 7P | 1939 | 16.00 | 4.50 | horizons_tmag | 11.35 | expected_seen |
| 8P | 1858 | 14.60 | 4.50 | horizons_tmag | 14.21 | unexpected_seen |
| 8P | 1871 | 14.60 | 4.50 | horizons_tmag | 13.86 | expected_seen |
| 8P | 1885 | 14.60 | 4.50 | horizons_tmag | 15.80 | expected_seen |
| 8P | 1899 | 14.60 | 4.50 | horizons_tmag | 15.79 | expected_seen |
| 8P | 1912 | 14.60 | 4.50 | horizons_tmag | 15.04 | expected_seen |
| 8P | 1926 | 14.60 | 4.50 | horizons_tmag | 15.77 | expected_seen |
| 8P | 1939 | 14.60 | 4.50 | horizons_tmag | 14.70 | expected_seen |
| C/1898 R1 | 1898 | 7.50 | 4.50 | horizons_tmag | 6.55 | unexpected_seen |
| C/1913 Y1 | 1914 | 4.80 | 4.25 | horizons_tmag | 6.03 | unexpected_seen |
| C/1914 F1 | 1914 | 11.10 | 4.50 | horizons_tmag | 10.02 | unexpected_seen |
| C/1915 C1 | 1915 | 7.70 | 4.50 | horizons_tmag | 6.01 | unexpected_seen |
| C/1931 O1 | 1931 | 5.70 | 4.75 | horizons_tmag | 6.77 | unexpected_seen |
| C/1932 M1 | 1932 | 11.10 | 4.50 | horizons_tmag | 12.99 | unexpected_seen |
| C/1932 M2 | 1932 | 6.10 | 4.50 | horizons_tmag | 9.34 | unexpected_seen |
| C/1939 H1 | 1939 | 6.00 | 4.50 | horizons_tmag | 3.97 | unexpected_seen |

## Manual M1/K1 candidates (Tier 3 non-periodics)

These non-periodic apparitions in scope have no SBDB photometric parameters
and produced no light curve. They are candidates for manual entry into
`data/raw/comet_sources/manual_M1K1.csv`. Sorted by perihelion year then
alphabetical by designation. Adding rows here and re-running the pipeline
will generate light curves for those apparitions.

Total Tier 3 non-periodic candidates: **207**

| pdes | comet_name | perihelion_date |
|---|---|---|
| 1850 J1 | C/1850 J1 (Petersen) | 1850-07-24 |
| 1850 Q1 | C/1850 Q1 (Bond) | 1850-10-19 |
| 1851 P1 | C/1851 P1 (Brorsen) | 1851-08-26 |
| 1851 U1 | C/1851 U1 (Brorsen) | 1851-10-01 |
| 1852 K1 | C/1852 K1 (Chacornac) | 1852-04-20 |
| 1853 E1 | C/1853 E1 (Secchi) | 1853-02-24 |
| 1853 G1 | C/1853 G1 (Schweizer) | 1853-05-10 |
| 1853 L1 | C/1853 L1 (Klinkerfues) | 1853-09-02 |
| 1853 R1 | C/1853 R1 (Bruhns) | 1853-10-17 |
| 1853 W1 | C/1853 W1 (van Arsdale) | 1854-01-04 |
| 1854 F1 | C/1854 F1 (Great comet) | 1854-03-24 |
| 1854 L1 | C/1854 L1 (Klinkerfues) | 1854-06-22 |
| 1854 R1 | C/1854 R1 (Klinkerfues) | 1854-10-28 |
| 1854 Y1 | C/1854 Y1 (Winnecke-Dien) | 1854-12-16 |
| 1855 G1 | C/1855 G1 (Schweizer) | 1855-02-05 |
| 1855 L1 | C/1855 L1 (Donati) | 1855-05-30 |
| 1855 V1 | C/1855 V1 (Bruhns) | 1855-11-25 |
| 1857 D1 | C/1857 D1 (d'Arrest) | 1857-03-21 |
| 1857 M1 | C/1857 M1 (Klinkerfues) | 1857-07-18 |
| 1857 O1 | C/1857 O1 (Peters) | 1857-08-24 |
| 1857 Q1 | C/1857 Q1 (Klinkerfues) | 1857-10-01 |
| 1857 V1 | C/1857 V1 (Donati-van Arsdale) | 1857-11-19 |
| 1858 K1 | C/1858 K1 (Bruhns) | 1858-06-05 |
| 1858 L1 | C/1858 L1 (Donati) | 1858-09-30 |
| 1858 R1 | C/1858 R1 (Tuttle) | 1858-10-13 |
| 1859 G1 | C/1859 G1 (Tempel) | 1859-05-29 |
| 1860 D1 | C/1860 D1 (Liais) | 1860-02-17 |
| 1860 H1 | C/1860 H1 (Rumker) | 1860-03-06 |
| 1860 M1 | C/1860 M1 (Great comet) | 1860-06-16 |
| 1860 U1 | C/1860 U1 (Tempel) | 1860-09-22 |
| 1861 G1 | C/1861 G1 (Thatcher) | 1861-06-03 |
| 1861 J1 | C/1861 J1 (Great comet) | 1861-06-12 |
| 1861 Y1 | C/1861 Y1 (Tuttle) | 1861-12-07 |
| 1862 N1 | C/1862 N1 (Schmidt) | 1862-06-22 |
| 1862 W1 | C/1862 W1 (Respighi) | 1862-12-28 |
| 1862 X1 | C/1862 X1 (Bruhns) | 1863-02-03 |
| 1863 G1 | C/1863 G1 (Klinkerfues) | 1863-04-05 |
| 1863 G2 | C/1863 G2 (Respighi) | 1863-04-21 |
| 1863 T1 | C/1863 T1 (Baeker) | 1863-12-29 |
| 1863 V1 | C/1863 V1 (Tempel) | 1863-11-09 |
| 1863 Y1 | C/1863 Y1 (Respighi) | 1863-12-28 |
| 1864 N1 | C/1864 N1 (Tempel) | 1864-08-16 |
| 1864 O1 | C/1864 O1 (Donati-Toussaint) | 1864-10-11 |
| 1864 R1 | C/1864 R1 (Donati) | 1864-07-28 |
| 1864 X1 | C/1864 X1 (Baeker) | 1864-12-22 |
| 1864 Y1 | C/1864 Y1 (Bruhns) | 1864-12-28 |
| 1865 B1 | C/1865 B1 (Great southern comet) | 1865-01-14 |
| 1867 S1 | C/1867 S1 (Baeker-Winnecke) | 1867-11-07 |
| 1868 L1 | C/1868 L1 (Winnecke) | 1868-06-26 |
| 1869 T1 | C/1869 T1 (Tempel) | 1869-10-10 |
| 1870 K1 | C/1870 K1 (Winnecke) | 1870-07-14 |
| 1870 Q1 | C/1870 Q1 (Coggia) | 1870-09-02 |
| 1870 W1 | C/1870 W1 (Winnecke) | 1870-12-20 |
| 1871 G1 | C/1871 G1 (Winnecke) | 1871-06-11 |
| 1871 L1 | C/1871 L1 (Tempel) | 1871-07-27 |
| 1871 V1 | C/1871 V1 (Tempel) | 1871-12-20 |
| 1873 Q1 | C/1873 Q1 (Borrelly) | 1873-09-11 |
| 1873 Q2 | C/1873 Q2 (Henry) | 1873-10-02 |
| 1874 D1 | C/1874 D1 (Winnecke) | 1874-03-10 |
| 1874 G1 | C/1874 G1 (Winnecke) | 1874-03-14 |
| 1874 H1 | C/1874 H1 (Coggia) | 1874-07-09 |
| 1874 O1 | C/1874 O1 (Borrelly) | 1874-08-27 |
| 1874 Q1 | C/1874 Q1 (Coggia) | 1874-07-18 |
| 1874 X1 | C/1874 X1 (Borrelly) | 1874-10-19 |
| 1877 C1 | C/1877 C1 (Borrelly) | 1877-01-19 |
| 1877 G1 | C/1877 G1 (Winnecke) | 1877-04-18 |
| 1877 G2 | C/1877 G2 (Swift) | 1877-04-27 |
| 1877 R1 | C/1877 R1 (Coggia) | 1877-09-11 |
| 1877 T1 | C/1877 T1 (Tempel) | 1877-06-27 |
| 1878 N1 | C/1878 N1 (Swift) | 1878-07-21 |
| 1879 Q1 | C/1879 Q1 (Palisa) | 1879-10-05 |
| 1879 Q2 | C/1879 Q2 (Hartwig) | 1879-08-29 |
| 1880 C1 | C/1880 C1 (Great southern comet) | 1880-01-28 |
| 1880 G1 | C/1880 G1 (Schaeberle) | 1880-07-02 |
| 1880 S1 | C/1880 S1 (Hartwig) | 1880-09-07 |
| 1880 Y1 | C/1880 Y1 (Pechule) | 1880-11-09 |
| 1881 J1 | C/1881 J1 (Swift) | 1881-05-20 |
| 1881 K1 | C/1881 K1 (Great comet) | 1881-06-16 |
| 1881 N1 | C/1881 N1 (Schaeberle) | 1881-08-22 |
| 1881 S1 | C/1881 S1 (Barnard) | 1881-09-14 |
| 1881 W1 | C/1881 W1 (Swift) | 1881-11-20 |
| 1882 F1 | C/1882 F1 (Wells) | 1882-06-11 |
| 1882 R1 | C/1882 R1 (Great September comet) | 1882-09-17 |
| 1882 R2 | C/1882 R2 (Barnard) | 1882-11-13 |
| 1883 D1 | C/1883 D1 (Brooks-Swift) | 1883-02-19 |
| 1884 A1 | C/1884 A1 (Ross) | 1883-12-25 |
| 1885 N1 | C/1885 N1 (Barnard) | 1885-08-06 |
| 1885 R1 | C/1885 R1 (Brooks) | 1885-08-10 |
| 1885 Y1 | C/1885 Y1 (Brooks) | 1885-11-25 |
| 1885 X1 | C/1885 X1 (Fabry) | 1886-04-06 |
| 1885 X2 | C/1885 X2 (Barnard) | 1886-05-03 |
| 1886 H1 | C/1886 H1 (Brooks) | 1886-06-07 |
| 1886 J1 | C/1886 J1 (Brooks) | 1886-05-04 |
| 1886 T1 | C/1886 T1 (Barnard-Hartwig) | 1886-12-16 |
| 1887 B3 | C/1887 B3 (Barnard) | 1886-11-28 |
| 1887 B1 | C/1887 B1 (Great southern comet) | 1887-01-11 |
| 1887 B2 | C/1887 B2 (Brooks) | 1887-03-17 |
| 1887 D1 | C/1887 D1 (Barnard) | 1887-03-28 |
| 1887 J1 | C/1887 J1 (Barnard) | 1887-06-17 |
| 1888 D1 | C/1888 D1 (Sawerthal) | 1888-03-17 |
| 1888 P1 | C/1888 P1 (Brooks) | 1888-07-31 |
| 1888 U1 | C/1888 U1 (Barnard) | 1888-09-13 |
| 1888 R1 | C/1888 R1 (Barnard) | 1889-01-31 |
| 1889 G1 | C/1889 G1 (Barnard) | 1889-06-11 |
| 1889 O1 | C/1889 O1 (Davidson) | 1889-07-19 |
| 1889 X1 | C/1889 X1 (Borrelly) | 1890-01-26 |
| 1890 F1 | C/1890 F1 (Brooks) | 1890-06-02 |
| 1890 O1 | C/1890 O1 (Coggia) | 1890-07-09 |
| 1890 O2 | C/1890 O2 (Denning) | 1890-09-25 |
| 1890 V1 | C/1890 V1 (Zona) | 1890-08-06 |
| 1891 F1 | C/1891 F1 (Barnard-Denning) | 1891-04-28 |
| 1891 T1 | C/1891 T1 (Barnard) | 1891-11-14 |
| 1892 E1 | C/1892 E1 (Swift) | 1892-04-07 |
| 1892 F1 | C/1892 F1 (Denning) | 1892-05-11 |
| 1892 Q1 | C/1892 Q1 (Brooks) | 1892-12-28 |
| 1892 W1 | C/1892 W1 (Brooks) | 1893-01-06 |
| 1893 N1 | C/1893 N1 (Rordame-Quenisset) | 1893-07-07 |
| 1893 U1 | C/1893 U1 (Brooks) | 1893-09-19 |
| 1894 G1 | C/1894 G1 (Gale) | 1894-04-13 |
| 1895 W1 | C/1895 W1 (Perrine) | 1895-12-18 |
| 1895 W2 | C/1895 W2 (Brooks) | 1895-10-21 |
| 1896 C1 | C/1896 C1 (Perrine-Lamp) | 1896-02-01 |
| 1896 G1 | C/1896 G1 (Swift) | 1896-04-18 |
| 1896 R1 | C/1896 R1 (Sperra) | 1896-07-11 |
| 1896 V1 | C/1896 V1 (Perrine) | 1897-02-08 |
| 1897 U1 | C/1897 U1 (Perrine) | 1897-12-09 |
| 1898 L1 | C/1898 L1 (Coddington-Pauly) | 1898-09-14 |
| 1898 L2 | C/1898 L2 (Perrine) | 1898-08-16 |
| 1898 M1 | C/1898 M1 (Giacobini) | 1898-07-25 |
| 1898 U1 | C/1898 U1 (Brooks) | 1898-11-23 |
| 1898 V1 | C/1898 V1 (Chase) | 1898-09-20 |
| 1899 E1 | C/1899 E1 (Swift) | 1899-04-13 |
| 1899 S1 | C/1899 S1 (Giacobini) | 1899-09-15 |
| 1900 B1 | C/1900 B1 (Giacobini) | 1900-04-29 |
| 1900 O1 | C/1900 O1 (Borrelly-Brooks) | 1900-08-03 |
| 1901 G1 | C/1901 G1 (Great comet) | 1901-04-24 |
| 1902 G1 | C/1902 G1 (Brooks) | 1902-05-07 |
| 1902 R1 | C/1902 R1 (Perrine) | 1902-11-24 |
| 1902 X1 | C/1902 X1 (Giacobini) | 1903-03-23 |
| 1903 A1 | C/1903 A1 (Giacobini) | 1903-03-16 |
| 1903 H1 | C/1903 H1 (Grigg) | 1903-03-25 |
| 1903 M1 | C/1903 M1 (Borrelly) | 1903-08-28 |
| 1904 H1 | C/1904 H1 (Brooks) | 1904-03-07 |
| 1904 Y1 | C/1904 Y1 (Giacobini) | 1904-11-03 |
| 1905 F1 | C/1905 F1 (Giacobini) | 1905-04-04 |
| 1905 W1 | C/1905 W1 (Schaer) | 1905-10-25 |
| 1906 E1 | C/1906 E1 (Kopff) | 1905-10-18 |
| 1905 X1 | C/1905 X1 (Giacobini) | 1906-01-22 |
| 1906 F1 | C/1906 F1 (Ross) | 1906-02-21 |
| 1906 V1 | C/1906 V1 (Thiele) | 1906-11-21 |
| 1907 E1 | C/1907 E1 (Giacobini) | 1907-03-19 |
| 1907 G1 | C/1907 G1 (Grigg-Mellish) | 1907-03-27 |
| 1907 L2 | C/1907 L2 (Daniel) | 1907-09-04 |
| 1907 T1 | C/1907 T1 (Mellish) | 1907-09-14 |
| 1908 R1 | C/1908 R1 (Morehouse) | 1908-12-26 |
| 1909 L1 | C/1909 L1 (Borrelly-Daniel) | 1909-06-05 |
| 1910 A1 | C/1910 A1 (Great January comet) | 1910-01-17 |
| 1910 P1 | C/1910 P1 (Metcalf) | 1910-09-16 |
| 1911 N1 | C/1911 N1 (Kiess) | 1911-06-30 |
| 1911 O1 | C/1911 O1 (Brooks) | 1911-10-28 |
| 1911 S2 | C/1911 S2 (Quenisset) | 1911-11-12 |
| 1911 S3 | C/1911 S3 (Beljawsky) | 1911-10-10 |
| 1912 R1 | C/1912 R1 (Gale) | 1912-10-05 |
| 1912 V1 | C/1912 V1 (Borrelly) | 1912-10-21 |
| 1913 J1 | C/1913 J1 (Schaumasse) | 1913-05-15 |
| 1913 R1 | C/1913 R1 (Metcalf) | 1913-09-14 |
| 1914 M1 | C/1914 M1 (Neujmin) | 1914-07-30 |
| 1914 S1 | C/1914 S1 (Campbell) | 1914-08-03 |
| 1915 R1 | C/1915 R1 (Mellish) | 1915-10-13 |
| 1918 L1 | C/1918 L1 (Reid) | 1918-06-06 |
| 1919 Y1 | C/1919 Y1 (Skjellerup) | 1920-01-03 |
| 1920 X1 | C/1920 X1 (Skjellerup) | 1920-12-11 |
| 1921 E1 | C/1921 E1 (Reid) | 1921-05-10 |
| 1921 H1 | C/1921 H1 (Dubiago) | 1921-05-05 |
| 1922 B1 | C/1922 B1 (Reid) | 1921-10-28 |
| 1922 U1 | C/1922 U1 (Baade) | 1922-10-26 |
| 1922 W1 | C/1922 W1 (Skjellerup) | 1923-01-04 |
| 1923 T1 | C/1923 T1 (Dubiago-Bernard) | 1923-11-18 |
| 1924 F1 | C/1924 F1 (Reid) | 1924-03-13 |
| 1924 R1 | C/1924 R1 (Finsler) | 1924-09-04 |
| 1925 F1 | C/1925 F1 (Shajn-Comas Sola) | 1925-09-06 |
| 1925 F2 | C/1925 F2 (Reid) | 1925-07-29 |
| 1925 G1 | C/1925 G1 (Orkisz) | 1925-04-01 |
| 1925 V1 | C/1925 V1 (Wilk-Peltier) | 1925-12-07 |
| 1925 W1 | C/1925 W1 (Van Biesbroeck) | 1925-10-02 |
| 1925 X1 | C/1925 X1 (Ensor) | 1926-02-11 |
| 1926 B1 | C/1926 B1 (Blathwayt) | 1926-01-02 |
| 1927 B1 | C/1927 B1 (Reid) | 1926-12-30 |
| 1927 A1 | C/1927 A1 (Blathwayt) | 1927-02-14 |
| 1927 E1 | C/1927 E1 (Stearns) | 1927-03-22 |
| 1927 X1 | C/1927 X1 (Skjellerup-Maristany) | 1927-12-18 |
| 1929 Y1 | C/1929 Y1 (Wilk) | 1930-01-22 |
| 1930 D1 | C/1930 D1 (Peltier-Schwassmann-Wachmann) | 1930-01-15 |
| 1930 E1 | C/1930 E1 (Beyer) | 1930-04-18 |
| 1930 F1 | C/1930 F1 (Wilk) | 1930-03-28 |
| 1930 L1 | C/1930 L1 (Forbes) | 1930-05-10 |
| 1931 P1 | C/1931 P1 (Ryves) | 1931-08-25 |
| 1932 H1 | C/1932 H1 (Carrasco) | 1931-11-29 |
| 1932 G1 | C/1932 G1 (Houghton-Ensor) | 1932-02-28 |
| 1935 M1 | C/1935 M1 (Jackson) | 1934-09-06 |
| 1935 Q1 | C/1935 Q1 (Van Biesbroeck) | 1936-05-11 |
| 1936 O1 | C/1936 O1 (Kaho-Kozik-Lis) | 1936-07-15 |
| 1937 P1 | C/1937 P1 (Hubble) | 1936-11-14 |
| 1937 D1 | C/1937 D1 (Wilk) | 1937-02-21 |
| 1939 V1 | C/1939 V1 (Friend) | 1939-11-05 |
| 1940 O1 | C/1940 O1 (Whipple-Paraskevopoulos) | 1940-10-08 |
| 1940 S1 | C/1940 S1 (Okabayasi-Honda) | 1940-08-15 |

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
