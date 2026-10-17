from backend.graph.client import get_graph

def get_critical_decisions(limit: int = 5) -> list:
    graph = get_graph()
    query = """
    MATCH (d:Decision)
    OPTIONAL MATCH (downstream:Decision)-[:DEPENDS_ON*1..4]->(d)
    OPTIONAL MATCH (d)-[:RELIES_ON]->(a:Assumption)
    WITH d, count(DISTINCT downstream) AS dependent_count, count(DISTINCT a) AS assumption_count
    RETURN d.id AS id, d.title AS title, d.domain AS domain,
           dependent_count, assumption_count,
           (dependent_count * 2 + assumption_count) AS centrality_score
    ORDER BY centrality_score DESC
    LIMIT $limit
    """
    res = graph.query(query, {"limit": limit})
    
    output = []
    if res.result_set:
        for r in res.result_set:
            output.append({
                "id": r[0],
                "title": r[1],
                "domain": r[2],
                "dependent_count": r[3],
                "assumption_count": r[4],
                "impact_score": r[5]
            })
    return output

def get_fragile_assumptions(limit: int = 5) -> list:
    graph = get_graph()
    query = """
    MATCH (a:Assumption)
    OPTIONAL MATCH (d:Decision)-[:RELIES_ON]->(a)
    OPTIONAL MATCH (downstream:Decision)-[:DEPENDS_ON*1..3]->(d)
    WITH a, count(DISTINCT d) AS direct_impact, count(DISTINCT downstream) AS cascade_impact
    RETURN a.id AS id, a.text AS text, a.valid AS valid,
           direct_impact, cascade_impact,
           (direct_impact + cascade_impact) AS blast_radius
    ORDER BY blast_radius DESC
    LIMIT $limit
    """
    res = graph.query(query, {"limit": limit})
    
    output = []
    if res.result_set:
        for r in res.result_set:
            output.append({
                "id": r[0],
                "text": r[1],
                "valid": r[2],
                "direct_impact": r[3],
                "cascade_impact": r[4],
                "blast_radius": r[5]
            })
    return output
