import { motion, AnimatePresence } from "framer-motion";
import { QUESTIONS_PER_ROUND } from "../utils/scoring";

export default function ScoreDisplay({
  score,
  round,
  questionNumber,
  history,
  highScore = 0,
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <div className="flex items-baseline gap-2">
        <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">
          This question
        </span>
        <AnimatePresence mode="popLayout">
          <motion.span
            key={score}
            initial={{ y: -8, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 8, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="text-2xl font-bold tabular-nums text-white"
          >
            {score}
          </motion.span>
        </AnimatePresence>
      </div>

      <div className="text-right text-xs text-slate-400">
        <div>
          Round{" "}
          <span className="text-slate-200 font-semibold">{round.number}</span> ·
          Q{" "}
          <span className="text-slate-200 font-semibold tabular-nums">
            {questionNumber}/{QUESTIONS_PER_ROUND}
          </span>
        </div>
        <div className="text-slate-500 tabular-nums">
          <span className="text-slate-300 font-semibold">
            {round.roundScore}
          </span>{" "}
          pts this round
          {highScore > 0 && (
            <>
              {" · best "}
              <span className="text-amber-300 font-semibold">
                {highScore}
              </span>
            </>
          )}
          {history.roundsCompleted > 0 && (
            <>
              {" · "}
              <span className="text-slate-300 font-semibold">
                {history.totalScore}
              </span>{" "}
              all-time
            </>
          )}
        </div>
      </div>
    </div>
  );
}
