export const STARTING_SCORE = 100;
export const HINT_COST = 10;
export const CLUBS_HINT_COST = 25;
export const WRONG_GUESS_COST = 10;
export const CORRECT_FLOOR = 50;
export const QUESTIONS_PER_ROUND = 5;
export const MAX_ROUND_SCORE = STARTING_SCORE * QUESTIONS_PER_ROUND;

/**
 * Given the round state, compute the live score (what the player currently has).
 * - Starts at STARTING_SCORE (100)
 * - −HINT_COST if the position hint was revealed
 * - −CLUBS_HINT_COST if the career-clubs hint was revealed
 * - −WRONG_GUESS_COST per wrong guess
 * - Floored at CORRECT_FLOOR while still playing
 */
export function liveScore({ hintUsed, clubsHintUsed, wrongCount }) {
  const raw =
    STARTING_SCORE -
    (hintUsed ? HINT_COST : 0) -
    (clubsHintUsed ? CLUBS_HINT_COST : 0) -
    wrongCount * WRONG_GUESS_COST;
  return Math.max(CORRECT_FLOOR, raw);
}

/**
 * Final score awarded at the end of the round.
 * - Correct guess: same as liveScore (always >= CORRECT_FLOOR)
 * - Gave up: 0 points
 */
export function finalScore({ status, hintUsed, clubsHintUsed, wrongCount }) {
  if (status === "won") return liveScore({ hintUsed, clubsHintUsed, wrongCount });
  if (status === "gave-up") return 0;
  return liveScore({ hintUsed, clubsHintUsed, wrongCount });
}

/**
 * Normalize a name for comparison: lowercase, strip diacritics, collapse
 * whitespace and remove punctuation. Used both for autocomplete matching and
 * for guess validation.
 */
export function normalizeName(s) {
  return (s || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[.'`’\-]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

/**
 * Returns true if `guess` should be considered a correct match for `target`.
 * Accepts:
 *   - exact normalized match of the full name
 *   - exact normalized match of the last token (surname-only guess)
 *   - exact normalized match of the first token if it is at least 5 chars
 *     (covers mononyms / well-known short names like "Ronaldo", "Pepe")
 *   - either side may carry a common generational suffix
 *     ("jr", "sr", "junior", "senior", "ii", "iii", "iv") which is stripped
 *     before comparison — so "Neymar Jr" matches the mononym "Neymar".
 */
const NAME_SUFFIXES = new Set([
  "jr",
  "sr",
  "junior",
  "senior",
  "ii",
  "iii",
  "iv",
]);

function stripNameSuffixes(tokens) {
  let end = tokens.length;
  while (end > 1 && NAME_SUFFIXES.has(tokens[end - 1])) end -= 1;
  return tokens.slice(0, end);
}

export function matchesPlayer(guess, target) {
  const g = normalizeName(guess);
  const t = normalizeName(target);
  if (!g || !t) return false;
  if (g === t) return true;

  const gTokens = stripNameSuffixes(g.split(" "));
  const tTokens = stripNameSuffixes(t.split(" "));
  const gStripped = gTokens.join(" ");
  const tStripped = tTokens.join(" ");
  if (gStripped === tStripped) return true;

  if (tTokens.length > 1) {
    if (gStripped === tTokens[tTokens.length - 1]) return true;
    if (tTokens[0].length >= 5 && gStripped === tTokens[0]) return true;
  }
  return false;
}
