import { useEffect, useRef, useState } from "react";
import confetti from "canvas-confetti";
import GameCard from "./components/GameCard";
import GuessInput from "./components/GuessInput";
import ScoreDisplay from "./components/ScoreDisplay";
import PostRound from "./components/PostRound";
import RoundSummary from "./components/RoundSummary";
import HowToPlay from "./components/HowToPlay";
import { useGameState } from "./hooks/useGameState";
import { usePlayerPool } from "./hooks/usePlayerPool";
import { QUESTIONS_PER_ROUND } from "./utils/scoring";

export default function App() {
  const {
    allPlayers,
    current,
    advance,
    reshuffleToken,
    poolSize,
  } = usePlayerPool();

  const game = useGameState(current);

  const [howToOpen, setHowToOpen] = useState(false);
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
    const raw = window.localStorage.getItem("playport.highScore");
    const n = raw ? parseInt(raw, 10) : 0;
    return Number.isFinite(n) && n > 0 ? n : 0;
  });
  const [pendingDelta, setPendingDelta] = useState(null);
  const lastScoredRound = useRef(null);

  useEffect(() => {
    if (!current) return;
    if (game.status === "playing") return;
    if (lastScoredRound.current === current.id) return;
    lastScoredRound.current = current.id;
    setPendingDelta(game.finalScoreValue);
    setRound((r) => ({
      ...r,
      roundScore: r.roundScore + game.finalScoreValue,
      completedQuestions: r.completedQuestions + 1,
    }));
    setRoundResults((rs) => [
      ...rs,
      {
        name: current.name,
        flag: current.flag_emoji,
        position: current.position,
        nationality: current.nationality,
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
    setToast("You've seen all players — reshuffling!");
    const t = setTimeout(() => setToast(null), 2400);
    return () => clearTimeout(t);
  }, [reshuffleToken]);

  const roundComplete = round.completedQuestions >= QUESTIONS_PER_ROUND;

  function handleNext() {
    setPendingDelta(null);
    if (showRoundSummary) {
      // Closing the summary → finalize this round into history and start next.
      setHistory((h) => ({
        roundsCompleted: h.roundsCompleted + 1,
        totalScore: h.totalScore + round.roundScore,
      }));
      if (round.roundScore > highScore) {
        setHighScore(round.roundScore);
        if (typeof window !== "undefined") {
          window.localStorage.setItem(
            "playport.highScore",
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
      // Just finished the last question of the round → show the summary
      // before advancing to the next player.
      setShowRoundSummary(true);
      return;
    }
    advance();
  }

  if (!allPlayers.length || allPlayers.length < 10) {
    return (
      <div className="min-h-full flex items-center justify-center p-6 text-center">
        <div className="max-w-md text-slate-300">
          <h1 className="text-2xl font-bold text-white mb-3">
            ⚽ Player Passport
          </h1>
          <p>
            Not enough validated players to play (need at least 10, found{" "}
            <span className="font-semibold">{allPlayers.length}</span>).
          </p>
          <p className="mt-3 text-slate-400 text-sm">
            Run the data scraper first:{" "}
            <code className="bg-slate-800 px-1.5 py-0.5 rounded">
              python3 main.py
            </code>{" "}
            and rebuild.
          </p>
        </div>
      </div>
    );
  }

  if (!current) return null;

  const guessesUsed = game.wrongGuesses.length;
  // Counter reflects the question currently on screen:
  //  - while playing, it's the next un-answered question
  //  - while showing the result, it's the question that was just answered
  const questionNumber =
    game.status === "playing"
      ? Math.min(round.completedQuestions + 1, QUESTIONS_PER_ROUND)
      : Math.max(round.completedQuestions, 1);

  return (
    <div className="min-h-full flex flex-col text-slate-100">
      <header className="px-4 sm:px-6 py-4 flex items-center justify-between max-w-2xl w-full mx-auto">
        <div className="flex items-center gap-2">
          <span className="text-2xl" aria-hidden>
            📘⚽
          </span>
          <h1 className="text-lg sm:text-xl font-bold tracking-tight">
            Player Passport
          </h1>
        </div>
        <button
          type="button"
          onClick={() => setHowToOpen(true)}
          className="text-xs sm:text-sm text-slate-400 hover:text-white px-3 py-2 rounded-lg ring-1 ring-slate-800 hover:ring-slate-700 transition-colors min-h-[44px]"
        >
          How to play
        </button>
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
            <GameCard
              player={current}
              hintRevealed={game.hintUsed}
              onRevealHint={game.revealHint}
              clubsRevealed={game.clubsHintUsed}
              onRevealClubsHint={game.revealClubsHint}
              status={game.status}
            />

            {game.status === "playing" ? (
              <GuessInput
                allPlayers={allPlayers}
                onSubmit={(g) => game.submitGuess(g)}
                wrongGuesses={game.wrongGuesses}
                shake={game.shake}
                disabled={false}
                onGiveUp={game.giveUp}
              />
            ) : (
              <PostRound
                player={current}
                status={game.status}
                finalScoreValue={game.finalScoreValue}
                guessesUsed={guessesUsed}
                round={round}
                history={history}
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

      <HowToPlay open={howToOpen} onClose={() => setHowToOpen(false)} />
      <span className="sr-only" aria-live="polite">
        {poolSize} players in pool.
      </span>
    </div>
  );
}
