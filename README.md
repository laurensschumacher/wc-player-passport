# Player Passport

A World Cup guessing game. You're shown a player's tournament history (years, games, goals, club at the time) and have to guess who it is. Reveal hints, lock in a guess, and chase a high score across rounds.

Built as two pieces:

- **Data pipeline** (Python): scrapes Transfermarkt + Wikipedia to build `world_cup_players.json`.
- **Game UI** (React + Vite + Tailwind): consumes that JSON and runs the quiz.

## Stack

- React 18, Vite 5, Tailwind v4, framer-motion, canvas-confetti
- Python 3 with `requests`, `cloudscraper`, `beautifulsoup4`, `lxml`

## Project layout

```
main.py                  # pipeline entrypoint (scrape + validate + write JSON)
scraper.py               # Transfermarkt / Wikipedia fetchers, caching, parsing
candidates.py            # curated list of ~350 candidate players (name, TM id, ...)
update_2026_squads.py    # patch in 2026 squad info
update_career_clubs.py   # enrich players with full career club timeline
world_cup_players.json   # generated dataset consumed by the UI
cache/                   # on-disk cache of TM API + HTML responses
index.html               # Vite entry
src/                     # React app (App.jsx, components/, hooks/, utils/)
```

## Quick start

### 1. Install

```sh
# Python deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# JS deps
npm install
```

### 2. Build the dataset (optional — `world_cup_players.json` is checked in)

```sh
python3 main.py
```

Useful flags:

- `--force` — ignore the on-disk cache and re-fetch.
- `--limit N` — only process the first N candidates (smoke test).
- `--start-at NAME` — skip until a candidate name matches.

The run is resumable: progress is persisted to `.progress.json` after every candidate, so re-running picks up where it left off. Delete that file to start fresh.

Optional enrichers (run after `main.py`):

```sh
python3 update_2026_squads.py
python3 update_career_clubs.py
```

### 3. Run the game

```sh
npm run dev        # local dev server
npm run build      # production build into dist/
npm run preview    # serve the built bundle
```

## Data shape

`world_cup_players.json`:

```json
{
  "metadata": { "generated_at": "...", "total_players": 286, "source": "transfermarkt.com" },
  "players": [
    {
      "id": "lionel-messi-arg",
      "name": "Lionel Messi",
      "nationality": "Argentina",
      "nationality_code": "ARG",
      "flag_emoji": "🇦🇷",
      "position": "ATT",
      "transfermarkt_url": "...",
      "world_cups": [
        { "year": 2006, "games": 3, "goals": 1, "club": "FC Barcelona" }
      ],
      "career_clubs": [
        { "start_year": 2004, "end_year": 2021, "club": "FC Barcelona" }
      ],
      "validation_status": "validated"
    }
  ]
}
```

## Notes

- All Transfermarkt requests are cached under `cache/` and rate-limited; the scraper is meant to be polite and re-runnable, not fast.
- Eligibility rule: a candidate is only included if they appear in at least two World Cups (2002–2026) per the validated TM data.
