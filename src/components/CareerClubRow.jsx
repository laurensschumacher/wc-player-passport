import { motion } from "framer-motion";
import ClubLogo from "./ClubLogo";

export default function CareerClubRow({ club, index }) {
  const range =
    club.start_year && club.end_year
      ? club.start_year === club.end_year
        ? `${club.start_year}`
        : `${club.start_year}–${club.end_year}`
      : club.start_year
        ? `${club.start_year}–`
        : "";

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      transition={{ delay: 0.03 * index, duration: 0.25, ease: "easeOut" }}
      className="flex items-center gap-3 px-4 py-2 border-t border-slate-800/60 bg-slate-900/40"
    >
      <div className="text-xs font-semibold text-slate-400 w-14 tabular-nums">
        {range}
      </div>
      <ClubLogo name={club.club} size={22} />
      <div className="flex-1 min-w-0 text-sm text-slate-300 truncate">
        {club.club}
      </div>
    </motion.div>
  );
}
