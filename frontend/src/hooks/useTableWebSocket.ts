import { useState, useEffect, useRef, useCallback } from "react";
import { getAccessToken } from "../auth";

const WS_BASE = (import.meta as any).env?.VITE_WS_BASE ?? "ws://localhost:8000";

export interface UseTableWebSocketResult {
  connected: boolean;
  pending: boolean;
  error: string | null;
  sendMessage: (action: string, data: any) => void;
}

export function useTableWebSocket(
  tableId: string | undefined,
  enabled: boolean,
  onMessage: (message: any) => void
): UseTableWebSocketResult {
  const [connected, setConnected] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const onMessageRef = useRef(onMessage);

  // Keep onMessage ref updated
  useEffect(() => {
    onMessageRef.current = onMessage;
  }, [onMessage]);

  useEffect(() => {
    if (!tableId || !enabled) return;

    const token = getAccessToken();
    // Connect with or without token - backend allows AnonymousUser
    const wsUrl = token
      ? `${WS_BASE}/ws/tables/${tableId}/?token=${encodeURIComponent(token)}`
      : `${WS_BASE}/ws/tables/${tableId}/`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket connected");
      setConnected(true);
      setPending(false);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        onMessageRef.current(message);

        if (message.type === "table_action") {
          setPending(false);
          setError(null);
        } else if (message.type === "error") {
          setError(
            message.data?.detail || message.data?.message || "An error occurred"
          );
          setPending(false);
        }
      } catch (e) {
        console.error("Failed to parse WebSocket message:", e);
        setPending(false);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setError("WebSocket connection error");
      setConnected(false);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      setConnected(false);
    };

    wsRef.current = ws;

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [tableId, enabled]);

  const sendMessage = useCallback((action: string, data: any) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      setError("WebSocket not connected");
      return;
    }

    setPending(true);
    setError(null);

    wsRef.current.send(
      JSON.stringify({
        action,
        data,
      })
    );
  }, []);

  return {
    connected,
    pending,
    error,
    sendMessage,
  };
}
