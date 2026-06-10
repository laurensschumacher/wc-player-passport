import { useState } from "react";
import { motion } from "framer-motion";
import { MAX_ROUND_SCORE, QUESTIONS_PER_ROUND } from "../utils/scoring";

export default function PostRound({
  player,
  status,
  finalScoreValue,
  guessesUsed,
  round,
  history,
  roundComplete,
  onNext,
}) {
  const [copied, setCopied] = useState(false);

  const won = status === "won";

  function buildShareText() {
    const flag = player.flag_emoji || "";
    const pos = player.position;
    const guesses = won ? Math.max(1, guessesUsed + 1) : 0;

    const headline = won
      ? `${flag} ${pos} — got it in ${guesses} guess${guesses === 1 ? "" : "es"}!`
      : `${flag} ${pos} — gave up.`;

    const lines = [
      `⚽ Player Passport`,
      headline,
      `Question: ${finalScoreValue}/100`,
      `Round ${round.number}: ${round.roundScore}/${MAX_ROUND_SCORE} (${round.completedQuestions}/${QUESTIONS_PER_ROUND})`,
    ];
    if (history.roundsCompleted > 0) {
      lines.push(
        `All-time: ${history.totalScore} pts across ${history.roundsCompleted} round${
          history.roundsCompleted === 1 ? "" : "s"
        }`,
      );
    }
    return lines.join("\n");
  }

  async function copyShare() {
    try {
      await navigator.clipboard.writeText(buildShareText());
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      // ignore
    }
  }

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
        <div className="text-3xl sm:text-4xl font-bold text-white">
          {player.name}
        </div>
        <div className="mt-2">
          <span className="inline-flex items-baseline gap-2 text-slate-400">
            <span className="text-xl">{player.flag_emoji}</span>
            <span>{player.nationality}</span>
          </span>
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
          <div className="text-xs text-slate-400 mt-1">
            Avg{" "}
            <span className="text-slate-200 font-semibold tabular-nums">
              {Math.round(round.roundScore / QUESTIONS_PER_ROUND)}
            </span>{" "}
            per question
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <button
          type="button"
          onClick={onNext}
          className="flex-1 min-h-[48px] rounded-xl bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 font-semibold text-white transition-colors"
        >
          {roundComplete ? "See round summary →" : "Next player →"}
        </button>
        <button
          type="button"
          onClick={copyShare}
          className="px-4 min-h-[48px] rounded-xl bg-slate-800 hover:bg-slate-700 active:bg-slate-700/70 ring-1 ring-slate-700 font-semibold text-slate-100 transition-colors"
        >
          {copied ? "Copied!" : "Share"}
        </button>
      </div>
    </motion.div>
  );
}
