import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.config import settings
from backend.graph.client import get_graph
from backend.graph.loader import load_seed_data
from backend.agents.briefing import stream_briefing
from backend.agents.recorder import process_document_ingestion
from backend.tools.writes import confirm_ticket

app = FastAPI(title="Why Did We? Institutional Memory Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class IngestRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    db_ok = False
    node_count = 0
    try:
        graph = get_graph()
        res = graph.query("MATCH (n) RETURN count(n) AS cnt")
        if res.result_set:
            node_count = res.result_set[0][0]
            db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "healthy" if db_ok else "database_unreachable",
        "database_connected": db_ok,
        "graph_nodes": node_count,
        "provider": settings.LLM_PROVIDER
    }

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    async def event_generator():
        async for chunk in stream_briefing(req.query):
            evt_type = chunk.get("event", "message")
            data_str = json.dumps(chunk.get("data", {}))
            yield f"event: {evt_type}\ndata: {data_str}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/ingest")
def ingest_endpoint(req: IngestRequest):
    try:
        result = process_document_ingestion(req.text)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/subgraph")
def get_subgraph(limit: int = 150):
    graph = get_graph()
    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT $limit
    """
    try:
        res = graph.query(query, {"limit": limit})
    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}

    nodes_dict = {}
    edges_list = []

    def format_node(n):
        if not n:
            return None
        props = getattr(n, "properties", {})
        labels = getattr(n, "labels", [])
        node_type = labels[0] if labels else "Node"
        node_id = props.get("id", str(getattr(n, "id", "unknown")))
        label = props.get("title") or props.get("name") or props.get("text") or node_id
        
        # Color & visual differentiation
        color = "#64748b" # default slate
        if node_type == "Decision":
            color = "#10b981" # emerald
            if props.get("status") == "superseded":
                color = "#94a3b8"
        elif node_type == "Assumption":
            color = "#10b981" if props.get("valid", True) else "#ef4444" # red if broken
        elif node_type == "Person":
            color = "#3b82f6" # blue
        elif node_type == "Team":
            color = "#8b5cf6" # purple
        elif node_type == "Source":
            color = "#a855f7" # violet
        elif node_type == "Ticket":
            color = "#f59e0b" if props.get("status") == "draft" else "#10b981" # amber or green
        elif node_type == "Event":
            color = "#f43f5e" # rose

        return {
            "data": {
                "id": node_id,
                "label": label[:30] + ("..." if len(label) > 30 else ""),
                "full_label": label,
                "type": node_type,
                "color": color,
                "properties": props
            }
        }

    if res.result_set:
        for row in res.result_set:
            n, r, m = row[0], row[1], row[2]
            if n:
                fn = format_node(n)
                if fn:
                    nodes_dict[fn["data"]["id"]] = fn
            if m:
                fm = format_node(m)
                if fm:
                    nodes_dict[fm["data"]["id"]] = fm
            if n and m and r:
                src_id = getattr(n, "properties", {}).get("id", str(getattr(n, "id", "")))
                tgt_id = getattr(m, "properties", {}).get("id", str(getattr(m, "id", "")))
                rel_type = getattr(r, "relation", "RELATED_TO")
                edges_list.append({
                    "data": {
                        "id": f"{src_id}->{tgt_id}:{rel_type}",
                        "source": src_id,
                        "target": tgt_id,
                        "label": rel_type
                    }
                })

    return {
        "nodes": list(nodes_dict.values()),
        "edges": edges_list
    }

@app.get("/tickets")
def get_tickets():
    graph = get_graph()
    query = """
    MATCH (tk:Ticket)
    OPTIONAL MATCH (tk)-[:REVIEWS_DECISION]->(d:Decision)
    RETURN tk.id, tk.title, tk.priority, tk.reason, tk.status, tk.created_at, d.id, d.title
    ORDER BY tk.created_at DESC
    """
    try:
        res = graph.query(query)
    except Exception:
        return []

    tickets = []
    if res.result_set:
        for r in res.result_set:
            tickets.append({
                "id": r[0],
                "title": r[1],
                "priority": r[2],
                "reason": r[3],
                "status": r[4],
                "created_at": r[5],
                "decision_id": r[6],
                "decision_title": r[7]
            })
    return tickets

@app.post("/tickets/{ticket_id}/confirm")
def confirm_ticket_endpoint(ticket_id: str):
    res = confirm_ticket(ticket_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.post("/graph/seed")
def seed_graph_endpoint():
    try:
        stats = load_seed_data(fresh=True)
        return {"status": "success", "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
