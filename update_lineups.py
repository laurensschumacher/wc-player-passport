#!/usr/bin/env python3
"""Scrape the 2026 FIFA World Cup squads page and emit src/data/lineups.json.

Each of the 48 teams gets a starting XI plus a derived formation. We pick the
lowest squad-number player per position-group to approximate a likely starting
XI (since the article only lists the 26-man squad, not last-match XIs).

Output schema:
  {
    "teams": [
      {
        "country": "Brazil",
        "code": "BRA",
        "alpha2": "BR",
        "flag": "🇧🇷",
        "group": "C",
        "coach": "Carlo Ancelotti",
        "formation": "4-3-3",
        "players": [
          { "no": 1, "pos": "GK", "name": "Alisson", "club": "Liverpool" },
          ...
        ],
        "bench": [ ... remaining 15 players ... ]
      },
      ...
    ]
  }
"""
from __future__ import annotations
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"
OUT = Path(__file__).parent / "src" / "data" / "lineups.json"

POS_MAP = {"GK": "GK", "DF": "DEF", "MF": "MID", "FW": "FWD"}

# Country -> (alpha3, alpha2). alpha2 used for flag emoji; alpha3 stays
# consistent with the existing nationality_code convention in the codebase.
COUNTRY_META: dict[str, tuple[str, str]] = {
    "Czech Republic": ("CZE", "CZ"),
    "Mexico": ("MEX", "MX"),
    "South Africa": ("RSA", "ZA"),
    "South Korea": ("KOR", "KR"),
    "Bosnia and Herzegovina": ("BIH", "BA"),
    "Canada": ("CAN", "CA"),
    "Qatar": ("QAT", "QA"),
    "Switzerland": ("SUI", "CH"),
    "Brazil": ("BRA", "BR"),
    "Haiti": ("HAI", "HT"),
    "Morocco": ("MAR", "MA"),
    "Scotland": ("SCO", "GB-SCT"),
    "Australia": ("AUS", "AU"),
    "Paraguay": ("PAR", "PY"),
    "Turkey": ("TUR", "TR"),
    "United States": ("USA", "US"),
    "Curaçao": ("CUW", "CW"),
    "Ecuador": ("ECU", "EC"),
    "Germany": ("GER", "DE"),
    "Ivory Coast": ("CIV", "CI"),
    "Japan": ("JPN", "JP"),
    "Netherlands": ("NED", "NL"),
    "Sweden": ("SWE", "SE"),
    "Tunisia": ("TUN", "TN"),
    "Belgium": ("BEL", "BE"),
    "Egypt": ("EGY", "EG"),
    "Iran": ("IRN", "IR"),
    "New Zealand": ("NZL", "NZ"),
    "Cape Verde": ("CPV", "CV"),
    "Saudi Arabia": ("KSA", "SA"),
    "Spain": ("ESP", "ES"),
    "Uruguay": ("URU", "UY"),
    "France": ("FRA", "FR"),
    "Iraq": ("IRQ", "IQ"),
    "Norway": ("NOR", "NO"),
    "Senegal": ("SEN", "SN"),
    "Algeria": ("ALG", "DZ"),
    "Argentina": ("ARG", "AR"),
    "Austria": ("AUT", "AT"),
    "Jordan": ("JOR", "JO"),
    "Colombia": ("COL", "CO"),
    "DR Congo": ("COD", "CD"),
    "Portugal": ("POR", "PT"),
    "Uzbekistan": ("UZB", "UZ"),
    "Croatia": ("CRO", "HR"),
    "England": ("ENG", "GB-ENG"),
    "Ghana": ("GHA", "GH"),
    "Panama": ("PAN", "PA"),
}

REGIONAL_INDICATOR_OFFSET = 0x1F1A5  # 'A' (0x41) + 0x1F1E6 - 0x41


def flag_emoji(alpha2: str) -> str:
    if alpha2 == "GB-ENG":
        return "🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f"
    if alpha2 == "GB-SCT":
        return "🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f"
    if alpha2 == "GB-WLS":
        return "🏴\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f"
    if not alpha2 or len(alpha2) != 2:
        return "🏳️"
    return "".join(chr(ord(c) + REGIONAL_INDICATOR_OFFSET) for c in alpha2.upper())


def fetch_html() -> str:
    r = requests.get(
        URL,
        headers={"User-Agent": "VibePlayportLineupScraper/1.0 (laschumacher)"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def parse_team_table(table) -> list[dict]:
    players: list[dict] = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all(["td", "th"])
        if len(cells) < 7:
            continue
        try:
            num = int(cells[0].get_text(strip=True))
        except ValueError:
            continue
        pos_link = cells[1].find("a")
        pos = pos_link.get_text(strip=True) if pos_link else ""
        if pos not in POS_MAP:
            continue
        # Player name: strip the (captain) marker, keep the rest.
        name = cells[2].get_text(" ", strip=True)
        is_captain = bool(re.search(r"\(\s*captain\s*\)", name, flags=re.I))
        name = re.sub(r"\s*\(\s*(?:vice-?)?captain\s*\)", "", name, flags=re.I)
        name = re.sub(r"\s+", " ", name).strip()
        # Club: prefer the second link in cell[6] (first link is the federation
        # flag-icon link, has no text); fall back to the cell text.
        club_links = [a for a in cells[6].find_all("a") if a.get_text(strip=True)]
        club = club_links[-1].get_text(strip=True) if club_links else ""
        if not club:
            club = cells[6].get_text(" ", strip=True)
        players.append(
            {
                "no": num,
                "pos": POS_MAP[pos],
                "name": name,
                "club": club,
                "is_captain": is_captain,
            }
        )
    return players


def find_coach(h3) -> str | None:
    """Coach text is in the first <p> after the h3, format: 'Coach: <name>'."""
    p = h3.find_next("p")
    if not p:
        return None
    txt = p.get_text(" ", strip=True)
    if not txt.lower().startswith("coach:"):
        return None
    coach = txt.split(":", 1)[1].strip()
    # Strip a leading nationality (e.g. "Italy Carlo Ancelotti"); the
    # nationality is rendered as a flag-icon link before the actual name.
    # The actual coach is the *last* link in the <p>.
    links = [a for a in p.find_all("a") if a.get_text(strip=True)]
    if links:
        return links[-1].get_text(strip=True)
    return coach


def find_group_label(h3) -> str | None:
    """Walk back to the nearest <h2> (e.g. 'Group A')."""
    node = h3
    while node:
        node = node.find_previous(["h2", "h3"])
        if node is None or node.name != "h2":
            if node and node.name == "h3":
                continue
            return None
        txt = node.get_text(strip=True)
        m = re.match(r"Group\s+([A-L])", txt)
        if m:
            return m.group(1)
    return None


# Standard formation lookup keyed by position counts in the picked XI.
FORMATIONS: dict[tuple[int, int, int], str] = {
    (4, 3, 3): "4-3-3",
    (4, 4, 2): "4-4-2",
    (4, 5, 1): "4-5-1",
    (4, 2, 4): "4-2-4",
    (3, 5, 2): "3-5-2",
    (3, 4, 3): "3-4-3",
    (5, 3, 2): "5-3-2",
    (5, 4, 1): "5-4-1",
}


def pick_starting_xi(squad: list[dict]) -> tuple[list[dict], list[dict], str]:
    """Pick a starting XI + bench + formation string.

    Strategy: take squad numbers 1–11; if their position counts match one of
    the standard formations, use that. Otherwise force a 4-3-3 by picking the
    lowest-numbered player at each position.
    """
    by_no = sorted(squad, key=lambda p: p["no"])
    first11 = by_no[:11]
    counts = {"GK": 0, "DEF": 0, "MID": 0, "FWD": 0}
    for p in first11:
        counts[p["pos"]] += 1
    if counts["GK"] == 1:
        key = (counts["DEF"], counts["MID"], counts["FWD"])
        if key in FORMATIONS:
            chosen_ids = {p["no"] for p in first11}
            bench = [p for p in by_no if p["no"] not in chosen_ids]
            return first11, bench, FORMATIONS[key]

    # Fallback: synthesize a 4-3-3 from lowest-numbered per position.
    chosen: list[dict] = []
    for pos, n in (("GK", 1), ("DEF", 4), ("MID", 3), ("FWD", 3)):
        avail = [p for p in by_no if p["pos"] == pos][:n]
        chosen.extend(avail)
    chosen_ids = {p["no"] for p in chosen}
    bench = [p for p in by_no if p["no"] not in chosen_ids]
    return chosen, bench, "4-3-3"


def main() -> int:
    print(f"Fetching {URL} …")
    html = fetch_html()
    soup = BeautifulSoup(html, "html.parser")

    teams_out: list[dict] = []
    seen: set[str] = set()

    for h3 in soup.find_all("h3"):
        country = h3.get_text(strip=True).strip()
        if country not in COUNTRY_META:
            continue
        if country in seen:
            continue
        table = h3.find_next("table")
        if not table:
            continue
        classes = table.get("class") or []
        if "sortable" not in classes or "wikitable" not in classes:
            continue
        header = table.find("tr")
        if not header or not header.get_text(" ", strip=True).startswith("No."):
            continue

        squad = parse_team_table(table)
        if len(squad) < 11:
            print(f"  ! {country}: only {len(squad)} players parsed, skipping")
            continue

        xi, bench, formation = pick_starting_xi(squad)
        coach = find_coach(h3)
        group = find_group_label(h3)
        alpha3, alpha2 = COUNTRY_META[country]

        teams_out.append(
            {
                "country": country,
                "code": alpha3,
                "alpha2": alpha2,
                "flag": flag_emoji(alpha2),
                "group": group,
                "coach": coach,
                "formation": formation,
                "players": xi,
                "bench": bench,
            }
        )
        seen.add(country)
        print(f"  ✓ {country}: {formation} ({len(squad)} squad, coach={coach})")

    if len(teams_out) != 48:
        print(f"\n!! Expected 48 teams, got {len(teams_out)}", file=sys.stderr)

    teams_out.sort(key=lambda t: t["country"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {"source": URL, "fetched_at": int(time.time()), "teams": teams_out},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {OUT} ({len(teams_out)} teams)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
