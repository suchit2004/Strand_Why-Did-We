from falkordb import FalkorDB
from backend.config import settings

_db = None
_graph = None

def get_db():
    global _db
    if _db is None:
        _db = FalkorDB(host=settings.FALKORDB_HOST, port=settings.FALKORDB_PORT)
    return _db

def get_graph():
    global _graph
    if _graph is None:
        db = get_db()
        _graph = db.select_graph(settings.FALKORDB_GRAPH)
    return _graph

def reset_graph():
    global _graph
    db = get_db()
    try:
        db.select_graph(settings.FALKORDB_GRAPH).delete()
    except Exception:
        pass
    _graph = db.select_graph(settings.FALKORDB_GRAPH)
    return _graph
