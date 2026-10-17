try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception:
        FastMCP = None

from backend.tools.traversal import trace_decision, find_dependents, search_decisions
from backend.tools.cypher import run_cypher_query
from backend.tools.algorithms import get_critical_decisions
from backend.tools.writes import update_assumption, draft_ticket, confirm_ticket

mcp_app = FastMCP("WhyDidWe-GraphTools") if FastMCP else None

if mcp_app:
    @mcp_app.tool()
    def mcp_trace_decision(decision_id: str, depth: int = 2) -> dict:
        return trace_decision(decision_id, depth)

    @mcp_app.tool()
    def mcp_find_dependents(assumption_id: str) -> dict:
        return find_dependents(assumption_id)

    @mcp_app.tool()
    def mcp_search_decisions(keyword: str, domain: str = None) -> list:
        return search_decisions(keyword, domain)

    @mcp_app.tool()
    def mcp_run_cypher(query: str) -> list:
        return run_cypher_query(query)

    @mcp_app.tool()
    def mcp_get_critical_decisions(limit: int = 5) -> list:
        return get_critical_decisions(limit)

    @mcp_app.tool()
    def mcp_update_assumption(assumption_id: str, valid: bool, reason: str = "") -> dict:
        return update_assumption(assumption_id, valid, reason)

    @mcp_app.tool()
    def mcp_draft_ticket(decision_id: str, title: str, priority: str = "P1", reason: str = "") -> dict:
        return draft_ticket(decision_id, title, priority, reason)

    @mcp_app.tool()
    def mcp_confirm_ticket(ticket_id: str) -> dict:
        return confirm_ticket(ticket_id)

if __name__ == "__main__":
    if mcp_app:
        mcp_app.run()
