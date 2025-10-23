import { useState } from "react";

const API_BASE =
  (import.meta as any).env?.VITE_API_BASE ?? "http://localhost:8000";

let accessTokenMemory: string | null = null;
const REFRESH_KEY = "refresh_token";

export function getAccessToken() {
  return accessTokenMemory;
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function setTokens(access: string, refresh: string) {
  accessTokenMemory = access;
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  accessTokenMemory = null;
  localStorage.removeItem(REFRESH_KEY);
}

export async function refreshAccessToken(): Promise<boolean> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    return false;
  }

  try {
    const res = await fetch(`${API_BASE}/api/v1/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!res.ok) {
      clearTokens();
      return false;
    }

    const data = await res.json();
    setTokens(data.access, refreshToken); // Keep the original refresh token
    return true;
  } catch (error) {
    clearTokens();
    return false;
  }
}

export function LoginForm({ onLoggedIn }: { onLoggedIn: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setTokens(data.access, data.refresh);
      onLoggedIn();
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-3">
      <div>
        <label className="block text-sm font-medium mb-1">Username</label>
        <input
          className="border rounded px-3 py-2 w-full"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Password</label>
        <input
          type="password"
          className="border rounded px-3 py-2 w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      {error && <div className="text-red-600 text-sm">{error}</div>}
      <button
        disabled={loading}
        className="bg-black text-white px-4 py-2 rounded"
      >
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}
