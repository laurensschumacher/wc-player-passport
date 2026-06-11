import { useState } from "react";
import PlayerPassportApp from "./PlayerPassportApp";
import LineupPassportApp from "./LineupPassportApp";

const MODE_KEY = "playport.mode";

export default function App() {
  const [mode, setMode] = useState(() => {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(MODE_KEY) || null;
  });

  function pick(m) {
    setMode(m);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(MODE_KEY, m);
    }
  }

  function exit() {
    setMode(null);
    if (typeof window !== "undefined") {
      window.localStorage.removeItem(MODE_KEY);
    }
  }

  if (mode === "player") return <PlayerPassportApp onExitMode={exit} />;
  if (mode === "lineup") return <LineupPassportApp onExitMode={exit} />;

  return <ModePicker onPick={pick} />;
}

function ModePicker({ onPick }) {
  return (
    <div className="min-h-full flex flex-col text-slate-100">
      <header className="px-4 sm:px-6 py-6 max-w-2xl w-full mx-auto text-center">
        <div className="text-4xl mb-2" aria-hidden>
          ⚽📘
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
          Playport
        </h1>
        <p className="text-slate-400 mt-2 text-sm">
          Pick a game mode to get started.
        </p>
      </header>

      <main className="flex-1 px-4 sm:px-6 pb-24 max-w-2xl w-full mx-auto space-y-4">
        <ModeCard
          title="Player Passport"
          subtitle="Guess the player from their World Cup history"
          icon="📘⚽"
          onClick={() => onPick("player")}
        />
        <ModeCard
          title="Lineup Passport"
          subtitle="Guess the national team from their starting XI's clubs"
          icon="🥅⚽"
          onClick={() => onPick("lineup")}
          badge="2026"
        />
      </main>
    </div>
  );
}

function ModeCard({ title, subtitle, icon, onClick, badge }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full text-left bg-slate-900 ring-1 ring-slate-800 hover:ring-indigo-500/50 rounded-2xl p-5 shadow-xl transition-all flex items-center gap-4 min-h-[88px]"
    >
      <span className="text-4xl shrink-0" aria-hidden>
        {icon}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h2 className="text-lg font-bold text-white">{title}</h2>
          {badge && (
            <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/20 ring-1 ring-indigo-500/50 text-indigo-300 font-semibold">
              {badge}
            </span>
          )}
        </div>
        <p className="text-sm text-slate-400 mt-0.5">{subtitle}</p>
      </div>
      <span className="text-slate-500 text-xl" aria-hidden>
        →
      </span>
    </button>
  );
}
