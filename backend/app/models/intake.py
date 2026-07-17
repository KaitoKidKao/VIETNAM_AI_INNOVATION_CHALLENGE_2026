from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.models.common import Message

class IntakeRequest(BaseModel):
    session_id: str = Field(..., description="Unique browser session ID")
    messages: List[Message] = Field(..., description="Chat message history")
    current_procedure_id: Optional[str] = Field(None, description="Currently detected procedure ID")

class IntakeResponse(BaseModel):
    detected_procedure_id: Optional[str] = Field(None, description="Detected procedure ID")
    message: str = Field(..., description="Reply from the copilot (questions or guidance)")
    trust_state: str = Field(..., description="verified_guidance | need_more_information | official_review_required")
    required_clarifications: List[str] = Field(default_factory=list, description="Pending clarifying questions")
    sources: List[Dict[str, str]] = Field(default_factory=list, description="Citations and source references")
