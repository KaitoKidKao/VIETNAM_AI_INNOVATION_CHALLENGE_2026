from fastapi import APIRouter, Depends

from app.dependencies import get_copilot_service
from app.models.validation import (
    PrefillRequest,
    PrefillResponse,
    ValidationRequest,
    ValidationResponse,
)
from app.services.copilot_service import CopilotService

router = APIRouter(prefix="/v1/applications", tags=["validation"])


@router.post("/validate", response_model=ValidationResponse)
async def validate_application(
    request: ValidationRequest,
    service: CopilotService = Depends(get_copilot_service),
) -> ValidationResponse:
    return await service.validate(request)


@router.post("/prefill", response_model=PrefillResponse)
async def prefill_application(
    request: PrefillRequest,
    service: CopilotService = Depends(get_copilot_service),
) -> PrefillResponse:
    return await service.prefill(request)
