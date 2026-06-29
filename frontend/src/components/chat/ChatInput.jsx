import { useState } from "react";
import VoiceButton from "./VoiceButton";
import { sendMessage } from "../../mocks/chatMock";

function ChatInput({
  messages,
  setMessages,
  setContext,
  language,
}) {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

 async function handleSend() {

  if (!message.trim() || isSending) return;

  const userMessage = {
    id: Date.now(),
    sender: "user",
    text: message,
  };

  setMessages((prev) => [...prev, userMessage]);

  const payload = {
    message: message,
    conversation_id: "demo-user",
    language: language,
  };

  setMessage("");
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
        text: "Something went wrong.",
      },
    ]);

  } finally {

    setIsSending(false);

  }

}
  const placeholders = {
 English: "Ask ArthaNetra anything...",
 Hindi: "हिंदी में लिखें...",
 Marathi: "मराठीत लिहा...",
 Gujarati: "ગુજરાતીમાં લખો...",
 Tamil: "தமிழில் தட்டச்சு செய்யவும்...",
 Telugu: "తెలుగులో టైప్ చేయండి...",
 Kannada: "ಕನ್ನಡದಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...",
 Malayalam: "മലയാളത്തിൽ ടൈപ്പ് ചെയ്യുക...",
 Bengali: "বাংলায় লিখুন...",
 Punjabi: "ਪੰਜਾਬੀ ਵਿੱਚ ਲਿਖੋ...",
 Odia: "ଓଡ଼ିଆରେ ଲେଖନ୍ତୁ...",
 Assamese: "অসমীয়াত লিখক...",
};

  return (
    <div className="border-t bg-white p-4">
      <div className="flex items-center gap-3">
        {/* Voice Button */}
        <VoiceButton />

        {/* Message Input */}
        <input
  type="text"
  placeholder={placeholders[language]}
  value={message}
  onChange={(e) => setMessage(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  }}
  disabled={isSending}
  className="flex-1 border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
/>

        {/* Send Button */}
        <button
  disabled={isSending}
  onClick={handleSend}
  className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition disabled:opacity-60 disabled:cursor-not-allowed"
>
          {isSending ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;