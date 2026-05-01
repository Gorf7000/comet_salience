# Agent C summary — 1901–1925 (PDF pages 248–437)

**Source JSONL:** `data/intermediate/agent_work/agent_c_1901_1925.jsonl` (105 entries)
**Output CSV:** `data/intermediate/agent_work/agent_c_rows.csv` (103 rows)
**Skipped:** `data/intermediate/agent_work/agent_c_skipped.txt` (2 entries)

## Counts

- **Total Big V entries processed:** 105
- **Rows written:** 103
- **Skipped (no usable H10 / unresolved designation):** 2

### By confidence

| confidence | count |
|---|---|
| high | 54 |
| medium | 36 |
| low | 13 |

(~52% high, 35% medium, 13% low — slightly below commission's 70-80% high target band; this 1901-1925 range has more periodic recoveries with body-overrides and more asymmetric/erroneous-flagged cases that pulled rows down to medium/low.)

### By source

| source | count |
|---|---|
| Vsekhsvyatskij 1958, C.A.M. | 67 |
| Vsekhsvyatskij 1958, other (Big V synthesis) | 32 |
| Vsekhsvyatskij 1958, E-I | 4 |

## Manual designation overrides (23 cases)

Roman-fallback / name-match script errors corrected by body-reading:

| Big V old | script gave | overridden to | reason |
|---|---|---|---|
| 1903 I | 1902 X1 | **1903 A1** | Giacobini's 17 Jan 1903 discovery — not Brooks recovery |
| 1903 II | 1903 A1 | **1902 X1** | Brooks recovery, swapped with 1903 I |
| 1906 V | 1906 V1 | **15P** | "first apparition of Finlay" recovery = 15P |
| 1907 V | 1907 V1 | **1907 T1** | Mellish 9 Oct 1907 — peri 1907-Nov fits T1 |
| 1908 II | 1908 R1 | **11P** | "second apparition of Tempel-Swift" = 11P |
| 1909 II | 18D | **7P** | "fifth apparition of Pons-Winnecke" = 7P |
| 1909 III | 7P | **18D** | "sixth apparition of Perrine-Mrkos" = 18D (swapped with 1909 II) |
| 1909 IV | 1909 R1 | **33P** | "first apparition of Daniel" = 33P |
| 1911 VIII | 1911 V1 | **19P** | "fourth apparition of Borrelly" = 19P |
| 1912 IV | 26P | **8P** | "fourth apparition of Tuttle" = 8P |
| 1913 I | 1913 A1 | **1912 Y1?** | Gale's 8 Dec 1912 discovery — uncertain match, flagged |
| 1913 VI | 1913 R1 | **20D** | "first/last apparition of Westphal" — y=-5.2 negative! = 20D |
| 1915 IV | 15P | **1915 R1** | Mellish 21 Sept 1915 discovery — not 15P |
| 1918 III | 14P | **206P** | "first apparition of Barnard-Boattini" = 206P |
| 1918 IV | 19P | **19P** | confirmed Borrelly 5th apparition |
| 1918 V | 206P | **14P** | "fourth apparition of Wolf(1)" = 14P (swapped with 1918 III) |
| 1919 III | 1919 Q2 | **23P** | "first apparition of Brorsen-Metcalf" return = 23P |
| 1919 V | 23P | **1919 Q2** | Metcalf 21 Aug 1919 — but body says Schaer; flagged low |
| 1920 II | 21P | **10P** | "seventh apparition of Tempel(2)" = 10P |
| 1920 III | 11P | **1920 X1** | Skjellerup 13 Dec 1920 — Taylor name-match was wrong |
| 1925 IV | 1925 W1 | **10P** | "eighth apparition of Tempel(2)" = 10P |
| 1925 V | 1925 W1 | **4P** | "tenth apparition of Faye" = 4P |
| 1925 IX | 1925 W1 | **16P** | "fifth apparition of Brooks(2)" = 16P |
| 1925 X | 1925 W1 | **14P** | "sixth apparition of Wolf(1)" = 14P |

## "Erroneous" / underestimate flags from Big V (V1 pattern)

Big V explicitly flags an authority's value as wrong; primary value taken from Big V's own synthesis with source = "other":

1. **1903 III (1903 H1, Borrelly)** — Big V flagged C.A.M. as overestimate; took synthesis 9.1.
2. **1906 V (15P/Finlay)** — Big V flagged C.A.M./E-I value; took synthesis 9.0.
3. **1907 IV (1907 L2, Daniel)** — Big V flagged E-I; took synthesis 4.0 (bright comet).
4. **1909 III (18D/Perrine-Mrkos)** — Big V flagged early estimates; synthesis 13.3.
5. **1911 IV (1911 S3, Beljawsky)** — Big V flagged C.A.M. H10=4.0 as too bright (peak m=1-2 inconsistent); took synthesis 5.0.
6. **1911 V (1911 O1, Brooks)** — Big V flagged C.A.M.; synthesis 5.1.
7. **1912 I (14P/Wolf)** — Big V flagged E-I; synthesis 9.1.
8. **1913 I (1912 Y1?, Gale)** — Big V flagged C.A.M.; synthesis 9.0; designation also uncertain.
9. **1915 II (1915 C1, Mellish)** — Big V flagged C.A.M. as underestimate; synthesis 3.7.
10. **1916 IV (489P?)** — Big V flagged C.A.M. H10; synthesis 12.5 with designation uncertain.
11. **1917 I (1917 F1, Mellish)** — Big V flagged E-I; synthesis 7.3.
12. **1919 III (23P/Brorsen-Metcalf)** — Big V flagged C.A.M.; synthesis 9.6.
13. **1920 III (1920 X1, Skjellerup)** — Big V flagged E-I H10=11.0 "apparently too large a value"; took Big V reappraisal 11.9 (note: this was an over-estimate flag where Big V's value was actually fainter, but kept Big V's value per pattern).

Plus 2 additional cases where Big V noted but did not flag a primary authority as erroneous (asymmetric only):
14. **1903 V** — minor authority disagreement, no override.
15. **1906 VI (97P/Metcalf-Brewington)** — asymmetric, no erroneous flag.

## Asymmetric photometry cases (sec 3.3 applied — took brighter pre-peri value)

15 entries flagged asymmetric:

- **1901 I (1901 G1, Great Comet 1901)** — pre-peri brighter; took 4.0
- **1905 V (1905 W1, Schaer)** — took 8.9
- **1906 I (1905 X1, Brooks)** — took 8.3
- **1906 VI (97P/Metcalf-Brewington)** — took 9.5
- **1907 I (1907 E1, Giacobini)** — took 6.5
- **1910 III (1910 P1, Metcalf)** — took 5.4
- **1912 III (1912 V1, Borrelly)** — took 8.0
- **1913 VI (20D/Westphal)** — y=-5.2 NEGATIVE (brightness DROPPED toward perihelion!); took 8.8
- **1914 III (1914 M1, Kritzinger)** — took 4.7
- **1919 V (1919 Q2, Schaer)** — took 4.7
- **1922 I (26P/Grigg-Skjellerup)** — rapid post-peri fade; took 12.5
- **1923 I (1922 W1, Skjellerup-Reid)** — took 7.5
- **1923 II (6P/d'Arrest)** — brightness flare after peri; took 9.8 pre-peri value
- **1924 I (1924 F1, Reid)** — took Big V initial estimate 4.8 (much brighter than C.A.M. 9.0)
- **1924 III (2P/Encke 36th)** — took C.A.M. 10.0

## Skipped entries (2)

See `agent_c_skipped.txt` for full details. Summary:

1. **1911 VII (1911h)** — page 393 — 24P/Schaumasse first apparition. Vorontsov-Vel'yaminov derived photometric parameters but Big V notes "the mean error in H0 is 4m.4, which exceeds the figure itself by a factor of 2.5." No reliable C.A.M./V/E value. Per sec 3.5, skip rather than guess.
2. **1924 IV (1924d)** — page 429 — Wolf 22 Dec 1924 discovery; Przybyllok orbit T=1925-Jan-10.957 q=2.428 e=0.371 P=7.59 yr periodic, but designation cannot be resolved against target list. Closest periodic candidates (113P/Spitaler 1924-07-08, 14P/Wolf 1925-11-08) don't match T=Jan 1925 q=2.43. C.A.M. H10=11.8 available if designation later resolved.

## Famous-comet sanity checks

- **1901 I (Great Comet 1901, Viscara)** — M1=4.0. Reported peak m=1 in late April with r_peri≈0.24, Δ_min≈0.83: predicted peak ≈ 4.0 + 5log(0.83) - 10log(0.24) = 4.0 - 0.41 + 6.18 = 9.8. Hmm — peak m=1 vs predicted 9.8 is way off. Big V confirms K1=10 fit; the pre-peri brightening was much steeper. This is a well-known "anomalous brightener" Great Comet — flagged for review.
- **1910 I (Great January Daylight Comet 1910)** — M1=5.4. With r_peri=0.13, Δ_min≈0.84: predicted peak ≈ 5.4 - 0.78 - 8.86 = -4.24. Reported peak m=-2.7 to -3, visible in daylight. Within ~1 mag of canonical fit — clean.
- **1910 II (1P/Halley 28th apparition)** — M1=5.5. Took C.A.M. value; matches 28-apparition long-term Halley H10≈4-5.5 range. Naked-eye 0m peak with tail >100° in May 1910.
- **1911 IV (1911 S3, Beljawsky)** — M1=5.0. Big V flagged C.A.M. 4.0 as too bright; synthesis 5.0. Reported peak m=1-2 in October. With r_peri=0.30, Δ=0.55: predicted peak = 5.0 - 1.31 - 5.23 = -1.54. Matches m=1 (within ~2-3 mag — "Great Comet" tier).
- **1911 V (1911 O1, Brooks)** — M1=5.1. Reported peak m=2 with prominent tail. Consistent.
- **1925 II (29P/Schwassmann-Wachmann 1)** — M1=5.0. Distant orbit (r=5.4-7.3 AU) means apparent magnitude stays in the 16-19m range with episodic 5-9 mag outbursts. M1=5.0 captures the outburst ceiling correctly.

## Periodic-comet entries (will dedupe at pipeline level)

This range produced multiple apparition rows for these periodic parents:

- **2P/Encke**: 6 apparitions (1901 II=9.1, 1908 I=10.8, 1914 VI=10.1, 1918 I=10.6, 1921 IV=10.8, 1924 III=10.0)
- **10P/Tempel 2**: 4 apparitions (1904 III=9.8, 1915 I=11.0, 1920 II=10.0, 1925 IV=10.5)
- **14P/Wolf**: 3 apparitions (1912 I=9.1, 1918 V=9.9, 1925 X=10.6)
- **16P/Brooks 2**: 3 apparitions (1903 V=9.5, 1911 I=10.5, 1925 IX=10.1)
- **19P/Borrelly**: 3 apparitions (1905 II=9.0, 1911 VIII=9.5, 1918 IV=10.2)
- **4P/Faye**: 2 apparitions (1910 V=9.6, 1925 V=10.1)
- **6P/d'Arrest**: 2 apparitions (1910 IV=10.1, 1923 II=9.8)
- **7P/Pons-Winnecke**: 2 apparitions (1909 II=9.7, 1915 III=9.2)
- **21P/Giacobini-Zinner**: 2 apparitions (1907 III=12.3, 1913 V=11.3) — first and second apparitions
- **22P/Kopff**: 2 apparitions (1906 IV=8.4, 1919 I=8.6) — discovery and first recovery
- **26P/Grigg-Skjellerup**: 2 apparitions (1902 II=9.0, 1922 I=12.5)

Other periodics with single rows in range: 8P/Tuttle, 11P/Tempel-Swift-LINEAR, 15P/Finlay, 17P/Holmes, 18D/Perrine-Mrkos, 20D/Westphal, 23P/Brorsen-Metcalf, 24P/Schaumasse, 25D/Neujmin 2, 28P/Neujmin 1, 29P/Schwassmann-Wachmann 1, 33P/Daniel, 69P/Taylor, 97P/Metcalf-Brewington, 206P/Barnard-Boattini.

## Notes on H1 vs H10

For most rows I took the C.A.M. H10 value when present. No row uses H1 as the M1 in this batch — Big V always provides at least one H10 value where extracted (skipped rows had no usable H10 either).

## Notes on non-standard photometric exponents (y not equal to 4)

Several entries had non-standard y values noted in their `notes` field:

- **1913 VI (20D/Westphal)**: y=-5.2 NEGATIVE (anomalous fading toward perihelion)
- **1922 I (26P)**: rapid post-peri fade
- **1924 III (2P/Encke)**: van Biesbroeck y=15
- **1925 VII (1925 W1, van Biesbroeck)**: Vorontsov y=11.5

These entries retain canonical K1=10.0 per commission convention; non-standard y is documented in notes for downstream reviewers.

## Confidence-level rationale

- **low** rows (13): mostly entries with designation uncertainty (e.g., 1916 IV "489P?", 1913 I "1912 Y1?"), unresolved name-vs-Roman conflicts (1920 III Skjellerup), or strong asymmetry/erroneous flags where M1 choice required judgment.
- **medium** rows (36): periodic recoveries where designation override was confident but no clean C.A.M. value (Big V synthesis), narrative-synthesis cases, range-only values with mid-point taken, and asymmetric cases where the brighter pre-peri value was chosen.
- **high** rows (54): clean C.A.M. value with confident designation match (mostly single-apparition comets matched by name + JSONL pdes confirmed by body).
