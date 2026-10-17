from backend.ingest.extract import extract_entities_from_text
from backend.tools.writes import update_assumption, draft_ticket, record_decision
from backend.tools.traversal import find_dependents

def process_document_ingestion(document_text: str) -> dict:
    extraction = extract_entities_from_text(document_text)
    
    actions_taken = {
        "summary": extraction.summary,
        "invalidated": [],
        "drafted_tickets": [],
        "new_decisions": []
    }

    # 1. Process assumption invalidations
    for item in extraction.invalidated_assumptions:
        res = update_assumption(
            assumption_id=item.assumption_id,
            valid=item.new_valid_state,
            reason=item.reason
        )
        actions_taken["invalidated"].append(res)
        
        # Calculate blast radius and draft tickets for affected systems
        deps = find_dependents(item.assumption_id)
        if "error" not in deps:
            for d in deps.get("direct_decisions", []) + deps.get("downstream_decisions", []):
                t_res = draft_ticket(
                    decision_id=d["id"],
                    title=f"Review {d['id']}: Assumption {item.assumption_id} invalidated",
                    priority="P0" if d.get("direct") else "P1",
                    reason=f"Impacted by broken assumption: {item.reason}"
                )
                actions_taken["drafted_tickets"].append(t_res)

    # 2. Process new decisions
    for d in extraction.new_decisions:
        d_res = record_decision(
            title=d.title,
            rationale=d.rationale,
            person_id="PER-ALEX",
            domain=d.domain,
            assumptions=d.assumptions
        )
        actions_taken["new_decisions"].append(d_res)

    return actions_taken
