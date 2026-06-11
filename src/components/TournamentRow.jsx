import { motion } from "framer-motion";
import { flagFromCode } from "../utils/flagEmoji";
import ClubLogo from "./ClubLogo";

export default function TournamentRow({ wc, nationalityCode, index }) {
  const isFutureSquadOnly =
    wc.year === 2026 && (wc.games == null || wc.games === 0);

  return (
    <motion.div
      initial={{ opacity: 0, x: -16 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.04 * index, duration: 0.25, ease: "easeOut" }}
      className="flex items-center gap-3 px-4 py-3 border-t border-slate-800 first:border-t-0"
    >
      <div className="text-lg font-bold text-slate-200 w-14 tabular-nums">
        {wc.year}
      </div>

      <div className="text-2xl shrink-0" aria-hidden>
        {flagFromCode(nationalityCode)}
      </div>

      <div className="flex-1 min-w-0">
        {isFutureSquadOnly ? (
          <div>
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-amber-400/15 text-amber-300 text-xs font-semibold ring-1 ring-amber-400/30">
              2026 Squad
            </span>
          </div>
        ) : (
          <div className="flex items-baseline gap-3 text-sm text-slate-300">
            <span className="tabular-nums">
              <span className="text-slate-100 font-semibold">{wc.games}</span>{" "}
              {wc.games === 1 ? "game" : "games"}
            </span>
            <span className="text-slate-500">·</span>
            <span className="tabular-nums">
              <span className="text-slate-100 font-semibold">{wc.goals}</span>{" "}
              {wc.goals === 1 ? "goal" : "goals"}
            </span>
          </div>
        )}
        <div
          title={wc.club}
          className="mt-0.5 text-sm text-slate-400 truncate flex items-center gap-1.5"
        >
          <ClubLogo name={wc.club} size={16} />
          <span className="truncate">{wc.club || "Unknown"}</span>
        </div>
      </div>
    </motion.div>
  );
}
