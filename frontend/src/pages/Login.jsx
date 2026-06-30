import { useState } from "react";
import LanguageSelector from "../components/chat/LanguageSelector";
import Logo from "../components/shared/Logo";
import Card from "../components/shared/Card";
import AuthTabs from "../components/auth/AuthTabs";

function Login() {
  const [language, setLanguage] = useState(
    localStorage.getItem("language") || "English"
  );

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem("language", newLang);
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-950 via-indigo-950 to-blue-950 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
      {/* Dynamic Background Glow Spheres */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none animate-pulse delay-700"></div>
      <div className="absolute top-1/2 right-1/3 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

      {/* Top Header Row */}
      <div className="w-full max-w-md flex items-center justify-between mb-6 z-10">
        <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-white/15 text-white/90 text-xs font-semibold tracking-wide">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span>AI Financial Eye</span>
        </div>
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-1 border border-white/15">
          <LanguageSelector
            language={language}
            setLanguage={handleLanguageChange}
          />
        </div>
      </div>

      {/* Main Authentication Card */}
      <div className="w-full max-w-md z-10 animate-fadeIn">
        <Card className="!p-6 sm:!p-8 lg:!p-10 shadow-2xl shadow-black/40 border-white/20">
          <div className="text-center mb-8">
            <Logo className="text-3xl sm:text-4xl justify-center mb-3" />
            <p className="text-sm font-medium text-slate-500">
              Your multilingual AI-powered financial companion
            </p>
          </div>

          <AuthTabs defaultTab="login" />

          <div className="mt-8 pt-6 border-t border-slate-100 text-center flex flex-col gap-2">
            <div className="flex items-center justify-center gap-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <span>🔒 256-Bit Secure</span>
              <span>•</span>
              <span>⚡ Fast OTP</span>
              <span>•</span>
              <span>🌐 Multilingual</span>
            </div>
          </div>
        </Card>
      </div>

      <p className="mt-6 text-xs text-slate-400/80 z-10 text-center">
        &copy; {new Date().getFullYear()} ArthaNetra AI • Financial Intelligence For Everyone
      </p>
    </div>
  );
}

export default Login;