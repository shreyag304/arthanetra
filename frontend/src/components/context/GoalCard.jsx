import { FiTarget, FiArrowRight } from "react-icons/fi";

function GoalCard({ goal = "Increase Savings" }) {
  return (
    <div className="bg-slate-800/60 hover:bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 shadow-md transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-pink-500/10 border border-pink-500/20 text-pink-400">
            <FiTarget className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Active Financial Goal
            </h3>
            <span className="text-[11px] text-slate-500">Primary Objective</span>
          </div>
        </div>

        <span className="text-[11px] font-bold text-pink-400 bg-pink-500/10 border border-pink-500/20 px-2.5 py-0.5 rounded-full">
          In Progress
        </span>
      </div>

      <div className="mt-2.5 bg-gradient-to-r from-slate-900 via-slate-900/90 to-pink-950/30 rounded-xl p-3.5 border border-pink-500/20 flex items-center justify-between">
        <span className="text-sm font-bold text-white tracking-wide">{goal}</span>
        <button className="flex items-center gap-1 text-[11px] text-pink-400 hover:text-pink-300 font-semibold group/btn transition-colors">
          Optimize
          <FiArrowRight className="w-3 h-3 transform group-hover/btn:translate-x-0.5 transition-transform" />
        </button>
      </div>
    </div>
  );
}

export default GoalCard;