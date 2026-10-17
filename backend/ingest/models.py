from typing import List, Optional
from pydantic import BaseModel, Field

class ExtractedAssumption(BaseModel):
    id: Optional[str] = None
    text: str
    valid: bool = True
    category: str = "General"

class ExtractedDecision(BaseModel):
    title: str
    rationale: str
    domain: str = "Architecture"
    author_name: str
    assumptions: List[str] = Field(default_factory=list)

class ExtractedInvalidation(BaseModel):
    assumption_id: str
    reason: str
    new_valid_state: bool = False

class DocumentExtractionResult(BaseModel):
    summary: str
    new_decisions: List[ExtractedDecision] = Field(default_factory=list)
    invalidated_assumptions: List[ExtractedInvalidation] = Field(default_factory=list)
    recommended_tickets: List[str] = Field(default_factory=list)
