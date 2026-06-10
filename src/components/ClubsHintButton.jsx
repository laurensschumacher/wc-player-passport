import { CLUBS_HINT_COST } from "../utils/scoring";

export default function ClubsHintButton({ revealed, onReveal, disabled, hasData }) {
  if (revealed || !hasData) return null;
  return (
    <button
      type="button"
      onClick={onReveal}
      disabled={disabled}
      className="w-full inline-flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 active:bg-slate-700/70 ring-1 ring-slate-700 text-sm font-medium text-slate-200 transition-colors min-h-[44px] disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span aria-hidden>🏟️</span>
      Reveal all clubs
      <span className="text-slate-400">−{CLUBS_HINT_COST} pts</span>
    </button>
  );
}
