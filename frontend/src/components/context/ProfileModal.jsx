import { useState } from "react";
import { FiX, FiUserCheck, FiBriefcase, FiDollarSign, FiTarget, FiCheckCircle, FiAlertCircle } from "react-icons/fi";
import { updateProfile } from "../../api/profile";
import Button from "../shared/Button";

const PERSONA_OPTIONS = [
  "Salaried Professional",
  "Student / Scholar",
  "Business / Entrepreneur",
  "Freelancer / Gig Worker",
  "Farmer / Agriculture",
  "Retired Senior Citizen",
  "Homemaker / Investor",
];

const INCOME_OPTIONS = [
  "Regular Monthly (Salaried)",
  "Variable / Seasonal",
  "Business Revenue",
  "Freelance Project Based",
  "Fixed Pension / Allowance",
];

const GOAL_OPTIONS = [
  "Budget Optimization & Savings",
  "Emergency Fund Building",
  "Wealth Accumulation & Investing",
  "Debt Reduction & Loan Payoff",
  "Retirement Planning",
  "Home / Major Asset Purchase",
];

export default function ProfileModal({ isOpen, onClose, user, context = {}, onSave }) {
  const [name, setName] = useState(() => user?.name || localStorage.getItem("user_name") || "ArthaNetra User");
  const [persona, setPersona] = useState(() => context?.persona || user?.persona || "Salaried Professional");
  const [incomeType, setIncomeType] = useState(() => context?.income_type || user?.income_type || "Regular Monthly (Salaried)");
  const [goal, setGoal] = useState(() => context?.goal || user?.goal || "Budget Optimization & Savings");

  const [customPersona, setCustomPersona] = useState("");
  const [customIncome, setCustomIncome] = useState("");
  const [customGoal, setCustomGoal] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    const finalPersona = customPersona.trim() ? customPersona.trim() : persona;
    const finalIncome = customIncome.trim() ? customIncome.trim() : incomeType;
    const finalGoal = customGoal.trim() ? customGoal.trim() : goal;

    try {
      const userId = user?.id || user?.user_id || localStorage.getItem("user_id");
      const updatedData = await updateProfile({
        user_id: userId ? Number(userId) : undefined,
        name: name.trim() || undefined,
        persona: finalPersona,
        income_type: finalIncome,
        goal: finalGoal,
      });

      if (name.trim()) {
        localStorage.setItem("user_name", name.trim());
      }

      setSuccess(true);
      if (onSave) {
        onSave({
          name: name.trim(),
          persona: finalPersona,
          income_type: finalIncome,
          goal: finalGoal,
          ...updatedData,
        });
      }

      setTimeout(() => {
        onClose();
      }, 900);
    } catch (err) {
      setError(err.message || "Failed to update profile. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-lg bg-slate-900 border border-slate-700/80 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-5 bg-gradient-to-r from-slate-900 via-indigo-950/50 to-slate-900 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-purple-500/20">
              {name ? name.charAt(0).toUpperCase() : "U"}
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-1.5">
                User Profile & Persona
              </h2>
              <p className="text-[11px] text-slate-400">
                Configure your occupation, income profile & financial targets
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-slate-800 transition-colors"
            aria-label="Close modal"
          >
            <FiX className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <form onSubmit={handleSave} className="p-6 overflow-y-auto space-y-6 flex-1 scrollbar-thin scrollbar-thumb-slate-700">
          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2.5">
              <FiAlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2.5">
              <FiCheckCircle className="w-4 h-4 shrink-0 text-emerald-400" />
              <span>Profile persona updated successfully! Adapting AI advisory...</span>
            </div>
          )}

          {/* User Name Section */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <FiUserCheck className="text-indigo-400" /> Display Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your Full Name"
              className="w-full bg-slate-950/60 border border-slate-700/80 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 outline-none transition-all"
            />
          </div>

          {/* Occupation / Persona Section */}
          <div className="space-y-2.5">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <FiBriefcase className="text-purple-400" /> Occupation / Persona
            </label>
            <p className="text-[11px] text-slate-400">
              Select your occupation so ArthaNetra AI can tailor financial insights for your demographic:
            </p>
            <div className="flex flex-wrap gap-2 pt-1">
              {PERSONA_OPTIONS.map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => {
                    setPersona(opt);
                    setCustomPersona("");
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                    persona === opt && !customPersona
                      ? "bg-purple-600/20 border-purple-500 text-purple-200 shadow-sm shadow-purple-500/20"
                      : "bg-slate-800/60 border-slate-700/80 text-slate-300 hover:bg-slate-800 hover:border-slate-600"
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
            <input
              type="text"
              value={customPersona}
              onChange={(e) => {
                setCustomPersona(e.target.value);
                if (e.target.value) setPersona(e.target.value);
              }}
              placeholder="Or type custom occupation (e.g. Architect, Doctor...)"
              className="w-full mt-2 bg-slate-950/60 border border-slate-700/80 focus:border-purple-500 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 outline-none transition-all"
            />
          </div>

          {/* Income Type Section */}
          <div className="space-y-2.5">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <FiDollarSign className="text-emerald-400" /> Income Structure
            </label>
            <div className="flex flex-wrap gap-2 pt-1">
              {INCOME_OPTIONS.map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => {
                    setIncomeType(opt);
                    setCustomIncome("");
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                    incomeType === opt && !customIncome
                      ? "bg-emerald-600/20 border-emerald-500 text-emerald-200 shadow-sm shadow-emerald-500/20"
                      : "bg-slate-800/60 border-slate-700/80 text-slate-300 hover:bg-slate-800 hover:border-slate-600"
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
            <input
              type="text"
              value={customIncome}
              onChange={(e) => {
                setCustomIncome(e.target.value);
                if (e.target.value) setIncomeType(e.target.value);
              }}
              placeholder="Or type custom income frequency/range..."
              className="w-full mt-2 bg-slate-950/60 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 outline-none transition-all"
            />
          </div>

          {/* Goal Section */}
          <div className="space-y-2.5">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <FiTarget className="text-amber-400" /> Primary Financial Goal
            </label>
            <div className="flex flex-wrap gap-2 pt-1">
              {GOAL_OPTIONS.map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => {
                    setGoal(opt);
                    setCustomGoal("");
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                    goal === opt && !customGoal
                      ? "bg-amber-600/20 border-amber-500 text-amber-200 shadow-sm shadow-amber-500/20"
                      : "bg-slate-800/60 border-slate-700/80 text-slate-300 hover:bg-slate-800 hover:border-slate-600"
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
            <input
              type="text"
              value={customGoal}
              onChange={(e) => {
                setCustomGoal(e.target.value);
                if (e.target.value) setGoal(e.target.value);
              }}
              placeholder="Or type specific financial goal..."
              className="w-full mt-2 bg-slate-950/60 border border-slate-700/80 focus:border-amber-500 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 outline-none transition-all"
            />
          </div>

          {/* Footer Actions */}
          <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              Cancel
            </button>
            <Button type="submit" isLoading={loading} variant="primary" className="!py-2 !px-5 !text-xs">
              Save & Apply Persona
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
