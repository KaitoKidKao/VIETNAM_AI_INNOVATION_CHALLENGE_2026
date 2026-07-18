"""Hybrid retrieval (keyword filter + lexical similarity) tren approved store.

Mac dinh (`rag_semantic_mode="lexical"`) khong dung numpy/scikit-learn/vector
DB (Neon/pgvector van la `Proposed`/`TBD` theo D-005/D-006) de tranh
dependency native nang, dung pure-Python term-frequency cosine similarity.
Khi bat `rag_semantic_mode="hybrid"` (D-013), score lexical duoc blend them
voi semantic similarity tu `vector_index.SemanticIndex` (embedding tieng
Viet + FAISS, chay in-process, khong ket noi service ngoai) — neu semantic
layer khong san sang (thieu dependency/model) thi tu dong fail-closed ve
dung lexical score nhu truoc, hanh vi khong doi. Chi truy hoi tren cac
chunk da duoc allowlist trong source_store.PROCEDURE_ALLOWLIST — khong co
PII, chat memory hay case memory nao trong index nay.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from functools import lru_cache
from typing import Dict, List

from app.config import get_settings
from app.services.rag.chunking import build_chunks
from app.services.rag.schemas import (
    EvidenceChunk,
    ProcedureCandidate,
    RetrievalEvidence,
    RetrievalQuery,
)
from app.services.rag.source_store import (
    PROCEDURE_DISPLAY_NAME,
    load_approved_records,
    strip_diacritics,
)
from app.services.rag.vector_index import SemanticIndex

_TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
_STOPWORDS = {
    "toi",
    "ban",
    "la",
    "va",
    "cua",
    "cho",
    "the",
    "nay",
    "o",
    "co",
    "khong",
    "muon",
    "can",
    "de",
    "voi",
    "tai",
    "mot",
    "nhung",
    "duoc",
    "phai",
    "khi",
    "tu",
    "ve",
    "hay",
    "nhu",
    "da",
    "se",
    "cac",
    "trong",
    "theo",
    "nguoi",
}


def _tokenize(text: str) -> List[str]:
    normalized = strip_diacritics(text).lower()
    tokens = _TOKEN_RE.findall(normalized)
    return [t for t in tokens if len(t) > 1 and t not in _STOPWORDS]


def _term_vector(tokens: List[str]) -> Counter:
    return Counter(tokens)


def _cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
    if not vec_a or not vec_b:
        return 0.0
    common = set(vec_a) & set(vec_b)
    dot = sum(vec_a[t] * vec_b[t] for t in common)
    if dot == 0:
        return 0.0
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class _ScoredChunk:
    __slots__ = ("chunk", "vector")

    def __init__(self, chunk: EvidenceChunk):
        self.chunk = chunk
        self.vector = _term_vector(
            _tokenize(f"{chunk.procedure_name} {chunk.section} {chunk.text}")
        )


def _blend(lexical_score: float, semantic_score: float) -> float:
    weight = get_settings().rag_semantic_weight
    return (1 - weight) * lexical_score + weight * semantic_score


@lru_cache(maxsize=1)
def _build_index() -> Dict[str, List[_ScoredChunk]]:
    records_by_procedure = load_approved_records()
    index: Dict[str, List[_ScoredChunk]] = {}
    for procedure_id, records in records_by_procedure.items():
        chunks = build_chunks(procedure_id, records)
        index[procedure_id] = [_ScoredChunk(c) for c in chunks]
    return index


class RetrievalService:
    """Facade cho tang RAG duoc Orchestrator/service khac goi.

    Static methods de cac router/service dung truc tiep khong can khoi tao
    instance rieng (index duoc cache o module-level, chi build mot lan).
    """

    @staticmethod
    def clear_cache() -> None:
        """Chi dung trong test: xoa cache khi doi RAG_SOURCE_DIR."""
        _build_index.cache_clear()
        load_approved_records.cache_clear()
        SemanticIndex.clear_cache()

    @staticmethod
    def known_procedure_ids() -> List[str]:
        return list(PROCEDURE_DISPLAY_NAME.keys())

    @staticmethod
    def recommend_procedure(query_text: str, top_k: int = 3) -> List[ProcedureCandidate]:
        query_vector = _term_vector(_tokenize(query_text))
        index = _build_index()
        semantic_available = SemanticIndex.is_available()
        best_per_procedure: Dict[str, float] = {}

        for procedure_id, scored_chunks in index.items():
            semantic_scores = (
                SemanticIndex.score_chunks(query_text, [s.chunk for s in scored_chunks])
                if semantic_available
                else {}
            )
            best_score = 0.0
            for scored in scored_chunks:
                lexical_score = _cosine_similarity(query_vector, scored.vector)
                score = (
                    _blend(lexical_score, semantic_scores[scored.chunk.chunk_id])
                    if scored.chunk.chunk_id in semantic_scores
                    else lexical_score
                )
                if score > best_score:
                    best_score = score
            best_per_procedure[procedure_id] = best_score

        ranked = sorted(best_per_procedure.items(), key=lambda kv: kv[1], reverse=True)
        return [
            ProcedureCandidate(
                procedure_id=pid,
                procedure_name=PROCEDURE_DISPLAY_NAME.get(pid, pid),
                score=round(score, 4),
            )
            for pid, score in ranked[:top_k]
        ]

    @staticmethod
    def retrieve(query: RetrievalQuery) -> RetrievalEvidence:
        index = _build_index()

        if query.procedure_id and query.procedure_id not in index:
            return RetrievalEvidence(
                procedure_id=query.procedure_id,
                chunks=[],
                citations=[],
                confidence=0.0,
                is_grounded=False,
                conflict=False,
            )

        candidate_procedures = [query.procedure_id] if query.procedure_id else list(index.keys())
        query_vector = _term_vector(_tokenize(query.text)) if query.text else Counter()
        semantic_available = bool(query.text) and SemanticIndex.is_available()

        scored: List[tuple] = []
        for procedure_id in candidate_procedures:
            procedure_chunks = index.get(procedure_id, [])
            semantic_scores = (
                SemanticIndex.score_chunks(query.text, [s.chunk for s in procedure_chunks])
                if semantic_available
                else {}
            )
            for scored_chunk in procedure_chunks:
                lexical_score = (
                    _cosine_similarity(query_vector, scored_chunk.vector) if query_vector else 1.0
                )
                score = (
                    _blend(lexical_score, semantic_scores[scored_chunk.chunk.chunk_id])
                    if scored_chunk.chunk.chunk_id in semantic_scores
                    else lexical_score
                )
                scored.append((score, scored_chunk.chunk))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        top_k = query.top_k or get_settings().rag_top_k
        top = scored[:top_k]

        resolved_procedure_id = query.procedure_id
        if resolved_procedure_id is None and top:
            resolved_procedure_id = top[0][1].procedure_id

        chunks: List[EvidenceChunk] = []
        seen_citations: Dict[str, Dict[str, str]] = {}
        for score, chunk in top:
            enriched = chunk.model_copy(update={"score": round(score, 4)})
            chunks.append(enriched)
            seen_citations[chunk.source_ref] = {
                "title": chunk.source_title,
                "url": chunk.source_url or "",
                "ref_code": chunk.source_ref,
            }

        confidence = top[0][0] if top else 0.0
        is_grounded = bool(chunks) and confidence >= get_settings().rag_min_confidence

        return RetrievalEvidence(
            procedure_id=resolved_procedure_id,
            procedure_name=(
                PROCEDURE_DISPLAY_NAME.get(resolved_procedure_id) if resolved_procedure_id else None
            ),
            chunks=chunks,
            citations=list(seen_citations.values()),
            confidence=round(confidence, 4),
            is_grounded=is_grounded,
            conflict=False,
            last_verified_at=chunks[0].last_verified_at if chunks else None,
        )

    @staticmethod
    def get_citations_for_procedure(procedure_id: str) -> List[Dict[str, str]]:
        evidence = RetrievalService.retrieve(
            RetrievalQuery(text="", procedure_id=procedure_id, top_k=50)
        )
        return evidence.citations
