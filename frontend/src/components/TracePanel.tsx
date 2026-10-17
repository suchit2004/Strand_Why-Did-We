import type { TraceStep } from "../api";
import { Activity, Terminal, ArrowRight, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

interface TracePanelProps {
  traces: TraceStep[];
  isStreaming: boolean;
}

export const TracePanel: React.FC<TracePanelProps> = ({ traces, isStreaming }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        backgroundColor: "#0f172a",
        color: "#f8fafc",
        borderRadius: "8px",
        overflow: "hidden",
        border: "1px solid #1e293b",
      }}
    >
      <div
        style={{
          padding: "12px 16px",
          borderBottom: "1px solid #1e293b",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          backgroundColor: "#1e293b",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600, fontSize: "14px" }}>
          <Activity size={18} color="#38bdf8" />
          <span>Agent Execution Trace</span>
        </div>
        {isStreaming && (
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", color: "#38bdf8" }}>
            <Loader2 size={14} className="spin-icon" style={{ animation: "spin 1s linear infinite" }} />
            <span>Traversing Graph...</span>
          </div>
        )}
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "16px", display: "flex", flexDirection: "column", gap: "12px" }}>
        {traces.length === 0 ? (
          <div style={{ color: "#64748b", textAlign: "center", marginTop: "40px", fontSize: "13px" }}>
            <Terminal size={32} style={{ margin: "0 auto 12px", opacity: 0.5 }} />
            No tool executions yet. Ask a question to see real-time graph reasoning!
          </div>
        ) : (
          traces.map((trace, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: "#1e293b",
                borderRadius: "6px",
                padding: "10px 12px",
                borderLeft: trace.step === "tool_call" ? "4px solid #38bdf8" : trace.step === "error" ? "4px solid #ef4444" : "4px solid #10b981",
                fontSize: "12px",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <span style={{ fontWeight: 700, color: trace.step === "tool_call" ? "#38bdf8" : "#34d399", display: "flex", alignItems: "center", gap: "6px" }}>
                  {trace.step === "tool_call" ? <ArrowRight size={13} /> : <CheckCircle size={13} />}
                  {trace.tool || "Operation"}
                </span>
                <span style={{ color: "#64748b", fontSize: "11px" }}>{trace.timestamp}</span>
              </div>

              {trace.args && (
                <div style={{ marginTop: "4px" }}>
                  <span style={{ color: "#94a3b8" }}>Arguments: </span>
                  <code style={{ color: "#fef08a", fontFamily: "monospace" }}>
                    {JSON.stringify(trace.args)}
                  </code>
                </div>
              )}

              {trace.result && (
                <div style={{ marginTop: "6px", backgroundColor: "#0f172a", padding: "6px 8px", borderRadius: "4px", overflowX: "auto" }}>
                  <pre style={{ margin: 0, fontFamily: "monospace", color: "#a7f3d0", fontSize: "11px" }}>
                    {JSON.stringify(trace.result, null, 2)}
                  </pre>
                </div>
              )}

              {trace.error && (
                <div style={{ marginTop: "4px", color: "#f87171", display: "flex", alignItems: "center", gap: "4px" }}>
                  <AlertCircle size={13} /> {trace.error}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
