import { FiCpu } from "react-icons/fi";

function TypingIndicator() {
  return (
    <div className="flex items-start gap-3.5 sm:gap-4 animate-fadeIn">
      {/* Avatar */}
      <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-blue-600 to-emerald-400 text-white flex items-center justify-center shrink-0 shadow-md shadow-indigo-500/20">
        <FiCpu className="w-4 h-4 stroke-[2.5] animate-spin" style={{ animationDuration: "3s" }} />
      </div>

      {/* Bubble */}
      <div className="flex flex-col items-start">
        <span className="text-xs font-semibold text-slate-400 mb-1 px-1">
          ArthaNetra AI
        </span>
        <div className="bg-slate-800/90 backdrop-blur-md border border-slate-700/80 rounded-2xl rounded-tl-xs px-5 py-3.5 shadow-lg shadow-black/30 flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: "0ms" }}></span>
            <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: "150ms" }}></span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: "300ms" }}></span>
          </div>
          <span className="text-xs sm:text-sm font-medium bg-gradient-to-r from-blue-300 to-emerald-300 bg-clip-text text-transparent">
            Synthesizing financial advice...
          </span>
        </div>
      </div>
    </div>
  );
}

export default TypingIndicator;