import React, { useEffect, useRef, useState } from "react";
import cytoscape from "cytoscape";
import type { GraphData } from "../api";
import { Maximize2, RefreshCw, X } from "lucide-react";

interface GraphViewProps {
  graphData: GraphData;
  onRefresh: () => void;
  isLoading: boolean;
}

export const GraphView: React.FC<GraphViewProps> = ({ graphData, onRefresh, isLoading }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const elements = [
      ...graphData.nodes.map((n) => ({
        group: "nodes" as const,
        data: {
          id: n.data.id,
          label: n.data.label,
          type: n.data.type,
          color: n.data.color,
          full_label: n.data.full_label,
          properties: n.data.properties,
        },
      })),
      ...graphData.edges.map((e) => ({
        group: "edges" as const,
        data: {
          id: e.data.id,
          source: e.data.source,
          target: e.data.target,
          label: e.data.label,
        },
      })),
    ];

    if (!cyRef.current) {
      cyRef.current = cytoscape({
        container: containerRef.current,
        elements: elements,
        style: [
          {
            selector: "node",
            style: {
              "background-color": "data(color)",
              label: "data(label)",
              color: "#ffffff",
              "font-size": "11px",
              "text-valign": "center",
              "text-halign": "center",
              "text-outline-color": "#0f172a",
              "text-outline-width": 2,
              width: 44,
              height: 44,
            },
          },
          {
            selector: "node[type = 'Decision']",
            style: {
              shape: "round-rectangle",
              width: 58,
              height: 38,
            },
          },
          {
            selector: "node[type = 'Assumption']",
            style: {
              shape: "diamond",
              width: 44,
              height: 44,
            },
          },
          {
            selector: "node[type = 'Ticket']",
            style: {
              shape: "hexagon",
              width: 48,
              height: 48,
              "border-width": 2,
              "border-color": "#ffffff",
              "border-style": "dashed",
            },
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#475569",
              "target-arrow-color": "#475569",
              "target-arrow-shape": "triangle",
              "curve-style": "bezier",
              label: "data(label)",
              "font-size": "8px",
              color: "#94a3b8",
              "text-rotation": "autorotate",
              "text-margin-y": -8,
            },
          },
          {
            selector: ":selected",
            style: {
              "border-width": 3,
              "border-color": "#38bdf8",
              "line-color": "#38bdf8",
              "target-arrow-color": "#38bdf8",
            },
          },
        ],
        layout: {
          name: "cose",
          animate: true,
          padding: 30,
        },
      });

      cyRef.current.on("tap", "node", (evt) => {
        const node = evt.target;
        setSelectedNode({
          id: node.data("id"),
          type: node.data("type"),
          label: node.data("full_label") || node.data("label"),
          color: node.data("color"),
          properties: node.data("properties") || {},
        });
      });

      cyRef.current.on("tap", (evt) => {
        if (evt.target === cyRef.current) {
          setSelectedNode(null);
        }
      });
    } else {
      cyRef.current.json({ elements });
      cyRef.current.layout({ name: "cose", animate: false, padding: 30 }).run();
    }
  }, [graphData]);

  const handleFit = () => {
    if (cyRef.current) cyRef.current.fit(undefined, 30);
  };

  return (
    <div
      style={{
        position: "relative",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#0b0f19",
        borderRadius: "8px",
        overflow: "hidden",
        border: "1px solid #1e293b",
      }}
    >
      <div
        style={{
          padding: "10px 16px",
          backgroundColor: "#1e293b",
          borderBottom: "1px solid #334155",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          color: "#f8fafc",
          fontSize: "13px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600 }}>
          <span>FalkorDB Knowledge Graph</span>
          <span style={{ fontSize: "11px", backgroundColor: "#334155", padding: "2px 8px", borderRadius: "10px" }}>
            {graphData.nodes.length} nodes · {graphData.edges.length} edges
          </span>
        </div>

        <div style={{ display: "flex", gap: "8px" }}>
          <button
            onClick={handleFit}
            title="Fit Graph"
            style={{
              padding: "4px 8px",
              borderRadius: "4px",
              backgroundColor: "#334155",
              color: "#f8fafc",
              border: "none",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: "4px",
              fontSize: "12px",
            }}
          >
            <Maximize2 size={13} /> Fit
          </button>
          <button
            onClick={onRefresh}
            disabled={isLoading}
            title="Refresh Graph"
            style={{
              padding: "4px 8px",
              borderRadius: "4px",
              backgroundColor: "#2563eb",
              color: "#ffffff",
              border: "none",
              cursor: isLoading ? "wait" : "pointer",
              display: "flex",
              alignItems: "center",
              gap: "4px",
              fontSize: "12px",
            }}
          >
            <RefreshCw size={13} className={isLoading ? "spin-icon" : ""} /> Refresh
          </button>
        </div>
      </div>

      <div ref={containerRef} style={{ flex: 1, width: "100%", height: "100%" }} />

      {/* Selected Node Details Drawer */}
      {selectedNode && (
        <div
          style={{
            position: "absolute",
            bottom: "16px",
            right: "16px",
            width: "320px",
            backgroundColor: "#1e293b",
            color: "#f8fafc",
            borderRadius: "8px",
            padding: "14px",
            boxShadow: "0 10px 25px -5px rgba(0,0,0,0.5)",
            border: `1px solid ${selectedNode.color}`,
            fontSize: "12px",
            zIndex: 10,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
            <div>
              <span
                style={{
                  display: "inline-block",
                  padding: "2px 6px",
                  borderRadius: "4px",
                  backgroundColor: selectedNode.color,
                  color: "#ffffff",
                  fontSize: "10px",
                  fontWeight: 700,
                  marginBottom: "4px",
                }}
              >
                {selectedNode.type}
              </span>
              <div style={{ fontWeight: 700, fontSize: "14px" }}>{selectedNode.id}</div>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer" }}
            >
              <X size={16} />
            </button>
          </div>

          <div style={{ color: "#cbd5e1", marginBottom: "8px" }}>{selectedNode.label}</div>

          <div style={{ backgroundColor: "#0f172a", padding: "8px", borderRadius: "4px", maxHeight: "150px", overflowY: "auto" }}>
            {Object.entries(selectedNode.properties).map(([k, v]) => (
              <div key={k} style={{ marginBottom: "4px" }}>
                <span style={{ color: "#94a3b8" }}>{k}: </span>
                <span style={{ color: "#f1f5f9" }}>{String(v)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
