import { getAccessToken, getRefreshToken, refreshAccessToken } from "./auth";

const API_BASE =
  (import.meta as any).env?.VITE_API_BASE ?? "http://localhost:8000";

export async function apiFetch(path: string, init: RequestInit = {}) {
  const url = path.startsWith("http")
    ? path
    : `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;
  const attempt = async (token?: string) =>
    fetch(url, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init.headers || {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

  let token = getAccessToken() ?? undefined;
  let res = await attempt(token);
  if (res.status === 401 && getRefreshToken()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      token = getAccessToken() ?? undefined;
      res = await attempt(token);
    }
  }

  if (!res.ok) {
    let errorMessage = `HTTP ${res.status}`;
    try {
      const errorText = await res.text();
      errorMessage = errorText || errorMessage;
    } catch {
      // If we can't read the response, use the status
    }
    throw new Error(errorMessage);
  }

  let text = "";
  try {
    text = await res.text();
    if (!text.trim()) {
      return {};
    }
    return JSON.parse(text);
  } catch (error) {
    console.error(
      "Response headers:",
      Object.fromEntries(res.headers.entries())
    );
    console.error("Response text:", text);
    throw new Error("Invalid JSON response from server");
  }
}
