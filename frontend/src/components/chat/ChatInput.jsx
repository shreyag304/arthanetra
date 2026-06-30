import { useState } from "react";
import VoiceButton from "./VoiceButton";
import { sendMessage } from "../../mocks/chatMock";
import { FiSend, FiLoader } from "react-icons/fi";

function ChatInput({
  messages,
  setMessages,
  setContext,
  language,
  onSendExternal,
}) {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

  async function handleSend(customText = null) {
    const textToSend = typeof customText === "string" ? customText : message;
    if (!textToSend.trim() || isSending) return;

    if (onSendExternal) {
      if (typeof customText !== "string") setMessage("");
      await onSendExternal(textToSend);
      return;
    }

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: textToSend,
    };

    setMessages((prev) => [...prev, userMessage]);

    const payload = {
      message: textToSend,
      conversation_id: "demo-user",
      language: language,
    };

    if (typeof customText !== "string") {
      setMessage("");
    }
    setIsSending(true);

    try {
      console.log(payload);
      const response = await sendMessage(payload);
      setContext(response.context);

      const assistantMessage = {
        id: Date.now() + 1,
        sender: "assistant",
        text: response.reply,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "assistant",
          text: "Something went wrong while connecting to ArthaNetra AI core.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  const placeholders = {
    English: "Ask ArthaNetra anything about financial health, loans, schemes...",
    Hindi: "वित्तीय स्वास्थ्य, ऋण या योजनाओं के बारे में कुछ भी पूछें...",
    Marathi: "आर्थिक आरोग्य, कर्ज किंवा योजनांबद्दल काहीही विचारा...",
    Gujarati: "નાણાકીય આરોગ્ય, લોન અથવા યોજનાઓ વિશે કંઈપણ પૂછો...",
    Tamil: "நிதி நிலை, கடன்கள் அல்லது திட்டங்கள் குறித்து எதுவும் கேளுங்கள்...",
    Telugu: "ఆర్థిక ఆరోగ్యం, రుణాలు లేదా పథకాల గురించి ఏదైనా అడగండి...",
    Kannada: "ಆರ್ಥಿಕ ಆರೋಗ್ಯ, ಸಾಲಗಳು ಅಥವಾ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಏನಾದರೂ ಕೇಳಿ...",
    Malayalam: "സാമ്പത്തിക ആരോഗ്യം, വായ്പകൾ എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ...",
    Bengali: "আর্থিক স্বাস্থ্য, ঋণ বা সরকারি প্রকল্প সম্পর্কে জিজ্ঞাসা করুন...",
    Punjabi: "ਵਿੱਤੀ ਸਿਹਤ, ਕਰਜ਼ੇ ਜਾਂ ਸਕੀਮਾਂ ਬਾਰੇ ਕੁਝ ਵੀ ਪੁੱਛੋ...",
    Odia: "ଆର୍ଥିକ ସ୍ୱାସ୍ଥ୍ୟ, ଋଣ କିମ୍ବା ଯୋଜନା ବିଷୟରେ ପଚାରନ୍ତୁ...",
    Assamese: "বিত্তীয় স্বাস্থ্য, ঋণ বা আঁচনিৰ বিষয়ে যিকোনো কথা সোধক...",
  };

  return (
    <div className="border-t border-slate-800/80 bg-slate-900/90 backdrop-blur-xl p-4 sm:p-5">
      <div className="flex items-center gap-2.5 sm:gap-3 max-w-5xl mx-auto">
        {/* Voice Button */}
        <VoiceButton
          onVoiceInput={(listening) => {
            if (!listening && !message) {
              setMessage("Check eligible government financial schemes for me");
            }
          }}
        />

        {/* Message Input Container */}
        <div className="flex-1 relative flex items-center">
          <input
            type="text"
            placeholder={placeholders[language] || placeholders["English"]}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={isSending}
            className="w-full bg-slate-800/80 border border-slate-700/80 rounded-2xl px-4.5 py-3.5 pr-12 text-sm text-slate-100 placeholder-slate-400 outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all disabled:opacity-60 shadow-inner"
          />
        </div>

        {/* Send Button */}
        <button
          disabled={!message.trim() || isSending}
          onClick={() => handleSend()}
          className="flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-5 py-3.5 rounded-2xl shadow-lg shadow-blue-600/25 hover:shadow-blue-600/40 transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none shrink-0 transform active:scale-95"
          title="Send message"
        >
          {isSending ? (
            <FiLoader className="w-5 h-5 animate-spin" />
          ) : (
            <FiSend className="w-5 h-5" />
          )}
          <span className="hidden sm:inline text-sm">Send</span>
        </button>
      </div>

      {/* Subtext info */}
      <div className="flex items-center justify-between max-w-5xl mx-auto mt-2.5 px-1 text-[11px] text-slate-400">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block animate-ping"></span>
          ArthaNetra AI • Financial Intelligence Core
        </span>
        <span className="hidden md:inline">
          Press Enter to send • 256-bit encrypted conversation
        </span>
      </div>
    </div>
  );
}

export default ChatInput;