import re
from backend.graph.client import get_graph

WRITE_KEYWORDS_PATTERN = re.compile(
    r"\b(CREATE|DELETE|SET|REMOVE|DROP|MERGE)\b",
    re.IGNORECASE
)

def run_cypher_query(query: str, params: dict = None) -> list:
    if WRITE_KEYWORDS_PATTERN.search(query):
        raise ValueError("Write operations (CREATE, DELETE, SET, MERGE, DROP, REMOVE) are strictly prohibited in run_cypher_query. Use dedicated write tools.")

    graph = get_graph()
    result = graph.query(query, params or {})
    
    output = []
    if result and result.result_set:
        header = [col[0] if isinstance(col, (list, tuple)) else str(col) for col in result.header] if hasattr(result, "header") and result.header else []
        for row in result.result_set:
            if header and len(header) == len(row):
                output.append(dict(zip(header, row)))
            else:
                output.append(row)
    return output
