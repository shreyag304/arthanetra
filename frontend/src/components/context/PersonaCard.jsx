import { FiShield, FiEdit3 } from "react-icons/fi";

function PersonaCard({ userName, persona = "Student", incomeType = "Variable", onEditProfile }) {
  const displayName = userName || localStorage.getItem("user_name") || "ArthaNetra User";

  return (
    <div
      onClick={onEditProfile}
      className="group bg-slate-800/60 hover:bg-slate-800/90 border border-slate-700/80 hover:border-indigo-500/50 rounded-2xl p-5 mb-4 shadow-md transition-all duration-300 cursor-pointer relative overflow-hidden"
    >
      <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-xl pointer-events-none group-hover:bg-indigo-500/10 transition-all"></div>

      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xs shadow-md shadow-purple-500/20">
            {displayName.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h3 className="text-sm font-bold text-white tracking-wide group-hover:text-indigo-300 transition-colors">
                {displayName}
              </h3>
              <FiEdit3 className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-400 transition-colors" />
            </div>
            <span className="text-[11px] text-slate-400">Click to edit occupation & goal</span>
          </div>
        </div>

        <span className="flex items-center gap-1 text-[10px] text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-full font-medium">
          <FiShield className="w-3 h-3" />
          Verified
        </span>
      </div>

      <div className="mt-3 flex items-center justify-between bg-slate-900/70 rounded-xl p-3.5 border border-slate-700/60 group-hover:border-slate-600/80 transition-all">
        <div>
          <span className="text-[10px] uppercase font-semibold text-slate-400 block tracking-wider">Occupation Persona</span>
          <span className="text-sm font-bold text-white tracking-wide">{persona}</span>
        </div>
        <div className="text-right">
          <span className="text-[10px] uppercase font-semibold text-slate-400 block tracking-wider">Income Profile</span>
          <span className="text-xs font-semibold text-purple-300">{incomeType || "Variable"}</span>
        </div>
      </div>
    </div>
  );
}

export default PersonaCard;