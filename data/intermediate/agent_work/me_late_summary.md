# Agent me_late summary — 1926-1940 (PDF pages 256-313, book pages 438-495)

**Source JSONL:** `data/intermediate/agent_work/me_late.jsonl` (77 entries assigned)
**Output CSV:** `data/intermediate/agent_work/me_late_rows.csv` (77 rows)
**Skipped:** `data/intermediate/agent_work/me_late_skipped.txt` (3 entries)

## Counts

- **Total Big V entries processed from JSONL:** 77
- **Plus 3 entries swallowed by segmenter, recovered from body merges:** 25D (1927 I), 4P (1932 IX), 14P (1934 I)
- **Skipped (no usable photometric data / doesn't match target list):** 3 (1928 III, 1930 VII, 1933 IV — all doubtful comets)
- **Rows written:** 77 (73 from JSONL after skipping 3 doubtful + 1 segmenter dupe + 4 added/recovered including 73P override)

### By confidence

| confidence | count |
|---|---|
| high | 57 |
| medium | 17 |
| low | 3 |

74% high, 22% medium, 4% low — within commission's 70-80% high target band.

## Manual designation overrides (10 cases)

Roman-fallback / name-match script errors corrected by body-reading:

| Big V old | script gave | overridden to | reason |
|---|---|---|---|
| 1927 I (paren 1926g) | (entry merged into 1926 VII Reid) | **25D** | Body explicitly: "second recorded apparition of the short-period Comet Neujmin (2)" — 25D/Neujmin 2; entry was bundled into 1926 VII body |
| 1927 III | 32P (segmenter labeled 1927 II) | **32P (correct, but bigv_designation_old corrected from "1927 II" to "1927 III")** | Roman III → II OCR confusion; Big V actually prints 1927 III for Comas Sola |
| 1930 II | 1930 D1 | **1929 Y1** | Wilk's 20 Dec 1929 Cracow discovery in Lyra (peri 1930-01-22), not the Peltier-Schwassmann-Wachmann (which is 1930 I) |
| 1930 III | 1929 Y1 | **1930 F1** | Wilk's separate 21 March 1930 discovery (peri 1930-03-28); two different Wilk comets in 1930 |
| 1930 VI | 1930 E1 (Beyer, duplicate) | **73P** | Body: discovered by Schwassmann-Wachmann 2 May 1930 at Bergedorf (independently rediscovered by Blathwayt) — first apparition of 73P/Schwassmann-Wachmann 3, peri 1930-06-14 matches (r,Δ) data |
| 1931 III | 1931 O1 (segmenter labeled 1931 II) | **1931 O1 (correct, but bigv_designation_old corrected from "1931 II" to "1931 III")** | Roman III → II OCR confusion; Big V actually prints 1931 III for Nagata |
| 1932 IX | (entry missing — segmenter swallowed it) | **4P** | Body of entry 1932 VIII contains 1932 IX (1932l) "eleventh recorded apparition of the short-period Comet Faye" merged in; recovered |
| 1934 I | (entry missing — segmenter swallowed it) | **14P** | Body of entry 1933 V contains 1934 I (1933l) "seventh recorded apparition of the short-period Comet Wolf I" merged in; recovered |
| 1935 III | 226P | **31P** | "second recorded apparition of the short-period Comet Schwassmann-Wachmann (2)" — 31P; 226P is a wrong Roman-fallback assignment |
| 1939 VIII | 35P | **489P** | Kulin's discovery 6 Jan 1940 as minor planet 1940 AB; 35P is the previous entry (Caroline Herschel-Rigollet, 1939 VI); 489P/Denning peri 1939-09-15 best matches (Jan 1940 = ~4 mo after peri) — flagged low for designation uncertainty |

## Segmenter problems (systematic)

Three entries were bundled into earlier entries by segmenter:

1. **1927 I (25D/Neujmin 2)** — bundled into entry #7 (1926 VII Reid)
2. **1932 IX (4P/Faye)** — bundled into entry #43 (1932 VIII Brooks 2). Commission flagged this risk.
3. **1934 I (14P/Wolf 1)** — bundled into entry #49 (1933 V Whipple)

All three were recovered by body-reading; rows written as additional CSV entries with proper `bigv_designation_old`.

Two entries from the JSONL print as Roman III but were OCR-misread as Roman II (giving duplicate "1931 II", "1927 II" labels in segmenter output):

1. Entry #9 ("1927 II (1926f)" Comas Sola) — actually printed as **1927 III** in book
2. Entry #33 ("1931 II (1931b)" Nagata) — actually printed as **1931 III** in book

Both designation_old fields corrected to the printed Roman III.

## "Erroneous" / underestimate flags from Big V (V1 pattern)

Big V explicitly flags a cited authority's value as wrong (similar to Donati 1858 VI in session log), prompting override to Big V's own synthesis:

1. **1927 IX (1927 X1, Skjellerup-Maristany)** p448-450 — C.A.M. H10=7.2 flagged "an apparent underestimate". Big V's synthesis: y=13.1, Hy=5.3, **H10=5.2** taken. Source = "other". Non-standard high y exponent. Confidence low (asymmetric photometry / non-standard law / famous comet flagged for review).
2. **1928 IV (27P/Crommelin)** p452 — C.A.M. H10=12 flagged as based on "van Biesbroeck's estimates (apparently underestimates)". Big V synthesis from naked-eye + various observers: H10=7.7-9.2 first period, H10=12 second period. Took first-period brighter end **7.7**. Source = "other". Confidence medium.

## Asymmetric photometry / phase-only values (§3.3 applied)

- **1926 V (15P/Finlay)**: C.A.M. H10=12.7 (final period); using August (initial) estimates Big V gets H10=11.6 → took 11.6 brighter; "comet grew faint more rapidly than r^-4*Δ^-2" (non-standard law).
- **1926 VI (21P/Giacobini-Zinner)**: H10(min)=15 on 4 March 1927, max H10=11.5 December 1926 → took maximum 11.5 per §3.6.
- **1927 IX (Skjellerup-Maristany)**: y=13.1 non-standard; took Big V H10=5.2 (synthesis after C.A.M. flagged erroneous).
- **1928 II (2P/Encke 1928)**: E-I H10=11.0 vs at r=0.6 H10=10.0 (Big V's r-corrected) — took 10.0 (brighter).
- **1928 IV (27P/Crommelin)**: see V1 list above — took first-period 7.7 brighter.
- **1929 II (37P/Forbes)**: E-I H10=11.4 from van Biesbroeck; initial period H10=9.9 (brighter) — took 9.9.
- **1929 I (31P/SW2)**: E-I H10=7.5 initial vs 8.3 second period — took 7.5 brighter.
- **1930 I (1930 D1)**: C.A.M. initial period H10=12.5, March H10=14.5 — took 12.5 brighter.
- **1930 V (1930 L1, Forbes)**: C.A.M. initial 9.3, after 21 June 11; Big V notes "comet apparently was rapidly exhausted" (non-standard) — took 9.3 brighter.
- **1932 VI (1932 M2, Geddes)**: E-I y=9.6, H10=3.5 chosen over Bobrovnikoff's H0=5.1 (which Big V flags as inconsistent with observed brightness 5m off).
- **1932 X (1932 Y1, Dodwell-Forbes)**: E-I H10=8.7 initial vs March/April 11-12.5 — took 8.7 brighter.
- **1933 I (1933 D1, Peltier 1933)**: E-I H10=9.5 initial period; rapid faintening end-March/April → took 9.5.
- **1933 II (7P/Pons-Winnecke)**: E-I post-peri y=15, H10=10.0 vs first period H10=13-15 — took 10.0 (post-peri brighter, contrary to typical pattern).
- **1937 IV (1937 C1, Whipple)**: pre-peri Hy=6.1 vs post-peri Hy=4.7 — Big V averages to H10=6.05; took average (post-peri actually brighter, unusual).
- **1937 V (1937 N1, Finsler)**: pre-peri y=8.2, post-peri y=2.5 — both H0=6.0; took H10=6.0.
- **1938 I (34D/Gale 1938)**: E-IV H10=12.0 vs Forbes/Johnson highest estimates 10-11 — took 10.0 (brighter midpoint of 10-11).
- **1939 V (7P/Pons-Winnecke)**: Richter H10=10.6 vs E-IV 11.4 — took Richter 10.6 (brighter, also more recent).
- **1939 VI (35P/Herschel-Rigollet)**: irregular brightness fluctuations; Nov-Jan decrease "much more rapid than r^-4*Δ^-2" (non-standard).

## Famous-comet sanity checks (§7 / external check)

- **1927 IX (Skjellerup-Maristany 1927 X1)** — M1=5.2, K1=10. Predicted m at 18 Dec (r=0.18, Δ=0.83): 5.2 + 5log(0.83) + 10log(0.18) = 5.2 - 0.40 - 7.41 = -2.6. Reported peak ~-6m on 15 Dec (per Baldet); the K1=10 fit can't reproduce sungrazer-like peak — y=13.1 very non-standard. Big V's H10=5.2 is the correct K1=10-equivalent representative. **Cross-check with Wikipedia/JPL**: 1927 X1 peri was 1927-12-18, q=0.176 AU, perihelion solar elongation low — consistent with Big V's account. Confidence low (asymmetric/non-standard). Designation 1927 X1 confirmed against target list.
- **1936 II (Peltier 1936 K1)** — M1=6.9, peri r=1.10, Δ_min=0.20. Predicted peak: 6.9 + 5log(0.20) + 10log(1.10) = 6.9 - 3.49 + 0.41 = 3.82. Reported peak m=2.9 on 1 Aug per Beyer (page 479). Reasonable agreement (M1 fit slightly underestimates peak — y was 11-19 in fits, brighter than n=4). Famous naked-eye comet with 2° tail.
- **1937 V (Finsler 1937 N1)** — M1=6.0, peri r=0.86, Δ_min=0.62. Predicted peak: 6.0 + 5log(0.62) + 10log(0.86) = 6.0 - 1.04 - 0.66 = 4.30. Reported peak 3.5-4.5 with naked eye (Vsekhsvyatskii Pulkovo binoculars). Good agreement. 7° tail naked eye.
- **1939 III (Jurlof-Achmarof-Hassel 1939 H1)** — M1=7.1, peri r=0.54, Δ=0.67. Predicted peak: 7.1 + 5log(0.67) + 10log(0.54) = 7.1 - 0.87 - 2.68 = 3.55. Reported peak m=3-3.5 naked eye on 20 April (Jeffers, van Biesbroeck). Excellent agreement.
- **1927 IV (Stearns 1927 E1)** — M1=2.0 looks anomalous bright but is correct for far-distance comet. Predicted m at 10 March (r=3.68, Δ=2.70): 2.0 + 5log(2.70) + 10log(3.68) = 2.0 + 2.16 + 5.66 = 9.82. Reported m=8.5 (van Biesbroeck), m=9.5 (Krumpholz). Reasonable. Comet observed for 4 years out to r=11.5 AU.
- **1934 II (Jackson 1935 M1)** — M1=4.4 (Konopleva 1950) is a far-distance fit. Predicted m at 3 July 1935 (r=4.24, Δ=2.90): 4.4 + 5log(2.90) + 10log(4.24) = 4.4 + 2.31 + 6.28 = 13.0 vs observed 13-15m. Acceptable (within 2m at faint end). Flagged medium for K1=10 fit at large r.

## Periodic-comet entries (will dedupe at pipeline level)

This range produced multiple apparition rows for these periodic parents:

- **2P/Encke**: 4 apparitions (1928 II=10.0, 1931 II=11.0, 1934 III=11.6, 1937 VI=10.4) — brightest 10.0
- **7P/Pons-Winnecke**: 3 apparitions (1927 VII=10.7, 1933 II=10.0, 1939 V=10.6) — brightest 10.0
- **8P/Tuttle**: 2 apparitions (1926 IV=10.6, 1939 X=11.4) — brightest 10.6
- **15P/Finlay**: 1 apparition (1926 V=11.6)
- **16P/Brooks 2**: 2 apparitions (1932 VIII=10.0, 1939 VII=11.2) — brightest 10.0
- **19P/Borrelly**: 1 apparition (1932 IV=9.2)
- **21P/Giacobini-Zinner**: 2 apparitions (1926 VI=11.5, 1933 III=12.1) — brightest 11.5
- **22P/Kopff**: 3 apparitions (1926 II=10.8, 1932 III=9.8, 1939 II=10.1) — brightest 9.8
- **24P/Schaumasse**: 1 apparition (1927 VIII=10.5)
- **25D/Neujmin 2**: 1 apparition (1927 I=10.7) — entry recovered from segmenter merge
- **26P/Grigg-Skjellerup**: 3 apparitions (1927 V=13.0, 1932 II=12.9, 1937 III=15.0) — brightest 12.9
- **27P/Crommelin**: 1 apparition (1928 IV=7.7)
- **28P/Neujmin 1**: 1 apparition (1931 I=10.9)
- **30P/Reinmuth 1**: 2 apparitions (1928 I=10.2, 1935 II=11.5) — brightest 10.2
- **31P/Schwassmann-Wachmann 2**: 2 apparitions (1929 I=7.5, 1935 III=9.9) — brightest 7.5
- **32P/Comas Sola**: 2 apparitions (1927 III=9.0, 1935 IV=9.6) — brightest 9.0
- **33P/Daniel**: 1 apparition (1937 I=12.1)
- **34D/Gale**: 2 apparitions (1927 VI=9.2, 1938 I=10.0) — brightest 9.2
- **35P/Herschel-Rigollet**: 1 apparition (1939 VI=8.5)
- **36P/Whipple**: 1 apparition (1933 V=8.0)
- **37P/Forbes**: 1 apparition (1929 II=9.9)
- **40P/Vaisala 1**: 1 apparition (1939 IV=12.2)
- **42P/Neujmin 3**: 1 apparition (1929 III=10.8)
- **4P/Faye**: 1 apparition (1932 IX=9.5) — entry recovered from segmenter merge
- **10P/Tempel 2**: 1 apparition (1930 VIII=10.3)
- **14P/Wolf 1**: 1 apparition (1934 I=12.4) — entry recovered from segmenter merge
- **58P/Jackson-Neujmin**: 1 apparition (1936 IV=13.3)
- **73P/Schwassmann-Wachmann 3**: 1 apparition (1930 VI=11.7) — designation override
- **489P/Denning**: 1 apparition (1939 VIII=12.4) — designation override, low confidence

## Non-standard photometric law flags (y values other than 4)

Several entries explicitly cite y values away from y=4 (K1=10 standard) or note non-standard brightness decline:

- 1927 IX (Skjellerup-Maristany): y=13.1 — extreme
- 1929 II (37P/Forbes): y=18 (Big V flags "not very reliable")
- 1929 III (42P/Neujmin 3): Boyer/Willis y=5
- 1930 II (1929 Y1, Wilk): y=10.4 (Kukarkin), 10.7 (Bobrovnikoff)
- 1930 III (1930 F1, Wilk): y=10.7-12.2 (varying with r)
- 1930 IV (1930 E1, Beyer): y=7.0
- 1932 V (1932 P1, Peltier-Whipple): y=21-28.5 — extreme
- 1932 VI (1932 M2, Geddes): y=6.2-10.1
- 1932 X (1932 Y1, Dodwell-Forbes): y=26 (E-I), y=16.6 (Beyer), y=5.2 (Bobrovnikoff)
- 1933 I (1933 D1, Peltier 1933): y=18.7 (E-I), y=8.0 (Beyer)
- 1933 V (36P/Whipple): y=15 (Cillie+Johnson)
- 1936 II (1936 K1, Peltier 1936): y=11-19.6
- 1936 III (1936 O1, Kaho-Kozik-Lis): y=16.8
- 1937 II (1937 D1, Wilk): y=9.7-11.1
- 1937 IV (1937 C1, Whipple): y=9.2-16.6
- 1937 V (1937 N1, Finsler): y=2.5 (post-peri) — extreme low
- 1937 VI (2P/Encke 1937): y=14.6 (Vsekhsvyatskii most recent)
- 1939 I (1939 B1, Kozik-Peltier): y=20
- 1939 III (1939 H1, Jurlof-Achmarof-Hassel): y=7.7-9.8
- 1939 V (7P): y=25 (Richter)
- 1939 IX (1939 V1, Friend): y=15
- 1939 X (8P): y=40 — extreme; Big V flags as uncertain
- Multiple entries note "decrease in brightness more rapid than r^-4*Δ^-2"

For all these, the K1=10 (n=4) fit is an approximation; M1 was chosen as the canonical Big V representative value most closely tied to the brightest observation period.

## Skipped entries (3 — see me_late_skipped.txt)

- **1928 III** Giacobini's doubtful comet (4 conflicting observers)
- **1930 VII** Nakamura's doubtful comet (Van Biesbroeck doubted records)
- **1933 IV** Carrasco's doubtful comet (single estimate, "data uncertain")

All three are doubtful comets that don't match any modern_pdes; per commission §3.7 skip.

## OCR / pymupdf garble notes

The body OCR has heavy artefacts in the photometry sentence. Page-image proofread used for all confidence-medium-and-low rows plus famous-comet rows (1927 IX, 1936 II, 1936 III, 1937 V, 1939 III, 1934 II, 1927 IV). Specific corrections caught:

- "Hjg", "Hj)", "Hip", "H10" all = H10
- Entry 12 (1927 VI Gale): printed text "in =T) rig = 9 20" decoded as "In E-I, H10=9.2"
- Entry 15 (Skjellerup-Maristany): the critical "an apparent underestimate" + "Hyg=5.2" recovered from page image; pymupdf garbled the "y=13.1" extraction into multi-line OCR
- Entry 23 (1930 I Peltier-SW): "Hyg" → H10
- Entry 73 (35P/Herschel-Rigollet): "r~A>*" decoded as "r^-4*Δ^-2"

## Known pages confirmed via PDF page-image proofread

Pages read as images during this extraction (used for OCR verification):
- 261-262 (1926 VI Reid → 1927 II Blathwayt)
- 262-264 (1927 III Comas Sola → 1927 IV Stearns)
- 266-267 (1927 VII 7P, 1927 VIII 24P/Schaumasse)
- 267-268 (1927 IX Skjellerup-Maristany)
- 268-269 (1927 IX continuation, 1928 I Reinmuth)
- 279-280 (1930 VII, 1930 VIII, 1931 I, 1931 II Encke, 1931 III Nagata)
- 284-285 (1932 II 26P, 1932 III 22P, 1932 IV 19P)
- 285-286 (1932 V Peltier-Whipple, 1932 VI Geddes start)
- 292-293 (1933 V 36P Whipple, 1934 I 14P Wolf, 1934 II Jackson)
- 297-298 (1935 IV 32P, 1936 I Van Biesbroeck, 1936 II Peltier 1936 start)
- 298-299 (1936 II continuation, 1936 III Kaho-Kozik-Lis)
- 303-304 (1937 IV Whipple, 1937 V Finsler start)
- 305-306 (1937 V continuation, 1937 VI 2P/Encke)
- 307-308 (1937 VI conclusion, 1938 I 34D, 1939 I Kozik-Peltier, 1939 II 22P, 1939 III start)
- 309-310 (1939 III conclusion, 1939 IV 40P/Vaisala)

## Confidence-level rationale

- **low** rows (3): 1927 IX (Skjellerup-Maristany — asymmetric/non-standard law/famous flagged for review); 1937 III (26P only post-peri value cited, very faint); 1939 VIII (489P/Denning — designation uncertainty; Kulin's discovery may not actually be 489P).
- **medium** rows (17): mostly entries with range-only values, asymmetric photometry where brighter end was taken, narrow ratio calculations with non-standard y, designation-confirmed-by-body but Roman fallback flagged in segmenter, or entries where Konopleva/Beyer (non-canonical) was the only available value.
- **high** rows (57): clean C.A.M. or unambiguous E-I/E-IV value with confident name+date designation match.

## Source citation distribution

| source | count |
|---|---|
| Vsekhsvyatskij 1958, C.A.M. | 22 |
| Vsekhsvyatskij 1958, E-I | 17 |
| Vsekhsvyatskij 1958, E-II | 0 |
| Vsekhsvyatskij 1958, Holetschek | 0 |
| Vsekhsvyatskij 1958, other | 38 |

The 1926-1940 range is dominated by E-IV (newer than E-II), Beyer, Bobrovnikoff, Konopleva, Richter, Vsekhsvyatskii reappraisal, all of which fall under "other" per format conventions. C.A.M. is the second-most-common source as Big V was building this catalogue. Holetschek (1894) does not cover this late period — hence zero rows. E-II references also drop out of this period (E-II is the older edition).
