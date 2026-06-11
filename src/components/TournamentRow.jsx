import { motion } from "framer-motion";
import ClubLogo from "./ClubLogo";

const WC_HOSTS = {
  2002: "South Korea / Japan",
  2006: "Germany",
  2010: "South Africa",
  2014: "Brazil",
  2018: "Russia",
  2022: "Qatar",
  2026: "USA / Canada / Mexico",
};

export default function TournamentRow({ wc, index }) {
  const isFutureSquadOnly =
    wc.year === 2026 && (wc.games == null || wc.games === 0);
  const host = WC_HOSTS[wc.year];

  return (
    <motion.div
      initial={{ opacity: 0, x: -16 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.04 * index, duration: 0.25, ease: "easeOut" }}
      className="flex items-center gap-3 px-4 py-3 border-t border-slate-800 first:border-t-0"
    >
      <img
        src={`/wc_logos/${wc.year}.png`}
        alt={`${wc.year} World Cup`}
        className="w-9 h-9 object-contain shrink-0"
      />

      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-2">
          <span className="text-lg font-bold text-slate-100 tabular-nums">
            {wc.year}
          </span>
          {host && (
            <span className="text-xs text-slate-400 truncate">{host}</span>
          )}
        </div>

        {isFutureSquadOnly ? (
          <div className="mt-0.5">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-amber-400/15 text-amber-300 text-xs font-semibold ring-1 ring-amber-400/30">
              2026 Squad
            </span>
          </div>
        ) : (
          <div className="mt-0.5 flex items-baseline gap-3 text-sm text-slate-300">
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
          className="mt-1 flex items-center gap-1.5 text-sm text-slate-400"
        >
          <span className="text-[10px] uppercase tracking-wider text-slate-500 shrink-0">
            Club at WC
          </span>
          <ClubLogo name={wc.club} size={16} />
          <span className="truncate">{wc.club || "Unknown"}</span>
        </div>
      </div>
    </motion.div>
  );
}
