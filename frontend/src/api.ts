export const API_BASE = "http://localhost:8000";

export interface GraphNode {
  data: {
    id: string;
    label: string;
    full_label: string;
    type: string;
    color: string;
    properties: Record<string, any>;
  };
}

export interface GraphEdge {
  data: {
    id: string;
    source: string;
    target: string;
    label: string;
  };
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface Ticket {
  id: string;
  title: string;
  priority: string;
  reason: string;
  status: "draft" | "confirmed";
  created_at: string;
  decision_id: string;
  decision_title: string;
}

export interface TraceStep {
  step: "tool_call" | "tool_result" | "error";
  tool?: string;
  args?: Record<string, any>;
  result?: any;
  error?: string;
  timestamp: string;
}

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchSubgraph(): Promise<GraphData> {
  const res = await fetch(`${API_BASE}/graph/subgraph`);
  return res.json();
}

export async function fetchTickets(): Promise<Ticket[]> {
  const res = await fetch(`${API_BASE}/tickets`);
  return res.json();
}

export async function confirmTicket(ticketId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/tickets/${ticketId}/confirm`, {
    method: "POST",
  });
  return res.json();
}

export async function ingestDocument(text: string): Promise<any> {
  const res = await fetch(`${API_BASE}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return res.json();
}

export async function seedGraph(): Promise<any> {
  const res = await fetch(`${API_BASE}/graph/seed`, { method: "POST" });
  return res.json();
}

export async function sendChatMessage(
  query: string,
  onTrace: (step: TraceStep) => void,
  onToken: (token: string) => void,
  onDone: () => void,
  onError: (err: string) => void
) {
  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!res.body) {
      onError("No response body received from server.");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n\n");
      buffer = lines.pop() || "";

      for (const block of lines) {
        if (!block.trim()) continue;
        const eventMatch = block.match(/event:\s*([^\n]+)/);
        const dataMatch = block.match(/data:\s*([^\n]+)/);

        const eventType = eventMatch ? eventMatch[1].trim() : "message";
        const dataStr = dataMatch ? dataMatch[1].trim() : "{}";

        try {
          const parsed = JSON.parse(dataStr);
          const now = new Date().toLocaleTimeString();

          if (eventType === "trace") {
            onTrace({ ...parsed, timestamp: now });
          } else if (eventType === "token") {
            if (parsed.content) onToken(parsed.content);
          } else if (eventType === "done") {
            onDone();
          }
        } catch (e) {
          console.error("Failed to parse SSE line", e);
        }
      }
    }
    onDone();
  } catch (err: any) {
    onError(err.message || String(err));
  }
}
