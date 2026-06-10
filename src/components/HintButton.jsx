export default function HintButton({ icon, label, cost, onReveal, disabled }) {
  return (
    <button
      type="button"
      onClick={onReveal}
      disabled={disabled}
      className="w-full inline-flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 active:bg-slate-700/70 ring-1 ring-slate-700 text-sm font-medium text-slate-200 transition-colors min-h-[44px] disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {icon && <span aria-hidden>{icon}</span>}
      {label}
      <span className="text-slate-400">−{cost} pts</span>
    </button>
  );
}
