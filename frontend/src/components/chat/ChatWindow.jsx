import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";
import { FiMessageSquare } from "react-icons/fi";

function ChatWindow({ messages = [], isSending = false }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isSending]);

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500 animate-fadeIn">
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