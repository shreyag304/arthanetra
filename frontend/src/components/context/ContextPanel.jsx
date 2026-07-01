import HealthScore from "./HealthScore";
import PersonaCard from "./PersonaCard";
import SchemeCard from "./SchemeCard";
import GoalCard from "./GoalCard";
import { FiBarChart2, FiShield } from "react-icons/fi";

function ContextPanel({ context = {}, connectionStatus = "connected", onGoalClick, onFhsUpdate }) {
  const isWsConnected = connectionStatus === "connected";
  const isWsConnecting = connectionStatus === "connecting";

  return (
    <div className="h-full bg-slate-900/85 backdrop-blur-2xl border-l border-slate-800/80 p-5 sm:p-6 overflow-y-auto flex flex-col justify-between scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800/80">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <FiBarChart2 className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">
                Live AI Telemetry
              </h2>
              <p className="text-[11px] text-slate-400">Real-time user intelligence</p>
            </div>
          </div>
          <span
            className={`flex items-center gap-1.5 text-[10px] uppercase font-bold px-2.5 py-1 rounded-full border ${
              isWsConnected
                ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
                : isWsConnecting
                ? "text-amber-400 bg-amber-500/10 border-amber-500/20"
                : "text-blue-400 bg-blue-500/10 border-blue-500/20"
            }`}
          >
            <span
              className={`w-1.5 h-1.5 rounded-full ${
                isWsConnected ? "bg-emerald-400 animate-pulse" : isWsConnecting ? "bg-amber-400 animate-ping" : "bg-blue-400"
              }`}
            ></span>
            {isWsConnected ? "WS Live Stream" : isWsConnecting ? "Connecting WS" : "HTTP Telemetry"}
          </span>
        </div>

        {/* Cards Stack */}
        <div className="space-y-4">
          <HealthScore score={context.financial_health_score} onUpdateScore={onFhsUpdate} />
          <PersonaCard persona={context.persona} incomeType={context.income_type} />
          <SchemeCard schemes={context.eligible_schemes || []} />
          <GoalCard goal={context.goal} onOptimize={onGoalClick} />
        </div>
      </div>

      {/* Footer Info */}
      <div className="mt-8 pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
        <span className="flex items-center gap-1">
          <FiShield className="text-blue-400" />
          End-to-End Secure
        </span>
        <span>ArthaNetra Core v2.4</span>
      </div>
    </div>
  );
}

export default ContextPanel;