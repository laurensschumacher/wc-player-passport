import ClubLogo from "./ClubLogo";

/**
 * Vertical football pitch with players placed by formation. Goalkeeper at
 * the bottom, forwards at the top. Formation string is "DEF-MID-FWD" (e.g.
 * "4-3-3"). The 11 players are expected to be ordered GK -> DEF -> MID ->
 * FWD with the slot count matching the formation.
 */
function parseFormation(formation) {
  const parts = (formation || "4-3-3").split("-").map((n) => parseInt(n, 10));
  const [def, mid, fwd] = parts.length === 3 ? parts : [4, 3, 3];
  return { def, mid, fwd };
}

function rowYs() {
  // Y % positions for 4 rows from goalkeeper (bottom) to forwards (top).
  return { gk: 92, def: 72, mid: 50, fwd: 24 };
}

function rowXs(n) {
  // Evenly spread n players across the pitch width with margins.
  if (n <= 0) return [];
  const inset = 10;
  const span = 100 - inset * 2;
  if (n === 1) return [50];
  return Array.from({ length: n }, (_, i) => inset + (span * i) / (n - 1));
}

export default function PitchDiagram({ players, formation, revealNames }) {
  const f = parseFormation(formation);
  const ys = rowYs();
  // Bucket players by position; preserve order they were given (which
  // matches squad-number order from the scraper).
  const gks = players.filter((p) => p.pos === "GK");
  const defs = players.filter((p) => p.pos === "DEF");
  const mids = players.filter((p) => p.pos === "MID");
  const fwds = players.filter((p) => p.pos === "FWD");

  const slots = [];
  const place = (list, n, y) => {
    const xs = rowXs(n);
    for (let i = 0; i < n; i++) {
      const p = list[i];
      if (!p) continue;
      slots.push({ p, x: xs[i], y });
    }
  };
  place(gks, 1, ys.gk);
  place(defs, f.def, ys.def);
  place(mids, f.mid, ys.mid);
  place(fwds, f.fwd, ys.fwd);

  return (
    <div
      className="relative w-full overflow-hidden rounded-2xl ring-1 ring-emerald-900/40 shadow-inner"
      style={{ aspectRatio: "2 / 3" }}
    >
      {/* Pitch background + markings */}
      <svg
        viewBox="0 0 100 150"
        preserveAspectRatio="none"
        className="absolute inset-0 w-full h-full"
        aria-hidden
      >
        {/* Stripes */}
        <defs>
          <pattern id="grass" width="100" height="15" patternUnits="userSpaceOnUse">
            <rect width="100" height="15" fill="#15803d" />
            <rect width="100" height="7.5" fill="#166534" />
          </pattern>
        </defs>
        <rect x="0" y="0" width="100" height="150" fill="url(#grass)" />
        {/* Outer line */}
        <rect
          x="3" y="3" width="94" height="144"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        {/* Halfway line */}
        <line
          x1="3" y1="75" x2="97" y2="75"
          stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        {/* Centre circle */}
        <circle
          cx="50" cy="75" r="9"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        <circle cx="50" cy="75" r="0.6" fill="rgba(255,255,255,0.7)" />
        {/* Top penalty area (forwards attack here) */}
        <rect
          x="22" y="3" width="56" height="16"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        <rect
          x="35" y="3" width="30" height="6"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        {/* Bottom penalty area (GK) */}
        <rect
          x="22" y="131" width="56" height="16"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
        <rect
          x="35" y="141" width="30" height="6"
          fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="0.4"
        />
      </svg>

      {/* Players */}
      <div className="absolute inset-0">
        {slots.map((s, i) => (
          <PlayerSlot
            key={`${s.p.no}-${i}`}
            player={s.p}
            x={s.x}
            y={s.y}
            revealName={revealNames}
          />
        ))}
      </div>
    </div>
  );
}

function PlayerSlot({ player, x, y, revealName }) {
  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-1"
      style={{ left: `${x}%`, top: `${y}%` }}
    >
      <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-white ring-2 ring-emerald-200 shadow flex items-center justify-center overflow-hidden">
        <ClubLogo name={player.club} size={40} />
      </div>
      <div className="text-[10px] sm:text-xs font-semibold text-white text-center max-w-[88px] leading-tight drop-shadow-[0_1px_1px_rgba(0,0,0,0.9)]">
        {revealName ? (
          <>
            <div>
              {player.name}
              {player.is_captain ? " (C)" : ""}
            </div>
            <div className="text-white/70 font-medium">{player.club}</div>
          </>
        ) : (
          <div className="truncate">{player.club}</div>
        )}
      </div>
    </div>
  );
}
