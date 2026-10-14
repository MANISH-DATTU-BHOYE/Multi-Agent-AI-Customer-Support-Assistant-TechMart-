// =========================================================
// frontend/pages/login.jsx
// -----------------------------------------------------------
// Module 1: User Authentication -> Login page.
// On success, stores the JWT and redirects to the chat page.
// =========================================================

import { useState } from "react";
import { useRouter } from "next/router";
import { loginUser } from "../services/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { access_token } = await loginUser(email, password);
      localStorage.setItem("access_token", access_token);
      router.push("/chat");
    } catch (err) {
      setError("Invalid email or password.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-md w-80">
        <h1 className="text-xl font-semibold mb-4">Sign in</h1>

        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          className="w-full border rounded-lg px-3 py-2 mb-3"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full border rounded-lg px-3 py-2 mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="w-full bg-blue-600 text-white rounded-lg py-2">
          Login
        </button>
      </form>
    </div>
  );
}
