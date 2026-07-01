import { FiUserCheck, FiShield } from "react-icons/fi";

function PersonaCard({ persona = "Student", incomeType = "Variable" }) {
  return (
    <div className="bg-slate-800/60 hover:bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 mb-4 shadow-md transition-all duration-300">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400">
            <FiUserCheck className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              User Profile
            </h3>
            <span className="text-[11px] text-slate-500">Active Demographic</span>
          </div>
        </div>

        <span className="flex items-center gap-1 text-[11px] text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 rounded-full font-medium">
          <FiShield className="w-3 h-3" />
          Verified
        </span>
      </div>

      <div className="mt-3 flex items-center justify-between bg-slate-900/60 rounded-xl p-3.5 border border-slate-700/60">
        <div>
          <span className="text-[11px] text-slate-400 block">Assigned Persona</span>
          <span className="text-base font-bold text-white tracking-wide">{persona}</span>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 block">Income Type</span>
          <span className="text-xs font-semibold text-purple-300">{incomeType || "Variable"}</span>
        </div>
      </div>
    </div>
  );
}

export default PersonaCard;