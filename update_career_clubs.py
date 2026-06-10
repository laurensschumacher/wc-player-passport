"""
Resolve every player's Wikipedia article via the World Cup squads pages
(2026, 2022, 2018, 2014, 2010, 2006, 2002), then scrape their senior club
career from the article infobox.

Why squad pages: the player name cell on every squad row contains a direct
<a href="/wiki/Article_Title"> link to that player's article. This avoids
title-guessing (Cafú vs Cafu, "Thomas Müller" vs "Thomas Muller", etc.) and
disambiguation pages.

The resulting `career_clubs` array is stored on each player as:
    [{"club": "Barcelona", "start_year": 2004, "end_year": 2021}, ...]
Loan rows ("(loan)" or rows with a leading "→") are skipped.

Already-checked players are NOT re-fetched. A player is considered checked
when `career_clubs` is a list (even an empty list, which we use to record
"we tried and found nothing").

Rate limit: ~1.2s between Wikipedia requests with exponential back-off on 429.
HTML is cached on disk so re-runs are fast.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).parent
CACHE_DIR = REPO_ROOT / "cache" / "wiki_career"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TITLE_INDEX_PATH = REPO_ROOT / "cache" / "squad_player_titles.json"

HEADERS = {
    "User-Agent": "PlayerPassport/1.0 (educational; career-clubs scraper)"
}

SQUAD_PAGES = [
    "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2014_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2010_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2006_FIFA_World_Cup_squads",
    "https://en.wikipedia.org/wiki/2002_FIFA_World_Cup_squads",
]

NATION_TO_WIKI_HEADING = {
    "Argentina": "Argentina", "Spain": "Spain", "Germany": "Germany",
    "Brazil": "Brazil", "France": "France", "England": "England",
    "Portugal": "Portugal", "Croatia": "Croatia", "Belgium": "Belgium",
    "Netherlands": "Netherlands", "Uruguay": "Uruguay",
    "United States": "United States", "South Korea": "South Korea",
    "Mexico": "Mexico", "Japan": "Japan", "Ghana": "Ghana",
    "Switzerland": "Switzerland", "Ivory Coast": "Ivory Coast",
    "Colombia": "Colombia", "Senegal": "Senegal", "Sweden": "Sweden",
    "Ecuador": "Ecuador", "Australia": "Australia", "Morocco": "Morocco",
    "Iran": "Iran", "Paraguay": "Paraguay", "Italy": "Italy",
    "Poland": "Poland", "Nigeria": "Nigeria", "Denmark": "Denmark",
    "Cameroon": "Cameroon", "Serbia": "Serbia", "Russia": "Russia",
}

# ---------------------------------------------------------------------------

_LAST_FETCH = 0.0
MIN_INTERVAL = 1.2


def _rate_limit() -> None:
    global _LAST_FETCH
    wait = MIN_INTERVAL - (time.time() - _LAST_FETCH)
    if wait > 0:
        time.sleep(wait)
    _LAST_FETCH = time.time()


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{hashlib.md5(key.encode()).hexdigest()}.html"


def fetch_html(url_or_title: str, *, max_retries: int = 5) -> str | None:
    url = (
        url_or_title
        if url_or_title.startswith("http")
        else f"https://en.wikipedia.org/wiki/{url_or_title.replace(' ', '_')}"
    )
    p = _cache_path(url)
    if p.exists():
        return p.read_text(encoding="utf-8")

    backoff = 5.0
    for _ in range(max_retries):
        _rate_limit()
        try:
            r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        except requests.RequestException as exc:
            print(f"    network error: {exc}; sleeping {backoff:.0f}s", flush=True)
            time.sleep(backoff)
            backoff *= 2
            continue
        if r.status_code == 200:
            p.write_text(r.text, encoding="utf-8")
            return r.text
        if r.status_code == 404:
            return None
        if r.status_code in (429, 503):
            print(f"    HTTP {r.status_code}; sleeping {backoff:.0f}s", flush=True)
            time.sleep(backoff)
            backoff *= 2
            continue
        print(f"    HTTP {r.status_code} for {url}", flush=True)
        return None
    return None


# ---------------------------------------------------------------------------

def normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"\s*\(captain\)\s*", " ", s)
    s = re.sub(r"\s*\(vice-?captain\)\s*", " ", s)
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"[.'`’\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_title_index() -> dict[str, str]:
    if TITLE_INDEX_PATH.exists():
        idx = json.loads(TITLE_INDEX_PATH.read_text(encoding="utf-8"))
        print(f"Loaded squad title index ({len(idx)} entries) from cache")
        return idx

    valid = set(NATION_TO_WIKI_HEADING.values())
    index: dict[str, str] = {}

    for url in SQUAD_PAGES:
        print(f"Indexing {url}", flush=True)
        html = fetch_html(url)
        if not html:
            print("  -> no HTML, skipping")
            continue
        soup = BeautifulSoup(html, "lxml")
        for h3 in soup.find_all(["h3", "h4"]):
            heading = re.sub(r"\[edit\]$", "", h3.get_text(strip=True)).strip()
            if heading not in valid:
                continue
            table = h3.find_next("table", class_="wikitable")
            if table is None:
                continue
            count = 0
            for tr in table.find_all("tr"):
                cells = tr.find_all(["td", "th"])
                if len(cells) < 3:
                    continue
                name_cell = cells[2]
                link = name_cell.find("a")
                if link is None:
                    continue
                href = link.get("href", "")
                if not href.startswith("/wiki/") or "redlink" in href:
                    continue
                title = unquote(href[len("/wiki/"):]).replace("_", " ")
                if ":" in title:
                    continue
                raw_name = link.get_text(" ", strip=True)
                key = f"{heading}|{normalize(raw_name)}"
                index.setdefault(key, title)
                count += 1
            if count:
                print(f"  {heading}: {count} players indexed", flush=True)

    TITLE_INDEX_PATH.write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote squad title index ({len(index)} entries)")
    return index


# ---------------------------------------------------------------------------

def parse_year_range(text: str) -> tuple[int | None, int | None]:
    text = text.replace("\u2013", "-").replace("\u2014", "-").strip()
    text = re.sub(r"\[[^\]]*\]", "", text).strip()
    m = re.match(r"^\s*(\d{4})\s*-\s*(\d{2,4})?\s*$", text)
    if m:
        start = int(m.group(1))
        end_raw = m.group(2)
        if end_raw is None:
            return start, None
        end = int(end_raw)
        if end < 100:
            century = start // 100 * 100
            end = century + end
            if end < start:
                end += 100
        return start, end
    m = re.match(r"^\s*(\d{4})\s*$", text)
    if m:
        y = int(m.group(1))
        return y, y
    return None, None


def extract_career_clubs(html: str) -> list[dict] | None:
    soup = BeautifulSoup(html, "lxml")
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return None
    senior_th = None
    for th in infobox.find_all("th"):
        if re.match(r"^Senior career", th.get_text(" ", strip=True), re.IGNORECASE):
            senior_th = th
            break
    if not senior_th:
        return None
    header_row = senior_th.find_parent("tr")
    if not header_row:
        return None

    clubs: list[dict] = []
    sib = header_row
    while True:
        sib = sib.find_next_sibling("tr")
        if sib is None:
            break
        cells = sib.find_all(["td", "th"])
        if not cells:
            continue
        if (
            len(cells) == 1
            and cells[0].name == "th"
            and "career" in cells[0].get_text(strip=True).lower()
        ):
            break
        text_cells = [c.get_text(" ", strip=True) for c in cells]
        if text_cells and text_cells[0].lower().startswith("years"):
            continue
        if len(cells) < 2:
            continue
        years_text, team_text = text_cells[0], text_cells[1]
        if not years_text or not team_text:
            continue
        if "→" in team_text or "(loan)" in team_text.lower():
            continue
        team_clean = re.sub(r"\[[^\]]*\]", "", team_text).strip()
        if team_clean.lower() == "total":
            continue
        start, end = parse_year_range(years_text)
        if start is None:
            continue
        clubs.append({"club": team_clean, "start_year": start, "end_year": end})

    return clubs


# ---------------------------------------------------------------------------

def main() -> int:
    json_paths = [
        REPO_ROOT / "world_cup_players.json",
        REPO_ROOT / "src" / "data" / "world_cup_players.json",
    ]
    primary = json_paths[0]
    if not primary.exists():
        print(f"ERROR: {primary} not found", file=sys.stderr)
        return 1

    data = json.loads(primary.read_text(encoding="utf-8"))
    players = data["players"]

    only = sys.argv[1:] if len(sys.argv) > 1 else None
    if only:
        print(f"Filtering to: {only}")

    index = build_title_index()

    found = 0
    empty = 0
    skipped = 0
    no_link = 0
    failures: list[str] = []

    for idx, p in enumerate(players, 1):
        if only and p["name"] not in only:
            continue
        # Skip players already checked (has a non-null career_clubs).
        if "career_clubs" in p and p["career_clubs"] is not None:
            skipped += 1
            continue

        nat = p.get("nationality", "")
        name = p["name"]
        key = f"{nat}|{normalize(name)}"
        title = index.get(key)

        if not title:
            no_link += 1
            p["career_clubs"] = []
            failures.append(f"{name} ({nat}) - no squad link")
            print(
                f"  [{idx:3d}/{len(players)}] {name:30s} -> no squad link",
                flush=True,
            )
            continue

        html = fetch_html(title)
        clubs = extract_career_clubs(html) if html else None

        if clubs:
            p["career_clubs"] = clubs
            found += 1
            print(
                f"  [{idx:3d}/{len(players)}] {name:30s} -> "
                f"{len(clubs)} clubs (via '{title}')",
                flush=True,
            )
        else:
            p["career_clubs"] = []
            empty += 1
            failures.append(f"{name} ({nat}) - '{title}' had no senior table")
            print(
                f"  [{idx:3d}/{len(players)}] {name:30s} -> "
                f"no senior career in '{title}'",
                flush=True,
            )

        if idx % 20 == 0:
            for path in json_paths:
                path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

    for path in json_paths:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  wrote {path}")

    print()
    print(f"Found career clubs:    {found}")
    print(f"Article had no table:  {empty}")
    print(f"No squad link at all:  {no_link}")
    print(f"Already checked:       {skipped}")
    if failures:
        print()
        print("Failures (manual review):")
        for f in failures[:100]:
            print(f"  - {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
