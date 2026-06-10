"""
Update world_cup_players.json with 2026 World Cup squad entries.
Fetches https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads, parses each
nation's squad table, and adds a 2026 entry (year=2026, games=0, goals=0,
club=2026 club) for any existing player who appears in the 2026 squad and
does not yet have a 2026 entry.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_squads"

# Map nationality strings used in our JSON to the Wikipedia heading text.
NATION_TO_WIKI_HEADING = {
    "Argentina": "Argentina",
    "Spain": "Spain",
    "Germany": "Germany",
    "Brazil": "Brazil",
    "France": "France",
    "England": "England",
    "Portugal": "Portugal",
    "Croatia": "Croatia",
    "Belgium": "Belgium",
    "Netherlands": "Netherlands",
    "Uruguay": "Uruguay",
    "United States": "United States",
    "South Korea": "South Korea",
    "Mexico": "Mexico",
    "Japan": "Japan",
    "Ghana": "Ghana",
    "Switzerland": "Switzerland",
    "Ivory Coast": "Ivory Coast",
    "Colombia": "Colombia",
    "Senegal": "Senegal",
    "Sweden": "Sweden",
    "Ecuador": "Ecuador",
    "Australia": "Australia",
    "Morocco": "Morocco",
    "Iran": "Iran",
    "Paraguay": "Paraguay",
    # Italy, Poland, Nigeria, Denmark, Cameroon, Serbia, Russia did not qualify.
}


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[.'`’\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def name_tokens(s: str) -> list[str]:
    return normalize(s).split()


def fetch_squads() -> dict[str, list[dict]]:
    """Return {nationality: [{name, club}, ...]} parsed from Wikipedia."""
    print(f"Fetching {URL} ...", flush=True)
    resp = requests.get(
        URL,
        headers={"User-Agent": "PlayerPassport/1.0 (educational)"},
        timeout=30,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Find h3 headings (nation names) under h2 group headings.
    squads: dict[str, list[dict]] = {}

    # Each nation has an <h3> like <span class="mw-headline" id="Argentina">Argentina</span>
    # followed by a <table class="wikitable"> for its squad.
    for h3 in soup.find_all(["h3", "h4"]):
        heading_text = h3.get_text(strip=True).strip()
        # Strip trailing [edit] if present
        heading_text = re.sub(r"\[edit\]$", "", heading_text).strip()
        if heading_text not in NATION_TO_WIKI_HEADING.values():
            continue

        # The next wikitable in document order is this nation's squad table.
        table = h3.find_next("table", class_="wikitable")
        if table is None:
            print(f"  ! no squad table for {heading_text}")
            continue

        rows = []
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            if len(cells) < 7:
                continue
            # Columns: number | pos | player | dob | caps | goals | club
            name_cell = cells[2]
            club_cell = cells[6]
            name = name_cell.get_text(" ", strip=True)
            # Strip "(captain)" / "(vice-captain)" suffix
            name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
            # Strip trailing [n] footnote markers
            name = re.sub(r"\[\d+\]", "", name).strip()
            club = club_cell.get_text(" ", strip=True)
            club = re.sub(r"\[\d+\]", "", club).strip()
            if not name:
                continue
            rows.append({"name": name, "club": club})

        if rows:
            squads[heading_text] = rows
            print(f"  · {heading_text}: {len(rows)} players")

    return squads


def best_match(player_name: str, squad: list[dict]) -> dict | None:
    target_norm = normalize(player_name)
    target_tokens = target_norm.split()
    target_last = target_tokens[-1] if target_tokens else ""
    target_first = target_tokens[0] if target_tokens else ""

    # 1. Exact normalized match.
    for entry in squad:
        if normalize(entry["name"]) == target_norm:
            return entry

    # 2. Match if our normalized name is a subset/superset of the squad
    # entry's normalized name (e.g. "Bukayo Saka" vs "Bukayo Saka").
    for entry in squad:
        sn = normalize(entry["name"])
        if not sn:
            continue
        # Substring either direction, but require >= 3 tokens shared or
        # last-name match to avoid false positives.
        s_tokens = sn.split()
        if not s_tokens:
            continue
        s_last = s_tokens[-1]
        if target_last and s_last == target_last:
            # Require some first-name overlap for safety on common surnames.
            if target_first and (target_first == s_tokens[0] or target_first in sn):
                return entry
            # Single-token target ("Pepe", "Neymar") matches by surname only.
            if len(target_tokens) == 1:
                return entry
            # If target has >1 token but the first letter of first names match
            # (handles "Heung-Min Son" vs "Son Heung-min"), accept.
            if target_first and s_tokens[0] and target_first[0] == s_tokens[0][0]:
                return entry

    # 3. Token-set match: all tokens of one are contained in the other.
    target_set = set(target_tokens)
    for entry in squad:
        s_set = set(normalize(entry["name"]).split())
        if not s_set or not target_set:
            continue
        if target_set <= s_set or s_set <= target_set:
            # Require at least one of these to share the surname.
            if target_last in s_set or (
                s_set and list(s_set)[-1] == target_last
            ):
                return entry

    return None


def main() -> int:
    repo_root = Path(__file__).parent
    json_paths = [
        repo_root / "world_cup_players.json",
        repo_root / "src" / "data" / "world_cup_players.json",
    ]
    primary = json_paths[0]
    if not primary.exists():
        print(f"ERROR: {primary} not found", file=sys.stderr)
        return 1

    data = json.loads(primary.read_text(encoding="utf-8"))
    players = data["players"]

    squads = fetch_squads()

    added = 0
    updated = 0
    skipped_no_match = 0
    skipped_already = 0
    skipped_no_squad = 0

    no_match_examples: list[str] = []

    for p in players:
        nat = p.get("nationality")
        wiki_heading = NATION_TO_WIKI_HEADING.get(nat)
        if not wiki_heading:
            continue
        squad = squads.get(wiki_heading)
        if not squad:
            skipped_no_squad += 1
            continue
        existing = next(
            (wc for wc in p.get("world_cups", []) if wc.get("year") == 2026),
            None,
        )
        # If a 2026 entry already exists with a real club, keep it.
        if existing and existing.get("club") and existing["club"] != "Unknown":
            skipped_already += 1
            continue
        match = best_match(p["name"], squad)
        if not match:
            # Player has an existing 2026 stub but isn't in the parsed
            # squad — keep the stub so we don't drop data.
            if existing:
                skipped_already += 1
            else:
                skipped_no_match += 1
                if len(no_match_examples) < 25:
                    no_match_examples.append(f"{p['name']} ({nat})")
            continue
        if existing:
            existing["club"] = match["club"]
            updated += 1
        else:
            p["world_cups"].append(
                {
                    "year": 2026,
                    "games": 0,
                    "goals": 0,
                    "club": match["club"],
                }
            )
            added += 1
        p["world_cups"].sort(key=lambda wc: wc["year"])

    # Recompute summary if present.
    summary = data.get("summary", {})
    summary["validated_players"] = sum(
        1 for p in players if p.get("validation_status") == "validated"
    )
    summary["players_with_2026_entry"] = sum(
        1 for p in players if any(wc.get("year") == 2026 for wc in p["world_cups"])
    )
    data["summary"] = summary

    for path in json_paths:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  wrote {path}")

    print()
    print(f"Added 2026 entries:        {added}")
    print(f"Updated existing stub:     {updated}")
    print(f"Already had complete 2026: {skipped_already}")
    print(f"Nation not in 2026:        {skipped_no_squad}")
    print(f"In 2026 nation but no name match: {skipped_no_match}")
    if no_match_examples:
        print()
        print("Examples of no-match (manual review):")
        for ex in no_match_examples:
            print(f"  - {ex}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
