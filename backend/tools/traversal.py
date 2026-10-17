from backend.graph.client import get_graph

def trace_decision(decision_id: str, depth: int = 2) -> dict:
    graph = get_graph()
    
    query = """
    MATCH (d:Decision {id: $id})
    OPTIONAL MATCH (d)-[:DECIDED_BY]->(p:Person)
    OPTIONAL MATCH (p)-[:MEMBER_OF]->(t:Team)
    OPTIONAL MATCH (d)-[:SOURCED_FROM]->(s:Source)
    OPTIONAL MATCH (d)-[:RELIES_ON]->(a:Assumption)
    OPTIONAL MATCH (d)-[:DEPENDS_ON]->(parent:Decision)
    RETURN d.id AS id, d.title AS title, d.rationale AS rationale, d.status AS status,
           d.domain AS domain, d.decided_at AS decided_at,
           p.name AS decided_by, t.name AS team, s.title AS source,
           collect(DISTINCT {id: a.id, text: a.text, valid: a.valid, category: a.category}) AS assumptions,
           collect(DISTINCT {id: parent.id, title: parent.title}) AS parents
    """
    res = graph.query(query, {"id": decision_id})
    if not res.result_set:
        return {"error": f"Decision {decision_id} not found"}

    row = res.result_set[0]
    return {
        "id": row[0],
        "title": row[1],
        "rationale": row[2],
        "status": row[3],
        "domain": row[4],
        "decided_at": row[5],
        "decided_by": row[6],
        "team": row[7],
        "source": row[8],
        "assumptions": [a for a in row[9] if a.get("id")],
        "parents": [p for p in row[10] if p.get("id")]
    }

def find_dependents(assumption_id: str) -> dict:
    graph = get_graph()
    
    query = """
    MATCH (a:Assumption {id: $id})
    OPTIONAL MATCH (d:Decision)-[:RELIES_ON]->(a)
    OPTIONAL MATCH (downstream:Decision)-[:DEPENDS_ON*1..3]->(d)
    OPTIONAL MATCH (d)-[:DECIDED_BY]->(owner:Person)
    OPTIONAL MATCH (downstream)-[:DECIDED_BY]->(downstream_owner:Person)
    RETURN a.id AS assumption_id, a.text AS text, a.valid AS valid,
           collect(DISTINCT {
               id: d.id,
               title: d.title,
               status: d.status,
               owner: owner.name,
               direct: true
           }) AS direct_decisions,
           collect(DISTINCT {
               id: downstream.id,
               title: downstream.title,
               status: downstream.status,
               owner: downstream_owner.name,
               direct: false
           }) AS downstream_decisions
    """
    res = graph.query(query, {"id": assumption_id})
    if not res.result_set:
        return {"error": f"Assumption {assumption_id} not found"}

    row = res.result_set[0]
    direct = [d for d in row[3] if d.get("id")]
    downstream = [d for d in row[4] if d.get("id")]
    
    all_affected = direct + downstream
    return {
        "assumption_id": row[0],
        "assumption_text": row[1],
        "is_valid": row[2],
        "total_blast_radius": len(all_affected),
        "direct_decisions": direct,
        "downstream_decisions": downstream
    }

def search_decisions(keyword: str, domain: str = None) -> list:
    graph = get_graph()
    
    where_clauses = ["toLower(d.title) CONTAINS toLower($kw) OR toLower(d.rationale) CONTAINS toLower($kw)"]
    params = {"kw": keyword}
    
    if domain:
        where_clauses.append("d.domain = $domain")
        params["domain"] = domain
        
    where_str = " AND ".join(where_clauses)
    query = f"""
    MATCH (d:Decision)
    WHERE {where_str}
    OPTIONAL MATCH (d)-[:DECIDED_BY]->(p:Person)
    RETURN d.id AS id, d.title AS title, d.domain AS domain, d.status AS status, p.name AS owner
    LIMIT 10
    """
    res = graph.query(query, params)
    
    items = []
    if res.result_set:
        for r in res.result_set:
            items.append({
                "id": r[0],
                "title": r[1],
                "domain": r[2],
                "status": r[3],
                "owner": r[4]
            })
    return items
