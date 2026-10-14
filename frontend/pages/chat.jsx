// =========================================================
// frontend/pages/chat.jsx
// -----------------------------------------------------------
// Main customer-facing page. Combines ChatWindow + MessageInput
// and drives them both through the useChat hook, per the
// architecture: Web Chat Interface -> Backend API Server.
// =========================================================

import { useMemo } from "react";
import ChatWindow from "../components/ChatWindow";
import MessageInput from "../components/MessageInput";
import { useChat } from "../hooks/useChat";

export default function ChatPage() {
  // A simple session id, generated once per browser tab.
  // In production this would come from the logged-in user's account.
  const sessionId = useMemo(
    () => `session-${Math.random().toString(36).slice(2)}`,
    []
  );

  const { messages, isTyping, error, sendMessage } = useChat(sessionId);

  return (
    <div className="max-w-2xl mx-auto mt-8 px-4">
      <h1 className="text-2xl font-bold mb-4">TechMart Support Assistant</h1>

      <ChatWindow messages={messages} isTyping={isTyping} />

      {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

      <MessageInput onSend={sendMessage} disabled={isTyping} />
    </div>
  );
}
