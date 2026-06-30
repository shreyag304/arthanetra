import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiPhone, FiLock, FiAlertCircle, FiCheckCircle } from "react-icons/fi";
import { login } from "../../api/auth";
import Input from "../shared/Input";
import Button from "../shared/Button";

export default function LoginForm({ onSwitchToRegister }) {
  const navigate = useNavigate();
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const validate = () => {
    if (!mobile || mobile.length !== 10 || !/^\d{10}$/.test(mobile)) {
      setError("Please enter a valid 10-digit mobile number");
      return false;
    }
    if (!password) {
      setError("Please enter your password");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMsg("");

    if (!validate()) return;

    setLoading(true);
    try {
      const data = await login(mobile, password);
      setSuccessMsg("Login successful! Redirecting to workspace...");
      if (data) {
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_name", data.name);
        localStorage.setItem("user_mobile", data.mobile);
      }
      setTimeout(() => {
        navigate("/workspace");
      }, 800);
    } catch (err) {
      setError(err.message || "Failed to log in. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5 animate-fadeIn">
      {error && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-start gap-3 shadow-sm">
          <FiAlertCircle className="w-5 h-5 shrink-0 text-rose-500 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-start gap-3 shadow-sm">
          <FiCheckCircle className="w-5 h-5 shrink-0 text-emerald-600 mt-0.5" />
          <span>{successMsg}</span>
        </div>
      )}

      <Input
        label="Mobile Number"
        type="tel"
        icon={FiPhone}
        placeholder="e.g. 9876543210"
        value={mobile}
        maxLength={10}
        onChange={(e) => {
          setMobile(e.target.value.replace(/\D/g, ""));
          setError("");
        }}
        disabled={loading}
      />

      <Input
        label="Password"
        type="password"
        icon={FiLock}
        placeholder="Enter your password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
          setError("");
        }}
        disabled={loading}
      />

      <div className="pt-2">
        <Button type="submit" isLoading={loading} variant="primary">
          Log In to ArthaNetra
        </Button>
      </div>

      <div className="pt-4 text-center border-t border-slate-100">
        <p className="text-sm text-slate-500">
          Don&apos;t have an account yet?{" "}
          <button
            type="button"
            onClick={onSwitchToRegister}
            className="font-semibold text-blue-600 hover:text-blue-700 underline underline-offset-4 transition-colors"
          >
            Create an account
          </button>
        </p>
      </div>
    </form>
  );
}
