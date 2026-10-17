import React, { useState } from "react";
import { confirmTicket } from "../api";
import type { Ticket } from "../api";
import { CheckCircle2, Clock } from "lucide-react";

interface TicketCardProps {
  ticket: Ticket;
  onRefresh: () => void;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket, onRefresh }) => {
  const [loading, setLoading] = useState(false);

  const handleConfirm = async () => {
    setLoading(true);
    try {
      await confirmTicket(ticket.id);
      onRefresh();
    } catch (err) {
      console.error("Failed to confirm ticket", err);
    } finally {
      setLoading(false);
    }
  };

  const isConfirmed = ticket.status === "confirmed";

  return (
    <div
      style={{
        padding: "12px",
        borderRadius: "8px",
        backgroundColor: isConfirmed ? "#f0fdf4" : "#fffbeb",
        border: `1px solid ${isConfirmed ? "#86efac" : "#fde68a"}`,
        marginBottom: "10px",
        fontSize: "13px",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontWeight: 600, color: "#1e293b" }}>{ticket.id}</span>
        <span
          style={{
            padding: "2px 8px",
            borderRadius: "12px",
            fontSize: "11px",
            fontWeight: 700,
            backgroundColor: ticket.priority === "P0" ? "#fee2e2" : "#fef3c7",
            color: ticket.priority === "P0" ? "#b91c1c" : "#b45309",
          }}
        >
          {ticket.priority}
        </span>
      </div>

      <div style={{ margin: "6px 0", fontWeight: 500, color: "#334155" }}>
        {ticket.title}
      </div>

      {ticket.reason && (
        <div style={{ color: "#64748b", fontSize: "12px", marginBottom: "8px" }}>
          {ticket.reason}
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: "11px", color: "#94a3b8" }}>
          Target: {ticket.decision_id || "Unassigned"}
        </span>

        {isConfirmed ? (
          <span
            style={{
              display: "flex",
              alignItems: "center",
              gap: "4px",
              color: "#15803d",
              fontWeight: 600,
              fontSize: "12px",
            }}
          >
            <CheckCircle2 size={14} /> Confirmed
          </span>
        ) : (
          <button
            onClick={handleConfirm}
            disabled={loading}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "4px",
              padding: "4px 10px",
              borderRadius: "6px",
              border: "none",
              backgroundColor: "#d97706",
              color: "#ffffff",
              cursor: loading ? "wait" : "pointer",
              fontWeight: 600,
              fontSize: "12px",
            }}
          >
            <Clock size={13} /> {loading ? "Updating..." : "Confirm Ticket"}
          </button>
        )}
      </div>
    </div>
  );
};
