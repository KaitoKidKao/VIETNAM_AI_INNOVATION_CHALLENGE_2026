from fastapi import APIRouter, HTTPException, Path
from app.models.checklist import ChecklistResponse, ChecklistRequest
from app.services.procedure_service import ProcedureService

router = APIRouter(prefix="/v1")


@router.get("/procedures")
def get_procedures():
    return ProcedureService.list_procedures()


@router.post("/procedures/{id}/checklist", response_model=ChecklistResponse)
def get_checklist(
    id: str = Path(..., description="Procedure ID"), request: ChecklistRequest = None
):
    if not ProcedureService.get_procedure(id):
        raise HTTPException(status_code=404, detail="Procedure pack not found")
    return ProcedureService.get_checklist(id)
