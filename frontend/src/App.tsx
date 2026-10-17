import React, { useState, useEffect } from "react";
import {
  checkHealth,
  fetchSubgraph,
  fetchTickets,
  ingestDocument,
  seedGraph,
  sendChatMessage,
} from "./api";
import type { GraphData, Ticket, TraceStep } from "./api";
import { Chat } from "./components/Chat";
import { TracePanel } from "./components/TracePanel";
import { GraphView } from "./components/GraphView";
import { TicketCard } from "./components/TicketCard";
import { Database, ShieldAlert, Cpu, RefreshCw, GitBranch } from "lucide-react";

export const App: React.FC = () => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] });
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [traces, setTraces] = useState<TraceStep[]>([]);
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [health, setHealth] = useState<any>({ database_connected: false, provider: "groq" });
  const [loadingGraph, setLoadingGraph] = useState(false);

  const loadAll = async () => {
    try {
      setLoadingGraph(true);
      const [h, g, t] = await Promise.all([checkHealth(), fetchSubgraph(), fetchTickets()]);
      setHealth(h);
      setGraphData(g);
      setTickets(t);
    } catch (err) {
      console.error("Failed to load initial data", err);
    } finally {
      setLoadingGraph(false);
    }
  };

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = (query: string) => {
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setIsStreaming(true);

    let assistantText = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    sendChatMessage(
      query,
      (traceStep) => {
        setTraces((prev) => [...prev, traceStep]);
      },
      (token) => {
        assistantText += token;
        setMessages((prev) => {
          const next = [...prev];
          next[next.length - 1] = { role: "assistant", content: assistantText };
          return next;
        });
      },
      () => {
        setIsStreaming(false);
        loadAll();
      },
      (err) => {
        setIsStreaming(false);
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `Error executing query: ${err}` },
        ]);
      }
    );
  };

  const handleIngestDemoDoc = async () => {
    setIsStreaming(true);
    setTraces((prev) => [
      ...prev,
      {
        step: "tool_call",
        tool: "process_document_ingestion",
        args: { file: "pricing_note.md" },
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);

    const demoText = `Executive Incident Note: Q1 Benchmark Audit. During our sustained peak load test, our unlogged PostgreSQL cache tables suffered write-lock contention, increasing p95 read latency to 85ms. Consequently, ASM-LATENCY-Q1 is broken and invalid under production scale. Immediate directive: invalidate ASM-LATENCY-Q1 and review dependent services.`;

    try {
      const res = await ingestDocument(demoText);
      setTraces((prev) => [
        ...prev,
        {
          step: "tool_result",
          tool: "process_document_ingestion",
          result: res,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Ingested Incident Note successfully! Assumption ASM-LATENCY-Q1 has been marked invalid, and review tickets have been automatically drafted for downstream dependent services.`,
        },
      ]);
      await loadAll();
    } catch (err: any) {
      console.error(err);
    } finally {
      setIsStreaming(false);
    }
  };

  const handleSeedGraph = async () => {
    try {
      setLoadingGraph(true);
      await seedGraph();
      await loadAll();
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingGraph(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "#f1f5f9", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <header
        style={{
          height: "56px",
          backgroundColor: "#0f172a",
          color: "#ffffff",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "0 20px",
          borderBottom: "1px solid #334155",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <GitBranch size={22} color="#38bdf8" />
            <span style={{ fontWeight: 700, fontSize: "16px", letterSpacing: "-0.02em" }}>Why Did We?</span>
          </div>
          <span style={{ fontSize: "12px", color: "#94a3b8", borderLeft: "1px solid #334155", paddingLeft: "12px" }}>
            Institutional Decision & Blast-Radius Engine
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", color: "#cbd5e1" }}>
            <Database size={14} color={health.database_connected ? "#4ade80" : "#f87171"} />
            <span>FalkorDB:</span>
            <strong style={{ color: health.database_connected ? "#4ade80" : "#f87171" }}>
              {health.database_connected ? `Connected (${health.graph_nodes} nodes)` : "Disconnected"}
            </strong>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", color: "#cbd5e1" }}>
            <Cpu size={14} color="#38bdf8" />
            <span>LLM:</span>
            <strong style={{ color: "#38bdf8", textTransform: "uppercase" }}>{health.provider || "groq"}</strong>
          </div>

          <button
            onClick={handleSeedGraph}
            disabled={loadingGraph}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              padding: "5px 12px",
              borderRadius: "6px",
              border: "1px solid #475569",
              backgroundColor: "#1e293b",
              color: "#f8fafc",
              fontSize: "12px",
              cursor: loadingGraph ? "wait" : "pointer",
            }}
          >
            <RefreshCw size={12} className={loadingGraph ? "spin-icon" : ""} />
            Seed / Reset Graph
          </button>
        </div>
      </header>

      {/* Main 3-Column Content */}
      <main style={{ flex: 1, display: "grid", gridTemplateColumns: "35% 30% 35%", gap: "12px", padding: "12px", overflow: "hidden" }}>
        {/* Left Column: Chat & Triage Tickets */}
        <section style={{ display: "flex", flexDirection: "column", gap: "12px", height: "100%", overflow: "hidden" }}>
          <div style={{ flex: 1, minHeight: 0 }}>
            <Chat
              onSendMessage={handleSendMessage}
              messages={messages}
              isStreaming={isStreaming}
              onIngestDemoDoc={handleIngestDemoDoc}
            />
          </div>

          {/* Actionable Review Tickets Drawer */}
          {tickets.length > 0 && (
            <div
              style={{
                height: "210px",
                backgroundColor: "#ffffff",
                borderRadius: "8px",
                border: "1px solid #e2e8f0",
                display: "flex",
                flexDirection: "column",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  padding: "8px 14px",
                  borderBottom: "1px solid #e2e8f0",
                  backgroundColor: "#f8fafc",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  fontSize: "13px",
                  fontWeight: 600,
                  color: "#0f172a",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <ShieldAlert size={15} color="#d97706" />
                  <span>Actionable Review Tickets ({tickets.length})</span>
                </div>
              </div>
              <div style={{ flex: 1, overflowY: "auto", padding: "10px" }}>
                {tickets.map((t) => (
                  <TicketCard key={t.id} ticket={t} onRefresh={loadAll} />
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Center Column: Execution Trace */}
        <section style={{ height: "100%", overflow: "hidden" }}>
          <TracePanel traces={traces} isStreaming={isStreaming} />
        </section>

        {/* Right Column: Cytoscape Knowledge Graph */}
        <section style={{ height: "100%", overflow: "hidden" }}>
          <GraphView graphData={graphData} onRefresh={loadAll} isLoading={loadingGraph} />
        </section>
      </main>
    </div>
  );
};

export default App;
