import client from "./client";

class ChatWebSocketService {
  constructor() {
    this.ws = null;
    this.status = "disconnected"; // "connecting" | "connected" | "disconnected" | "error"
    this.listeners = new Map();
    this.pendingRequests = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectTimer = null;
    this.url = this.getWebSocketUrl();
  }

  getWebSocketUrl() {
    if (import.meta.env.VITE_WS_URL) {
      return import.meta.env.VITE_WS_URL;
    }
    const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
    const wsBase = apiUrl.replace(/^http/, "ws");
    return `${wsBase.replace(/\/$/, "")}/ws/chat`;
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach((cb) => {
        try {
          cb(data);
        } catch (e) {
          console.error(`Error in WebSocket listener for ${event}:`, e);
        }
      });
    }
  }

  setStatus(newStatus) {
    if (this.status !== newStatus) {
      this.status = newStatus;
      this.emit("status_change", newStatus);
    }
  }

  connect() {
    if (
      this.ws &&
      (this.ws.readyState === WebSocket.CONNECTING ||
        this.ws.readyState === WebSocket.OPEN)
    ) {
      return;
    }

    this.setStatus("connecting");

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.setStatus("connected");
        this.reconnectAttempts = 0;
        this.emit("open");
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          // Emit general message event
          this.emit("message", data);

          // Check if data contains live context update
          if (data.context) {
            this.emit("context_update", data.context);
          }

          // Resolve pending request if correlated by request_id
          if (data.request_id && this.pendingRequests.has(data.request_id)) {
            const { resolve, timer } = this.pendingRequests.get(data.request_id);
            clearTimeout(timer);
            this.pendingRequests.delete(data.request_id);
            resolve(data);
          } else if (this.pendingRequests.size > 0) {
            // Resolve oldest pending request if request_id not returned
            const [firstKey, { resolve, timer }] = this
              .pendingRequests
              .entries()
              .next().value;
            clearTimeout(timer);
            this.pendingRequests.delete(firstKey);
            resolve(data);
          }
        } catch (err) {
          console.error("Failed to parse WebSocket message:", err);
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket connection error:", error);
        this.setStatus("error");
        this.emit("error", error);
      };

      this.ws.onclose = (event) => {
        this.setStatus("disconnected");
        this.emit("close", event);
        this.scheduleReconnect();
      };
    } catch (e) {
      console.error("Failed to construct WebSocket:", e);
      this.setStatus("error");
      this.scheduleReconnect();
    }
  }

  scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      this.reconnectAttempts++;
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = setTimeout(() => {
        this.connect();
      }, delay);
    }
  }

  disconnect() {
    clearTimeout(this.reconnectTimer);
    this.maxReconnectAttempts = 0;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.setStatus("disconnected");
  }

  sendRequest(payload, timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
      const request_id = `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
      const requestData =
        typeof payload === "string" ? { message: payload } : { ...payload };

      const storedUserId = localStorage.getItem("user_id");
      if (!requestData.user_id && storedUserId) {
        requestData.user_id = parseInt(storedUserId, 10);
      }
      requestData.request_id = request_id;

      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        const timer = setTimeout(() => {
          if (this.pendingRequests.has(request_id)) {
            this.pendingRequests.delete(request_id);
            // Fallback to HTTP if WS request times out
            this.sendHttpFallback(requestData).then(resolve).catch(reject);
          }
        }, timeoutMs);

        this.pendingRequests.set(request_id, { resolve, reject, timer });
        this.ws.send(JSON.stringify(requestData));
      } else {
        // If WS not open, use HTTP directly (do NOT also trigger WS connect while HTTP is in-flight to avoid double responses)
        this.connect(); // connect for future requests only
        this.sendHttpFallback(requestData).then(resolve).catch(reject);
      }
    });
  }

  async sendHttpFallback(requestData) {
    try {
      const response = await client.post("/chat", requestData);
      if (response.data?.context) {
        this.emit("context_update", response.data.context);
      }
      return response.data;
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to send chat message over WebSocket and HTTP fallback.";
      throw new Error(message, { cause: error });
    }
  }
}

export const chatSocket = new ChatWebSocketService();

export async function sendMessage(payload) {
  return chatSocket.sendRequest(payload);
}