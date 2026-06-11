import { motion } from "framer-motion";
import { MAX_ROUND_SCORE, QUESTIONS_PER_ROUND } from "../utils/scoring";

export default function LineupPostRound({
  team,
  status,
  finalScoreValue,
  round,
  roundComplete,
  onNext,
}) {
  const won = status === "won";
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      <div className="text-center">
        <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-1">
          {won ? "Solved" : "Revealed"}
        </div>
        <div className="text-3xl sm:text-4xl font-bold text-white inline-flex items-center gap-2">
          <span className="text-3xl">{team.flag}</span>
          {team.country}
        </div>
        <div className="mt-2 text-slate-400 text-sm">
          {team.formation} · {team.coach || "—"}
          {team.group ? ` · Group ${team.group}` : ""}
        </div>
      </div>

      <div className="bg-slate-900 ring-1 ring-slate-800 rounded-2xl p-4 text-center">
        <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">
          Question score
        </div>
        <div
          className={`text-5xl font-bold tabular-nums mt-1 ${
            won ? "text-emerald-400" : "text-slate-300"
          }`}
        >
          {finalScoreValue}
          <span className="text-2xl text-slate-500 font-semibold">/100</span>
        </div>
        <div className="mt-3 text-xs text-slate-400 grid grid-cols-3 gap-2">
          <div>
            <div className="text-slate-500">Round</div>
            <div className="text-slate-200 font-semibold tabular-nums">
              {round.number}
            </div>
          </div>
          <div>
            <div className="text-slate-500">Question</div>
            <div className="text-slate-200 font-semibold tabular-nums">
              {round.completedQuestions}/{QUESTIONS_PER_ROUND}
            </div>
          </div>
          <div>
            <div className="text-slate-500">Round pts</div>
            <div className="text-slate-200 font-semibold tabular-nums">
              {round.roundScore}
            </div>
          </div>
        </div>
      </div>

      {roundComplete && (
        <div className="bg-emerald-500/10 ring-1 ring-emerald-500/40 rounded-2xl p-4 text-center">
          <div className="text-xs uppercase tracking-wider text-emerald-400 font-semibold">
            Round {round.number} complete
          </div>
          <div className="text-4xl font-bold tabular-nums mt-1 text-emerald-300">
            {round.roundScore}
            <span className="text-2xl text-emerald-500/70 font-semibold">
              /{MAX_ROUND_SCORE}
            </span>
          </div>
        </div>
      )}

      <button
        type="button"
        onClick={onNext}
        className="w-full min-h-[48px] rounded-xl bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 font-semibold text-white transition-colors"
      >
        {roundComplete ? "See round summary →" : "Next team →"}
      </button>
    </motion.div>
  );
}
