import { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { flagFromCode } from "../utils/flagEmoji";
import HintButton from "./HintButton";
import PositionBadge from "./PositionBadge";
import TournamentRow from "./TournamentRow";
import CareerClubRow from "./CareerClubRow";
import { CLUBS_HINT_COST, HINT_COST } from "../utils/scoring";

function buildTimeline(player, includeClubs) {
  const wcs = (player.world_cups || [])
    .slice()
    .sort((a, b) => a.year - b.year)
    .map((wc) => ({ kind: "wc", year: wc.year, data: wc }));

  if (!includeClubs) return wcs;

  const clubs = (player.career_clubs || [])
    .slice()
    .filter((c) => c && (c.start_year || c.end_year))
    .sort((a, b) => (a.start_year || 0) - (b.start_year || 0))
    .map((c) => ({
      kind: "club",
      year: c.start_year || c.end_year || 0,
      data: c,
    }));

  // Stable merge by year. A club with start_year == WC year appears BEFORE
  // the WC row, since playing for the club typically begins before the
  // tournament that summer.
  const merged = [];
  let i = 0;
  let j = 0;
  while (i < clubs.length && j < wcs.length) {
    if (clubs[i].year <= wcs[j].year) {
      merged.push(clubs[i++]);
    } else {
      merged.push(wcs[j++]);
    }
  }
  while (i < clubs.length) merged.push(clubs[i++]);
  while (j < wcs.length) merged.push(wcs[j++]);
  return merged;
}

export default function GameCard({
  player,
  hintRevealed,
  onRevealHint,
  clubsRevealed,
  onRevealClubsHint,
  status,
}) {
  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    if (status === "won") {
      setPulse(true);
      const t = setTimeout(() => setPulse(false), 1000);
      return () => clearTimeout(t);
    }
  }, [status]);

  const showClubs = clubsRevealed || status !== "playing";
  const hasClubData =
    Array.isArray(player?.career_clubs) && player.career_clubs.length > 0;

  const timeline = useMemo(
    () => (player ? buildTimeline(player, showClubs && hasClubData) : []),
    [player, showClubs, hasClubData],
  );

  if (!player) return null;

  const positionRevealedNow = hintRevealed || status !== "playing";
  const showPositionButton = status === "playing" && !hintRevealed;
  const showClubsButton =
    status === "playing" && !clubsRevealed && hasClubData;

  return (
    <motion.div
      key={player.id}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`bg-slate-900 ring-1 ring-slate-800 rounded-2xl shadow-xl overflow-hidden ${
        pulse ? "animate-pulse-green" : ""
      } ${status === "won" ? "ring-emerald-500/50" : ""}`}
    >
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-3xl leading-none" aria-label={player.nationality}>
            {flagFromCode(player.nationality_code)}
          </span>
          <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">
            {status === "playing" ? "Mystery Player" : player.name}
          </span>
        </div>
        {positionRevealedNow && <PositionBadge position={player.position} />}
      </div>

      <div>
        <AnimatePresence initial={false}>
          {timeline.map((row, i) =>
            row.kind === "wc" ? (
              <TournamentRow
                key={`wc-${row.data.year}`}
                wc={row.data}
                nationalityCode={player.nationality_code}
                index={i}
              />
            ) : (
              <CareerClubRow
                key={`club-${row.data.start_year}-${row.data.club}-${i}`}
                club={row.data}
                index={i}
              />
            ),
          )}
        </AnimatePresence>
      </div>

      {(showPositionButton || showClubsButton) && (
        <div className="px-4 pb-3 pt-3 border-t border-slate-800/60 space-y-2">
          {showPositionButton && (
            <HintButton
              icon="🎯"
              label="Reveal position"
              cost={HINT_COST}
              onReveal={onRevealHint}
            />
          )}
          {showClubsButton && (
            <HintButton
              icon="🏟️"
              label="Reveal all clubs"
              cost={CLUBS_HINT_COST}
              onReveal={onRevealClubsHint}
            />
          )}
        </div>
      )}
    </motion.div>
  );
}
