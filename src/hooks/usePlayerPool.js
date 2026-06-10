import { useCallback, useMemo, useRef, useState } from "react";
import data from "../data/world_cup_players.json";

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Loads the dataset, filters to validated players, maintains a shuffled
 * pool with no repeats until exhausted, then reshuffles and notifies via
 * the `reshuffled` flag.
 */
export function usePlayerPool() {
  const validated = useMemo(
    () =>
      (data.players || []).filter(
        (p) => p.validation_status === "validated" && p.world_cups?.length > 0,
      ),
    [],
  );

  const [pool, setPool] = useState(() => shuffle(validated));
  const [index, setIndex] = useState(0);
  const [reshuffleToken, setReshuffleToken] = useState(0);
  const seenRef = useRef(new Set());

  const current = pool[index] ?? null;
  if (current) seenRef.current.add(current.id);

  const advance = useCallback(() => {
    setIndex((i) => {
      const next = i + 1;
      if (next >= pool.length) {
        // Pool exhausted — reshuffle, signal toast.
        setPool(shuffle(validated));
        setReshuffleToken((t) => t + 1);
        seenRef.current = new Set();
        return 0;
      }
      return next;
    });
  }, [pool.length, validated]);

  return {
    allPlayers: validated,
    current,
    advance,
    reshuffleToken,
    poolSize: validated.length,
    roundsRemaining: pool.length - index,
  };
}
