"""AERITH (Yoshida) periodic-comet apparition scraper.

Per the survey done in this session:

- AERITH's catalog indexes only cover 1995 onward (modern era).
- AERITH's per-comet pages (one per periodic comet) carry the full
  historical apparition list, with status icons and JPL-compatible
  designations like "1P/1910 R1".

This module enumerates the periodic-comet pages and parses each one
for individual apparition rows. Filtering to spec date range happens
downstream so we keep the raw scraped data unfiltered.

Status icon legend, parsed from any per-comet page:

    pr_ball.gif (!)  Discovered
    gr_ball.gif (*)  Appeared
    rd_ball.gif (-)  Not observed
    cy_ball.gif (#)  Appeared before discovery
    or_ball.gif (+)  Not observed before discovery
    wh_ball.gif (.)  Returns in the future
"""

from __future__ import annotations

import logging
import re
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup

from . import config

logger = logging.getLogger(__name__)

# Suppress the self-signed cert warning per config.AERITH_VERIFY_SSL.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ICON_TO_STATUS = {
    "pr_ball.gif": "Discovered",
    "gr_ball.gif": "Appeared",
    "rd_ball.gif": "Not observed",
    "cy_ball.gif": "Appeared before discovery",
    "or_ball.gif": "Not observed before discovery",
    "wh_ball.gif": "Returns in the future",
}

MONTH_ABBREV = {
    "Jan.": 1, "Feb.": 2, "Mar.": 3, "Apr.": 4, "May": 5, "May.": 5,
    "June": 6, "July": 7, "Aug.": 8, "Sept.": 9, "Sep.": 9,
    "Oct.": 10, "Nov.": 11, "Dec.": 12,
}


@dataclass
class AerithApparition:
    comet_id: str            # e.g., "0001P"
    comet_name: str          # e.g., "1P/Halley"
    designation: str         # e.g., "1P/1910 R1"
    perihelion_date: str     # ISO-ish "YYYY-MM-DD"
    perihelion_year: int
    raw_status_icon: str     # e.g., "gr_ball.gif"
    raw_aerith_status: str   # e.g., "Appeared"
    source_url: str
    source_row_html: str


def _cache_path(url: str) -> Path:
    """Local cache file for a URL response."""
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", url)
    return config.AERITH_CACHE / f"{safe}.html"


def _fetch(url: str, refresh: bool = False) -> str:
    """Fetch a URL, caching the response. Self-signed cert tolerated per spec."""
    cache = _cache_path(url)
    if cache.exists() and not refresh and config.CACHE_REMOTE_QUERIES:
        return cache.read_text(encoding="utf-8", errors="replace")
    logger.info("HTTP GET %s", url)
    r = requests.get(
        url,
        verify=config.AERITH_VERIFY_SSL,
        timeout=config.HTTP_TIMEOUT_SEC,
    )
    r.raise_for_status()
    cache.write_text(r.text, encoding="utf-8", errors="replace")
    time.sleep(config.HTTP_THROTTLE_SEC)
    return r.text


def list_periodic_comet_ids(refresh: bool = False) -> list[str]:
    """Return all periodic-comet IDs (e.g., '0001P', '0003D') indexed by AERITH."""
    url = f"{config.AERITH_BASE_URL}/index-periodic.html"
    html = _fetch(url, refresh=refresh)
    ids = sorted(set(re.findall(r"(\d{4}[PD])/index\.html", html)))
    logger.info("Found %d periodic comet IDs in AERITH index", len(ids))
    return ids


def _parse_perihelion_date(raw: str, year_hint: int | None = None) -> tuple[str | None, int | None]:
    """Parse strings like '1910 Apr. 20' or 'Apr. 20' (year falls back to hint).

    Returns (ISO date or None, year or None).
    """
    raw = raw.strip()
    # Format with year: "1910 Apr. 20", "1910 Apr.  9", or "1682 Sept.15" (no space).
    m = re.match(r"(\d{4})\s+([A-Za-z]+\.?)\s*(\d{1,2})", raw)
    if m:
        year, mon_s, day = int(m.group(1)), m.group(2), int(m.group(3))
        mon = MONTH_ABBREV.get(mon_s) or MONTH_ABBREV.get(mon_s + ".")
        if mon:
            return f"{year:04d}-{mon:02d}-{day:02d}", year
        return None, year
    return None, year_hint


def parse_comet_page(comet_id: str, refresh: bool = False) -> list[AerithApparition]:
    """Parse one per-comet AERITH page into individual apparition rows."""
    url = f"{config.AERITH_BASE_URL}/{comet_id}/index.html"
    html = _fetch(url, refresh=refresh)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("title").get_text(strip=True) if soup.find("title") else comet_id
    comet_name = title.strip()

    rows: list[AerithApparition] = []
    for tr in soup.find_all("tr"):
        img = tr.find("img")
        if not img:
            continue
        src = img.get("src", "")
        icon = src.rsplit("/", 1)[-1]
        if icon not in ICON_TO_STATUS:
            continue
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue
        # Layout: [icon-td] [designation-td] [perihelion-date-td]
        designation = tds[1].get_text(" ", strip=True)
        peri_raw = tds[2].get_text(" ", strip=True)
        # Skip rows where no designation present (icon-only legend rows)
        if not peri_raw:
            continue
        peri_iso, peri_year = _parse_perihelion_date(peri_raw)
        if peri_year is None:
            # Could still be useful if we can extract year from designation
            m = re.match(r"\d+[PDIC]?/(\d{4})", designation)
            if m:
                peri_year = int(m.group(1))
        rows.append(AerithApparition(
            comet_id=comet_id,
            comet_name=comet_name,
            designation=designation if designation else f"{comet_id}/?",
            perihelion_date=peri_iso or "",
            perihelion_year=peri_year if peri_year is not None else -1,
            raw_status_icon=icon,
            raw_aerith_status=ICON_TO_STATUS[icon],
            source_url=url,
            source_row_html=str(tr),
        ))
    return rows


def scrape_all_apparitions(refresh: bool = False, progress_every: int = 50) -> pd.DataFrame:
    """Scrape every periodic comet page; return raw apparition rows as DataFrame.

    No date filtering applied here; downstream filters to spec range.
    """
    ids = list_periodic_comet_ids(refresh=refresh)
    all_rows: list[AerithApparition] = []
    for i, cid in enumerate(ids, 1):
        try:
            rows = parse_comet_page(cid, refresh=refresh)
            all_rows.extend(rows)
        except requests.HTTPError as e:
            logger.warning("AERITH fetch failed for %s: %s", cid, e)
        except Exception as e:
            logger.warning("Parse failed for %s: %s", cid, e)
        if i % progress_every == 0:
            logger.info("Scraped %d/%d periodic comets, %d apparition rows so far",
                        i, len(ids), len(all_rows))
    df = pd.DataFrame([a.__dict__ for a in all_rows])
    return df


def filter_to_scope(df: pd.DataFrame, start_year: int = config.START_YEAR,
                    end_year: int = config.END_YEAR) -> pd.DataFrame:
    """Keep apparitions whose perihelion year falls inside the scope range.

    Rows missing perihelion year are flagged (kept) for audit, not dropped.
    """
    in_scope = (df["perihelion_year"] >= start_year) & (df["perihelion_year"] <= end_year)
    out = df.copy()
    out["in_scope"] = in_scope
    return out
