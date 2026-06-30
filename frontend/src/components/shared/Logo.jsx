import { FiTrendingUp } from "react-icons/fi";

export default function Logo({ className = "text-3xl" }) {
  return (
    <div className={`flex items-center justify-center gap-2.5 font-extrabold tracking-tight ${className}`}>
      <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-indigo-500/30 text-white transform hover:rotate-6 transition-transform duration-300">
        <FiTrendingUp className="w-6 h-6 stroke-[2.5]" />
      </div>
      <span className="bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-700 bg-clip-text text-transparent">
        Artha<span className="text-blue-600 font-black">Netra</span>
      </span>
    </div>
  );
}
