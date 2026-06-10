"""
update_club_logos.py

Download a logo for every unique club referenced by world_cup_players.json
(both world_cups[].club and career_clubs[].club) and write a name -> public
path mapping the UI can consume.

Strategy:
  1. Resolve each club name to a Wikipedia article title via the MediaWiki
     opensearch API ("{name} football club").
  2. Fetch the article HTML (cached) and pull the first <img> in the infobox.
  3. Download the logo to public/club_logos/{slug}.{ext}.
  4. Emit club_logos.json (root + src/data) mapping
     {"Real Madrid": "/club_logos/real-madrid.png", ...}.

Re-runs are idempotent: cached HTML on disk and existing logos are reused.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

import requests
from bs4 import BeautifulSoup


REPO_ROOT = Path(__file__).resolve().parent
DATA_PATH = REPO_ROOT / "world_cup_players.json"
JSON_OUTPUTS = [
    REPO_ROOT / "src" / "data" / "club_logos.json",
    REPO_ROOT / "club_logos.json",
]
LOGOS_DIR = REPO_ROOT / "public" / "club_logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = REPO_ROOT / "cache" / "wiki_clubs"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TITLE_CACHE = REPO_ROOT / "cache" / "club_titles.json"

UA = "PlayerPassport/1.0 (private hobby project; contact: local)"
RATE_LIMIT_S = 0.6
_last_call = 0.0

session = requests.Session()
session.headers.update({"User-Agent": UA})


def _rate_limit() -> None:
    global _last_call
    delta = time.time() - _last_call
    if delta < RATE_LIMIT_S:
        time.sleep(RATE_LIMIT_S - delta)
    _last_call = time.time()


def get(url: str, *, max_retries: int = 4, timeout: int = 30) -> bytes | None:
    for attempt in range(max_retries):
        _rate_limit()
        try:
            r = session.get(url, timeout=timeout)
        except requests.RequestException as e:
            print(f"   ! {e}; retry {attempt + 1}")
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 200:
            return r.content
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "10"))
            print(f"   429 backoff {wait}s")
            time.sleep(wait)
            continue
        if 500 <= r.status_code < 600:
            time.sleep(2 ** attempt)
            continue
        return None
    return None


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or hashlib.md5((s or "x").encode()).hexdigest()[:8]


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{hashlib.md5(key.encode()).hexdigest()}.html"


def fetch_html(url: str) -> str | None:
    p = _cache_path(url)
    if p.exists():
        return p.read_text(encoding="utf-8")
    body = get(url)
    if body is None:
        return None
    text = body.decode("utf-8", errors="replace")
    p.write_text(text, encoding="utf-8")
    return text


def opensearch(name: str) -> str | None:
    q = f"{name} football club"
    url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=opensearch"
        f"&search={quote(q)}"
        "&limit=1&namespace=0&format=json"
    )
    body = get(url)
    if not body:
        return None
    try:
        data = json.loads(body)
        titles = data[1] if len(data) > 1 else []
        return titles[0] if titles else None
    except Exception:
        return None


def collect_clubs(players: list[dict]) -> list[str]:
    s: set[str] = set()
    for p in players:
        for w in p.get("world_cups") or []:
            club = w.get("club")
            if club:
                s.add(club.strip())
        for c in p.get("career_clubs") or []:
            club = c.get("club")
            if club:
                s.add(club.strip())
    return sorted(s)


def find_logo_url(html: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return None
    img = infobox.find("img")
    if not img:
        return None
    src = img.get("src")
    if not src:
        return None
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        src = "https://en.wikipedia.org" + src
    return src


def ext_from_url(url: str) -> str:
    path = urlparse(url).path
    name = unquote(path.rsplit("/", 1)[-1])
    m = re.search(r"\.(png|jpg|jpeg|svg|gif|webp)$", name, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return "png"


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    body = get(url)
    if not body:
        return False
    dest.write_bytes(body)
    return True


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    clubs = collect_clubs(data["players"])
    print(f"Unique clubs: {len(clubs)}")

    titles: dict[str, str] = {}
    if TITLE_CACHE.exists():
        titles = json.loads(TITLE_CACHE.read_text(encoding="utf-8"))

    only = sys.argv[1:] if len(sys.argv) > 1 else None
    if only:
        print(f"Filtering to: {only}")

    logos: dict[str, str] = {}
    succ = 0
    fail = 0
    failures: list[str] = []

    for i, club in enumerate(clubs, 1):
        if only and club not in only:
            continue

        slug = slugify(club)
        existing = sorted(LOGOS_DIR.glob(f"{slug}.*"))
        if existing and not only:
            rel = f"/club_logos/{existing[0].name}"
            logos[club] = rel
            succ += 1
            continue

        title = titles.get(club)
        if not title:
            title = opensearch(club)
            if title:
                titles[club] = title
                TITLE_CACHE.write_text(
                    json.dumps(titles, indent=2, ensure_ascii=False, sort_keys=True),
                    encoding="utf-8",
                )
        if not title:
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> no article")
            failures.append(f"{club} (no article)")
            fail += 1
            continue

        url = f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
        html = fetch_html(url)
        if not html:
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> fetch failed")
            failures.append(f"{club} (fetch failed)")
            fail += 1
            continue

        logo_url = find_logo_url(html)
        if not logo_url:
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> no infobox img ({title})")
            failures.append(f"{club} -> {title} (no img)")
            fail += 1
            continue

        ext = ext_from_url(logo_url)
        dest = LOGOS_DIR / f"{slug}.{ext}"
        if download(logo_url, dest):
            rel = f"/club_logos/{dest.name}"
            logos[club] = rel
            succ += 1
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> {rel}")
        else:
            print(f"  [{i:3d}/{len(clubs)}] {club:35s} -> download failed")
            failures.append(f"{club} (download failed)")
            fail += 1

        if i % 25 == 0 and not only:
            for path in JSON_OUTPUTS:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(logos, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8",
                )

    for path in JSON_OUTPUTS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(logos, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {path}")

    print(f"\nSuccess: {succ} | Fail: {fail} | Total seen: {succ + fail}")
    if failures:
        print(f"\nFirst {min(20, len(failures))} failures:")
        for f in failures[:20]:
            print(f"  - {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
