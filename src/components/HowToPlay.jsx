import { motion, AnimatePresence } from "framer-motion";

export default function HowToPlay({ open, onClose }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-end sm:items-center justify-center p-3"
        >
          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 30, opacity: 0 }}
            transition={{ type: "spring", stiffness: 280, damping: 26 }}
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-md bg-slate-900 ring-1 ring-slate-800 rounded-2xl p-5 space-y-4"
          >
            <div className="flex items-start justify-between">
              <h2 className="text-xl font-bold text-white">How to play</h2>
              <button
                type="button"
                onClick={onClose}
                aria-label="Close"
                className="text-slate-400 hover:text-white text-xl leading-none px-2 py-1"
              >
                ×
              </button>
            </div>
            <ul className="space-y-3 text-sm text-slate-300">
              <li>
                <span className="text-slate-100 font-semibold">Goal:</span> name
                the mystery footballer from their World Cup career.
              </li>
              <li>
                Each row shows one tournament: year, games, goals, and the club
                they were at during that World Cup. Their nationality flag is a
                free clue at the top.
              </li>
              <li>
                <span className="text-slate-100 font-semibold">Round:</span> 8
                player passports per round.
              </li>
              <li>
                <span className="text-slate-100 font-semibold">Score:</span>{" "}
                start each question at{" "}
                <span className="font-semibold">100</span>. Each wrong guess is{" "}
                <span className="font-semibold">−10</span>, floored at{" "}
                <span className="font-semibold">50</span>. Giving up gives{" "}
                <span className="font-semibold">0</span>. Max round score:{" "}
                <span className="font-semibold">800</span>.
              </li>
              <li>
                <span className="text-slate-100 font-semibold">Hints:</span>{" "}
                <span className="font-semibold">−10</span> to reveal the
                position,{" "}
                <span className="font-semibold">−25</span> to reveal every club
                they've ever played for with year ranges.
              </li>
              <li>
                Type to search the dataset; pick from the dropdown or type the
                full name.
              </li>
            </ul>
            <button
              type="button"
              onClick={onClose}
              className="w-full min-h-[48px] mt-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-semibold text-white"
            >
              Let's play
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
