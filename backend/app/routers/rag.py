from fastapi import APIRouter

from app.models.rag import EvidenceSearchRequest, EvidenceSearchResponse
from app.services.rag_service import RAGService


router = APIRouter(prefix="/v1")


@router.post("/rag/search", response_model=EvidenceSearchResponse)
def search_evidence(request: EvidenceSearchRequest):
    return RAGService.search_evidence(
        query=request.query,
        procedure_id=request.procedure_id,
        top_k=request.top_k,
    )
