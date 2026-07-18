from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI, OpenAIError

from app.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENAI_TIMEOUT_SECONDS,
)
from app.models.rag import EvidenceHit, GroundedAnswerResponse
from app.services.rag_service import RAGService


OFFICIAL_REVIEW_REQUIRED = "official_review_required"


@dataclass(frozen=True)
class LLMResult:
    text: str
    model: str


class LLMClient(Protocol):
    def complete_grounded_answer(
        self,
        *,
        query: str,
        evidence: list[EvidenceHit],
    ) -> LLMResult:
        ...


class OpenAILLMClient:
    def __init__(
        self,
        *,
        api_key: str = OPENAI_API_KEY,
        model: str = OPENAI_MODEL,
        base_url: str = OPENAI_BASE_URL,
        timeout_seconds: float = OPENAI_TIMEOUT_SECONDS,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def complete_grounded_answer(
        self,
        *,
        query: str,
        evidence: list[EvidenceHit],
    ) -> LLMResult:
        if not self.api_key:
            raise RuntimeError("missing_openai_api_key")

        client_kwargs = {
            "api_key": self.api_key,
            "timeout": self.timeout_seconds,
        }
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        client = OpenAI(**client_kwargs)

        response = client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ban la tro ly thu tuc hanh chinh. Chi tra loi dua tren "
                        "EVIDENCE duoc cung cap. Neu evidence khong du de ket luan, "
                        "noi can chuyen can bo/nguon chinh thuc xem lai. Khong them "
                        "can cu ngoai evidence. Moi y quan trong phai gan ma nguon "
                        "dang [chunk_id]."
                    ),
                },
                {
                    "role": "user",
                    "content": _build_grounded_prompt(query=query, evidence=evidence),
                },
            ],
        )
        content = response.choices[0].message.content or ""
        return LLMResult(text=content.strip(), model=self.model)


def _build_grounded_prompt(*, query: str, evidence: list[EvidenceHit]) -> str:
    evidence_blocks = []
    for index, hit in enumerate(evidence, start=1):
        source_ref = hit.source_refs[0] if hit.source_refs else hit.source_id
        evidence_blocks.append(
            "\n".join(
                [
                    f"EVIDENCE {index}",
                    f"chunk_id: {hit.chunk_id}",
                    f"source_ref: {source_ref}",
                    f"score: {hit.score:.4f}",
                    f"context: {hit.context_prefix}",
                    f"text: {hit.text}",
                ]
            )
        )
    return (
        f"CAU HOI NGUOI DUNG:\n{query}\n\n"
        "EVIDENCE DA DUYET:\n"
        + "\n\n".join(evidence_blocks)
        + "\n\nYEU CAU TRA LOI:\n"
        "- Tra loi ngan gon bang tieng Viet.\n"
        "- Chi su dung thong tin trong EVIDENCE.\n"
        "- Neu canh bao/rang buoc quan trong, neu ro va dan [chunk_id].\n"
        "- Khong khang dinh dieu khong co trong EVIDENCE.\n"
    )


def _citations_from_hits(hits: list[EvidenceHit]) -> list[str]:
    citations: list[str] = []
    for hit in hits:
        if hit.chunk_id not in citations:
            citations.append(hit.chunk_id)
    return citations


class GroundedRAGAnswerService:
    @staticmethod
    def answer(
        *,
        query: str,
        procedure_id: str | None = None,
        top_k: int = 5,
        llm_client: LLMClient | None = None,
    ) -> GroundedAnswerResponse:
        evidence_result = RAGService.search_evidence(
            query=query,
            procedure_id=procedure_id,
            top_k=top_k,
        )
        if evidence_result.status != "ok" or not evidence_result.hits:
            return GroundedAnswerResponse(
                status=OFFICIAL_REVIEW_REQUIRED,
                reason=evidence_result.reason or "no_evidence",
                model=OPENAI_MODEL,
                citations=[],
                evidence=evidence_result.hits,
                store_path=evidence_result.store_path,
                loaded_chunks=evidence_result.loaded_chunks,
            )

        client = llm_client or OpenAILLMClient()
        try:
            llm_result = client.complete_grounded_answer(
                query=query,
                evidence=evidence_result.hits,
            )
        except (OpenAIError, RuntimeError) as exc:
            return GroundedAnswerResponse(
                status=OFFICIAL_REVIEW_REQUIRED,
                reason=str(exc) or "llm_provider_error",
                model=OPENAI_MODEL,
                citations=_citations_from_hits(evidence_result.hits),
                evidence=evidence_result.hits,
                store_path=evidence_result.store_path,
                loaded_chunks=evidence_result.loaded_chunks,
            )

        return GroundedAnswerResponse(
            status="ok",
            reason=None,
            answer=llm_result.text,
            model=llm_result.model,
            citations=_citations_from_hits(evidence_result.hits),
            evidence=evidence_result.hits,
            store_path=evidence_result.store_path,
            loaded_chunks=evidence_result.loaded_chunks,
        )
