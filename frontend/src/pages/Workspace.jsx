import ChatWindow from "../components/chat/ChatWindow";
import ContextPanel from "../components/context/ContextPanel";
import SuggestedPrompts from "../components/chat/SuggestedPrompts";
import ChatInput from "../components/chat/ChatInput";

import { useState } from "react";

function Workspace() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "assistant",
      text: "Hello! I'm ArthaNetra. How can I help you today?",
    },
  ]);

  const [context, setContext] = useState({
    financial_health_score: 72,
    persona: "Student",
    income_type: "Student",
    language: "English",
    goal: "Increase Savings",
    eligible_schemes: ["PM-KISAN"],
  });

  const language =
  localStorage.getItem("language") || "English";

  return (
    <div className="min-h-screen bg-slate-100">

      {/* Header */}
      <header className="bg-white shadow-sm px-8 py-4">
        <h1 className="text-2xl font-bold text-blue-700">
          ArthaNetra
        </h1>
      </header>

      {/* Main Layout */}
      <div className="grid grid-cols-12 h-[calc(100vh-72px)]">

        {/* Chat Section */}
        <div className="col-span-8 flex flex-col border-r">

          <div className="flex-1 overflow-y-auto">
            <ChatWindow messages={messages} />
          </div>

          <SuggestedPrompts
            onPromptClick={(prompt) => {
              console.log(prompt);
            }}
          />

          <ChatInput
            messages={messages}
            setMessages={setMessages}
            setContext={setContext}
            language={language}
          />

        </div>

        {/* Context Panel */}
        <div className="col-span-4 bg-white">
          <ContextPanel context={context} />
        </div>

      </div>

    </div>
  );
}

export default Workspace;