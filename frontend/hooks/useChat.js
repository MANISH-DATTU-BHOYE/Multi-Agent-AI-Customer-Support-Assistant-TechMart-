// =========================================================
// frontend/hooks/useChat.js
// -----------------------------------------------------------
// Custom hook that owns all chat state: the message list, the
// "assistant is typing" indicator, and the function that sends
// a new message to the backend. Keeping this logic in a hook
// (instead of directly in the component) keeps ChatWindow.jsx
// focused purely on rendering (Module 2: Chat Interface).
// =========================================================

import { useState, useCallback } from "react";
import { sendChatMessage } from "../services/api";

export function useChat(sessionId) {
  const [messages, setMessages] = useState([]);   // { role, content, sources, agentUsed }
  const [isTyping, setIsTyping] = useState(false); // drives the "typing indicator"
  const [error, setError] = useState(null);

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim()) return;

      // Optimistically add the user's own message to the UI immediately
      setMessages((prev) => [...prev, { role: "user", content: text }]);
      setIsTyping(true);
      setError(null);

      try {
        const response = await sendChatMessage(sessionId, text);
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: response.answer,
            sources: response.sources,
            agentUsed: response.agent_used,
            escalated: response.escalated,
          },
        ]);
      } catch (err) {
        setError("Something went wrong. Please try again.");
      } finally {
        setIsTyping(false);
      }
    },
    [sessionId]
  );

  return { messages, isTyping, error, sendMessage };
}
