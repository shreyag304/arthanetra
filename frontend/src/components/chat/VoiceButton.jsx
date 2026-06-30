import { useState } from "react";
import { FiMic, FiMicOff } from "react-icons/fi";

function VoiceButton({ onVoiceInput }) {
  const [isListening, setIsListening] = useState(false);

  const toggleListen = () => {
    setIsListening(!isListening);
    if (onVoiceInput) {
      onVoiceInput(!isListening);
    }
  };

  return (
    <button
      type="button"
      onClick={toggleListen}
      title={isListening ? "Listening... Click to stop" : "Voice Input"}
      className={`relative flex items-center justify-center p-3.5 rounded-xl border transition-all duration-300 shadow-sm ${
        isListening
          ? "bg-gradient-to-r from-red-500 to-pink-600 border-transparent text-white shadow-red-500/30 shadow-md animate-pulse"
          : "bg-slate-800/80 hover:bg-slate-800 border-slate-700/80 text-slate-300 hover:text-white hover:border-slate-600"
      }`}
    >
      {isListening ? (
        <>
          <span className="absolute -top-1 -right-1 flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </span>
          <FiMicOff className="w-5 h-5" />
        </>
      ) : (
        <FiMic className="w-5 h-5 transition-transform group-hover:scale-110" />
      )}
    </button>
  );
}

export default VoiceButton;