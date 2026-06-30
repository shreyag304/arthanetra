import { FiAward, FiCheckCircle, FiExternalLink } from "react-icons/fi";

function SchemeCard({ schemes = [] }) {
  return (
    <div className="bg-slate-800/60 hover:bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 mb-4 shadow-md transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
            <FiAward className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Eligible Schemes
            </h3>
            <span className="text-[11px] text-slate-500">Government Support</span>
          </div>
        </div>

        <span className="text-xs font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-full">
          {schemes.length} Active
        </span>
      </div>

      <div className="space-y-2 mt-3">
        {schemes.length === 0 ? (
          <p className="text-xs text-slate-400 italic py-2">No specific schemes detected yet.</p>
        ) : (
          schemes.map((scheme) => (
            <div
              key={scheme}
              className="flex items-center justify-between bg-slate-900/70 hover:bg-slate-900 border border-slate-700/60 hover:border-amber-500/40 rounded-xl px-3.5 py-2.5 transition-all group"
            >
              <div className="flex items-center gap-2.5">
                <FiCheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="text-xs sm:text-sm font-medium text-slate-200 group-hover:text-white transition-colors">
                  {scheme}
                </span>
              </div>
              <FiExternalLink className="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-400 transition-colors shrink-0 cursor-pointer" />
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SchemeCard;