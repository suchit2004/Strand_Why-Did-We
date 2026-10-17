TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "trace_decision",
            "description": "Trace the full lineage of a technical or architectural decision: rationale, author, team, source RFC/contract, and core assumptions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_id": {
                        "type": "string",
                        "description": "Unique ID of the decision (e.g. DEC-POSTGRES-CACHE)"
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Depth of parent traversal (default 2)",
                        "default": 2
                    }
                },
                "required": ["decision_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_dependents",
            "description": "Calculate the blast radius of an assumption or decision. Returns all direct and cascading downstream decisions that will break or need review.",
            "parameters": {
                "type": "object",
                "properties": {
                    "assumption_id": {
                        "type": "string",
                        "description": "The assumption ID to check blast radius for (e.g. ASM-LATENCY-Q1 or ASM-STRIPE-FEE)"
                    }
                },
                "required": ["assumption_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_decisions",
            "description": "Search decisions in the graph by keyword in title or rationale, optionally filtered by domain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keywords to search for (e.g. 'Postgres', 'Stripe', 'caching', 'auth')"
                    },
                    "domain": {
                        "type": "string",
                        "description": "Optional engineering domain filter (e.g. Database, Billing, Architecture, Security)"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_cypher_query",
            "description": "Execute a custom read-only Cypher graph query on FalkorDB for complex queries. Mutations are blocked.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Cypher MATCH query returning graph entities or aggregates"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_critical_decisions",
            "description": "Identify architectural bottlenecks and high-impact decisions based on graph centrality score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum decisions to return (default 5)",
                        "default": 5
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_assumption",
            "description": "Update the validity of an assumption (e.g. set valid to false) and log an invalidation event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "assumption_id": {
                        "type": "string",
                        "description": "ID of the assumption (e.g. ASM-LATENCY-Q1)"
                    },
                    "valid": {
                        "type": "boolean",
                        "description": "New validity state (false if invalidated/broken)"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Explanation or benchmark showing why assumption changed"
                    }
                },
                "required": ["assumption_id", "valid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_ticket",
            "description": "Draft an actionable architectural review ticket for a compromised decision.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_id": {
                        "type": "string",
                        "description": "ID of the decision needing review"
                    },
                    "title": {
                        "type": "string",
                        "description": "Clear title for the review ticket"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority: P0 (Critical), P1 (High), P2 (Medium)",
                        "default": "P1"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why the review is required"
                    }
                },
                "required": ["decision_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_ticket",
            "description": "Confirm a drafted ticket, updating its status to confirmed in the graph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Unique ID of the ticket to confirm"
                    }
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_decision",
            "description": "Record a new architectural or engineering decision into the graph with assumptions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "rationale": {"type": "string"},
                    "person_id": {"type": "string"},
                    "domain": {"type": "string"},
                    "assumptions": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["title", "rationale", "person_id", "domain"]
            }
        }
    }
]
