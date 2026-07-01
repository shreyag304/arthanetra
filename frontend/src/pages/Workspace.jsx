import ChatWindow from "../components/chat/ChatWindow";
import ContextPanel from "../components/context/ContextPanel";
import SuggestedPrompts from "../components/chat/SuggestedPrompts";
import ChatInput from "../components/chat/ChatInput";
import Logo from "../components/shared/Logo";
import LanguageSelector from "../components/chat/LanguageSelector";
import ProfileModal from "../components/context/ProfileModal";
import { sendMessage, chatSocket } from "../api/chat";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { FiRefreshCw } from "react-icons/fi";

function Workspace() {
  const { user, refreshProfile } = useContext(AuthContext);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "assistant",
      text: "Namaste! I'm ArthaNetra AI, your multilingual financial companion. How can I assist you with budgets, loans, or government schemes today?",
    },
  ]);

  const [context, setContext] = useState({
    financial_health_score: 72,
    persona: "Student",
    income_type: "Student",
    language: localStorage.getItem("language") || "English",
    goal: "Increase Savings",
    eligible_schemes: ["PM Scholarship", "PM Jan Dhan Yojana"],
  });

  const [language, setLanguage] = useState(
    localStorage.getItem("language") || "English"
  );
  const [isSending, setIsSending] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(chatSocket.status);

  useEffect(() => {
    chatSocket.connect();

    const handleStatus = (status) => setConnectionStatus(status);
    const handleContextUpdate = (newContext) => {
      setContext((prev) => ({ ...prev, ...newContext }));
    };
    const handleWsMessage = (data) => {
      if (data && (data.type === "alert" || data.type === "push_message")) {
        setMessages((prev) => [
          ...prev,
          { id: Date.now(), sender: "assistant", text: data.message || data.text },
        ]);
      }
    };

    chatSocket.on("status_change", handleStatus);
    chatSocket.on("context_update", handleContextUpdate);
    chatSocket.on("message", handleWsMessage);

    return () => {
      chatSocket.off("status_change", handleStatus);
      chatSocket.off("context_update", handleContextUpdate);
      chatSocket.off("message", handleWsMessage);
    };
  }, []);

  useEffect(() => {
    if (user) {
      setContext((prev) => ({
        ...prev,
        persona: user.persona || prev.persona,
        income_type: user.income_type || prev.income_type,
        goal: user.goal || prev.goal,
        financial_health_score: user.financial_health_score || prev.financial_health_score,
      }));
    } else if (refreshProfile) {
      refreshProfile();
    }
  }, [user, refreshProfile]);

  const userName = user?.name || localStorage.getItem("user_name") || "ArthaNetra User";

  const handleProfileSave = (updatedData) => {
    setContext((prev) => ({
      ...prev,
      persona: updatedData.persona || prev.persona,
      income_type: updatedData.income_type || prev.income_type,
      goal: updatedData.goal || prev.goal,
    }));
    if (refreshProfile) {
      refreshProfile(true);
    }
  };

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem("language", newLang);
    setContext((prev) => ({ ...prev, language: newLang }));
  };

  const handleResetSession = () => {
    setMessages([
      {
        id: Date.now(),
        sender: "assistant",
        text: `Session refreshed. I am ready to assist you in ${language}. What financial target should we explore?`,
      },
    ]);
  };

  const handleSendPrompt = async (text) => {
    if (!text.trim() || isSending) return;

    const userMsg = { id: Date.now(), sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setIsSending(true);

    try {
      const response = await sendMessage({
        message: text,
        user_id: user?.user_id || null,
        conversation_id: "demo-user",
        language,
      });
      if (response?.context) {
        setContext(response.context);
      }
      const replyText =
        response?.reply ||
        response?.message ||
        response?.text ||
        (typeof response === "string"
          ? response
          : "Received response from ArthaNetra AI.");
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: "assistant", text: replyText },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "assistant",
          text:
            e?.message ||
            "Unable to reach ArthaNetra AI core. Please try again.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 flex flex-col text-slate-100">
      {/* Ambient Background Glow Spheres */}
      <div className="absolute top-1/4 left-1/3 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-1/3 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none animate-pulse delay-700"></div>

      {/* Top Header Bar */}
      <header className="bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-3.5 flex items-center justify-between z-20 sticky top-0">
        <div className="flex items-center gap-4">
          <Logo className="text-xl sm:text-2xl" />
          <div className="hidden md:flex items-center gap-2 bg-slate-800/80 border border-slate-700/60 px-3 py-1 rounded-full text-[11px] text-slate-300">
            <span
              className={`w-2 h-2 rounded-full ${
                connectionStatus === "connected"
                  ? "bg-emerald-400 animate-ping"
                  : connectionStatus === "connecting"
                  ? "bg-amber-400 animate-pulse"
                  : "bg-blue-400"
              }`}
            ></span>
            <span>
              {connectionStatus === "connected"
                ? "AI Eye Active • WS Realtime"
                : connectionStatus === "connecting"
                ? "Connecting WS Stream..."
                : "AI Eye Active • HTTP Fallback"}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5 sm:gap-3">
          {/* User Profile Trigger Button */}
          <button
            onClick={() => setIsProfileModalOpen(true)}
            title="Edit Profile, Persona & Goal"
            className="flex items-center gap-2 bg-gradient-to-r from-purple-900/60 to-indigo-900/60 hover:from-purple-800 hover:to-indigo-800 border border-purple-500/30 hover:border-purple-400 text-white px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm group"
          >
            <span className="w-5 h-5 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-500 flex items-center justify-center text-[10px] font-bold shadow-inner group-hover:scale-105 transition-transform">
              {userName.charAt(0).toUpperCase()}
            </span>
            <span className="max-w-[90px] sm:max-w-[130px] truncate">{userName}</span>
          </button>

          <button
            onClick={handleResetSession}
            title="Reset Conversation"
            className="flex items-center gap-1.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 hover:border-slate-600 text-slate-300 hover:text-white px-3 py-1.5 rounded-xl text-xs font-medium transition-all"
          >
            <FiRefreshCw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">New Chat</span>
          </button>

          <LanguageSelector
            language={language}
            setLanguage={handleLanguageChange}
          />
        </div>
      </header>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 flex-1 overflow-hidden h-[calc(100vh-69px)] z-10">
        {/* Chat Console Section */}
        <div className="col-span-1 lg:col-span-8 flex flex-col border-r border-slate-800/80 bg-slate-950/40 backdrop-blur-md h-full overflow-hidden">
          {/* Messages Window */}
          <ChatWindow
            messages={messages}
            isSending={isSending}
            connectionStatus={connectionStatus}
          />

          {/* Suggested Inquiries */}
          <SuggestedPrompts onPromptClick={handleSendPrompt} />

          {/* Prompt Console */}
          <ChatInput
            messages={messages}
            setMessages={setMessages}
            setContext={setContext}
            language={language}
            onSendExternal={handleSendPrompt}
            connectionStatus={connectionStatus}
          />
        </div>

        {/* Live AI Analytics & Context Sidebar */}
        <div className="col-span-1 lg:col-span-4 h-full overflow-hidden">
          <ContextPanel
            context={context}
            connectionStatus={connectionStatus}
            onGoalClick={handleSendPrompt}
            userName={userName}
            onEditProfile={() => setIsProfileModalOpen(true)}
          />
        </div>
      </div>

      {/* Profile Popup Menu / Modal */}
      {isProfileModalOpen && (
        <ProfileModal
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
          user={user}
          context={context}
          onSave={handleProfileSave}
        />
      )}
    </div>
  );
}

export default Workspace;