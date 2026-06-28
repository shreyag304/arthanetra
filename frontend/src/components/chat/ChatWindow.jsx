import ChatMessage from "./ChatMessage";

function ChatWindow({ messages }) {
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          sender={message.sender}
          text={message.text}
        />
      ))}
    </div>
  );
}

export default ChatWindow;