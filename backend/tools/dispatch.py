import json
from backend.tools.cypher import run_cypher_query
from backend.tools.traversal import trace_decision, find_dependents, search_decisions
from backend.tools.algorithms import get_critical_decisions, get_fragile_assumptions
from backend.tools.writes import update_assumption, draft_ticket, confirm_ticket, record_decision

TOOL_REGISTRY = {
    "trace_decision": trace_decision,
    "find_dependents": find_dependents,
    "search_decisions": search_decisions,
    "run_cypher_query": run_cypher_query,
    "get_critical_decisions": get_critical_decisions,
    "get_fragile_assumptions": get_fragile_assumptions,
    "update_assumption": update_assumption,
    "draft_ticket": draft_ticket,
    "confirm_ticket": confirm_ticket,
    "record_decision": record_decision,
}

def dispatch_tool(tool_name: str, arguments: dict) -> dict:
    handler = TOOL_REGISTRY.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        if isinstance(arguments, str):
            arguments = json.loads(arguments)
        return handler(**arguments)
    except Exception as exc:
        return {"error": f"Tool execution failed: {str(exc)}"}
