import { useState } from "react";
import VoiceButton from "./VoiceButton";

function ChatInput({ messages, setMessages }) {
  const [message, setMessage] = useState("");

  function handleSend() {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: message,
    };

    // Add user's message to the chat
    setMessages((prev) => [...prev, userMessage]);

    // Backend API will be called here later

    // Clear the input field
    setMessage("");
  }

  return (
    <div className="border-t bg-white p-4">
      <div className="flex items-center gap-3">
        {/* Voice Button */}
        <VoiceButton />

        {/* Message Input */}
        <input
          type="text"
          placeholder="Ask ArthaNetra anything..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          className="flex-1 border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatInput;