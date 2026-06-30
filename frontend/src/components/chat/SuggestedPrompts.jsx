import { FiZap, FiPieChart, FiShield, FiAward, FiTrendingUp, FiArrowUpRight } from "react-icons/fi";

function SuggestedPrompts({ onPromptClick }) {
  const promptData = [
    {
      text: "Help me create a monthly budget",
      icon: FiPieChart,
      category: "Planning",
      gradient: "from-blue-500/20 to-cyan-500/20 hover:border-cyan-500/50 text-cyan-300",
    },
    {
      text: "Check if this loan is safe",
      icon: FiShield,
      category: "Security",
      gradient: "from-purple-500/20 to-pink-500/20 hover:border-pink-500/50 text-pink-300",
    },
    {
      text: "Find government schemes",
      icon: FiAward,
      category: "Benefits",
      gradient: "from-amber-500/20 to-orange-500/20 hover:border-amber-500/50 text-amber-300",
    },
    {
      text: "Improve my Financial Health Score",
      icon: FiTrendingUp,
      category: "Growth",
      gradient: "from-emerald-500/20 to-teal-500/20 hover:border-emerald-500/50 text-emerald-300",
    },
  ];

  return (
    <div className="border-t border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-6 py-4 transition-all">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
        <FiSparkles className="w-3.5 h-3.5 text-blue-400 animate-pulse" />
        <span>Suggested AI Queries</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
        {promptData.map((item) => {
          const IconComponent = item.icon;
          return (
            <button
              key={item.text}
              onClick={() => onPromptClick && onPromptClick(item.text)}
              className={`group flex items-center justify-between gap-3 text-left bg-slate-800/50 hover:bg-gradient-to-r ${item.gradient} border border-slate-700/60 rounded-xl px-3.5 py-2.5 transition-all duration-200 transform hover:-translate-y-0.5 shadow-sm`}
            >
              <div className="flex items-center gap-2.5 overflow-hidden">
                <div className="p-1.5 rounded-lg bg-slate-800/80 group-hover:bg-slate-900/60 border border-slate-700/50 shrink-0 transition-colors">
                  <IconComponent className="w-4 h-4 text-slate-300 group-hover:text-white transition-colors" />
                </div>
                <span className="text-xs font-medium text-slate-300 group-hover:text-white truncate transition-colors">
                  {item.text}
                </span>
              </div>
              <FiArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-white shrink-0 opacity-0 group-hover:opacity-100 transition-all transform group-hover:translate-x-0.5 -translate-x-1" />
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default SuggestedPrompts;