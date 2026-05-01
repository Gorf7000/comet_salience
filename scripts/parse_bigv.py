"""Segment Big V (Vsekhsvyatskij 1958) entries and resolve designations.

This script does the deterministic plumbing only:

  1. Extract text from data/inputs/BigV_comet_extracts.pdf via pymupdf.
  2. Segment into entries on the `<year> <Roman> (<paren_id>).` header.
  3. Resolve each entry's modern_pdes from data/inputs/bigv_target_list.csv
     using name + apparition_year, with Roman-numeral order as a tiebreak
     when multiple targets share the surname in that year.
  4. Write data/intermediate/bigv_entries.jsonl: one JSON record per entry
     with full body text, designation match, and metadata.

H10 selection — choosing among multiple candidates, recognizing
"erroneously"-flagged C.A.M. values, handling asymmetric photometry,
non-standard photometric exponents, and the H1-vs-H10 distinction —
happens downstream in conversation by reading the body text directly,
NOT in this script. See reports/bigv_extraction_session.md (decision D5).

Run inside the .bigv_venv sidecar:
    .bigv_venv/Scripts/python.exe scripts/parse_bigv.py

There is also a final --dedupe-staging mode that runs the periodic-comet
collapse on a complete bigv_staging.csv (commission §3.6).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "data" / "inputs" / "BigV_comet_extracts.pdf"
TARGET_LIST_PATH = PROJECT_ROOT / "data" / "inputs" / "bigv_target_list.csv"
RAW_TEXT_PATH = PROJECT_ROOT / "data" / "intermediate" / "bigv_raw.txt"
ENTRIES_JSONL_PATH = PROJECT_ROOT / "data" / "intermediate" / "bigv_entries.jsonl"
STAGING_CSV_PATH = PROJECT_ROOT / "data" / "inputs" / "bigv_staging.csv"
FIRST_BOOK_PAGE = 182  # PDF page 0 -> printed book page 182.

# Header marker we inject between pages to track book page numbers.
PAGE_MARKER_RE = re.compile(
    r"^===PAGE_(\d{4}) \(book p\.(\d+)\)===$",
    re.MULTILINE,
)

# Entry header. Tolerates:
#   - Roman numerals OCR'd with `1` for `I`, `l` for `I`.
#   - An optional second parenthetical (e.g. "1882 I (1882b) (a in current publications).").
ENTRY_HEADER_RE = re.compile(
    r"^(?P<year>\d{4})\s+"
    r"(?P<roman>[IVXl1]{1,6})\s*"
    r"\((?P<paren>[^)]*)\)"
    r"(?:\s+\([^)]*\))?"
    r"\.",
    re.MULTILINE,
)

# Discoverer-name patterns. Pull surname tokens from the entry head so we
# can match against bigv_target_list.csv's comet_name surname.
DISCOVERER_PATTERNS = [
    re.compile(r"[Dd]iscovered (?:in [^.]+? )?by\s+([A-Z][\wÀ-ſ'’\-]+)"),
    re.compile(r"[Dd]iscovered by\s+([A-Z][\wÀ-ſ'’\-]+)"),
    re.compile(r"[Dd]iscovered independently by\s+([A-Z][\wÀ-ſ'’\-]+)"),
    re.compile(r"[Dd]etected by\s+([A-Z][\wÀ-ſ'’\-]+)"),
    re.compile(r"recovery by\s+([A-Z][\wÀ-ſ'’\-]+)"),
    re.compile(r"observation of (?:the )?(?:short-period\s+)?([A-Z][\wÀ-ſ'’\-]+)\s+Comet"),
    # Periodic-comet recovery forms: "the Encke Comet", "the Encke-Backlund Comet",
    # "apparition of the Halley Comet", "Faye's Comet".
    re.compile(r"(?:apparition|return) of (?:the )?(?:short-period\s+|periodic\s+)?"
               r"([A-Z][\wÀ-ſ'’\-]+(?:-[A-Z][\wÀ-ſ'’\-]+)*)(?:[' ]s?)?\s*Comet"),
    re.compile(r"\bthe (?:short-period\s+|periodic\s+)?"
               r"([A-Z][\wÀ-ſ'’\-]+(?:-[A-Z][\wÀ-ſ'’\-]+)*)(?:'s)?\s+Comet"),
    re.compile(r"\b([A-Z][\wÀ-ſ'’\-]+(?:-[A-Z][\wÀ-ſ'’\-]+)*)'s\s+(?:short-period\s+)?[Cc]omet"),
    # "Schweizer (Moscow)" form — capitalized name immediately followed by parenthesized place.
    re.compile(r"\b([A-Z][\wÀ-ſ'’\-]{2,})\s+\([A-Z][\w\s,'\.\-]*\)"),
]

# Tokens that look like names but aren't (cities, common words, months).
NAME_BLACKLIST = {
    # cities / observatories
    "leipzig", "berlin", "paris", "vienna", "moscow", "geneva", "kazan",
    "kremsmunster", "altona", "brussels", "rome", "petersburg", "hamburg",
    "marseilles", "cambridge", "liverpool", "cordoba", "athens", "santiago",
    "florence", "padua", "potsdam", "perth", "munich", "konigsberg",
    "pulkovo", "harvard", "leiden", "bonn", "dorpat", "markree", "albany",
    "nantucket", "senftenberg", "christiania", "stockholm", "copenhagen",
    "oxford", "edinburgh", "greenwich", "lick", "yerkes", "lowell",
    "observatory", "obs", "u.s.a.", "usa", "england", "germany",
    # months / common words / verbs
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "comet", "discovered", "observed", "detected", "first", "passage",
    "before", "after", "between", "near", "moonlight", "twilight",
    "spotted", "seen", "described", "reported", "passed", "moved",
    "located", "found", "estimated", "measured", "compared",
    "very", "quite", "still", "again",
    # adjectives that combine with "Comet" but aren't names
    "great", "bright", "brilliant", "faint", "telescopic", "naked",
    "new", "the", "another", "second", "third",
    # roman-numeral artefacts
    "vi", "vii", "viii", "ix", "iv", "ii", "iii",
}


@dataclass
class Entry:
    year: int
    roman: str
    paren_id: str
    book_page: int
    pdf_page_idx: int
    body: str
    discoverer_candidates: list[str] = field(default_factory=list)
    modern_pdes: str | None = None
    match_basis: str = ""
    match_confidence_hint: str = ""


# ---------------------------------------------------------------------------
# Roman numeral helpers
# ---------------------------------------------------------------------------

def normalize_roman(token: str) -> str | None:
    """OCR-tolerant Roman numeral normalization. Returns None if invalid."""
    norm = token.upper().replace("1", "I").replace("L", "I")
    if not re.fullmatch(r"[IVX]+", norm):
        return None
    try:
        n = roman_to_int(norm)
    except KeyError:
        return None
    if 1 <= n <= 39 and int_to_roman(n) == norm:
        return norm
    return None


def roman_to_int(s: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10}
    total, prev = 0, 0
    for ch in reversed(s):
        v = vals[ch]
        total += -v if v < prev else v
        prev = v
    return total


def int_to_roman(n: int) -> str:
    pairs = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for val, sym in pairs:
        while n >= val:
            out.append(sym)
            n -= val
    return "".join(out)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text(pdf_path: Path, raw_path: Path, force: bool = False) -> str:
    """Cache PDF text to raw_path with page markers."""
    if not force and raw_path.exists() and raw_path.stat().st_mtime > pdf_path.stat().st_mtime:
        return raw_path.read_text(encoding="utf-8")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    doc = pymupdf.open(pdf_path)
    for i, page in enumerate(doc):
        chunks.append(f"\n===PAGE_{i:04d} (book p.{FIRST_BOOK_PAGE + i})===\n")
        chunks.append(page.get_text())
    text = "".join(chunks)
    raw_path.write_text(text, encoding="utf-8")
    return text


# ---------------------------------------------------------------------------
# Segmentation
# ---------------------------------------------------------------------------

def segment_entries(text: str) -> list[Entry]:
    page_positions = [
        (m.start(), int(m.group(1)), int(m.group(2)))
        for m in PAGE_MARKER_RE.finditer(text)
    ]

    def page_of(pos: int) -> tuple[int, int]:
        last = (0, FIRST_BOOK_PAGE)
        for start, idx, book in page_positions:
            if start > pos:
                break
            last = (idx, book)
        return last

    headers: list[tuple[int, int, str, str]] = []
    for m in ENTRY_HEADER_RE.finditer(text):
        year = int(m.group("year"))
        raw_roman = m.group("roman")
        paren = m.group("paren")
        roman = normalize_roman(raw_roman)
        if roman is None:
            continue
        # Paren id is "year + lowercase discovery letter" (e.g. 1851a).
        # Allow l/I/O as OCR stand-ins for 1/1/0.
        if not re.match(r"[\dlIO]{4}[a-zA-Z]", paren):
            continue
        headers.append((m.start(), year, roman, paren))

    entries: list[Entry] = []
    for i, (pos, year, roman, paren) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        body = text[pos:end]
        # Strip page-marker lines from the body (they're navigation, not content).
        body = PAGE_MARKER_RE.sub("", body).strip()
        pdf_idx, book_page = page_of(pos)
        entries.append(Entry(
            year=year,
            roman=roman,
            paren_id=paren,
            book_page=book_page,
            pdf_page_idx=pdf_idx,
            body=body,
        ))
    return entries


# ---------------------------------------------------------------------------
# Designation matching
# ---------------------------------------------------------------------------

def load_target_list(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["perihelion_date"])
    df["surname"] = df["comet_name"].apply(extract_surname)
    df["surname_lower"] = df["surname"].str.lower()
    return df


def extract_surname(name: str) -> str:
    """Get discoverer surname from comet_name strings.

    Examples:
      'C/1850 J1 (Petersen)'        -> 'Petersen'
      '6P/d\\'Arrest'                -> 'd\\'Arrest'
      '54P/de Vico-Swift-NEAT'      -> 'de Vico-Swift-NEAT'
      'C/1858 L1 (Donati)'          -> 'Donati'
    """
    if not isinstance(name, str):
        return ""
    if "/" in name and not name.startswith("C/"):
        return name.split("/", 1)[1].strip()
    m = re.search(r"\(([^)]+)\)\s*$", name)
    if m:
        return m.group(1).strip()
    return ""


def extract_discoverer_candidates(body: str) -> list[str]:
    """Return ordered, deduped surname candidates from entry head."""
    head = body[:1500]  # first ~25 lines
    raw: list[str] = []
    for pat in DISCOVERER_PATTERNS:
        for m in pat.finditer(head):
            n = m.group(1).strip("'’-")
            if len(n) < 3:
                continue
            if n.lower() in NAME_BLACKLIST:
                continue
            raw.append(n)
    seen, out = set(), []
    for n in raw:
        if n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out


def match_designation(entry: Entry, targets: pd.DataFrame) -> tuple[str | None, str, str]:
    """Resolve modern_pdes for an entry. Returns (pdes, basis, confidence_hint)."""
    year_targets = targets[targets["apparition_year"] == entry.year]
    if year_targets.empty:
        return None, "no targets in apparition year", "low"

    candidates = extract_discoverer_candidates(entry.body)
    entry.discoverer_candidates = candidates

    # 1. Surname match within year using the discoverer-candidate list
    #    (extracted from entry head). Bidirectional contains so
    #    "Encke-Backlund" matches target "Encke", and split on hyphens for
    #    multi-discoverer periodics like "de Vico-Swift-NEAT".
    #
    #    When multiple targets share the surname (e.g. 3 Brorsen comets in
    #    1851), Big V's Roman is the year-wide perihelion position, NOT the
    #    Nth within the surname-matched subset. So tiebreak using the
    #    year-sorted position: pick the surname-matched target at year
    #    position Roman_int, if it exists.
    def cand_variants(c: str) -> list[str]:
        cv = c.lower()
        out = [cv]
        for sep in ("-", " "):
            if sep in cv:
                out.extend(part for part in cv.split(sep) if len(part) >= 3)
        return out

    sorted_year = year_targets.sort_values("perihelion_date").reset_index(drop=True)
    roman_int = roman_to_int(entry.roman)

    for cand in candidates:
        for cv in cand_variants(cand):
            mask = sorted_year["surname_lower"].apply(
                lambda s: cv in s or s in cv if isinstance(s, str) else False
            )
            hits = sorted_year[mask]
            if len(hits) == 1:
                return hits.iloc[0]["modern_pdes"], f"name ({cand}) + year", "high"
            if len(hits) > 1:
                # Year-wide Roman position must point to a surname-matched row.
                if 1 <= roman_int <= len(sorted_year) and bool(mask.iloc[roman_int - 1]):
                    return (
                        sorted_year.iloc[roman_int - 1]["modern_pdes"],
                        f"name ({cand}) + year + Roman position {roman_int}",
                        "medium",
                    )

    # 2. Body scan: look for any target-year surname (or surname token)
    #    appearing as a word anywhere in the body. Catches periodic-comet
    #    recoveries that mention the namesake later in the entry, and great
    #    comets known by descriptive name. Tokens go through NAME_BLACKLIST
    #    so we don't false-match on common words ("comet", "great",
    #    "september") embedded in descriptive comet_names like
    #    "Great September comet".
    # Restrict body scan to head of entry. Late mentions of a name (e.g.
    # Barnard observing the 1882 Great September Comet) are not discoverer
    # signal and produce false matches. Periodic-comet recoveries typically
    # name the comet in the first paragraph anyway.
    body_lower = entry.body[:800].lower()
    body_hits: list[tuple[str, str]] = []  # (pdes, matched_token)
    for _, target_row in year_targets.iterrows():
        sn = target_row["surname_lower"]
        if not isinstance(sn, str) or len(sn) < 3:
            continue
        tokens: set[str] = set()
        # Always include the full surname as a phrase.
        if " " not in sn or sn not in NAME_BLACKLIST:
            tokens.add(sn)
        # Split on hyphens and spaces; filter blacklisted tokens.
        for sep in ("-", " "):
            if sep in sn:
                for part in sn.split(sep):
                    if len(part) >= 4 and part not in NAME_BLACKLIST:
                        tokens.add(part)
        if not tokens:
            continue
        for tok in tokens:
            if re.search(r"\b" + re.escape(tok) + r"\b", body_lower):
                body_hits.append((target_row["modern_pdes"], tok))
                break
    # Dedupe by pdes; keep first match per pdes.
    seen = set()
    unique_body_hits = []
    for pdes, tok in body_hits:
        if pdes not in seen:
            seen.add(pdes)
            unique_body_hits.append((pdes, tok))

    if len(unique_body_hits) == 1:
        pdes, tok = unique_body_hits[0]
        return pdes, f"body scan token '{tok}' + year", "medium"
    if len(unique_body_hits) > 1:
        # Multiple hits: tiebreak by year-wide Roman position. Only return
        # if the year-position-N target is one of the body-scan-matched
        # targets.
        matched_pdes = {p for p, _ in unique_body_hits}
        if 1 <= roman_int <= len(sorted_year):
            cand_at_pos = sorted_year.iloc[roman_int - 1]["modern_pdes"]
            if cand_at_pos in matched_pdes:
                return (
                    cand_at_pos,
                    f"body scan + year + Roman position {roman_int}",
                    "low",
                )

    # 3. Roman-numeral fallback (LOW — unverified; will need manual review
    #    during the body-reading pass).
    if 1 <= roman_int <= len(sorted_year):
        return (
            sorted_year.iloc[roman_int - 1]["modern_pdes"],
            f"Roman fallback unverified (#{roman_int} of {len(sorted_year)})",
            "low",
        )
    return None, f"Roman index {roman_int} > {len(sorted_year)} targets", "low"


# ---------------------------------------------------------------------------
# JSONL output
# ---------------------------------------------------------------------------

def write_entries_jsonl(entries: list[Entry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(asdict(e), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Periodic-comet dedupe (§3.6) — runs on a populated bigv_staging.csv
# ---------------------------------------------------------------------------

def dedupe_staging(csv_path: Path, target_list_path: Path) -> dict:
    """Collapse multiple apparitions of a periodic comet to one row.

    For each periodic pdes with >1 row: prefer the row whose source_citation
    contains 'C.A.M.'; else pick the row with the brightest (smallest) M1.
    Append collapsed alternates to notes.
    """
    targets = pd.read_csv(target_list_path)
    periodic_pdes = set(targets.loc[targets["is_periodic"], "modern_pdes"].unique())

    df = pd.read_csv(csv_path)
    groups = df.groupby("pdes", sort=False)

    keep_rows: list[dict] = []
    collapsed = 0
    for pdes, group in groups:
        if pdes not in periodic_pdes or len(group) == 1:
            keep_rows.extend(group.to_dict(orient="records"))
            continue
        cam_mask = group["source_citation"].str.contains("C.A.M.", na=False, regex=False)
        cam_rows = group[cam_mask]
        if len(cam_rows) >= 1:
            chosen = cam_rows.sort_values("M1").iloc[0]
        else:
            chosen = group.sort_values("M1").iloc[0]
        others = group.drop(chosen.name)
        if len(others) > 0:
            extra = "; ".join(
                f"{r['bigv_designation_old']}: M1={r['M1']}"
                for _, r in others.iterrows()
            )
            chosen = chosen.copy()
            sep = "; " if str(chosen["notes"]).strip() else ""
            chosen["notes"] = f"{chosen['notes']}{sep}periodic dedupe across apparitions [{extra}]"
            collapsed += len(others)
        keep_rows.append(chosen.to_dict())

    out_df = pd.DataFrame(keep_rows, columns=df.columns)
    out_df.to_csv(csv_path, index=False)
    return {"input_rows": len(df), "output_rows": len(out_df), "collapsed": collapsed}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--force-extract", action="store_true",
                   help="Re-run pymupdf text extraction even if cached.")
    p.add_argument("--limit-pages", type=int, default=None,
                   help="Process only entries on the first N PDF pages.")
    p.add_argument("--diagnostics", type=Path, default=None,
                   help="Optional path for a markdown diagnostics report.")
    p.add_argument("--dedupe-staging", action="store_true",
                   help="Run periodic-comet dedupe on data/inputs/bigv_staging.csv "
                        "in place. Use after the LLM judgment pass is complete.")
    args = p.parse_args(argv)

    if args.dedupe_staging:
        if not STAGING_CSV_PATH.exists():
            print(f"ERROR: {STAGING_CSV_PATH} not found", file=sys.stderr)
            return 1
        stats = dedupe_staging(STAGING_CSV_PATH, TARGET_LIST_PATH)
        print(f"dedupe: input={stats['input_rows']} output={stats['output_rows']} "
              f"collapsed={stats['collapsed']}")
        return 0

    text = extract_text(PDF_PATH, RAW_TEXT_PATH, force=args.force_extract)
    targets = load_target_list(TARGET_LIST_PATH)
    entries = segment_entries(text)
    if args.limit_pages is not None:
        entries = [e for e in entries if e.pdf_page_idx < args.limit_pages]

    matched_high = matched_med = matched_low = unmatched = 0
    for e in entries:
        pdes, basis, hint = match_designation(e, targets)
        e.modern_pdes = pdes
        e.match_basis = basis
        e.match_confidence_hint = hint
        if pdes is None:
            unmatched += 1
        elif hint == "high":
            matched_high += 1
        elif hint == "medium":
            matched_med += 1
        else:
            matched_low += 1

    write_entries_jsonl(entries, ENTRIES_JSONL_PATH)

    print(f"entries={len(entries)} matched_high={matched_high} matched_med={matched_med} "
          f"matched_low={matched_low} unmatched={unmatched}")
    print(f"wrote {ENTRIES_JSONL_PATH}")

    if args.diagnostics:
        with args.diagnostics.open("w", encoding="utf-8") as f:
            f.write("# parse_bigv segmentation diagnostics\n\n")
            f.write(f"- entries: {len(entries)}\n")
            f.write(f"- matched_high: {matched_high}\n")
            f.write(f"- matched_medium: {matched_med}\n")
            f.write(f"- matched_low: {matched_low}\n")
            f.write(f"- unmatched: {unmatched}\n\n")
            f.write("## low-confidence and unmatched entries\n\n")
            for e in entries:
                if e.match_confidence_hint in ("low",) or e.modern_pdes is None:
                    f.write(
                        f"- {e.year} {e.roman} ({e.paren_id}) "
                        f"p.{e.book_page} -> "
                        f"{e.modern_pdes or 'UNMATCHED'} "
                        f"({e.match_basis})\n"
                    )
                    if e.discoverer_candidates:
                        f.write(f"    discoverer_candidates: {e.discoverer_candidates}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
