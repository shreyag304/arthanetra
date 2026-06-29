import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";

function ChatWindow({ messages = [], isSending = false }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isSending]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">

      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          sender={message.sender}
          text={message.text}
        />
      ))}

      {isSending && <TypingIndicator />}

      <div ref={bottomRef}></div>

    </div>
  );
}

export default ChatWindow;