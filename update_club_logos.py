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
JSON_OUTPUTS = [
    REPO_ROOT / "src" / "data" / "club_logos.json",
    REPO_ROOT / "club_logos.json",
]
LOGOS_DIR = REPO_ROOT / "public" / "club_logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)
TITLE_CACHE = REPO_ROOT / "cache" / "club_titles.json"
TITLE_CACHE.parent.mkdir(parents=True, exist_ok=True)

UA = "PlayerPassport/1.0 (private hobby project; contact: local)"
RATE_LIMIT_S = 0.3

session = requests.Session()
session.headers.update({"User-Agent": UA})
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
)


def _rate_limit() -> None:
    global _last_call
    delta = time.time() - _last_call
    if delta < RATE_LIMIT_S:
        time.sleep(RATE_LIMIT_S - delta)
    _last_call = time.time()


def get(url: str, *, max_retries: int = 4, timeout: int = 30) -> requests.Response | None:
    for attempt in range(max_retries):
        _rate_limit()
        try:
            r = session.get(url, timeout=timeout)
        except requests.RequestException as e:
            print(f"   ! {e}; retry {attempt + 1}")
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "5"))
            print(f"   429 backoff {wait}s")
            time.sleep(wait)
            continue
        if 500 <= r.status_code < 600:
            time.sleep(2 ** attempt)
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
            if club:
                s.add(club)
        for c in p.get("career_clubs") or []:
            club = (c.get("club") or "").strip()
            if club:
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

    has_marker = bool(FOOTY_TITLE_RE.search(name))

    # If the name contains "FC ..." or "... FC", that's our strongest signal.
    if has_marker:
        add(name)
        # Try the dotted form
        add(re.sub(r"\bFC\b", "F.C.", name))
        add(re.sub(r"\bF\.C\.", "FC", name))
    else:
        # Add disambiguator suffix/prefix variants
        add(f"{name} F.C.")
        add(f"FC {name}")
        # Last resort: bare name (could be city/country, validated by desc)
        add(name)

    return out[:4]


def fetch_summary(title: str) -> dict | None:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}"
    r = get(url)
    if not r or r.status_code != 200:
        return None
    try:
        return r.json()
    except Exception:
        return None


def is_club(summary: dict) -> bool:
    desc = (summary.get("description") or "").lower()
    if any(tok in desc for tok in FOOTY_DESC_TOKENS):
        return True
    title = summary.get("title", "")
    if FOOTY_TITLE_RE.search(title):
        # Title contains a footy marker — still require desc to NOT explicitly
        # say "city"/"town"/"village" to avoid false positives like "AFC Asia".
        if not re.search(r"\b(city|town|village|comune|capital|municipality)\b", desc):
            return True
    return False


def resolve_club(name: str) -> dict | None:
    """Return summary dict for the article representing this club, else None."""
    for cand in title_candidates(name):
        summ = fetch_summary(cand)
        if not summ:
            continue
        if summ.get("type") == "disambiguation":
            continue
        if not is_club(summ):
            continue
        thumb = (summ.get("thumbnail") or {}).get("source")
        orig = (summ.get("originalimage") or {}).get("source")
        url = thumb or orig
        if not url:
            continue
        return {
            "title": summ.get("title"),
            "thumb": url,
            "description": summ.get("description"),
        }
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

    only = sys.argv[1:] if len(sys.argv) > 1 else None
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
        info = resolve_club(club)
        if info:
            resolved[club] = info
            title_cache[club] = info
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> {info['title']!r}")
        else:
            failures.append(club)
            title_cache[club] = {"failed": True}
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
                print(f"  downloaded {i}/{len(resolved)}")
        else:
            fail += 1
            print(f"  ! download failed for {club} ({thumb})")

    for path in JSON_OUTPUTS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(logos, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {path}")

    print(f"\nLogos saved: {succ} | Download failures: {fail} | Unresolved clubs: {len(failures)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

