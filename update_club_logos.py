"""
update_club_logos.py

For every unique club referenced by world_cup_players.json, fetch its
Wikipedia page crest and write a name -> public path mapping.

Approach:
  1. Collect unique club names from both world_cups[].club and
     career_clubs[].club.
  2. For each club, try a small set of candidate Wikipedia titles
     (variant order: as-is, "{name} F.C.", "FC {name}", and a couple of
     punctuation variants) against the REST summary endpoint at
     /api/rest_v1/page/summary/{title}, which DOES return crests for
     fair-use images.
  3. Validate the result is actually a football club (description
     contains "football club"/"soccer club"/etc., or title carries an
     unambiguous footy marker).
  4. Download the thumbnail into public/club_logos/{slug}.png and emit
     club_logos.json (root + src/data) mapping the original club name to
     the public URL.

Idempotent: title resolutions cached in cache/club_titles.json, image
files reused if already present.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote, urlparse, unquote

import requests


REPO_ROOT = Path(__file__).resolve().parent
DATA_PATH = REPO_ROOT / "world_cup_players.json"
LINEUPS_PATH = REPO_ROOT / "src" / "data" / "lineups.json"
JSON_OUTPUTS = [
    REPO_ROOT / "src" / "data" / "club_logos.json",
    REPO_ROOT / "club_logos.json",
]
LOGOS_DIR = REPO_ROOT / "public" / "club_logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)
TITLE_CACHE = REPO_ROOT / "cache" / "club_titles.json"
TITLE_CACHE.parent.mkdir(parents=True, exist_ok=True)

UA = "PlayerPassportBot/1.0 (private hobby; runs once to assemble crests)"
RATE_LIMIT_S = 1.0
MAX_429_WAIT = 30  # cap honored Retry-After to keep the script moving
# Clubs that are placeholders, not real teams.
SKIP_CLUBS = {"Without Club", ""}

session = requests.Session()
session.headers.update({"User-Agent": UA, "Api-User-Agent": UA})
_last_call = 0.0

FOOTY_TITLE_RE = re.compile(
    r"\b(F\.?C\.?|CF|SC|AC|A\.S\.|AFC|AS|BV|VfB|VfL|SSC|S\.S\.C\.|TSV|FSV|"
    r"SpVgg|RSC|RC|UD|CD|Atletico|Athletic|United|City)\b",
    re.IGNORECASE,
)
FOOTY_DESC_TOKENS = (
    "football club",
    "soccer club",
    "football team",
    "soccer team",
    "association football",
    "professional football",
    "sports club",
    "sport club",
    "footballing",
)

# Manual Wikipedia title overrides for clubs whose informal name doesn't
# resolve via the candidate-generation heuristics. Tried first, before
# any other variants. Names match the strings used in lineups.json /
# world_cup_players.json.
MANUAL_TITLES: dict[str, str] = {
    "AEK Larnaca": "AEK Larnaca FC",
    "APOEL": "APOEL FC",
    "Akron Tolyatti": "FC Akron Tolyatti",
    "Al Ahly": "Al Ahly SC",
    "Al Bataeh": "Al Bataeh Club",
    "Al Dhafra": "Al Dhafra FC",
    "Al Nasr": "Al Nasr SC (Dubai)",
    "Al-Ahli": "Al-Ahli Saudi FC",
    "Al-Faisaly": "Al-Faisaly FC",
    "Al-Fateh": "Al-Fateh SC",
    "Al-Hussein": "Al-Hussein SC (Irbid)",
    "Al-Karma": "Al-Karma SC",
    "Al-Qadsiah": "Al-Qadsiah FC",
    "Al-Sadd": "Al Sadd SC",
    "Al-Sailiya": "Al-Sailiya SC",
    "Al-Talaba": "Al-Talaba SC",
    "Al-Wakrah": "Al-Wakrah SC",
    "Al-Zawraa": "Al-Zawraa SC",
    "Angers": "Angers SCO",
    "Antwerp": "Royal Antwerp F.C.",
    "Apollon Limassol": "Apollon Limassol FC",
    "Astana": "FC Astana",
    "Atlanta United FC": "Atlanta United FC",
    "Atromitos": "Atromitos F.C.",
    "Auckland FC": "Auckland FC",
    "Bodø/Glimt": "FK Bodø/Glimt",
    "Brøndby": "Brøndby IF",
    "Castellón": "CD Castellón",
    "Charlton Athletic": "Charlton Athletic F.C.",
    "Chaves": "G.D. Chaves",
    "Club Africain": "Club Africain",
    "Club Brugge": "Club Brugge KV",
    "Cremonese": "U.S. Cremonese",
    "Dender": "F.C.V. Dender E.H.",
    "Derby County": "Derby County F.C.",
    "Dibba": "Dibba Al-Hisn SC",
    "Dinamo Samarqand": "FC Dinamo Samarqand",
    "Dynamo Makhachkala": "FC Dynamo Makhachkala",
    "El Paso Locomotive FC": "El Paso Locomotive FC",
    "Elche": "Elche CF",
    "Espérance de Tunis": "Espérance Sportive de Tunis",
    "Estrela Amadora": "C.F. Estrela da Amadora",
    "FC Augsburg": "FC Augsburg",
    "FC Dallas": "FC Dallas",
    "FC St. Pauli": "FC St. Pauli",
    "FCSB": "FCSB",
    "Gangwon FC": "Gangwon FC",
    "Gaziantep": "Gaziantep F.K.",
    "Gil Vicente": "Gil Vicente F.C.",
    "Girona": "Girona FC",
    "Grazer AK": "Grazer AK",
    "Guadalajara": "C.D. Guadalajara",
    "Heart of Midlothian": "Heart of Midlothian F.C.",
    "Heracles Almelo": "Heracles Almelo",
    "Hibernian": "Hibernian F.C.",
    "Hradec Králové": "FC Hradec Králové",
    "Huracán": "Club Atlético Huracán",
    "Ironi Kiryat Shmona": "Hapoel Ironi Kiryat Shmona F.C.",
    "Iğdır": "Iğdır F.K.",
    "JS Kabylie": "JS Kabylie",
    "Jagiellonia Białystok": "Jagiellonia Białystok",
    "Juárez": "FC Juárez",
    "Kashima Antlers": "Kashima Antlers",
    "Kasımpaşa": "Kasımpaşa S.K.",
    "Kifisia": "Kifisia F.C.",
    "Le Havre": "Le Havre AC",
    "Levante": "Levante UD",
    "Maccabi Haifa": "Maccabi Haifa F.C.",
    "Mamelodi Sundowns": "Mamelodi Sundowns F.C.",
    "Maribor": "NK Maribor",
    "Mazatlán": "Mazatlán F.C.",
    "Miami FC": "Miami FC",
    "Motherwell": "Motherwell F.C.",
    "Nashville SC": "Nashville SC",
    "Navbahor Namangan": "Navbahor Namangan",
    "Neftchi Fergana": "Neftchi Fergana",
    "New York City FC": "New York City FC",
    "Nice": "OGC Nice",
    "Nordsjælland": "FC Nordsjælland",
    "Orlando Pirates": "Orlando Pirates F.C.",
    "Oviedo": "Real Oviedo",
    "PEC Zwolle": "PEC Zwolle",
    "Pafos": "Pafos FC",
    "Pakhtakor": "Pakhtakor Tashkent FK",
    "Pari Nizhny Novgorod": "FC Pari Nizhny Novgorod",
    "Persepolis": "Persepolis F.C.",
    "Peterborough United": "Peterborough United F.C.",
    "Philadelphia Union": "Philadelphia Union",
    "Pogoń Szczecin": "Pogoń Szczecin",
    "Polokwane City": "Polokwane City F.C.",
    "Port": "Port F.C.",
    "Pyramids": "Pyramids FC",
    "RKC Waalwijk": "RKC Waalwijk",
    "Raja Casablanca": "Raja CA",
    "Real Betis": "Real Betis",
    "River Plate": "Club Atlético River Plate",
    "Santos": "Santos FC",
    "Saprissa": "Deportivo Saprissa",
    "Sassuolo": "U.S. Sassuolo Calcio",
    "Selangor": "Selangor F.C.",
    "Sepahan": "Sepahan S.C.",
    "Shamrock Rovers": "Shamrock Rovers F.C.",
    "Sheffield United": "Sheffield United F.C.",
    "Slavia Prague": "SK Slavia Prague",
    "Slovan Bratislava": "ŠK Slovan Bratislava",
    "Sparta Prague": "AC Sparta Prague",
    "Spartak Moscow": "FC Spartak Moscow",
    "St. Gallen": "FC St. Gallen",
    "Stade Nyonnais": "Stade Nyonnais FC",
    "Strasbourg": "RC Strasbourg Alsace",
    "Toluca": "Deportivo Toluca F.C.",
    "Torreense": "S.C.U. Torreense",
    "Tractor": "Tractor S.C.",
    "USM Alger": "USM Alger",
    "Union Saint-Gilloise": "Royale Union Saint-Gilloise",
    "Viking": "Viking FK",
    "Viktoria Plzeň": "FC Viktoria Plzeň",
    "Volendam": "FC Volendam",
    "Wellington Phoenix": "Wellington Phoenix FC",
    "Werder Bremen": "SV Werder Bremen",
    "West Ham United": "West Ham United F.C.",
    "Widzew Łódź": "Widzew Łódź",
    "Young Boys": "BSC Young Boys",
    "Zamalek": "Zamalek SC",
    "Zürich": "FC Zürich",
    "Çaykur Rizespor": "Çaykur Rizespor",
}


def _rate_limit() -> None:
    global _last_call
    delta = time.time() - _last_call
    if delta < RATE_LIMIT_S:
        time.sleep(RATE_LIMIT_S - delta)
    _last_call = time.time()


def get(url: str, *, max_retries: int = 4, timeout: int = 30) -> requests.Response | None:
    attempt = 0
    while attempt < max_retries:
        _rate_limit()
        try:
            r = session.get(url, timeout=timeout)
        except requests.RequestException as e:
            print(f"   ! {e}; retry {attempt + 1}")
            time.sleep(2 ** attempt)
            attempt += 1
            continue
        if r.status_code == 429:
            wait = min(int(r.headers.get("Retry-After", "5")), MAX_429_WAIT)
            print(f"   429 backoff {wait}s")
            time.sleep(wait)
            continue
        if 500 <= r.status_code < 600:
            time.sleep(2 ** attempt)
            attempt += 1
            continue
        return r
    return None


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or hashlib.md5((s or "x").encode()).hexdigest()[:8]


def collect_clubs(players: list[dict]) -> list[str]:
    s: set[str] = set()
    for p in players:
        for w in p.get("world_cups") or []:
            club = (w.get("club") or "").strip()
            if club and club not in SKIP_CLUBS:
                s.add(club)
        for c in p.get("career_clubs") or []:
            club = (c.get("club") or "").strip()
            if club and club not in SKIP_CLUBS:
                s.add(club)
    if LINEUPS_PATH.exists():
        lineups = json.loads(LINEUPS_PATH.read_text(encoding="utf-8"))
        for t in lineups.get("teams") or []:
            for p in (t.get("players") or []) + (t.get("bench") or []):
                club = (p.get("club") or "").strip()
                if club and club not in SKIP_CLUBS:
                    s.add(club)
    return sorted(s)


def title_candidates(name: str) -> list[str]:
    """Likely Wikipedia article titles for a club, in priority order."""
    out: list[str] = []
    seen: set[str] = set()

    def add(t: str) -> None:
        t = re.sub(r"\s+", " ", t).strip()
        if t and t not in seen:
            seen.add(t)
            out.append(t)

    # Manual override always wins.
    if name in MANUAL_TITLES:
        add(MANUAL_TITLES[name])

    has_marker = bool(FOOTY_TITLE_RE.search(name))

    if has_marker:
        add(name)
        add(re.sub(r"\bFC\b", "F.C.", name))
        add(re.sub(r"\bF\.C\.", "FC", name))
    else:
        add(f"{name} F.C.")
        add(f"FC {name}")
        # Bare name (could resolve via redirects to e.g. RSC Anderlecht)
        add(name)
        # Disambiguator parenthetical for clubs like "Banfield (football club)"
        add(f"{name} (football club)")

    return out[:6]


def fetch_summary(title: str) -> dict | None:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}"
    r = get(url)
    if not r or r.status_code != 200:
        return None
    try:
        return r.json()
    except Exception:
        return None


def opensearch_titles(query: str, limit: int = 5) -> list[str]:
    """Wikipedia OpenSearch — returns candidate article titles for query."""
    url = (
        "https://en.wikipedia.org/w/api.php?action=opensearch&format=json"
        f"&limit={limit}&search={quote(query)}"
    )
    r = get(url)
    if not r or r.status_code != 200:
        return []
    try:
        data = r.json()
        return list(data[1] or [])
    except Exception:
        return []


def is_club(summary: dict) -> bool:
    desc = (summary.get("description") or "").lower()
    if any(tok in desc for tok in FOOTY_DESC_TOKENS):
        return True
    title = summary.get("title", "")
    if FOOTY_TITLE_RE.search(title):
        if not re.search(r"\b(city|town|village|comune|capital|municipality)\b", desc):
            return True
    return False


def _try_summary(title: str, *, trusted: bool = False) -> dict | None:
    summ = fetch_summary(title)
    if not summ or summ.get("type") == "disambiguation":
        return None
    if not trusted and not is_club(summ):
        return None
    thumb = (summ.get("thumbnail") or {}).get("source")
    orig = (summ.get("originalimage") or {}).get("source")
    url = thumb or orig
    if not url:
        return None
    return {
        "title": summ.get("title"),
        "thumb": url,
        "description": summ.get("description"),
    }


def _name_matches_title(name: str, title: str) -> bool:
    """Sanity check: returned title shares a meaningful token with the query."""
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
    name_tokens = {t for t in norm(name).split() if len(t) >= 3}
    title_norm = norm(title)
    if not name_tokens:
        return name.lower() in title.lower()
    return any(t in title_norm for t in name_tokens)


def resolve_club(name: str) -> dict | None:
    """Return summary dict for the article representing this club, else None."""
    manual = MANUAL_TITLES.get(name)
    if manual:
        info = _try_summary(manual, trusted=True)
        if info:
            return info
    for cand in title_candidates(name):
        if cand == manual:
            continue  # already tried as trusted
        info = _try_summary(cand)
        if info:
            return info
    # Fallback: opensearch — try multiple queries, then deeper bare-name list
    seen_titles: set[str] = set()
    queries = [f"{name} football club", f"{name} club", f"{name} FC", name]
    for query in queries:
        for cand in opensearch_titles(query, limit=10):
            if cand in seen_titles:
                continue
            seen_titles.add(cand)
            if not _name_matches_title(name, cand):
                continue
            info = _try_summary(cand)
            if info:
                return info
    return None


def ext_from_url(url: str) -> str:
    path = urlparse(url).path
    name = unquote(path.rsplit("/", 1)[-1])
    m = re.search(r"\.(png|jpg|jpeg|gif|webp)$", name, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return "png"


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    r = get(url)
    if not r or r.status_code != 200:
        return False
    dest.write_bytes(r.content)
    return True


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    clubs = collect_clubs(data["players"])
    print(f"Unique clubs: {len(clubs)}")

    title_cache: dict[str, dict] = {}
    if TITLE_CACHE.exists():
        title_cache = json.loads(TITLE_CACHE.read_text(encoding="utf-8"))

    only = [a for a in sys.argv[1:] if not a.startswith("--")] or None
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    skip_uncached = "--no-retry-failures" in flags
    if only:
        clubs = [c for c in clubs if c in only]
        print(f"Filtered to {len(clubs)} clubs")

    resolved: dict[str, dict] = {}
    failures: list[str] = []

    for i, club in enumerate(clubs, 1):
        cached = title_cache.get(club)
        if cached and cached.get("thumb"):
            resolved[club] = cached
            continue
        if skip_uncached:
            failures.append(club)
            continue
        info = resolve_club(club)
        if info:
            resolved[club] = info
            title_cache[club] = info
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> {info['title']!r}")
        else:
            failures.append(club)
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> NO MATCH")
        if i % 20 == 0:
            TITLE_CACHE.write_text(
                json.dumps(title_cache, indent=2, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

    TITLE_CACHE.write_text(
        json.dumps(title_cache, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )

    print(f"\nResolved: {len(resolved)} / {len(clubs)}")
    if failures:
        print(f"Unresolved ({len(failures)}):")
        for c in failures[:30]:
            print(f"  - {c}")
        if len(failures) > 30:
            print(f"  … and {len(failures) - 30} more")

    # Download. Reuse files for clubs that point to the same thumbnail URL.
    logos: dict[str, str] = {}
    url_to_path: dict[str, str] = {}
    succ = 0
    fail = 0

    def write_logos() -> None:
        for path in JSON_OUTPUTS:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(logos, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )

    for i, (club, info) in enumerate(sorted(resolved.items()), 1):
        thumb = info["thumb"]
        if thumb in url_to_path:
            logos[club] = url_to_path[thumb]
            continue
        slug = slugify(club)
        ext = ext_from_url(thumb)
        existing = sorted(LOGOS_DIR.glob(f"{slug}.*"))
        if existing:
            rel = f"/club_logos/{existing[0].name}"
            logos[club] = rel
            url_to_path[thumb] = rel
            succ += 1
            continue
        dest = LOGOS_DIR / f"{slug}.{ext}"
        if download(thumb, dest):
            rel = f"/club_logos/{dest.name}"
            logos[club] = rel
            url_to_path[thumb] = rel
            succ += 1
            if i % 25 == 0:
                print(f"  downloaded {i}/{len(resolved)}", flush=True)
                write_logos()
        else:
            fail += 1
            print(f"  ! download failed for {club} ({thumb})")

    write_logos()
    for path in JSON_OUTPUTS:
        print(f"Wrote {path}")

    print(f"\nLogos saved: {succ} | Download failures: {fail} | Unresolved clubs: {len(failures)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

