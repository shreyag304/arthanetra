import { FiGlobe } from "react-icons/fi";

function LanguageSelector({ language, setLanguage }) {
  const languages = [
    "English",
    "Hindi",
    "Marathi",
    "Gujarati",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Punjabi",
    "Odia",
    "Assamese",
  ];

  return (
    <div className="relative inline-flex items-center gap-2 bg-slate-900/80 hover:bg-slate-800/90 border border-slate-700/80 rounded-xl px-3 py-1.5 shadow-sm transition-all duration-200">
      <FiGlobe className="w-4 h-4 text-blue-400 shrink-0 animate-pulse" />
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="bg-transparent text-slate-200 text-xs sm:text-sm font-medium outline-none cursor-pointer pr-5 appearance-none focus:text-white"
        aria-label="Select Language"
      >
        {languages.map((lang) => (
          <option key={lang} value={lang} className="bg-slate-900 text-slate-200 py-1">
            {lang}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute right-2.5 flex items-center text-slate-400">
        <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 20 20">
          <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
        </svg>
      </div>
    </div>
  );
}

export default LanguageSelector;