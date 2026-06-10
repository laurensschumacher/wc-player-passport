"""
Transfermarkt data fetcher for World Cup player data.

Primary data source: TM internal JSON API (tmapi.transfermarkt.technology)
  - /player/{id}/performance-game  -> per-game stats; filter competitionId=='FIWC'
  - /club/{id}                     -> club name lookup

Secondary: TM profile page (static HTML) for identity validation.

All API responses cached on disk to avoid re-fetching.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
from collections import Counter
from typing import Optional

import cloudscraper
from bs4 import BeautifulSoup
import requests as _requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://www.transfermarkt.com"
API_BASE = "https://tmapi.transfermarkt.technology"

HEADERS_HTML = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Referer": "https://www.transfermarkt.com/",
    "DNT": "1",
}

HEADERS_API = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.transfermarkt.com",
    "Referer": "https://www.transfermarkt.com/",
    "DNT": "1",
}

WC_YEARS = [2002, 2006, 2010, 2014, 2018, 2022, 2026]

# TM season ID -> FIFA World Cup year
# Season 2001 = 2001/02 season, contains 2002 WC (Jun-Jul 2002)
# Season 2025 = 2025/26 season, contains 2026 WC (Jun-Jul 2026)
SEASON_TO_WC: dict[int, int] = {
    2001: 2002,
    2005: 2006,
    2009: 2010,
    2013: 2014,
    2017: 2018,
    2021: 2022,
    2025: 2026,
}

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# In-memory caches
# ---------------------------------------------------------------------------

_club_name_cache: dict[int, str] = {}

# ---------------------------------------------------------------------------
# HTTP: HTML pages (cloudscraper, bypasses Cloudflare)
# ---------------------------------------------------------------------------

_scraper: Optional[cloudscraper.CloudScraper] = None


def _get_scraper() -> cloudscraper.CloudScraper:
    global _scraper
    if _scraper is None:
        _scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        _scraper.headers.update(HEADERS_HTML)
    return _scraper


def _html_cache_path(url: str) -> str:
    key = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{key}.html")


def fetch(url: str, *, force: bool = False) -> Optional[str]:
    """Fetch *url* (HTML) with on-disk caching and polite delay."""
    path = _html_cache_path(url)
    if not force and os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()

    delay = 0.8 + random.random() * 0.7
    time.sleep(delay)

    sc = _get_scraper()
    try:
        resp = sc.get(url, timeout=20)
    except Exception as exc:
        print(f"  [NET ERROR] {url}: {exc}")
        return None

    if resp.status_code == 403:
        print(f"  [403] {url} -- retrying after extra delay ...")
        time.sleep(5 + random.random() * 3)
        try:
            resp = sc.get(url, timeout=20)
        except Exception as exc2:
            print(f"  [NET ERROR on retry] {url}: {exc2}")
            return None

    if resp.status_code != 200:
        print(f"  [HTTP {resp.status_code}] {url}")
        return None

    html = resp.text
    with open(path, "w", encoding="utf-8", errors="replace") as fh:
        fh.write(html)
    return html


# ---------------------------------------------------------------------------
# HTTP: JSON API (plain requests, no Cloudflare needed)
# ---------------------------------------------------------------------------

_api_session = _requests.Session()
_api_session.headers.update(HEADERS_API)


def _api_cache_path(url: str) -> str:
    key = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{key}.json")


def fetch_api(path: str, *, force: bool = False) -> Optional[dict]:
    """Fetch a JSON endpoint from the TM internal API with caching."""
    url = f"{API_BASE}{path}"
    cache_path = _api_cache_path(url)

    if not force and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    delay = 0.3 + random.random() * 0.3
    time.sleep(delay)

    try:
        resp = _api_session.get(url, timeout=20)
    except Exception as exc:
        print(f"  [API NET ERROR] {url}: {exc}")
        return None

    if resp.status_code != 200:
        print(f"  [API HTTP {resp.status_code}] {url}")
        return None

    data = resp.json()
    with open(cache_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return data


# ---------------------------------------------------------------------------
# Player identity check via API profile
# ---------------------------------------------------------------------------

def fetch_player_api_name(tm_id: int) -> Optional[str]:
    """Return the canonical name TM has for *tm_id*, or None on failure."""
    data = fetch_api(f"/player/{tm_id}")
    if not data or not data.get("success"):
        return None
    pdata = data.get("data", {}) or {}
    # Prefer the longest of the available name fields
    for key in ("name", "displayName", "shortName", "artistName"):
        v = pdata.get(key)
        if v:
            return v
    return None


def player_id_matches_candidate(tm_id: int, expected_name: str) -> bool:
    """Return True iff the TM profile at *tm_id* plausibly matches *expected_name*.

    Match rule (lenient enough to handle mononyms like "Ronaldo" vs "Ronaldo
    Nazario", and strict enough to reject "Per Karlsson" vs "Thierry Henry"):
    after lowercasing + accent stripping, any token of length >= 4 from one
    name must appear as a substring of the other.
    """
    tm_name = fetch_player_api_name(tm_id)
    if not tm_name:
        return False
    norm_tm = _normalise(tm_name)
    norm_exp = _normalise(expected_name)
    if not norm_exp or not norm_tm:
        return False
    tm_tokens = [t for t in norm_tm.split() if len(t) >= 4]
    exp_tokens = [t for t in norm_exp.split() if len(t) >= 4]
    for t in exp_tokens:
        if t in norm_tm:
            return True
    for t in tm_tokens:
        if t in norm_exp:
            return True
    return False


# ---------------------------------------------------------------------------
# Club name lookup
# ---------------------------------------------------------------------------

def fetch_club_name(club_id: int, *, force: bool = False) -> str:
    """Return the English club name for *club_id* from TM API."""
    if club_id in _club_name_cache and not force:
        return _club_name_cache[club_id]

    data = fetch_api(f"/club/{club_id}", force=force)
    if data and data.get("success") and data.get("data"):
        name = data["data"].get("name") or data["data"].get("baseDetails", {}).get("shortName", "")
        if name:
            _club_name_cache[club_id] = name
            return name

    fallback = f"Club#{club_id}"
    _club_name_cache[club_id] = fallback
    return fallback


# ---------------------------------------------------------------------------
# World Cup stats via TM performance-game API
# ---------------------------------------------------------------------------

def fetch_wc_stats(tm_id: int, *, force: bool = False) -> dict[int, dict]:
    """Fetch per-tournament World Cup stats for a player.

    Returns dict keyed by WC year:
      {
        2022: {"games": 7, "goals": 7, "club_id": 583, "club": "Paris Saint-Germain"},
        2018: {"games": 4, "goals": 1, "club_id": 131, "club": "FC Barcelona"},
        ...
      }

    Only tournaments where the player has at least 1 FIWC game record are included.
    """
    data = fetch_api(f"/player/{tm_id}/performance-game", force=force)
    if not data or not data.get("success"):
        return {}

    performances = data.get("data", {}).get("performance", [])
    if not performances:
        return {}

    # Group FIWC games by WC year.
    # participationState values seen in the TM API:
    #   "played"        -- player got minutes on the pitch
    #   "in squad"      -- on the matchday bench, did not enter
    #   "injured"       -- in the tournament squad but injured for this game
    #   "absent"        -- in the tournament squad but unavailable (suspension etc.)
    #   "not in squad"  -- not in matchday squad (ambiguous; may or may not be in tournament squad)
    # We count played / in-squad / injured / absent as a WC appearance, but
    # only "played" entries count for the games stat.
    SQUAD_STATES = {"played", "in squad", "injured", "absent"}
    wc_played: dict[int, list[dict]] = {}
    wc_in_squad: dict[int, list[dict]] = {}
    for perf in performances:
        gi = perf.get("gameInformation", {})
        if gi.get("competitionId") != "FIWC":
            continue
        season_id = gi.get("seasonId")
        wc_year = SEASON_TO_WC.get(season_id)
        if wc_year is None:
            continue
        state = perf.get("statistics", {}).get("generalStatistics", {}).get("participationState")
        if state == "played":
            wc_played.setdefault(wc_year, []).append(perf)
        elif state in SQUAD_STATES:
            wc_in_squad.setdefault(wc_year, []).append(perf)
        # "not in squad" and unknown states: skip

    # All WC years where player was at least in the tournament squad
    wc_years = set(wc_played) | set(wc_in_squad)
    wc_games = {y: wc_played.get(y, []) + wc_in_squad.get(y, []) for y in wc_years}

    # Compute stats per WC year
    result: dict[int, dict] = {}
    for wc_year in wc_years:
        played_games = wc_played.get(wc_year, [])
        all_games = wc_games[wc_year]

        # games = matches the player actually got minutes in
        total_games = len(played_games)
        total_goals = 0
        for g in played_games:
            gs = g.get("statistics", {}).get("goalStatistics", {})
            goals = gs.get("goalsScoredTotal") or 0
            total_goals += goals

        # Club from any entry (squad membership), prefer played-game data
        club_id_counter: Counter = Counter()
        for g in all_games:
            club_id = g.get("statistics", {}).get("generalStatistics", {}).get("primaryClubId")
            if club_id:
                club_id_counter[club_id] += 1

        # Most common club during that WC
        primary_club_id = club_id_counter.most_common(1)[0][0] if club_id_counter else None
        club_name = fetch_club_name(primary_club_id) if primary_club_id else "Unknown"

        result[wc_year] = {
            "games": total_games,
            "goals": total_goals,
            "club_id": primary_club_id,
            "club": club_name,
        }

    return result


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------

def profile_url(slug: str, tm_id: int) -> str:
    return f"{BASE_URL}/{slug}/profil/spieler/{tm_id}"


# ---------------------------------------------------------------------------
# Parser: player identity check (from static profile page)
# ---------------------------------------------------------------------------

def _normalise(text: str) -> str:
    """Lower-case, strip accents & punctuation for fuzzy name matching."""
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9 ]", "", ascii_str.lower()).strip()


def validate_player_identity(
    html: str, expected_name: str, expected_nationality: str
) -> tuple[bool, str]:
    """Check that the fetched profile page belongs to the expected player."""
    soup = BeautifulSoup(html, "lxml")

    name_tag = (
        soup.find("h1", class_=re.compile(r"data-header__headline"))
        or soup.find("h1", {"itemprop": "name"})
        or soup.find("h1")
    )
    if name_tag is None:
        return False, "Player name header not found on page"

    page_name = _normalise(name_tag.get_text(" ", strip=True))
    exp_name = _normalise(expected_name)

    last_token = exp_name.split()[-1]
    if last_token not in page_name and exp_name not in page_name:
        return False, f"Name mismatch: page has '{page_name}', expected '{exp_name}'"

    return True, "ok"


# ---------------------------------------------------------------------------
# Parser: player position from profile
# ---------------------------------------------------------------------------

_POSITION_MAP = {
    "goalkeeper": "gk",
    "keeper": "gk",
    "centre-back": "defender",
    "center-back": "defender",
    "central defence": "defender",
    "left-back": "defender",
    "right-back": "defender",
    "defender": "defender",
    "defence": "defender",
    "sweeper": "defender",
    "defensive midfield": "midfielder",
    "central midfield": "midfielder",
    "attacking midfield": "midfielder",
    "left midfield": "midfielder",
    "right midfield": "midfielder",
    "midfield": "midfielder",
    "second striker": "attacker",
    "centre-forward": "attacker",
    "center-forward": "attacker",
    "left winger": "attacker",
    "right winger": "attacker",
    "winger": "attacker",
    "forward": "attacker",
    "striker": "attacker",
    "attack": "attacker",
}


def extract_position(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["dd", "span", "td", "li"]):
        text = tag.get_text(" ", strip=True).lower()
        for key, val in _POSITION_MAP.items():
            if key in text:
                return val
    return None


# ---------------------------------------------------------------------------
# TM player search (fallback for wrong / missing IDs)
# ---------------------------------------------------------------------------

def search_tm_player(name: str) -> list[tuple[str, int]]:
    """Search TM for *name* and return a list of (slug, tm_id) candidates.

    Tries several query variants so hyphenated and ordered names (e.g.
    Korean "Son Heung-min" -> TM's "Heung-Min Son") still find a match.
    Results from later variants are appended if not already seen.
    """
    seen: set[int] = set()
    result: list[tuple[str, int]] = []

    queries: list[str] = [name]
    # If name contains a hyphen, also try the "given-name last" swap that TM uses
    if "-" in name:
        tokens = name.split()
        if len(tokens) == 2:
            # "Son Heung-min" -> "Heung-min Son", and also accent-free "Heung-Min Son"
            queries.append(f"{tokens[1]} {tokens[0]}")
            queries.append(f"{tokens[1].title()} {tokens[0]}")
    # Last-token-only fallback for unusual orderings
    queries.append(name.split()[-1])

    for q in queries:
        query = q.replace(" ", "+")
        url = (
            f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche"
            f"?query={query}&x=0&y=0"
        )
        html = fetch(url)
        if not html:
            continue
        matches = re.findall(r'href="/([-a-z0-9]+)/profil/spieler/(\d+)"', html)
        for slug, pid_str in matches:
            pid = int(pid_str)
            if pid not in seen:
                seen.add(pid)
                result.append((slug, pid))
        if result:
            # Stop trying further variants once we have at least one hit
            break
    return result


# ---------------------------------------------------------------------------
# High-level: scrape one candidate
# ---------------------------------------------------------------------------

def scrape_candidate(candidate: dict, wiki_2026: dict) -> dict:
    """Fetch and validate one candidate.

    Returns a result dict with:
      status   "validated" | "needs_manual_review" | "disqualified"
      data     (if validated) -- the player dict
      review_entry  (if needs_manual_review or disqualified)
      reason   (if disqualified)
    """
    name = candidate["name"]
    slug = candidate["tm_slug"]
    tm_id = candidate["tm_id"]
    prof_url = profile_url(slug, tm_id)

    print(f"  Scraping: {name} ({candidate['code']}) ...")

    # --- 1. Fetch WC stats from API (with identity check + search fallback) ---
    # We trust the original tm_id only if BOTH:
    #   (a) the API profile name matches the candidate's name, AND
    #   (b) the player has at least 1 FIWC game record in our WC year range.
    # Otherwise we search TM and try the top results.
    wc_stats: dict[int, dict] = {}
    identity_ok = player_id_matches_candidate(tm_id, name)
    if identity_ok:
        wc_stats = fetch_wc_stats(tm_id)

    if not identity_ok or not wc_stats:
        candidates_found = search_tm_player(name)
        for s_slug, s_id in candidates_found[:5]:
            if s_id == tm_id and identity_ok:
                continue  # already tried
            if not player_id_matches_candidate(s_id, name):
                continue
            s_stats = fetch_wc_stats(s_id)
            if s_stats:
                if s_id != tm_id:
                    print(f"    [search fix] {name}: corrected ID {tm_id} -> {s_id}")
                tm_id = s_id
                slug = s_slug
                prof_url = profile_url(slug, tm_id)
                wc_stats = s_stats
                break
        else:
            return _review(name, prof_url, "No FIWC game records found -- wrong TM ID or player never had WC data")

    # --- 2. Check eligibility: >=2 WCs as part of a tournament squad ---
    # wc_stats contains every WC the player was in the matchday squad for
    # (played OR on bench). All entries qualify as a WC appearance.
    wcs_appeared = dict(wc_stats)

    if len(wcs_appeared) < 2:
        # Check if they're in 2026 squad (tournament just started)
        norm_name = _normalise(name)
        in_2026_squad = norm_name in wiki_2026
        has_2026_fiwc = 2026 in wc_stats

        if len(wcs_appeared) == 1 and (in_2026_squad or has_2026_fiwc):
            # Accept: 1 past WC + 2026 squad membership (games may accumulate)
            wcs_appeared[2026] = wc_stats.get(
                2026,
                {"games": 0, "goals": 0, "club_id": None, "club": "Unknown"}
            )
        else:
            n = len(wcs_appeared)
            return {
                "status": "disqualified",
                "reason": f"Only {n} WC(s) in tournament squad (needs >=2)",
                "review_entry": {
                    "name": name,
                    "transfermarkt_url": prof_url,
                    "reason": f"Only {n} WC(s) in tournament squad",
                },
            }

    # --- 3. Build world_cups list (use position from candidates.py) ---
    _POSITION_MAP = {
        "goalkeeper": "GK", "gk": "GK",
        "defender": "DEF", "def": "DEF",
        "midfielder": "MID", "mid": "MID",
        "attacker": "ATT", "att": "ATT", "forward": "ATT",
    }
    raw_pos = candidate["position"].lower()
    position = _POSITION_MAP.get(raw_pos, raw_pos.upper())

    world_cups = []
    for yr in sorted(wcs_appeared.keys()):
        s = wcs_appeared[yr]
        world_cups.append({
            "year": yr,
            "games": s["games"],
            "goals": s["goals"],
            "club": s["club"],
        })

    player_id = f"{slug}-{candidate['code'].lower()}"

    data = {
        "id": player_id,
        "name": name,
        "nationality": candidate["nationality"],
        "nationality_code": candidate["code"],
        "flag_emoji": candidate["flag"],
        "position": position,
        "transfermarkt_url": prof_url,
        "world_cups": world_cups,
        "validation_status": "validated",
    }

    return {"status": "validated", "data": data}


def _review(name: str, url: str, reason: str) -> dict:
    return {
        "status": "needs_manual_review",
        "review_entry": {"name": name, "transfermarkt_url": url, "reason": reason},
    }


# ---------------------------------------------------------------------------
# Wikipedia 2026 squad data (fallback for eligibility check)
# ---------------------------------------------------------------------------

WIKI_2026_URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"


def fetch_wiki_2026_squads() -> dict[str, bool]:
    """Return set of normalised player names known to be in a 2026 WC squad."""
    html = fetch(WIKI_2026_URL)
    if not html:
        return {}
    soup = BeautifulSoup(html, "lxml")
    squad_names: dict[str, bool] = {}
    for tag in soup.find_all(["a", "td", "th"]):
        text = tag.get_text(strip=True)
        if 2 < len(text) < 50 and re.match(r"^[A-ZA-O][a-za-o]", text):
            squad_names[_normalise(text)] = True
    return squad_names
