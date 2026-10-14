// =========================================================
// frontend/services/api.js
// -----------------------------------------------------------
// Centralized Axios client for every backend call the frontend
// makes. Keeping this in one file means the base URL, headers,
// and error handling only need to be defined once.
// =========================================================

import axios from "axios";

// Read the backend URL from an env variable so it's easy to
// point at localhost during development or a deployed URL in prod.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the JWT (if present) to every outgoing request
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/** Register a new user account. */
export async function registerUser(name, email, password) {
  const { data } = await apiClient.post("/auth/register", { name, email, password });
  return data;
}

/** Log an existing user in. */
export async function loginUser(email, password) {
  const { data } = await apiClient.post("/auth/login", { email, password });
  return data;
}

/** Send a chat message and get back the multi-agent aggregated response. */
export async function sendChatMessage(sessionId, message) {
  const { data } = await apiClient.post("/chat/", { session_id: sessionId, message });
  return data;
}

/** Load a session's full conversation history (used on page reload). */
export async function getChatHistory(sessionId) {
  const { data } = await apiClient.get(`/chat/history/${sessionId}`);
  return data;
}

export default apiClient;
