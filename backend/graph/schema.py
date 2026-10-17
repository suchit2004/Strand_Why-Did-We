from backend.graph.client import get_graph

def initialize_schema():
    graph = get_graph()
    
    indices = [
        "CREATE INDEX FOR (d:Decision) ON (d.id)",
        "CREATE INDEX FOR (d:Decision) ON (d.status)",
        "CREATE INDEX FOR (a:Assumption) ON (a.id)",
        "CREATE INDEX FOR (a:Assumption) ON (a.valid)",
        "CREATE INDEX FOR (p:Person) ON (p.id)",
        "CREATE INDEX FOR (t:Team) ON (t.id)",
        "CREATE INDEX FOR (s:Source) ON (s.id)",
        "CREATE INDEX FOR (tk:Ticket) ON (tk.id)",
        "CREATE INDEX FOR (tk:Ticket) ON (tk.status)",
        "CREATE INDEX FOR (e:Event) ON (e.id)",
    ]
    
    for idx_query in indices:
        try:
            graph.query(idx_query)
        except Exception:
            pass

    return True
