import React, { useState, useRef, useEffect } from "react";
import { Send, Sparkles, FileText, Upload } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatProps {
  onSendMessage: (query: string) => void;
  messages: Message[];
  isStreaming: boolean;
  onIngestDemoDoc: () => void;
}

export const Chat: React.FC<ChatProps> = ({ onSendMessage, messages, isStreaming, onIngestDemoDoc }) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    onSendMessage(input.trim());
    setInput("");
  };

  const handleChipClick = (query: string) => {
    if (isStreaming) return;
    onSendMessage(query);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        backgroundColor: "#ffffff",
        borderRadius: "8px",
        overflow: "hidden",
        border: "1px solid #e2e8f0",
      }}
    >
      <div
        style={{
          padding: "12px 16px",
          borderBottom: "1px solid #e2e8f0",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          backgroundColor: "#f8fafc",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600, color: "#0f172a", fontSize: "14px" }}>
          <Sparkles size={18} color="#2563eb" />
          <span>Briefing & Recorder Agent</span>
        </div>
        <button
          onClick={onIngestDemoDoc}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "4px",
            padding: "4px 8px",
            borderRadius: "6px",
            border: "1px solid #cbd5e1",
            backgroundColor: "#ffffff",
            fontSize: "12px",
            cursor: "pointer",
            fontWeight: 500,
            color: "#334155",
          }}
          title="Ingest pricing_note.md benchmark report"
        >
          <Upload size={13} color="#2563eb" />
          Ingest Demo Note
        </button>
      </div>

      {/* Suggested demo chips */}
      <div style={{ padding: "8px 12px", borderBottom: "1px solid #f1f5f9", display: "flex", gap: "6px", overflowX: "auto" }}>
        <button
          onClick={() => handleChipClick("Why did we switch to Postgres for caching?")}
          style={{
            padding: "4px 8px",
            borderRadius: "14px",
            border: "1px solid #e2e8f0",
            backgroundColor: "#f8fafc",
            color: "#475569",
            fontSize: "11px",
            cursor: "pointer",
            whiteSpace: "nowrap",
          }}
        >
          Trace Postgres Caching
        </button>
        <button
          onClick={() => handleChipClick("What breaks if benchmark latency assumption ASM-LATENCY-Q1 is invalid?")}
          style={{
            padding: "4px 8px",
            borderRadius: "14px",
            border: "1px solid #e2e8f0",
            backgroundColor: "#f8fafc",
            color: "#475569",
            fontSize: "11px",
            cursor: "pointer",
            whiteSpace: "nowrap",
          }}
        >
          Blast Radius: ASM-LATENCY-Q1
        </button>
        <button
          onClick={() => handleChipClick("Who decided on Stripe payments and what was the rationale?")}
          style={{
            padding: "4px 8px",
            borderRadius: "14px",
            border: "1px solid #e2e8f0",
            backgroundColor: "#f8fafc",
            color: "#475569",
            fontSize: "11px",
            cursor: "pointer",
            whiteSpace: "nowrap",
          }}
        >
          Trace Stripe Agreement
        </button>
      </div>

      {/* Message history */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", display: "flex", flexDirection: "column", gap: "12px" }}>
        {messages.length === 0 ? (
          <div style={{ color: "#94a3b8", textAlign: "center", marginTop: "40px", fontSize: "13px" }}>
            <FileText size={32} style={{ margin: "0 auto 12px", opacity: 0.5 }} />
            Ask why any architectural decision was made, or inspect blast radius for invalid assumptions.
          </div>
        ) : (
          messages.map((m, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                maxWidth: "85%",
                padding: "10px 14px",
                borderRadius: "10px",
                fontSize: "13px",
                lineHeight: "1.5",
                backgroundColor: m.role === "user" ? "#2563eb" : "#f1f5f9",
                color: m.role === "user" ? "#ffffff" : "#0f172a",
                whiteSpace: "pre-wrap",
              }}
            >
              {m.content}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <form onSubmit={handleSubmit} style={{ padding: "12px", borderTop: "1px solid #e2e8f0", display: "flex", gap: "8px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask why a decision was made, or check blast radius..."
          disabled={isStreaming}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "6px",
            border: "1px solid #cbd5e1",
            outline: "none",
            fontSize: "13px",
          }}
        />
        <button
          type="submit"
          disabled={isStreaming || !input.trim()}
          style={{
            padding: "10px 16px",
            borderRadius: "6px",
            border: "none",
            backgroundColor: "#2563eb",
            color: "#ffffff",
            cursor: isStreaming || !input.trim() ? "not-allowed" : "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Send size={15} />
        </button>
      </form>
    </div>
  );
};
