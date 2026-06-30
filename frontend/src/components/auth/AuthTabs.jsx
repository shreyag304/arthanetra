import { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function AuthTabs({ defaultTab = "login" }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <div className="w-full">
      {/* Sleek Tab Switcher */}
      <div className="flex rounded-2xl bg-slate-100/80 p-1.5 mb-8 border border-slate-200/60 shadow-inner">
        <button
          type="button"
          onClick={() => setActiveTab("login")}
          className={`flex-1 py-3 px-4 rounded-xl font-bold text-sm transition-all duration-300 ${
            activeTab === "login"
              ? "bg-white text-blue-700 shadow-md shadow-slate-200/50 scale-[1.01]"
              : "text-slate-500 hover:text-slate-800 hover:bg-white/40"
          }`}
        >
          Sign In
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("register")}
          className={`flex-1 py-3 px-4 rounded-xl font-bold text-sm transition-all duration-300 ${
            activeTab === "register"
              ? "bg-white text-blue-700 shadow-md shadow-slate-200/50 scale-[1.01]"
              : "text-slate-500 hover:text-slate-800 hover:bg-white/40"
          }`}
        >
          Create Account
        </button>
      </div>

      {/* Active Form */}
      <div className="relative">
        {activeTab === "login" ? (
          <LoginForm onSwitchToRegister={() => setActiveTab("register")} />
        ) : (
          <RegisterForm onSwitchToLogin={() => setActiveTab("login")} />
        )}
      </div>
    </div>
  );
}
