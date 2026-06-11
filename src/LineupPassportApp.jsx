import { useEffect, useRef, useState } from "react";
import confetti from "canvas-confetti";
import LineupCard from "./components/LineupCard";
import LineupGuessInput from "./components/LineupGuessInput";
import LineupPostRound from "./components/LineupPostRound";
import ScoreDisplay from "./components/ScoreDisplay";
import RoundSummary from "./components/RoundSummary";
import { useLineupGameState } from "./hooks/useLineupGameState";
import { useLineupPool } from "./hooks/useLineupPool";
import { QUESTIONS_PER_ROUND } from "./utils/scoring";

export default function LineupPassportApp({ onExitMode }) {
  const { allTeams, current, advance, reshuffleToken, poolSize } =
    useLineupPool();

  const game = useLineupGameState(current);

  const [toast, setToast] = useState(null);
  const [round, setRound] = useState({
    number: 1,
    roundScore: 0,
    completedQuestions: 0,
  });
  const [roundResults, setRoundResults] = useState([]);
  const [showRoundSummary, setShowRoundSummary] = useState(false);
  const [history, setHistory] = useState({ roundsCompleted: 0, totalScore: 0 });
  const [highScore, setHighScore] = useState(() => {
    if (typeof window === "undefined") return 0;
    const raw = window.localStorage.getItem("playport.lineupHighScore");
    const n = raw ? parseInt(raw, 10) : 0;
    return Number.isFinite(n) && n > 0 ? n : 0;
  });
  const [pendingDelta, setPendingDelta] = useState(null);
  const lastScoredTeam = useRef(null);

  useEffect(() => {
    if (!current) return;
    if (game.status === "playing") return;
    if (lastScoredTeam.current === current.code) return;
    lastScoredTeam.current = current.code;
    setPendingDelta(game.finalScoreValue);
    setRound((r) => ({
      ...r,
      roundScore: r.roundScore + game.finalScoreValue,
      completedQuestions: r.completedQuestions + 1,
    }));
    setRoundResults((rs) => [
      ...rs,
      {
        name: current.country,
        flag: current.flag,
        position: current.formation,
        nationality: current.country,
        status: game.status,
        score: game.finalScoreValue,
      },
    ]);
    if (game.status === "won") {
      const burst = (originX) =>
        confetti({
          particleCount: 60,
          spread: 70,
          startVelocity: 35,
          origin: { x: originX, y: 0.55 },
          colors: ["#22c55e", "#10b981", "#34d399", "#fbbf24", "#6366f1"],
        });
      burst(0.3);
      burst(0.7);
    }
  }, [game.status, game.finalScoreValue, current]);

  useEffect(() => {
    if (reshuffleToken === 0) return;
    setToast("You've seen all teams — reshuffling!");
    const t = setTimeout(() => setToast(null), 2400);
    return () => clearTimeout(t);
  }, [reshuffleToken]);

  const roundComplete = round.completedQuestions >= QUESTIONS_PER_ROUND;

  function handleNext() {
    setPendingDelta(null);
    if (showRoundSummary) {
      setHistory((h) => ({
        roundsCompleted: h.roundsCompleted + 1,
        totalScore: h.totalScore + round.roundScore,
      }));
      if (round.roundScore > highScore) {
        setHighScore(round.roundScore);
        if (typeof window !== "undefined") {
          window.localStorage.setItem(
            "playport.lineupHighScore",
            String(round.roundScore),
          );
        }
      }
      setRound({
        number: round.number + 1,
        roundScore: 0,
        completedQuestions: 0,
      });
      setRoundResults([]);
      setShowRoundSummary(false);
      advance();
      return;
    }
    if (roundComplete) {
      setShowRoundSummary(true);
      return;
    }
    advance();
  }

  if (!current) {
    return (
      <div className="min-h-full flex items-center justify-center p-6 text-center text-slate-300">
        Loading lineups…
      </div>
    );
  }

  const questionNumber =
    game.status === "playing"
      ? Math.min(round.completedQuestions + 1, QUESTIONS_PER_ROUND)
      : Math.max(round.completedQuestions, 1);

  return (
    <div className="min-h-full flex flex-col text-slate-100">
      <header className="px-4 sm:px-6 py-4 flex items-center justify-between max-w-2xl w-full mx-auto">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onExitMode}
            className="text-xs sm:text-sm text-slate-400 hover:text-white px-2 py-2 rounded-lg ring-1 ring-slate-800 hover:ring-slate-700 transition-colors min-h-[44px]"
            aria-label="Back to mode picker"
          >
            ← Modes
          </button>
          <span className="text-2xl ml-1" aria-hidden>
            🥅⚽
          </span>
          <h1 className="text-lg sm:text-xl font-bold tracking-tight">
            Lineup Passport
          </h1>
        </div>
        <span className="text-xs text-slate-500 tabular-nums">
          {poolSize} teams
        </span>
      </header>

      <main className="flex-1 px-4 sm:px-6 pb-24 max-w-2xl w-full mx-auto space-y-4">
        <ScoreDisplay
          score={game.score}
          round={round}
          questionNumber={questionNumber}
          history={history}
          highScore={highScore}
        />

        {showRoundSummary ? (
          <RoundSummary
            round={round}
            results={roundResults}
            history={history}
            highScore={highScore}
            onStartNext={handleNext}
          />
        ) : (
          <>
            <LineupCard
              team={current}
              hintRevealed={game.hintUsed}
              onRevealHint={game.revealHint}
              status={game.status}
            />

            {game.status === "playing" ? (
              <LineupGuessInput
                allTeams={allTeams}
                onSubmit={(g) => game.submitGuess(g)}
                wrongGuesses={game.wrongGuesses}
                shake={game.shake}
                disabled={false}
                onGiveUp={game.giveUp}
              />
            ) : (
              <LineupPostRound
                team={current}
                status={game.status}
                finalScoreValue={game.finalScoreValue}
                round={round}
                roundComplete={roundComplete}
                onNext={handleNext}
              />
            )}
          </>
        )}
      </main>

      {toast && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-slate-800 text-slate-100 ring-1 ring-slate-700 px-4 py-2 rounded-full shadow-lg text-sm z-40">
          {toast}
        </div>
      )}

      {pendingDelta != null && game.status !== "playing" && !showRoundSummary && (
        <div
          className="fixed top-16 left-1/2 -translate-x-1/2 text-emerald-300 font-bold pointer-events-none z-30"
          aria-live="polite"
        >
          +{pendingDelta} pts
        </div>
      )}
    </div>
  );
}
