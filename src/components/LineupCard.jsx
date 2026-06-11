import { motion } from "framer-motion";
import PitchDiagram from "./PitchDiagram";
import HintButton from "./HintButton";
import { HINT_COST } from "../utils/scoring";

/**
 * Lineup-mode card. Shows a starting XI on a pitch with club logos at
 * each position. Country name + flag are hidden until the round ends.
 * The single hint reveals the formation + coach.
 */
export default function LineupCard({
  team,
  hintRevealed,
  onRevealHint,
  status,
}) {
  if (!team) return null;
  const playing = status === "playing";
  const showFormation = hintRevealed || !playing;
  const showCoach = hintRevealed || !playing;
  const showCountry = !playing;

  return (
    <motion.div
      key={team.code}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`bg-slate-900 ring-1 ring-slate-800 rounded-2xl shadow-xl overflow-hidden ${
        status === "won" ? "ring-emerald-500/50" : ""
      }`}
    >
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900/80">
        <div className="flex items-center gap-2 min-w-0">
          {showCountry ? (
            <>
              <span className="text-3xl leading-none" aria-hidden>
                {team.flag}
              </span>
              <span className="text-sm font-semibold text-white truncate">
                {team.country}
                {team.group ? (
                  <span className="text-slate-500 font-normal ml-1">
                    · Group {team.group}
                  </span>
                ) : null}
              </span>
            </>
          ) : (
            <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">
              Mystery National Team
            </span>
          )}
        </div>
        <div className="text-xs text-slate-400 font-medium tabular-nums">
          {showFormation ? team.formation : "?-?-?"}
        </div>
      </div>

      <div className="p-3">
        <PitchDiagram
          players={team.players}
          formation={team.formation}
          revealNames={!playing}
        />
      </div>

      <div className="px-4 py-2 text-xs text-slate-400 border-t border-slate-800/60 flex items-center justify-between">
        <span>
          {showCoach ? (
            <>Coach: <span className="text-slate-200">{team.coach || "—"}</span></>
          ) : (
            <span className="text-slate-600">Coach hidden</span>
          )}
        </span>
        <span className="text-slate-600">starting XI</span>
      </div>

      {playing && !hintRevealed && (
        <div className="px-4 pb-3 pt-3 border-t border-slate-800/60">
          <HintButton
            icon="🧭"
            label="Reveal formation & coach"
            cost={HINT_COST}
            onReveal={onRevealHint}
          />
        </div>
      )}
    </motion.div>
  );
}
