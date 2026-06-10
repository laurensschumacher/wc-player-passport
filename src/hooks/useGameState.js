import { useCallback, useState } from "react";
import {
  CLUBS_HINT_COST,
  CORRECT_FLOOR,
  HINT_COST,
  STARTING_SCORE,
  WRONG_GUESS_COST,
  finalScore,
  liveScore,
  matchesPlayer,
} from "../utils/scoring";

/**
 * Round-level state machine: tracks score, guesses, hint usage, and
 * win/give-up status for one round. Resets when `player` changes.
 */
export function useGameState(player) {
  const [hintUsed, setHintUsed] = useState(false);
  const [clubsHintUsed, setClubsHintUsed] = useState(false);
  const [wrongGuesses, setWrongGuesses] = useState([]); // [{guess, deduction}]
  const [status, setStatus] = useState("playing"); // playing | won | gave-up
  const [shake, setShake] = useState(0); // increments on wrong guess (anim trigger)

  // Reset synchronously when the player changes so the new player never
  // renders with the previous round's status (which would briefly reveal
  // the answer / hints on the new card).
  const [prevPlayerId, setPrevPlayerId] = useState(player?.id);
  if (player?.id !== prevPlayerId) {
    setPrevPlayerId(player?.id);
    setHintUsed(false);
    setClubsHintUsed(false);
    setWrongGuesses([]);
    setStatus("playing");
    setShake(0);
  }

  const score = liveScore({
    hintUsed,
    clubsHintUsed,
    wrongCount: wrongGuesses.length,
  });

  const revealHint = useCallback(() => {
    if (hintUsed || status !== "playing") return;
    setHintUsed(true);
  }, [hintUsed, status]);

  const revealClubsHint = useCallback(() => {
    if (clubsHintUsed || status !== "playing") return;
    setClubsHintUsed(true);
  }, [clubsHintUsed, status]);

  const submitGuess = useCallback(
    (guess) => {
      if (status !== "playing" || !player) return { ok: false };
      const trimmed = (guess || "").trim();
      if (!trimmed) return { ok: false };
      if (matchesPlayer(trimmed, player.name)) {
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
    [player, status],
  );

  const giveUp = useCallback(() => {
    if (status !== "playing") return;
    setStatus("gave-up");
  }, [status]);

  const final = finalScore({
    status,
    hintUsed,
    clubsHintUsed,
    wrongCount: wrongGuesses.length,
  });

  return {
    status,
    score,
    finalScoreValue: final,
    hintUsed,
    clubsHintUsed,
    wrongGuesses,
    shake,
    revealHint,
    revealClubsHint,
    submitGuess,
    giveUp,
    constants: {
      STARTING_SCORE,
      HINT_COST,
      CLUBS_HINT_COST,
      WRONG_GUESS_COST,
      CORRECT_FLOOR,
    },
  };
}
