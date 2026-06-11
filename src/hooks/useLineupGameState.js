import { useCallback, useState } from "react";
import {
  CORRECT_FLOOR,
  HINT_COST,
  STARTING_SCORE,
  WRONG_GUESS_COST,
  matchesCountry,
} from "../utils/scoring";

/**
 * Round-level state machine for Lineup Passport mode. Mirrors useGameState
 * but: target is the team's country name, the only hint is "show formation
 * + coach", and there's no career-clubs hint.
 */
export function useLineupGameState(team) {
  const [hintUsed, setHintUsed] = useState(false);
  const [wrongGuesses, setWrongGuesses] = useState([]);
  const [status, setStatus] = useState("playing");
  const [shake, setShake] = useState(0);

  const [prevTeamCode, setPrevTeamCode] = useState(team?.code);
  if (team?.code !== prevTeamCode) {
    setPrevTeamCode(team?.code);
    setHintUsed(false);
    setWrongGuesses([]);
    setStatus("playing");
    setShake(0);
  }

  const wrongCount = wrongGuesses.length;
  const raw =
    STARTING_SCORE - (hintUsed ? HINT_COST : 0) - wrongCount * WRONG_GUESS_COST;
  const score = Math.max(CORRECT_FLOOR, raw);
  const finalScoreValue = status === "gave-up" ? 0 : score;

  const revealHint = useCallback(() => {
    if (hintUsed || status !== "playing") return;
    setHintUsed(true);
  }, [hintUsed, status]);

  const submitGuess = useCallback(
    (guess) => {
      if (status !== "playing" || !team) return { ok: false };
      const trimmed = (guess || "").trim();
      if (!trimmed) return { ok: false };
      if (matchesCountry(trimmed, team.country)) {
        setStatus("won");
        return { ok: true, correct: true };
      }
      setWrongGuesses((prev) => [
        ...prev,
        { guess: trimmed, deduction: WRONG_GUESS_COST },
      ]);
      setShake((s) => s + 1);
      return { ok: true, correct: false };
    },
    [team, status],
  );

  const giveUp = useCallback(() => {
    if (status !== "playing") return;
    setStatus("gave-up");
  }, [status]);

  return {
    status,
    score,
    finalScoreValue,
    hintUsed,
    wrongGuesses,
    shake,
    revealHint,
    submitGuess,
    giveUp,
  };
}
