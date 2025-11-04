import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getAccessToken } from "../auth";

const WS_BASE = (import.meta as any).env?.VITE_WS_BASE ?? "ws://localhost:8000";

export function TableWebSocket() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const wsRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [inputMessage, setInputMessage] = useState("");

  useEffect(() => {
    if (!id) {
      navigate("/tables");
      return;
    }

    const token = getAccessToken();
    if (!token) {
      navigate("/login");
      return;
    }

    const wsUrl = `${WS_BASE}/ws/tables/${id}/?token=${encodeURIComponent(
      token
    )}`;
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    wsRef.current = ws;

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [id, navigate]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN ||
      !inputMessage.trim()
    ) {
      return;
    }

    wsRef.current.send(JSON.stringify({ message: inputMessage }));
    setInputMessage("");
  };

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h1>WebSocket: {id}</h1>

      <form onSubmit={sendMessage} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type message and press Enter..."
          style={{ width: "500px", padding: "8px" }}
        />
        <button
          type="submit"
          style={{ marginLeft: "10px", padding: "8px 16px" }}
        >
          Send
        </button>
      </form>

      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          minHeight: "400px",
          maxHeight: "600px",
          overflow: "auto",
        }}
      >
        <h2>Responses:</h2>
        {messages.length === 0 ? (
          <p>No messages yet...</p>
        ) : (
          messages.map((msg, idx) => (
            <pre key={idx} style={{ margin: "5px 0", whiteSpace: "pre-wrap" }}>
              {msg}
            </pre>
          ))
        )}
      </div>
    </div>
  );
}
