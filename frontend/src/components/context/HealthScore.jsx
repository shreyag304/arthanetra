import { FiActivity, FiTrendingUp } from "react-icons/fi";

function HealthScore({ score = 72 }) {
  const getStatus = (val) => {
    if (val >= 75) return { label: "Excellent", color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", bar: "from-emerald-500 to-teal-400" };
    if (val >= 60) return { label: "Good", color: "text-blue-400 bg-blue-500/10 border-blue-500/30", bar: "from-blue-500 to-indigo-400" };
    return { label: "Needs Work", color: "text-amber-400 bg-amber-500/10 border-amber-500/30", bar: "from-amber-500 to-orange-400" };
  };

  const status = getStatus(score);

  return (
    <div className="bg-slate-800/60 hover:bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 mb-4 shadow-md transition-all duration-300 group">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400">
            <FiActivity className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Financial Health Score
            </h3>
            <span className="text-[11px] text-slate-500">AI Assessed Index</span>
          </div>
        </div>

        <span className={`text-xs px-2.5 py-1 rounded-full font-semibold border ${status.color}`}>
          {status.label}
        </span>
      </div>

      <div className="flex items-baseline justify-between mb-3 mt-1">
        <div className="flex items-baseline gap-1.5">
          <span className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            {score}
          </span>
          <span className="text-sm font-medium text-slate-400">/ 100</span>
        </div>

        <div className="flex items-center gap-1 text-xs text-emerald-400 font-medium bg-emerald-500/10 px-2 py-1 rounded-lg">
          <FiTrendingUp className="w-3.5 h-3.5" />
          <span>+4 pts MoM</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-900/80 h-2.5 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
        <div
          className={`h-full bg-gradient-to-r ${status.bar} rounded-full transition-all duration-700 ease-out`}
          style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
        ></div>
      </div>
    </div>
  );
}

export default HealthScore;