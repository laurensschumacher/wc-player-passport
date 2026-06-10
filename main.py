#!/usr/bin/env python3
"""
main.py — World Cup Player Passport builder.

Usage:
    python main.py [--force] [--limit N] [--start-at NAME]

Flags:
    --force       Re-fetch cached pages (ignore local cache).
    --limit N     Only process the first N candidates (useful for testing).
    --start-at    Skip candidates until one whose name starts with NAME.

Output:
    world_cup_players.json   (in the same directory as this script)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime

from candidates import CANDIDATES
from scraper import (
    WC_YEARS,
    fetch_wiki_2026_squads,
    scrape_candidate,
)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "world_cup_players.json")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), ".progress.json")


# ---------------------------------------------------------------------------
# Progress persistence (re-run friendly)
# ---------------------------------------------------------------------------

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"validated": [], "review": [], "disqualified": [], "done_names": []}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as fh:
        json.dump(progress, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------

def print_summary(validated: list, disqualified: list, review: list) -> None:
    total = len(CANDIDATES)
    n_val = len(validated)
    n_dis = len(disqualified)
    n_rev = len(review)

    pos_counter: Counter[str] = Counter()
    year_counter: Counter[int] = Counter()

    for player in validated:
        pos_counter[player["position"]] += 1
        for wc in player["world_cups"]:
            year_counter[wc["year"]] += 1

    print()
    print("=" * 48)
    print(f"Total candidates:        {total}")
    print(f"Validated & eligible:    {n_val}")
    print(f"Disqualified:            {n_dis}")
    print(f"Needs manual review:     {n_rev}")
    print()
    print("By position:")
    print(f"  GK:   {pos_counter.get('GK', 0)}")
    print(f"  DEF:  {pos_counter.get('DEF', 0)}")
    print(f"  MID:  {pos_counter.get('MID', 0)}")
    print(f"  ATT:  {pos_counter.get('ATT', 0)}")
    print()
    print("By tournament:")
    for year in WC_YEARS:
        count = year_counter.get(year, 0)
        print(f"  {year}:  {count:3d} players")
    print("=" * 48)
    print()


# ---------------------------------------------------------------------------
# JSON writer
# ---------------------------------------------------------------------------

def write_json(validated: list, review: list) -> None:
    output = {
        "metadata": {
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d"),
            "total_players": len(validated),
            "source": "transfermarkt.com",
            "notes": "All stats validated against Transfermarkt.",
        },
        "players": validated,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)
    print(f"[✓] Written → {OUTPUT_FILE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build World Cup Player Passport JSON.")
    parser.add_argument("--force", action="store_true", help="Ignore local page cache")
    parser.add_argument("--limit", type=int, default=0, help="Process only first N candidates")
    parser.add_argument("--start-at", type=str, default="", help="Skip until name matches")
    args = parser.parse_args()

    print(f"[*] Loading progress …")
    progress = load_progress()
    done_names: set[str] = set(progress["done_names"])
    validated: list[dict] = progress["validated"]
    review: list[dict] = progress["review"]
    disqualified: list[dict] = progress["disqualified"]

    print(f"[*] Fetching Wikipedia 2026 squad data …")
    wiki_2026 = fetch_wiki_2026_squads()
    print(f"    Found {len(wiki_2026)} name entries from Wikipedia 2026 squads page.")

    candidates = CANDIDATES
    if args.start_at:
        skip_until = args.start_at.lower()
        idx = next(
            (i for i, c in enumerate(candidates) if skip_until in c["name"].lower()),
            0,
        )
        candidates = candidates[idx:]
        print(f"[*] Starting at candidate #{idx}: {candidates[0]['name']}")

    if args.limit:
        candidates = candidates[: args.limit]
        print(f"[*] Processing only first {args.limit} candidates.")

    total = len(candidates)
    for i, candidate in enumerate(candidates, 1):
        name = candidate["name"]

        if name in done_names:
            print(f"  [{i}/{total}] Skipping (already done): {name}")
            continue

        print(f"[{i}/{total}]", end=" ")
        result = scrape_candidate(candidate, wiki_2026)

        if result["status"] == "validated":
            validated.append(result["data"])
        elif result["status"] == "disqualified":
            disqualified.append(result["review_entry"])
        elif result["status"] == "needs_manual_review":
            review.append(result["review_entry"])

        done_names.add(name)
        progress["validated"] = validated
        progress["review"] = review
        progress["disqualified"] = disqualified
        progress["done_names"] = list(done_names)
        save_progress(progress)

    # Write final JSON
    write_json(validated, review)
    print_summary(validated, disqualified, review)


if __name__ == "__main__":
    main()
