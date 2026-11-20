import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { FiUser, FiPhone, FiLock, FiMail, FiAlertCircle, FiCheckCircle } from "react-icons/fi";
import { checkRegistration, register } from "../../api/auth";
import { AuthContext } from "../../context/AuthContext";
import Input from "../shared/Input";
import Button from "../shared/Button";

export default function RegisterForm({ onSwitchToLogin }) {
  const navigate = useNavigate();
  const { login: authLogin } = useContext(AuthContext);
  const [name, setName] = useState("");
  const [mobile, setMobile] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [checkingMobile, setCheckingMobile] = useState(false);
  const [mobileStatusMsg, setMobileStatusMsg] = useState("");
  const [mobileError, setMobileError] = useState("");
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleMobileBlur = async () => {
    if (mobile.length === 10) {
      setCheckingMobile(true);
      setMobileError("");
      setMobileStatusMsg("");
      try {
        const res = await checkRegistration(mobile);
        if (res && res.is_registered) {
          setMobileError("This mobile number is already registered.");
        } else {
          setMobileStatusMsg("Mobile number is available!");
        }
      } catch (err) {
        // Silently ignore network or check errors during blur
        console.warn("Could not check mobile status:", err.message);
      } finally {
        setCheckingMobile(false);
      }
    }
  };

  const validate = () => {
    if (!name.trim()) {
      setError("Please enter your full name.");
      return false;
    }
    if (!mobile || mobile.length !== 10 || !/^\d{10}$/.test(mobile)) {
      setError("Please enter a valid 10-digit mobile number.");
      return false;
    }
    if (mobileError) {
      setError(mobileError);
      return false;
    }
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("Please enter a valid email address.");
      return false;
    }
    if (!password || password.length < 4) {
      setError("Password must be at least 4 characters long.");
      return false;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
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
      const data = await register(mobile, password, name.trim(), email.trim() || null);
      setSuccessMsg("Account created successfully! Redirecting to workspace...");
      if (data) {
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_name", data.name);
        localStorage.setItem("user_mobile", data.mobile);
        authLogin(data);
      }
      setTimeout(() => {
        navigate("/workspace");
      }, 1000);
    } catch (err) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 animate-fadeIn">
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
        label="Full Name"
        type="text"
        icon={FiUser}
        placeholder="Enter your full name"
        value={name}
        onChange={(e) => {
          setName(e.target.value);
          setError("");
        }}
        disabled={loading}
      />

      <div>
        <Input
          label="Mobile Number"
          type="tel"
          icon={FiPhone}
          placeholder="10-digit mobile number"
          value={mobile}
          maxLength={10}
          onChange={(e) => {
            setMobile(e.target.value.replace(/\D/g, ""));
            setError("");
            setMobileError("");
            setMobileStatusMsg("");
          }}
          onBlur={handleMobileBlur}
          error={mobileError}
          helperText={
            checkingMobile
              ? "Checking availability..."
              : mobileStatusMsg || "Used for secure OTP and login"
          }
          disabled={loading}
        />
      </div>

      <Input
        label="Email Address (Optional)"
        type="email"
        icon={FiMail}
        placeholder="name@example.com"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
          setError("");
        }}
        disabled={loading}
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Password"
          type="password"
          icon={FiLock}
          placeholder="Create password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            setError("");
          }}
          disabled={loading}
        />
        <Input
          label="Confirm Password"
          type="password"
          icon={FiLock}
          placeholder="Confirm password"
          value={confirmPassword}
          onChange={(e) => {
            setConfirmPassword(e.target.value);
            setError("");
          }}
          disabled={loading}
        />
      </div>

      <div className="pt-2">
        <Button type="submit" isLoading={loading} variant="primary">
          Create ArthaNetra Account
        </Button>
      </div>

      <div className="pt-4 text-center border-t border-slate-100">
        <p className="text-sm text-slate-500">
          Already have an account?{" "}
          <button
            type="button"
            onClick={onSwitchToLogin}
            className="font-semibold text-blue-600 hover:text-blue-700 underline underline-offset-4 transition-colors"
          >
            Sign in instead
          </button>
        </p>
      </div>
    </form>
  );
}
