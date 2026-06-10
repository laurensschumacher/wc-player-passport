import { motion } from "framer-motion";
import { HINT_COST } from "../utils/scoring";

const POSITION_STYLES = {
  GK: "bg-yellow-500/20 text-yellow-300 ring-yellow-500/40",
  DEF: "bg-blue-500/20 text-blue-300 ring-blue-500/40",
  MID: "bg-emerald-500/20 text-emerald-300 ring-emerald-500/40",
  ATT: "bg-red-500/20 text-red-300 ring-red-500/40",
};

export default function HintButton({ revealed, position, onReveal, disabled }) {
  if (revealed || disabled) {
    const style = POSITION_STYLES[position] || "bg-slate-700 text-slate-200";
    return (
      <motion.div
        key="badge"
        initial={{ scale: 0.6, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", stiffness: 400, damping: 18 }}
        className={`inline-flex items-center justify-center px-3 py-1 rounded-full text-sm font-bold tracking-wide ring-1 ${style}`}
      >
        {position}
      </motion.div>
    );
  }

  return (
    <button
      type="button"
      onClick={onReveal}
      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 active:bg-slate-700/70 ring-1 ring-slate-700 text-xs font-medium text-slate-300 transition-colors min-h-[36px]"
    >
      Position?
      <span className="text-slate-400">−{HINT_COST}pts</span>
    </button>
  );
}
