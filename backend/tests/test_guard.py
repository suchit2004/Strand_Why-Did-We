import pytest
from backend.tools.cypher import run_cypher_query

def test_cypher_guard_blocks_create():
    with pytest.raises(ValueError, match="strictly prohibited"):
        run_cypher_query("CREATE (n:Test {name: 'test'})")

def test_cypher_guard_blocks_delete():
    with pytest.raises(ValueError, match="strictly prohibited"):
        run_cypher_query("MATCH (n:Test) DELETE n")

def test_cypher_guard_blocks_set():
    with pytest.raises(ValueError, match="strictly prohibited"):
        run_cypher_query("MATCH (n:Test) SET n.name = 'changed'")

def test_cypher_guard_blocks_merge():
    with pytest.raises(ValueError, match="strictly prohibited"):
        run_cypher_query("MERGE (n:Test {id: 1})")
