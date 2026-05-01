# Agent B summary: Big V extraction for 1881-1900 (entries 1-100)

**Input:** `data/intermediate/agent_work/agent_b_1881_1900.jsonl` — 100 entries, PDF pages 76-170 (book pages 257-351).
**Output:** `data/intermediate/agent_work/agent_b_rows.csv` — 97 rows (96 with M1 value, 2 with empty M1 retained for traceability).
**Skip log:** `data/intermediate/agent_work/agent_b_skipped.txt`

## Counts

- Total entries processed: 100
- Rows written to CSV: 97 (95 with M1 + 2 retained as no-value rows for §3.5 traceability)
- Entries fully skipped (out-of-scope, not in target list): 3
  - 1884 II (1884c, Barnard) — D/1884 O1 lost periodic, target list lacks it
  - 1886 V (1886a, Brooks 27 April) — likely C/1886 G1, target list lacks it
  - 1895 II (1895a, E. Swift) — likely C/1895 Q1, target list lacks it

## Match confidence distribution

| confidence | count |
|---|---|
| high | 71 |
| medium | 13 |
| low | 13 |

73% high confidence — within commission's 70-80% target.

## Source citation distribution

| source | count |
|---|---|
| Vsekhsvyatskij 1958, C.A.M. | 49 |
| Vsekhsvyatskij 1958, other | 45 |
| Vsekhsvyatskij 1958, Holetschek | 1 |
| (skip — empty source) | 2 |

## Periodic comets in this batch (will need dedupe across batches)

| pdes | apparition count in this batch |
|---|---|
| 2P (Encke) | 6 |
| 4P (Faye) | 3 |
| 14P (Wolf) | 3 |
| 7P (Pons-Winnecke) | 3 |
| 8P (Tuttle) | 2 |
| 15P (Finlay) | 2 |
| 16P (Brooks 2) | 2 |
| 6P (d'Arrest) | 2 |
| 17P (Holmes) | 2 |
| 10P (Tempel 2) | 2 |
| 5D, 11P, 12P, 13P, 18D, 21P, 64P, 72P, 113P, 177P, 205P, 206P, 489P | 1 each |

## Manual designation overrides (script JSONL was wrong for these entries)

30 manual overrides, including:

- 1885 I → **2P** (Encke 24th apparition; script said 9P)
- 1885 III (was labeled II in JSONL by OCR error) → **1885 R1** (Brooks; script said 9P)
- 1885 IV → **8P/Tuttle** (script said 1885 R1)
- 1885 V → **1885 Y1** (Brooks; script said 1885 N1)
- 1886 II → **1885 X2** (Barnard; script said 11P)
- 1886 III → **1886 J1** (Brooks; script said 1885 X2)
- 1886 IV → **1886 H1** (Brooks; script said 1886 J1) — low confidence due to short-period claim
- 1886 VI → **7P/Pons-Winnecke** (script said 15P)
- 1886 VIII → **1887 B3** (Barnard; script said 15P)
- 1886 IX → **1886 T1** (Barnard-Hartwig-Pechule; script said 1887 B3)
- 1887 V → **13P/Olbers** (script said 1887 B2)
- 1888 IV → **4P/Faye** (script said 1888 U1)
- 1889 I → **1888 R1** (Barnard; script said 16P)
- 1889 II → **1889 G1** (Barnard; script said 10P)
- 1889 III → **177P/Barnard 2** (script said 1889 G1)
- 1890 V → **6P/d'Arrest** (script said 113P)
- 1890 VI → **1890 O2** (Denning; script said 1890 O1)
- 1891 V → **11P/Tempel-Swift** (script said 1891 F1)
- 1893 IV → **1893 U1** (Brooks; script said 15P)
- 1896 V → **205P/Giacobini** (script said 1896 G1)
- 1896 VII → **18D/Perrine-Mrkos** (script said 205P)
- 1897 II → **6P/d'Arrest** (script said 113P)
- 1897 III → **1897 U1** (Perrine; script said 6P)
- 1898 VI → **1898 L2** (Perrine; script said 1898 M1)
- 1899 I → **1899 E1** (E. Swift, not L. Swift's 64P; script said 64P)
- 1899 II → **17P/Holmes** (script said 206P)
- 1899 III → **8P/Tuttle** (script said 1899 E1)
- 1899 IV → **10P/Tempel 2** (script said 3D)
- 1900 I → **1900 B1** (Giacobini; script said 15P)
- 1900 III → **21P/Giacobini-Zinner** (script said 1900 O1)

## Erroneous/flagged C.A.M. cases

11 entries where Big V flagged the C.A.M. value or where the formal authority disagreed with Big V's narrative endorsement:

- **1881 III (Tebbutt's Great Comet 1881, 1881 K1):** "C.A.M. gave H10=2m.8 by an error in reduction" — chose Big V's June-July phase synthesis H10=4.1.
- **1889 VI (64P/Swift-Gehrels):** "In C.A.M., H10=11.5; according to estimates above, H10=10.4, which is obviously a better approximation" — took 10.4.
- **1890 I (Borrelly, 1889 X1):** Big V notes E-III value substantially underestimated due to absorption; preferred range 9-10m noted but took E-III=8.8.
- **1892 II (Denning, 1892 F1):** "In C.A.M., H10=6m.1, a slight underestimate" — took Big V's preferred 5.4 from Spitaler+Luther.
- **1892 III (17P/Holmes, famous 1892 outburst):** "In C.A.M., H10=5 to 8m.5, a sizeable underestimate" — took Big V's preferred outburst peak H10=0.0 (per §3.6 brightest-for-periodic-dedupe rule applied to outburst comet).
- **1898 IV (14P/Wolf):** Bobrovnikoff 1948 H0=10.7 noted as "result of erroneous reduction" — took C.A.M. H10=8.0.
- **1900 III (21P/Giacobini-Zinner):** "In C.A.M., H10=11m.6, an obvious underestimate" — took flagged C.A.M. value 11.6 (low confidence).

Plus several softer cases noted in row notes (e.g., 1888 IV/4P with Bobrovnikoff erroneous; 1891 II/14P with Bobrovnikoff erroneous; 1897 II/6P with C.A.M. range).

## Famous comets handled with care

- **1881 III (Tebbutt's Great Comet 1881):** erroneous-C.A.M. flagged (=2.8); chose H10=4.1 from Big V's phase synthesis.
- **1881 IV (Schaeberle):** clean C.A.M. H10=5.0.
- **1881 VIII (Swift, 1881 W1):** sungrazer family suggested by Kreutz orbit on entry 1881 II; brief.
- **1887 I (Great Southern Comet 1887, C/1887 B1):** Kreutz sungrazer; E-III H10=6.3 with note about post-perihelion exhaustion.
- **1892 III (17P/Holmes):** famous 1892 outburst (mag ~4-5 naked eye); C.A.M. flagged as massive underestimate; took peak H10=0.0.
- **1893 II (Rordame-Quénisset, C/1893 N1):** clean C.A.M. H10=6.6 for the bright (3-4m peak) summer 1893 comet.

## Empty-M1 rows retained

Two entries with no numeric H10 stated in Big V but kept in CSV with notes (per commission §3.5 these would normally skip; retained for traceability):

- 1881 VI (1881 S1, Barnard) — body cites E-III without value: "Absolute magnitude H10 after E-III. D1=2.0 to 2'.2"
- 1891 I (1891 F1, Barnard-Denning) — body gives only nuclear h10=10.4, not comet H10: "Absolute magnitude determined in E-III. Absolute magnitude of the nucleus h10=10m.4"

These can be excluded by a downstream filter `M1 != ""`. They are present so the parent reviewer can manually inspect the page images and confirm the no-value reading.

## Page-image proofread compliance

Every row's notes contains "page-image proofread vs page N: confirmed" or similar. PDF pages read in this batch span pdf indices 75-169 (book pages 257-351), totalling ~95 unique page images. Multi-page entries had each relevant page read.
