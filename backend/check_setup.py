import sys
from backend.config import settings

def run_checks():
    print("=" * 60)
    print(" 'Why Did We?' Environment Verification Check")
    print("=" * 60)
    
    # 1. Config check
    print(f"[1] LLM Provider configured: {settings.LLM_PROVIDER}")
    if settings.LLM_PROVIDER == "groq":
        key_status = "SET (length: " + str(len(settings.GROQ_API_KEY)) + ")" if settings.GROQ_API_KEY else "NOT SET (using mock/demo fallback)"
        print(f"    Groq Model: {settings.GROQ_MODEL} | API Key: {key_status}")
    elif settings.LLM_PROVIDER == "ollama":
        print(f"    Ollama URL: {settings.OLLAMA_BASE_URL} | Model: {settings.OLLAMA_MODEL}")

    # 2. FalkorDB check
    print("\n[2] Testing FalkorDB connection at localhost:6379...")
    try:
        from backend.graph.client import get_db, get_graph
        db = get_db()
        info = db.connection.ping()
        print("    [PASS] FalkorDB is connected and responding to PING!")
    except Exception as e:
        print(f"    [FAIL] FalkorDB connection failed: {e}")
        print("    --> Action needed: Open Docker Desktop and run:")
        print("        docker run -d --name falkordb -p 6379:6379 -p 3000:3000 -v falkordb_data:/var/lib/falkordb/data falkordb/falkordb:latest")

    # 3. Cypher Injection & Mutation Guard check
    print("\n[3] Testing Cypher Read-Only Guard...")
    from backend.tools.cypher import run_cypher_query
    try:
        run_cypher_query("CREATE (n:BadNode {test: true})")
        print("    [FAIL] Write query was not blocked!")
    except ValueError as val_err:
        print(f"    [PASS] Injection blocked successfully: {val_err}")

    # 4. Tool Registry check
    print("\n[4] Testing Tool Registry & Dispatch...")
    from backend.tools.dispatch import dispatch_tool
    res = dispatch_tool("unknown_tool", {})
    if "error" in res:
        print("    [PASS] Unknown tools cleanly rejected.")

    print("\n" + "=" * 60)
    print(" Check completed.")
    print("=" * 60)

if __name__ == "__main__":
    run_checks()
