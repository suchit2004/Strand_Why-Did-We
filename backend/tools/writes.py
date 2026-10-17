import uuid
from datetime import datetime
from backend.graph.client import get_graph

def update_assumption(assumption_id: str, valid: bool, reason: str = "") -> dict:
    graph = get_graph()
    now_iso = datetime.utcnow().isoformat() + "Z"
    event_id = f"EVT-{uuid.uuid4().hex[:8].upper()}"
    
    query = """
    MATCH (a:Assumption {id: $aid})
    SET a.valid = $valid, a.validated_at = $now
    CREATE (e:Event {id: $eid, description: $reason, timestamp: $now})
    CREATE (e)-[:INVALIDATES]->(a)
    RETURN a.id AS id, a.valid AS valid, e.id AS event_id
    """
    res = graph.query(query, {
        "aid": assumption_id,
        "valid": valid,
        "now": now_iso,
        "eid": event_id,
        "reason": reason or f"Assumption validity changed to {valid}"
    })
    
    if not res.result_set:
        return {"error": f"Assumption {assumption_id} not found"}
        
    return {
        "status": "success",
        "assumption_id": assumption_id,
        "valid": valid,
        "event_id": event_id
    }

def draft_ticket(decision_id: str, title: str, priority: str = "P1", reason: str = "") -> dict:
    graph = get_graph()
    ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    query = """
    MATCH (d:Decision {id: $did})
    CREATE (tk:Ticket {
        id: $tid,
        title: $title,
        priority: $priority,
        reason: $reason,
        status: 'draft',
        created_at: $now
    })
    CREATE (tk)-[:REVIEWS_DECISION]->(d)
    RETURN tk.id AS ticket_id, tk.status AS status, d.id AS decision_id
    """
    res = graph.query(query, {
        "did": decision_id,
        "tid": ticket_id,
        "title": title,
        "priority": priority,
        "reason": reason,
        "now": now_iso
    })
    
    if not res.result_set:
        return {"error": f"Decision {decision_id} not found"}
        
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "decision_id": decision_id,
        "title": title,
        "ticket_status": "draft"
    }

def confirm_ticket(ticket_id: str) -> dict:
    graph = get_graph()
    query = """
    MATCH (tk:Ticket {id: $tid})
    SET tk.status = 'confirmed'
    RETURN tk.id AS ticket_id, tk.status AS status
    """
    res = graph.query(query, {"tid": ticket_id})
    if not res.result_set:
        return {"error": f"Ticket {ticket_id} not found"}
        
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "ticket_status": "confirmed"
    }

def record_decision(title: str, rationale: str, person_id: str, domain: str, assumptions: list = None) -> dict:
    graph = get_graph()
    decision_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    query = """
    MATCH (p:Person {id: $pid})
    CREATE (d:Decision {
        id: $did,
        title: $title,
        rationale: $rationale,
        domain: $domain,
        status: 'active',
        confidence: 0.95,
        decided_at: $now
    })
    CREATE (d)-[:DECIDED_BY]->(p)
    RETURN d.id AS id
    """
    res = graph.query(query, {
        "pid": person_id,
        "did": decision_id,
        "title": title,
        "rationale": rationale,
        "domain": domain,
        "now": now_iso
    })
    
    if not res.result_set:
        return {"error": f"Person {person_id} not found"}
        
    # Link or create assumptions
    if assumptions:
        for idx, asm_text in enumerate(assumptions):
            asm_id = f"ASM-{uuid.uuid4().hex[:8].upper()}"
            graph.query("""
            MATCH (d:Decision {id: $did})
            CREATE (a:Assumption {id: $aid, text: $text, valid: true, category: 'General', validated_at: $now})
            CREATE (d)-[:RELIES_ON]->(a)
            """, {
                "did": decision_id,
                "aid": asm_id,
                "text": asm_text,
                "now": now_iso
            })
            
    return {
        "status": "success",
        "decision_id": decision_id,
        "title": title
    }
