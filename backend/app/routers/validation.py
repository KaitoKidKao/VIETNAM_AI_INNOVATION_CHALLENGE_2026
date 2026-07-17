from fastapi import APIRouter
from app.models.validation import ValidationRequest, ValidationResponse
from app.services.validation_service import ValidationService

router = APIRouter(prefix="/v1")


@router.post("/applications/validate", response_model=ValidationResponse)
def validate_application(request: ValidationRequest):
    return ValidationService.validate(request.procedure_id, request.form_data)
