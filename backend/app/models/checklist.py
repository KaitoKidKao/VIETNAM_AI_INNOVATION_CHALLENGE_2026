from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.models.common import Citation

class ChecklistRequest(BaseModel):
    procedure_id: str = Field(..., description="Procedure ID")
    clarification_answers: Dict[str, Any] = Field(default_factory=dict, description="Answers to clarifying questions")

class ChecklistItem(BaseModel):
    id: str
    title: str
    required: bool
    description: str
    citations: List[Citation]

class Step(BaseModel):
    step_number: int
    title: str
    description: str
    processing_time: str
    fees: str

class ChecklistResponse(BaseModel):
    procedure_id: str
    procedure_name: str
    required_documents: List[ChecklistItem]
    optional_documents: List[ChecklistItem]
    steps: List[Step]
    form_schema: Dict[str, Any] = Field(..., description="JSON Schema for the dynamic form")
    effective_date: str
    sources: List[Citation]
