import json
from pathlib import Path
from backend.graph.client import get_graph, reset_graph
from backend.graph.schema import initialize_schema
from data.seed.generate import generate_seed_dataset

def load_seed_data(fresh: bool = False):
    if fresh:
        reset_graph()
    initialize_schema()
    graph = get_graph()
    
    seed_file = Path(__file__).resolve().parent.parent.parent / "data" / "seed" / "seed_data.json"
    if not seed_file.exists():
        generate_seed_dataset()
        
    with open(seed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Teams
    graph.query("""
        UNWIND $rows AS row
        MERGE (t:Team {id: row.id})
        SET t.name = row.name
    """, {"rows": data["teams"]})

    # 2. People + MEMBER_OF
    graph.query("""
        UNWIND $rows AS row
        MERGE (p:Person {id: row.id})
        SET p.name = row.name, p.role = row.role, p.email = row.email
        WITH p, row
        MATCH (t:Team {id: row.team_id})
        MERGE (p)-[:MEMBER_OF]->(t)
    """, {"rows": data["people"]})

    # 3. Sources
    graph.query("""
        UNWIND $rows AS row
        MERGE (s:Source {id: row.id})
        SET s.title = row.title, s.type = row.type, s.url = row.url, s.created_at = row.created_at
    """, {"rows": data["sources"]})

    # 4. Assumptions
    graph.query("""
        UNWIND $rows AS row
        MERGE (a:Assumption {id: row.id})
        SET a.text = row.text, a.valid = row.valid, a.category = row.category, a.validated_at = row.validated_at
    """, {"rows": data["assumptions"]})

    # 5. Decisions + DECIDED_BY + SOURCED_FROM
    graph.query("""
        UNWIND $rows AS row
        MERGE (d:Decision {id: row.id})
        SET d.title = row.title, d.rationale = row.rationale, d.status = row.status,
            d.decided_at = row.decided_at, d.domain = row.domain, d.confidence = row.confidence
        WITH d, row
        MATCH (p:Person {id: row.person_id})
        MERGE (d)-[:DECIDED_BY]->(p)
        WITH d, row
        MATCH (s:Source {id: row.source_id})
        MERGE (d)-[:SOURCED_FROM]->(s)
    """, {"rows": data["decisions"]})

    # 6. RELIES_ON relationships
    relies_tuples = []
    for d in data["decisions"]:
        for a_id in d.get("relies_on", []):
            relies_tuples.append({"decision_id": d["id"], "assumption_id": a_id})

    graph.query("""
        UNWIND $rows AS row
        MATCH (d:Decision {id: row.decision_id}), (a:Assumption {id: row.assumption_id})
        MERGE (d)-[:RELIES_ON]->(a)
    """, {"rows": relies_tuples})

    # 7. DEPENDS_ON relationships
    depends_tuples = []
    for d in data["decisions"]:
        for dep_id in d.get("depends_on", []):
            depends_tuples.append({"source_id": d["id"], "target_id": dep_id})

    graph.query("""
        UNWIND $rows AS row
        MATCH (d1:Decision {id: row.source_id}), (d2:Decision {id: row.target_id})
        MERGE (d1)-[:DEPENDS_ON]->(d2)
    """, {"rows": depends_tuples})

    return {
        "status": "success",
        "teams": len(data["teams"]),
        "people": len(data["people"]),
        "sources": len(data["sources"]),
        "assumptions": len(data["assumptions"]),
        "decisions": len(data["decisions"])
    }

if __name__ == "__main__":
    result = load_seed_data(fresh=True)
    print("Seed load completed:", result)
