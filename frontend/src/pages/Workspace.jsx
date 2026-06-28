import ChatWindow from "../components/chat/ChatWindow";
import ContextPanel from "../components/context/ContextPanel";
import SuggestedPrompts from "../components/chat/SuggestedPrompts";
import ChatInput from "../components/chat/ChatInput";

function Workspace() {
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
            <ChatWindow />
          </div>

          <SuggestedPrompts />

          <ChatInput />

        </div>

        {/* Context Panel */}
        <div className="col-span-4 bg-white">
          <ContextPanel />
        </div>

      </div>

    </div>
  );
}

export default Workspace;