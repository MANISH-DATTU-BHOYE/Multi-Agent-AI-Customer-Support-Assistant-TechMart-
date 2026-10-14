// =========================================================
// frontend/components/ChatWindow.jsx
// -----------------------------------------------------------
// Module 2: Chat Interface -> Chat window, conversation history,
// typing indicator. Pure presentation component; all state comes
// from the useChat hook so this file only handles rendering.
// =========================================================

import { useEffect, useRef } from "react";

export default function ChatWindow({ messages, isTyping }) {
  const bottomRef = useRef(null);

  // Auto-scroll to the newest message whenever the list changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex flex-col gap-3 overflow-y-auto p-4 h-[70vh] bg-gray-50 rounded-lg">
      {messages.map((msg, idx) => (
        <MessageBubble key={idx} message={msg} />
      ))}

      {isTyping && (
        <div className="text-sm text-gray-400 italic">Assistant is typing...</div>
      )}

      {/* invisible anchor element used to auto-scroll to the bottom */}
      <div ref={bottomRef} />
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-2 whitespace-pre-wrap ${
          isUser ? "bg-blue-600 text-white" : "bg-white border border-gray-200"
        }`}
      >
        <p>{message.content}</p>

        {/* Show which agent(s) answered + source documents (transparency for the user) */}
        {!isUser && message.agentUsed && (
          <p className="text-xs text-gray-400 mt-1">
            Handled by: {message.agentUsed.join(", ")}
            {message.sources?.length > 0 && ` · Sources: ${message.sources.join(", ")}`}
          </p>
        )}

        {!isUser && message.escalated && (
          <p className="text-xs text-orange-500 mt-1">
            This query has been escalated to a human agent.
          </p>
        )}
      </div>
    </div>
  );
}
