import { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { normalizeName, WRONG_GUESS_COST } from "../utils/scoring";

export default function GuessInput({
  allPlayers,
  onSubmit,
  wrongGuesses,
  shake,
  disabled,
  onGiveUp,
}) {
  const [value, setValue] = useState("");
  const [activeIdx, setActiveIdx] = useState(-1);
  const [open, setOpen] = useState(false);
  const inputRef = useRef(null);
  const submitRef = useRef(null);
  const formRef = useRef(null);

  const suggestions = useMemo(() => {
    const q = normalizeName(value);
    if (q.length < 2) return [];
    return allPlayers
      .filter((p) => normalizeName(p.name).includes(q))
      .slice(0, 8);
  }, [value, allPlayers]);

  // Trigger shake animation on the form when shake counter changes.
  useEffect(() => {
    if (!formRef.current || shake === 0) return;
    const el = formRef.current;
    el.classList.remove("animate-shake");
    // Force reflow so the animation can replay.
    void el.offsetWidth;
    el.classList.add("animate-shake");
  }, [shake]);

  // Focus input on mount and when re-enabled.
  useEffect(() => {
    if (!disabled) inputRef.current?.focus();
  }, [disabled]);

  function pick(p) {
    setValue(p.name);
    setOpen(false);
    setActiveIdx(-1);
    requestAnimationFrame(() => submitRef.current?.focus());
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (disabled || !value.trim()) return;
    onSubmit(value.trim());
    setValue("");
    setOpen(false);
    setActiveIdx(-1);
    inputRef.current?.focus();
  }

  function handleKeyDown(e) {
    if (!open || suggestions.length === 0) {
      if (e.key === "ArrowDown" && suggestions.length > 0) {
        setOpen(true);
        setActiveIdx(0);
        e.preventDefault();
      }
      return;
    }
    if (e.key === "ArrowDown") {
      setActiveIdx((i) => Math.min(suggestions.length - 1, i + 1));
      e.preventDefault();
    } else if (e.key === "ArrowUp") {
      setActiveIdx((i) => Math.max(0, i - 1));
      e.preventDefault();
    } else if (e.key === "Enter" && activeIdx >= 0) {
      e.preventDefault();
      pick(suggestions[activeIdx]);
    } else if (e.key === "Escape") {
      setOpen(false);
      setActiveIdx(-1);
    }
  }

  return (
    <div className="space-y-2">
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="space-y-2"
      >
        <div className="relative">
          <input
            ref={inputRef}
            type="text"
            value={value}
            onChange={(e) => {
              setValue(e.target.value);
              setOpen(true);
              setActiveIdx(-1);
            }}
            onFocus={() => setOpen(true)}
            onBlur={() => setTimeout(() => setOpen(false), 120)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Guess the player…"
            autoComplete="off"
            spellCheck={false}
            className="w-full px-4 py-3 min-h-[48px] rounded-xl bg-slate-900 ring-1 ring-slate-700 focus:ring-2 focus:ring-indigo-500/60 focus:outline-none text-white placeholder-slate-500 disabled:opacity-50"
          />
          {open && suggestions.length > 0 && (
            <ul
              role="listbox"
              className="absolute left-0 right-0 mt-1 bg-slate-900 ring-1 ring-slate-700 rounded-xl shadow-2xl overflow-hidden z-20 max-h-72 overflow-y-auto"
            >
              {suggestions.map((s, i) => (
                <li
                  key={s.id}
                  role="option"
                  aria-selected={i === activeIdx}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    pick(s);
                  }}
                  onMouseEnter={() => setActiveIdx(i)}
                  className={`px-4 py-2.5 cursor-pointer flex items-center justify-between gap-2 min-h-[44px] ${
                    i === activeIdx ? "bg-slate-800" : ""
                  }`}
                >
                  <span className="text-slate-100">{s.name}</span>
                  <span className="text-xs text-slate-500">
                    {s.nationality_code}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="flex gap-2">
          <button
            ref={submitRef}
            type="submit"
            disabled={disabled || !value.trim()}
            className="flex-1 min-h-[48px] rounded-xl bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed font-semibold text-white transition-colors"
          >
            Guess
          </button>
          <button
            type="button"
            onClick={onGiveUp}
            disabled={disabled}
            className="flex-1 min-h-[48px] rounded-xl bg-slate-700 hover:bg-slate-600 active:bg-slate-700/70 disabled:opacity-40 disabled:cursor-not-allowed font-semibold text-slate-100 transition-colors"
          >
            Give up
          </button>
        </div>
      </form>

      <AnimatePresence initial={false}>
        {wrongGuesses.length > 0 && (
          <motion.ul
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-1"
          >
            {wrongGuesses.map((g, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -6 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center justify-between text-sm bg-red-500/10 ring-1 ring-red-500/30 rounded-lg px-3 py-1.5"
              >
                <span className="line-through text-red-300">{g.guess}</span>
                <span className="text-xs text-red-400 font-medium">
                  −{g.deduction ?? WRONG_GUESS_COST} pts
                </span>
              </motion.li>
            ))}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  );
}
