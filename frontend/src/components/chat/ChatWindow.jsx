import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";
import { FiMessageSquare, FiWifi, FiAlertCircle } from "react-icons/fi";

function ChatWindow({ messages = [], isSending = false, connectionStatus = "connected" }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isSending, connectionStatus]);

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent flex flex-col">
      {/* WebSocket Status Banner */}
      {connectionStatus === "connecting" && (
        <div className="flex items-center justify-center gap-2 bg-amber-500/10 border border-amber-500/20 text-amber-300 px-3.5 py-2 rounded-xl text-xs animate-pulse mx-auto">
          <FiWifi className="w-3.5 h-3.5 animate-spin" />
          <span>Establishing real-time WebSocket connection...</span>
        </div>
      )}
      {(connectionStatus === "disconnected" || connectionStatus === "error") && (
        <div className="flex items-center justify-center gap-2 bg-slate-800/80 border border-slate-700 text-slate-300 px-3.5 py-2 rounded-xl text-xs mx-auto">
          <FiAlertCircle className="w-3.5 h-3.5 text-amber-400" />
          <span>WebSocket offline • Communicating via secure HTTP fallback</span>
        </div>
      )}

      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center p-6 text-slate-500 animate-fadeIn my-auto">
          <div className="w-16 h-16 rounded-3xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center mb-4 shadow-inner">
            <FiMessageSquare className="w-8 h-8 text-blue-400 stroke-[1.5]" />
          </div>
          <h3 className="text-base font-semibold text-slate-300 mb-1">
            No Messages Yet
          </h3>
          <p className="text-xs sm:text-sm text-slate-400 max-w-sm">
            Ask ArthaNetra AI about budgets, loans, financial health, or government schemes below.
          </p>
        </div>
      ) : (
        messages.map((message) => (
          <ChatMessage
            key={message.id}
            sender={message.sender}
            text={message.text}
          />
        ))
      )}

      {isSending && <TypingIndicator />}

      <div ref={bottomRef} className="h-2"></div>
    </div>
  );
}

export default ChatWindow;