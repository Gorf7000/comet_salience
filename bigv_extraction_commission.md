# Commission: Extract Comet Photometric Parameters from Vsekhsvyatskij 1958

## 0. Purpose and context

This commission is a focused extraction job for a downstream pipeline.

The parent project (Comet Salience, Chapter 5 of a dissertation) builds a brightness-duration dataset for comet apparitions between 1850 and 1940. JPL's Small-Body Database (SBDB) does not store photometric parameters (M1, K1) for many of the historically observed pre-1950 comets, and for some periodic comets it stores nuclear-biased fits that systematically underestimate active-coma brightness by 5–10 magnitudes near perihelion.

Vsekhsvyatskij's 1958 *Physical Characteristics of Comets* (NASA Technical Translation TT F-80, hereafter "Big V") is the standard historical photometric reference for this period. It compiles per-apparition `H10` values (absolute magnitude assuming K1 = 10) drawn from contemporary observations, with citations to Holetschek 1894, individual observatory archives, and Vsekhsvyatskij's own *Catalogue of Absolute Magnitudes* (C.A.M.).

**Your job is to read Big V and produce a structured CSV of `pdes, M1, K1, source_citation, notes` rows that the parent pipeline can ingest.**

The extraction must be faithful to the source, traceable to the page, and matched against the parent project's modern designations so ingestion is automatic.

---

## 1. Inputs

You will find these files in the parent project's working tree:

1. **The PDF** (or a folder of PDF pages) at `data/inputs/`. The dissertation author has extracted the pages relevant to the 1850–1940 scope — you should not need the whole book.
2. **`data/inputs/bigv_target_list.csv`** — every apparition in scope (1850–1940), with the modern designation we use (`modern_pdes`), the comet name, the perihelion date, and a `priority` flag indicating how badly we need that comet's H10. **Use this file as your designation lookup table.**
3. **`data/processed/comet_apparitions_coded.csv`** — the full apparition scaffold, if you need additional context.
4. **`comet_visibility_commission_v2.md`** — the parent-project commission, for context on how the values will be used.

You do not need to read the JPL/MPC data or the AERITH scrape — those are the parent pipeline's concern.

---

## 2. Deliverable

A single CSV at:

```
data/inputs/bigv_staging.csv
```

with the following exact columns:

| column | content |
|---|---|
| `pdes` | the **modern** designation. For periodics, the parent comet (e.g., `6P`, `2P`). For non-periodics, the modern apparition designation without the `C/` prefix (e.g., `1858 L1`, `1882 R1`). Must match a `modern_pdes` value in `bigv_target_list.csv`. |
| `M1` | H10 value (numeric, decimal). Use Vsekhsvyatskij's C.A.M. value if cited; else Holetschek midpoint; else E-II; else other authority. |
| `K1` | always `10.0` (Big V's universal assumption). |
| `source_citation` | the specific Big V subreference, formatted exactly: `Vsekhsvyatskij 1958, C.A.M.` / `Vsekhsvyatskij 1958, Holetschek` / `Vsekhsvyatskij 1958, E-II` / `Vsekhsvyatskij 1958, other` |
| `notes` | short human-readable note: alternate values cited, asymmetry remarks, anomalies, comet behaviour |
| `match_confidence` | one of `high` / `medium` / `low` — see §5 below |
| `bigv_designation_old` | the Big V entry's header designation as printed (e.g., `1851 I`, `1858 II`, `1858d`) |
| `bigv_page` | page number in the source PDF |
| `ocr_excerpt` | the relevant snippet of OCR text (1–3 lines) showing where the H10 came from. Keep it raw — do not clean OCR artefacts |

**Optional second deliverable**: if you write a reproducible parser, commit it as `scripts/parse_bigv.py`. Not required, but encouraged.

---

## 3. Extraction rules

### 3.1 H10 selection

Big V often cites multiple authorities. Prefer in this order:

1. **Vsekhsvyatskij's own C.A.M.** if cited (`In C.A.M. H10 = X`)
2. **Holetschek midpoint** — if Holetschek gives a range (`H10 = 9.9 to 10.4`), use the midpoint (`10.15`)
3. **E-II** if cited
4. **Any other authority** Big V quotes
5. **Vsekhsvyatskij's own narrative estimate** if no formal authority is cited (low confidence)

Record the chosen subreference in `source_citation` and the alternates in `notes`.

### 3.2 OCR notation legend

| OCR | Real meaning |
|---|---|
| `9™.5` / `7™.6` etc. | `9.5ᵐ` / `7.6ᵐ` — magnitudes (the `™` is a misread superscript m) |
| `Hj)` / `H,;` / `H1)` / `H~)` | `H10` |
| `m=` | apparent magnitude at a date (not absolute) |
| `(r, A)` | `(r, Δ)` — heliocentric / geocentric distance in AU |
| `D9` / `Dy` | `D₀` — coma diameter in arcminutes |
| `~` between values | "approximately" / "≈" |

### 3.3 Asymmetric photometry

Big V occasionally distinguishes pre- and post-perihelion H10 values (e.g., "E-II (7.6 before perihelion and 12 after)"). The parent pipeline uses a symmetric photometric law and cannot accommodate asymmetric fits. **Use the brighter of the two** values for `M1` and record the asymmetry in `notes` (e.g., `pre-peri 7.6, post-peri 12; took pre-peri (brighter)`). The pipeline will then capture the comet's peak observability.

### 3.4 Range-only or qualitative values

If Big V gives only a range with no preferred value (`10 to 11`), use the midpoint (`10.5`) and flag `match_confidence = medium` with note `Big V cites 10-11 only`.

If Big V provides only qualitative descriptions (`bright`, `faint`, `telescopic only`) with no numeric H10, **skip the entry** — produce no row. Do not invent values from descriptive text.

### 3.5 Missing or unclear H10

If the entry has no H10 anywhere, **skip the entry**. Do not produce a row with a guessed value.

If you can read the entry's narrative observed magnitudes (`m = 9.5 at discovery, m = 11 at last observation`) but no H10 is stated, **skip** unless the magnitudes can be unambiguously converted to H10 (which usually they cannot without orbital geometry computation).

### 3.6 Periodic vs non-periodic policy

For **periodic comets**, you should produce **at most one row per parent comet** (`pdes` = bare designation like `2P`, `6P`, `8P`). If Big V gives different H10 values for different apparitions of the same comet:

- Prefer the **C.A.M. value** (it is Big V's preferred synthesis across apparitions)
- If multiple per-apparition H10s are given without a synthesis, **use the brightest**, and note in `notes` (e.g., `Big V gives 9.5 in 1851, 10 in 1857, 9.8 in 1862; took 9.5`). The parent pipeline applies the M1/K1 row to all apparitions of that comet, so the brightest is the right choice for the chapter's question.

For **non-periodic comets**, produce one row per apparition. The `pdes` is the full modern designation (e.g., `1858 L1`).

### 3.7 Out-of-scope entries

Skip entirely:

- Apparitions outside 1850–1940 (Big V covers a wider range; only extract entries that match a row in `bigv_target_list.csv`)
- Entries that do not match any `modern_pdes` in the target list (rare, but possible if Big V lists a doubtful comet that didn't make it into modern catalogs)

Do **not** produce rows for skipped entries. Skipping silently is fine.

---

## 4. Designation matching

This is the hardest part. Big V uses old designations like `1851 I` (year + Roman numeral, in order of perihelion passage that year) and old discoverer names. The parent pipeline uses modern IAU designations (`1851 P1` for the first comet discovered in the second half of August 1851, etc.).

Match in this order:

1. **By comet name + apparition year.** If Big V says `1858 II (Donati)` and the target list has `1858 L1 (Donati)` with `apparition_year = 1858`, that's a match. This works for nearly all named non-periodics and for periodic comets discoverable by name.
2. **By perihelion date proximity.** Big V states a perihelion date for each entry (often in the (r, Δ) line series). If the date matches a row in `bigv_target_list.csv` within ±2 days, that's a match.
3. **By Roman-numeral order within the year.** If the first two methods fail and Big V's `1851 I` corresponds to the chronologically first 1851 comet in the target list, that's a match. Fallback only.

Record the match basis in `notes` (`matched by name`, `matched by perihelion date`, `matched by year + Roman numeral order`).

If you cannot match an in-scope entry to any `modern_pdes`, **flag it with `match_confidence = low`** and put the best-guess `pdes` field with a `?` suffix (e.g., `1851 P1?`). The dissertation author will resolve manually.

---

## 5. Quality flags

Set `match_confidence` per row:

- **`high`** — both: (a) clean H10 extraction (C.A.M. value, or unambiguous Holetschek/E-II), AND (b) confident designation match (by name, with year corroboration).
- **`medium`** — one of: (a) H10 came from a range or alternate authority, (b) designation matched by perihelion date alone, (c) some OCR ambiguity in the value but a defensible reading.
- **`low`** — the row should be reviewed by hand: poor OCR, ambiguous match, conflicting authorities, asymmetric photometry, etc.

Aim for ~70–80% `high` rows. The author will spot-check `medium` and read every `low` row.

---

## 6. Worked examples

### Example 1: clean periodic, C.A.M. value (high confidence)

OCR snippet (roughly):

> 1851 I (1851a). The first recorded observation of the short-period d'Arrest Comet. Discovered by d'Arrest (Leipzig) in Pisces on 27 June. ... In C.A.M. Hj)=9™.5. At the beginning of August D, =2'.2.

Output row (the d'Arrest comet's modern pdes from the target list is `6P`):

```
pdes,M1,K1,source_citation,notes,match_confidence,bigv_designation_old,bigv_page,ocr_excerpt
6P,9.5,10.0,"Vsekhsvyatskij 1958, C.A.M.","matched by name (d'Arrest); Holetschek 9.9-10.4 also cited; first apparition of 6P/d'Arrest",high,1851 I,XXX,"In C.A.M. Hj)=9™.5"
```

### Example 2: non-periodic, asymmetric photometry (medium confidence)

OCR snippet:

> 1851 III (1851b). Discovered by Brorsen (Senftenberg) ... Absolute magnitude was first estimated in E-II (7™.6 before perihelion and 12™ after).

This is comet 5D/Brorsen's 1851 apparition. Wait — actually this is a non-periodic discovered by Brorsen in 1851. Modern designation in the target list: confirm via the target list. Suppose it matches `1851 P1` (or whatever the target list shows for the 1851 Brorsen discovery in Canes Venatici).

Output row:

```
pdes,M1,K1,source_citation,notes,match_confidence,bigv_designation_old,bigv_page,ocr_excerpt
1851 U1,7.6,10.0,"Vsekhsvyatskij 1958, E-II","matched by name + year; pre-peri 7.6, post-peri 12; took pre-peri (brighter); no C.A.M. value cited",medium,1851 III,XXX,"Absolute magnitude was first estimated in E-II (7™.6 before perihelion and 12™ after)"
```

(The actual `pdes` depends on what the target list shows — verify rather than guessing.)

### Example 3: skip — qualitative only

OCR snippet:

> 1872 V (1872c). Discovered by ... A telescopic object, faint throughout. References ...

No numeric H10 anywhere. **Skip — produce no row.**

---

## 7. Process suggestions

You may use any approach (regex, LLM extraction, manual transcription, hybrid). The output CSV is the deliverable; the path to it is your choice.

A workable pipeline:

1. OCR the PDF pages to text (you can use whatever OCR tool produces the cleanest output for this typeface).
2. Split the OCR by entry headers (lines matching `^(18\d\d) ([IVX]+)\b` or similar).
3. For each entry: extract the year + Roman numeral; resolve to `modern_pdes` via the target list; extract H10; emit a CSV row.
4. Write the CSV to `data/inputs/bigv_staging.csv`.

If you write a script for this, place it at `scripts/parse_bigv.py` and commit it. Reproducibility is appreciated but not required.

---

## 8. Delivery

Two acceptable methods:

1. **Commit `bigv_staging.csv` (and optionally `scripts/parse_bigv.py`) to the repo.** Branch name your choice; the dissertation author will merge.
2. **Provide the CSV as raw text** for the dissertation author to paste into the file.

Either way, the dissertation author will review `match_confidence = low` rows by hand against the page-numbered OCR excerpts, then promote approved rows from `bigv_staging.csv` into `data/inputs/manual_M1K1.csv`. The parent pipeline will then regenerate the dataset with the new values.

---

## 9. Out of scope

- Do **not** modify any file outside `data/inputs/bigv_staging.csv` and (optionally) `scripts/parse_bigv.py`.
- Do **not** edit `data/inputs/manual_M1K1.csv` directly. That promotion is the dissertation author's call.
- Do **not** alter the parent commission spec or any of the pipeline source modules.
- Do **not** invent values from qualitative descriptions or fill missing H10s with guesses. Skip entries with no usable photometric data.

---

## 10. Final note

The dissertation chapter compares modeled brightness-duration measures against newspaper coverage of historical apparitions. The Big V values you extract will largely determine what the model reports for the great comets of the era — Donati 1858, Tebbutt 1861, Coggia 1874, the Great September Comet 1882, Halley 1910, the Great January Comet 1910, Skjellerup-Maristany 1927, Jurlof-Achmarof-Hassel 1939. Faithful, well-cited extraction directly serves the chapter's defensibility.

Quality matters more than completeness. A clean `bigv_staging.csv` of 200 confidently-matched rows is more valuable than a sloppy 400 rows the author has to second-guess.
