import { useCallback, useMemo, useRef, useState } from "react";
import data from "../data/lineups.json";

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Lineup-mode equivalent of usePlayerPool: cycles through the 48 World Cup
 * teams, reshuffling once exhausted and emitting a token so the UI can
 * surface a "you've seen them all" toast.
 */
export function useLineupPool() {
  const teams = useMemo(() => data.teams || [], []);

  const [pool, setPool] = useState(() => shuffle(teams));
  const [index, setIndex] = useState(0);
  const [reshuffleToken, setReshuffleToken] = useState(0);
  const seenRef = useRef(new Set());

  const current = pool[index] ?? null;
  if (current) seenRef.current.add(current.code);

  const advance = useCallback(() => {
    setIndex((i) => {
      const next = i + 1;
      if (next >= pool.length) {
        setPool(shuffle(teams));
        setReshuffleToken((t) => t + 1);
        seenRef.current = new Set();
        return 0;
      }
      return next;
    });
  }, [pool.length, teams]);

  return {
    allTeams: teams,
    current,
    advance,
    reshuffleToken,
    poolSize: teams.length,
  };
}
