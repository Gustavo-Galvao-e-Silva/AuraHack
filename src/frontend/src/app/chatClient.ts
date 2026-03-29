export type CloudChatMessage = {
  id: string;
  role: "self" | "other";
  content: string;
  created_at: string;
};

export type ConversationHistoryResponse = {
  conversation_id: string;
  messages: CloudChatMessage[];
};

export type ChatSocketEvent =
  | {
      type: "connection_established";
      conversation_id: string;
    }
  | {
      type: "new_message";
      conversation_id: string;
      message: CloudChatMessage;
    }
  | {
      type: "error";
      message: string;
    };

const CHAT_HTTP_BASE_URL = "http://35.172.182.0:6000";
const CHAT_WS_BASE_URL   = "ws://35.172.182.0:6000";

export async function fetchConversationHistory(
  conversationId: string,
  perspective: string
): Promise<ConversationHistoryResponse> {
  const response = await fetch(
    `${CHAT_HTTP_BASE_URL}/chat/history/${encodeURIComponent(conversationId)}?perspective=${encodeURIComponent(perspective)}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (!response.ok) {
    throw new Error("Failed to fetch conversation history.");
  }
  return response.json();
}

export function createConversationSocket(
  conversationId: string,
  email: string,
  handlers?: {
    onOpen?: () => void;
    onClose?: () => void;
    onError?: (event: Event) => void;
    onMessage?: (event: ChatSocketEvent) => void;
  }
): WebSocket {
  const socket = new WebSocket(
    `${CHAT_WS_BASE_URL}/chat/ws/${encodeURIComponent(conversationId)}`
  );

  socket.onopen = () => {
    // Complete the identity handshake as soon as the socket opens.
    // The server sends an "identify" challenge first — we respond immediately.
    socket.send(JSON.stringify({ type: "identify", email }));
    handlers?.onOpen?.();
  };

  socket.onclose = () => {
    handlers?.onClose?.();
  };

  socket.onerror = (event) => {
    handlers?.onError?.(event);
  };

  socket.onmessage = (event) => {
    try {
      const parsed = JSON.parse(event.data) as ChatSocketEvent;
      // Skip the identify challenge and connection_established internally —
      // only surface new_message and error to the caller.
      if (
        (parsed as any).type === "identify" ||
        parsed.type === "connection_established"
      ) {
        return;
      }
      handlers?.onMessage?.(parsed);
    } catch (error) {
      console.error("Failed to parse websocket message:", error);
    }
  };

  return socket;
}

export function sendSocketMessage(
  socket: WebSocket,
  payload: {
    content: string;
  }
) {
  if (socket.readyState !== WebSocket.OPEN) {
    throw new Error("WebSocket is not open.");
  }
  socket.send(JSON.stringify(payload));
}
