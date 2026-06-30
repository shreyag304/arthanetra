import { FiCpu, FiUser, FiCheckCircle } from "react-icons/fi";

function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div
      className={`flex items-start gap-3.5 sm:gap-4 animate-fadeIn ${
        isUser ? "flex-row-reverse" : "flex-row"
      }`}
    >
      {/* Avatar */}
      <div
        className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-md ${
          isUser
            ? "bg-gradient-to-tr from-blue-600 to-indigo-600 text-white shadow-blue-500/20"
            : "bg-gradient-to-tr from-indigo-600 via-blue-600 to-emerald-400 text-white shadow-indigo-500/20"
        }`}
      >
        {isUser ? (
          <FiUser className="w-4 h-4 stroke-[2.5]" />
        ) : (
          <FiCpu className="w-4 h-4 stroke-[2.5]" />
        )}
      </div>

      {/* Message Bubble & Metadata */}
      <div className={`flex flex-col max-w-[80%] sm:max-w-[75%] ${isUser ? "items-end" : "items-start"}`}>
        <div className="flex items-center gap-2 mb-1 px-1">
          <span className="text-xs font-semibold text-slate-400">
            {isUser ? "You" : "ArthaNetra AI"}
          </span>
          {!isUser && (
            <span className="inline-flex items-center gap-1 text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full font-medium">
              <FiCheckCircle className="w-2.5 h-2.5" />
              Verified Advisor
            </span>
          )}
        </div>

        <div
          className={`rounded-2xl px-5 py-3.5 text-sm sm:text-[14.5px] leading-relaxed shadow-lg ${
            isUser
              ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-tr-xs shadow-blue-600/20 font-normal"
              : "bg-slate-800/90 backdrop-blur-md border border-slate-700/80 text-slate-100 rounded-tl-xs shadow-black/30"
          }`}
        >
          <p className="whitespace-pre-line">{text}</p>
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;