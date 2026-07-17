from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ValidationRequest(BaseModel):
    procedure_id: str = Field(..., description="Procedure ID")
    form_data: Dict[str, Any] = Field(..., description="Form fields content")


class Finding(BaseModel):
    field: Optional[str] = None
    severity: str = Field(..., description="error (red) | warning (yellow) | info (blue)")
    message: str
    fix_suggestion: Optional[str] = None
    rule_id: str
    source_ref: Optional[str] = None


class ValidationResponse(BaseModel):
    procedure_id: str
    is_valid: bool
    findings: List[Finding]
    summary_message: str
