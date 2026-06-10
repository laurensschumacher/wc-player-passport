import { motion } from "framer-motion";
import { MAX_ROUND_SCORE, QUESTIONS_PER_ROUND } from "../utils/scoring";

export default function RoundSummary({
  round,
  results,
  history,
  highScore = 0,
  onStartNext,
}) {
  const total = results.reduce((sum, r) => sum + r.score, 0);
  const avg =
    results.length > 0 ? Math.round(total / results.length) : 0;
  const solved = results.filter((r) => r.status === "won").length;
  const isNewHigh = total > highScore;
  const bestSoFar = Math.max(highScore, total);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      <div className="text-center">
        <div className="text-xs uppercase tracking-wider text-emerald-400 font-semibold mb-1">
          Round {round.number} complete
        </div>
        <div className="text-4xl sm:text-5xl font-bold tabular-nums text-white">
          {total}
          <span className="text-2xl text-slate-500 font-semibold">
            /{MAX_ROUND_SCORE}
          </span>
        </div>
        <div className="text-xs text-slate-400 mt-1">
          {solved}/{QUESTIONS_PER_ROUND} solved · avg{" "}
          <span className="text-slate-200 font-semibold tabular-nums">
            {avg}
          </span>{" "}
          per question
        </div>
        {isNewHigh ? (
          <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/15 ring-1 ring-amber-500/40 text-amber-300 text-xs font-semibold">
            <span aria-hidden>🏆</span>
            New high score!
          </div>
        ) : highScore > 0 ? (
          <div className="mt-2 text-xs text-slate-500">
            Best:{" "}
            <span className="text-slate-300 font-semibold tabular-nums">
              {bestSoFar}
            </span>
          </div>
        ) : null}
      </div>

      <div className="bg-slate-900 ring-1 ring-slate-800 rounded-2xl overflow-hidden">
        <div className="grid grid-cols-[2rem_1.5rem_1fr_2.5rem_3rem] items-center gap-2 px-3 py-2 text-[10px] uppercase tracking-wider text-slate-500 font-semibold border-b border-slate-800">
          <div>#</div>
          <div></div>
          <div>Player</div>
          <div className="text-center">Got</div>
          <div className="text-right">Pts</div>
        </div>
        {results.map((r, i) => {
          const won = r.status === "won";
          return (
            <div
              key={i}
              className="grid grid-cols-[2rem_1.5rem_1fr_2.5rem_3rem] items-center gap-2 px-3 py-2.5 text-sm border-b border-slate-800/60 last:border-b-0"
            >
              <div className="text-slate-500 tabular-nums">{i + 1}</div>
              <div className="text-lg leading-none" aria-hidden>
                {r.flag}
              </div>
              <div className="min-w-0 truncate text-slate-100 font-medium">
                {r.name}
              </div>
              <div
                className={`text-center text-base ${
                  won ? "text-emerald-400" : "text-rose-400"
                }`}
                aria-label={won ? "solved" : "gave up"}
              >
                {won ? "✓" : "✕"}
              </div>
              <div
                className={`text-right tabular-nums font-semibold ${
                  r.score > 0 ? "text-emerald-300" : "text-slate-500"
                }`}
              >
                {r.score}
              </div>
            </div>
          );
        })}
      </div>

      {history.roundsCompleted > 0 && (
        <div className="text-center text-xs text-slate-500">
          All-time:{" "}
          <span className="text-slate-300 font-semibold tabular-nums">
            {history.totalScore + total}
          </span>{" "}
          pts across{" "}
          <span className="text-slate-300 font-semibold tabular-nums">
            {history.roundsCompleted + 1}
          </span>{" "}
          rounds
        </div>
      )}

      <button
        type="button"
        onClick={onStartNext}
        className="w-full min-h-[48px] rounded-xl bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 font-semibold text-white transition-colors"
      >
        Start new round →
      </button>
    </motion.div>
  );
}
