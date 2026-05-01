# Big V extraction — session log

**Session ID:** `cc012fbc-7b0c-468d-9924-7458b02ab392`
**Started:** 2026-05-01
**Commission:** `bigv_extraction_commission.md`
**Output target:** `data/inputs/bigv_staging.csv`
**Source PDF:** `data/inputs/BigV_comet_extracts.pdf` (314 pages, scanned w/ extractable text layer)

A living log of decisions and their rationale, written as we go so the
extraction's decision tree can be reconstructed later. Not a verbatim
transcript — a decision and discovery record.

---

## Inputs verified at session start

- `data/inputs/BigV_comet_extracts.pdf` — 314 pages, book pages 182–495.
- `data/inputs/bigv_target_list.csv` — 644 apparitions, 1850–1940. 413 periodic
  apparitions across 65 unique periodic comets; 231 non-periodic.
- `data/processed/comet_apparitions_coded.csv` — present, used as fallback context.
- `data/inputs/manual_M1K1.csv` — empty of Big V values (user has not added any
  manually yet, so no overlap concerns).

PDF text-layer quality: workable. PyMuPDF extracts cleanly. Notable OCR
artefacts to handle:

| Artefact | What it represents |
|---|---|
| `Hjg`, `Hj)`, `Hi`, `Hip`, `Hiq`, `H1)`, `Hjj`, `Hjyg`, `Hio`, `Hig`, `Hj0` | `H10` (Vsekhsvyatskij's absolute magnitude with K1=10) |
| `H,`, `H;`, `H~`, `H1` (alone) | `H1` (Holetschek's reduced magnitude, generally NOT equal to H10 unless n=4) |
| `™`, `"`, `m` between integer and decimal | superscript-m magnitude unit |
| `�` | catch-all for non-ASCII the OCR couldn't decode (em-dash, ᵐ, accents) |

---

## Decisions

### D1. Scope: extract everything Big V offers, not just high-priority.
Per user: "Just do them all." The target list's `priority` field
(`high_nuclear_biased`, `high_tier3`, `medium_sbdb_good`) does not gate
what we extract from Big V; the dissertation author will decide later
which extracted rows to promote into `manual_M1K1.csv`.

### D2. No overlap check against `manual_M1K1.csv` needed.
User confirmed: nothing manually entered yet, so re-extraction won't
duplicate anything that's already been hand-vetted.

### D3. Trust the PDF on Roman-numeral convention; the commission's worked Example 1 is illustrative only.
Big V's `<year> <Roman>` header is by **perihelion-passage year, in order
within that year**. The parenthesized `(1851a)` form is the older
discovery-sequence designation. The commission's Example 1 claim that
"1851 I = 6P/d'Arrest" is wrong — d'Arrest's 1851 apparition reached
perihelion in September, so it'd be 1851 IV or V. The actual `1851 I` in
the PDF is Faye's short-period comet, with its 28 Nov 1850 perihelion
falling into the 1851 numbering window. Designation matching follows
commission §4 (name+year > perihelion date > Roman fallback); the
example's specific labels are disregarded.

### D4. Sample-first delivery.
Run on a small slice first (~5–10 pages, ~15 rows), check in with user,
then scale. Quality > completeness per commission §10.

### D5. Parser script kept lean and reproducible-only-where-deterministic.
Originally planned a full parser (header → H10 → CSV) in
`scripts/parse_bigv.py`. After auditing the variation across entries
(see "Discoveries" below), pivoted to a **leaner script** that only does
the deterministic work:

- Segment OCR text into entries.
- Resolve each entry's `modern_pdes` from the target list (name+year >
  perihelion date > Roman fallback).
- Write `data/intermediate/bigv_entries.jsonl` (one record per entry
  with `{year, roman, paren_id, book_page, pdf_page_idx, body,
  modern_pdes, match_basis, match_confidence_hint}`).

The contextual judgment — which H value to take, asymmetric handling,
detecting "erroneously C.A.M.", non-standard photometric laws — is done
by Claude reading each entry's `body` directly within this session. The
notes field captures the rationale per row.

This was the explicit pivot from the original "Option A" hybrid (regex
candidates + LLM judgment) to "Option B" (LLM reads the whole entry).
Reason: a regex-driven candidate extractor relies on anomaly
heuristics to know when to fall back to body-reading, and the heuristics
are lossy in ways that miss what a human reader would catch (Big V
self-flagging "erroneous" C.A.M. values, non-standard n exponents,
fragmentation/outburst context). The user explicitly raised this
concern; the trade-off favors plan-usage tokens over silent
extraction errors.

### D6. Sidecar venv for OCR step; no changes to repo `requirements.txt`.
`requirements.txt` is pinned for the dissertation pipeline. PyMuPDF
isn't in it, and adding it just for an OCR step would be overkill. Set
up `.bigv_venv/` at repo root for parser execution. Only the parser
script depends on it; the rest of the pipeline is unaffected.

### D7. Periodic-comet dedupe runs at the end of the script, not in the LLM pass.
For periodic comets, Big V often has multiple per-apparition entries
across the 1850–1940 window. The dissertation pipeline applies one M1
to all apparitions of that comet, so we need at most one row per
parent. Per §3.6: prefer C.A.M. value if cited; else brightest. This
dedupe is mechanical once the per-apparition rows exist, and runs in
the script after CSV emission. Each survivor's `notes` field
preserves the per-apparition values that were collapsed.

### D8. Session report (this file) maintained as we go.
User explicitly requested. Updated when a decision is made or a
discovery affects future calls. Located at
`reports/bigv_extraction_session.md`.

---

## Discoveries that drove the approach

### V1. C.A.M. is not always the right value, even when cited (Donati 1858 VI)

`Hj)=1™.0` is what C.A.M. gave for Donati. Big V's own narrative says
"C.A.M. erroneously gave Hjg=1™.0", then quotes Holetschek H1=2.5 and a
Bobrovnikoff/synthesis value of H10=3.3 (with non-standard n=8.9). A
naive §3.1-priority parser would emit M1=1.0 and never see the
"erroneously" annotation. This single example is the strongest argument
for body-reading rather than candidate-only extraction.

### V2. H values appear with non-standard photometric laws

For Donati 1858 VI: `y=8.7, Hp=3™.39` and `y=11.2, Hg=4™.3` are H values
fit at non-default exponents. Used naively as M1 with K1=10, they
misrepresent the comet's brightness profile. These need to be
*recognized* and either the K1=10-equivalent value chosen, or the row
flagged.

### V3. Header parenthetical drift

`1882 I (1882b) (a in current publications).` — a second parenthetical
follows the first. Header regex must allow it: `^(\d{4})\s+([IVXl1]+)\s+\(([^)]*)\)(?:\s+\([^)]*\))?\.`

### V4. Roman-numeral OCR confusion

`II` shows up as `I1`, `Il`, `1I`, `1l`. `III` as `Ill`, `Il1`, etc.
Roman-numeral parser needs to normalize `1`/`l` → `I` then validate as
real Roman numeral.

### V5. H1 vs H10 distinction is real and matters

Big V often quotes Holetschek's `H1` (his convention, value depends on
his fitted n) alongside Vsekhsvyatskij's `H10` (assumes K1=10, n=4).
For comets where Holetschek used n=4, these are the same number. For
others, they differ. The commission's worked example assumes H10
throughout, but the actual book uses both labels. When only an H1 value
is present, flag it explicitly so the reviewer can decide whether to
treat as H10 (n=4) or skip.

### V6. Phase-specific H10 values appear in dense entries

For 1882 I (Wells), Big V quotes H10=3.3 (discovery period), H10=4.1
(C.A.M. synthesis), H10=4.6 (post-perihelion), H1=7.4 (May–June, faint
on bright background). The C.A.M. value is the right *single*
representative; alternates go in `notes`.

---

## Plan from here

1. **Rewrite the script** to the leaner D5 shape: segmenter +
   designation matcher → JSONL with full body. Drop the H10 extractor.
2. **Run on full PDF** (just segmentation/matching is cheap).
3. **Inspect 10–15 entries from the JSONL** by hand to confirm
   segmentation and designation matching are clean.
4. **Read entries in batches** and write CSV rows directly. Capture
   judgment in `notes`. Watch for V1/V2/V5/V6 patterns specifically.
5. **Sample check-in:** show user ~15 finished rows mid-extraction for
   spot-check before continuing.
6. **Periodic dedup** as a final mechanical step.
7. **Diagnostics file** written alongside the CSV: counts of skipped
   entries (qualitative-only, no H10) and reasons.

## Open questions / risks

- **Token budget.** Reading ~400 entries' worth of OCR text is feasible
  on plan usage but not free. If the conversation gets compacted
  partway through, state about which entries are done lives in the
  CSV itself (resumable).
- **Compaction recovery.** If session is compacted, the next-pass
  Claude needs to know: which JSONL records are already in the CSV,
  what conventions we've adopted (this report), and what flags to
  watch for. This file is the recovery anchor.

---

## Stage A (segmenter+matcher) results — 2026-05-01

After several iterations on the matcher, final stats from
`scripts/parse_bigv.py` on the full PDF:

| metric | count |
|---|---|
| entries segmented | 397 |
| matched_high (name + year) | 231 |
| matched_medium (body-scan or Roman tiebreak) | 97 |
| matched_low (Roman fallback unverified) | 68 |
| unmatched | 1 (1849 III, out of scope before 1850) |

83% are confidently matched. The remaining 68 entries fall to Roman
fallback because of one of these patterns; **all need manual
verification during the body-reading pass:**

1. **Big V skips a target-list comet** that wasn't observed brightly
   that apparition (e.g. 289P/Blanpain 1882 is a retrospective
   recovery). This shifts the Roman index relative to target list
   ordering.
2. **Target list uses a descriptive comet_name** (`Great January comet`,
   `Great September comet`, `Great comet`) for a famous comet that
   Big V refers to by discoverer surname (Innes, Tebbutt, etc.). The
   surname extractor pulls "Great January comet", which doesn't match
   on individual tokens after blacklisting "great" / "january" /
   "comet". 10 such targets in the list:

   - `1854 F1`, `1860 M1`, `1861 J1`, `1865 B1`, `1880 C1`,
     `1881 K1`, `1882 R1`, `1887 B1`, `1901 G1`, `1910 A1`

   For these, the script's Roman-fallback answer is *often* right
   (e.g., `1910 I → 1910 A1` is correct), but flagged low.
3. **OCR-mangled surname** that escaped the bidirectional contains
   check.

### Specific known-wrong matches found during spot-check

- **`1882 II → 289P` is wrong** — should be `1882 R1` (Great September
  Comet). Target list 1882 has 5 entries; sorted by date 289P sits at
  position 2. Big V's 1882 II is the September Comet (position 3 by
  date), but Big V skipped 289P in its 1882 coverage so its Roman II
  shifts to position 2 in the date-sorted list. Manual override
  during body-reading pass.

These are the failure modes; the body-reading pass will resolve them.

### Decisions captured during Stage A iteration

- **D9. Body-scan restricted to first 800 chars.** Late-body name
  mentions (Barnard observing the 1882 September Comet) are not
  discoverer signal and produce false matches. Trade-off: some
  periodic-comet recoveries that mention the namesake only later in
  the entry will fall to Roman fallback. Accepted.
- **D10. NAME_BLACKLIST applied at body-scan time.** Without this,
  tokens like "comet" (from `1882 R1 (Great September comet)`'s
  surname) match every entry's body and corrupt the body-scan
  tiebreak.
- **D11. Header regex made whitespace-flexible** between Roman and
  paren. `1910 1(1910a).` (no whitespace, OCR-mangled) was being
  dropped, losing 1910 I (Great January Comet). 12 additional entries
  recovered after this fix.
- **D12. No alias dictionary in script.** Could custom-map e.g.
  `1861 J1 → ['Tebbutt']` to upgrade descriptive-name target matches,
  but this would entangle the script with curatorial decisions that
  belong to the body-reading pass. Rejected.
- **D13. Paren-id validation tolerates `l`/`I`/`O` as digit OCR stand-ins.**
  Discovered while reading the 1851 d'Arrest entry: header
  `1851 I1 (185la).` was being silently dropped because `185la` doesn't
  pass `\d{4}[a-zA-Z]`. The OCR rendered the `1` in `1851` as `l`.
  Relaxed to `[\dlIO]{4}[a-zA-Z]`. Recovered 4 more entries (397→401)
  including 1851 II (d'Arrest's first apparition).

### Final Stage A stats (2026-05-01)

| metric | count |
|---|---|
| entries segmented | 401 |
| matched_high | 230 |
| matched_medium | 103 |
| matched_low | 67 |
| unmatched | 1 |

### D14. Roman tiebreak uses year-wide position, not subset position
Discovered while reading 1851 III (Brorsen): when multiple targets in
the year share the discoverer surname (e.g. 3 Brorsen comets in 1851:
1851 P1, 5D, 1851 U1), Big V's Roman III is the comet's perihelion
position in the **whole year** (1851 III = 3rd of all 1851 comets =
1851 P1, the first Brorsen). The original tiebreak picked the 3rd
match within the surname-filtered subset (= 1851 U1, third Brorsen by
date), which is wrong. Fixed: tiebreak verifies that the year-wide
sorted position with that Roman index has a surname matching one of
the candidates.

---

## Stage B (body-reading judgment) — sample run

8 sample rows written to `data/inputs/bigv_staging.csv` covering
deliberately diverse cases:

| # | Big V old | modern_pdes | M1 | conf | sample property |
|---|---|---|---|---|---|
| 1 | 1851 I | 4P | 5.5 | medium | no C.A.M. cited; multiple authorities; H1 vs H10 distinction |
| 2 | 1851 II | 6P | 9.5 | high | clean C.A.M. value; canonical worked-example shape |
| 3 | 1851 III | 1851 P1 | 7.6 | low | asymmetric photometry (pre-peri 7.6, post-peri 12) |
| 4 | 1858 VI | 1858 L1 | 3.3 | low | **Big V flags C.A.M. as erroneous; took synthesis** (V1 from session report) |
| 5 | 1882 I | 1882 F1 | 4.1 | high | clean C.A.M. with phase-specific alts in body |
| 6 | 1882 II | 1882 R1 | 0.8 | high | **manual designation override** — script said 289P, body identifies as Great September Comet |
| 7 | 1882 III | 1882 R2 | 7.4 | high | only E-II value, brief entry |
| 8 | 1910 II | 1P | 4.6 | medium | no clean C.A.M.; Big V's narrative endorses 4.6 over Bobrovnikoff's underprediction |

The sample is a checkpoint for user spot-check before scaling to all
401 entries. Specific judgment calls a reviewer should sanity-check:

- **Row 1 (4P/Faye 1851):** chose Cherednichenko (1953) H10(av)=5.5 over
  Vsekhsvyatskij (1930) H10=5.8-6.8 mid 6.3. Justification: both are
  H10 values, Cherednichenko is more recent and apparition-specific.
  Alternative: take Vsekhsvyatskij 1930 mid 6.3. The choice doesn't
  matter if the periodic dedupe later picks a 4P entry with C.A.M.
  cite.
- **Row 4 (Donati 1858):** overrode §3.1 priority to skip the
  C.A.M.-flagged-erroneous value. M1=3.3 from synthesis at y=8.9. The
  K1=10 stays per commission, but worth noting that this H10 was
  derived from a non-trivially non-standard photometric law. Confidence
  marked `low` to flag for review.
- **Row 6 (Great September 1882):** manual designation override of the
  script's 289P → 1882 R1. Confidence high because the override is
  obvious from the body and the C.A.M. value is clean.
- **Row 8 (Halley 1910):** chose Big V's narrative-endorsed H10=4.6
  over Bobrovnikoff's published Hy=5.62 (which Big V demonstrates
  underpredicts the observed magnitudes). Source labeled "other" since
  this is Big V's own synthesis statement, not a quoted authority.
  **CORRECTED post-proofread — see Stage B-prime below.**

---

## Stage B-prime — OCR proofread + external cross-check (D15)

### D15. Per-row cross-check protocol added to the bulk pass.
After completing the 8-row sample, the user (sensibly) raised the
question of how to verify my OCR transcriptions and interpretive
judgments without specialist knowledge. Two cross-checks were added:

**Per-row cross-check 1 — OCR proofread.** For every row at
`low`/`medium` confidence (and for every row producing a "famous"
designation), re-render the relevant PDF page as an image via the
Read tool and verify the H10 value against the printed text. The page
image is also visible to the user, providing an auditable layer they
can inspect even without comet-photometry expertise.

**Per-row cross-check 2 — external literature spot-check** for the
small set of "great comet" entries (Donati 1858, Tebbutt 1861/1881,
Coggia 1874, Great September 1882, Halley 1910, Great January 1910,
Skjellerup-Maristany 1927, Jurlof-Achmarof-Hassel 1939, plus periodic
favorites). Compute implied apparent magnitude at peak from the
extracted H10 + orbital geometry, compare against widely-documented
contemporary observations. This catches gross extraction errors;
modern published values use different photometric laws (often n>4) and
are not directly comparable to Big V's K1=10 convention.

### Errors caught by the sample-row proofread

Three real corrections, one of them substantive:

| row | comet | issue | fix |
|---|---|---|---|
| 5 | Wells 1882 I | note said "May-June H1=7.4"; printed text is H10=7.4 | note text only; M1 unchanged |
| 6 | Great September 1882 | note said "no clean Holetschek H10"; printed text gives Holetschek H1=0.8-1.5 (range) | note expanded |
| 7 | Barnard 1882 III | source said "E-II"; printed text is **E-III** (three I's, different reference) | source `E-II` → `other`; M1 unchanged |
| 8 | Halley 1910 | I MISSED a C.A.M. citation: `in C.A.M., H10=4m.6` was garbled by pymupdf as `Ho=4007ta 886:`. Attributed to "narrative endorsement" instead | source `other` → `C.A.M.`; confidence `medium` → `high`; M1 unchanged |

The Halley correction is the load-bearing one: it's exactly the kind
of error a candidate-list-only Stage A would miss (the C.A.M. citation
was lost in OCR garbage; only re-reading the page image recovered it).
This is direct evidence the proofread step is worth its cost.

### External cross-checks — all three famous comets pass sanity

Implied apparent-magnitude at peak (from H10 + orbital geometry vs
reported peak in modern references):

- Halley 1910 — H10=4.6 → ~mag -1.8 at closest approach; reported ~0 ✓
- Donati 1858 — H10=3.3 → ~mag -0.6 at closest approach; reported ~-1 ✓
- Donati hypothetical with C.A.M.'s erroneous 1.0 → ~mag -2.9; way
  too bright. **Independent confirmation that Big V's "erroneous" flag
  was correct.**
- Great September 1882 — H10=0.8 + sungrazer perihelion → very bright;
  reported peak -17 ✓ (sungrazer geometry dominates; comparison is
  qualitative)

### Updated sample CSV state

After the proofread + corrections, the 8-row sample now reads:
- 5 high confidence (was 4) — Halley promoted
- 1 medium (was 2)
- 2 low (was 2) — Brorsen asymmetric, Donati flagged-erroneous-CAM

A `popular_name` column was added per user request, to avoid
crosswalking modern designations against newspaper-era coverage in
Chapter 5.


---

## Final extraction complete (2026-05-01)

### Buckets and totals

| Bucket | Years | Entries | Rows | Owner |
|---|---|---|---|---|
| Sample | scattered | 8 | 8 | parent thread (sample-first) |
| me_early | 1850-1860 | 23 | 25 | parent thread |
| Agent A | 1861-1880 | 73 | 68 | subagent |
| Agent B | 1881-1900 | 100 | 97 | subagent |
| Agent C | 1901-1925 | 105 | 103 | subagent (after retry; first run stalled at 600s watchdog) |
| me_late | 1926-1940 | 77 | 77 | subagent |
| **Pre-dedupe total** |  | **386** | **378** | (rounded; small adjustments from in-bucket additions/skips) |

After running `scripts/parse_bigv.py --dedupe-staging` (collapses periodic
comet apparitions into one row per parent comet, preferring the C.A.M.-
sourced row else brightest M1):

- Input rows: 392 (includes the 14 sample/early-pages rows merged into
  the parent thread before agent buckets were assigned)
- Output rows: **274**
- Collapsed: 118 periodic apparitions

### Final confidence distribution

- **190 high (69%)** — within 70-80% target band
- **52 medium (19%)**
- **32 low (12%)**

### Final source distribution

- C.A.M.: 129 (47%)
- other: 96 (35%) — dominated by Big V's own narrative synthesis,
  E-III, E-IV, Konopleva, Beyer, Bobrovnikoff, Richter
- E-II: 28
- E-I: 18
- Holetschek: 1
- (blank): 2 — Agent B's intentional retention of two entries with no
  numeric H10 (1881 S1, 1891 F1) for traceability

### Sub-agent retry note

Agent C's first run stalled at the 600s stream watchdog before writing
its CSV — it was preparing to do all 105 entries in a single Python
script. Replacement Agent C2 was launched with explicit guardrails to
write incrementally in 10-row chunks, and completed without issue.
Lesson: large LLM-judgment passes should always emit work
incrementally, never accumulate to a final batch write.

### Pre-dedupe backup

`data/inputs/bigv_staging.predupe.csv` retains the 392-row pre-dedupe
state in case the dedupe needs to be re-run with different priority
rules.

### Per-bucket summary files preserved

All four agent buckets wrote summary markdown documenting their
overrides, erroneous-flag catches, asymmetric-photometry treatments,
and famous-comet sanity checks:

- `data/intermediate/agent_work/agent_a_summary.md`
- `data/intermediate/agent_work/agent_b_summary.md`
- `data/intermediate/agent_work/agent_c_summary.md`
- `data/intermediate/agent_work/me_late_summary.md`

These are the audit trail for the M1 choices.
