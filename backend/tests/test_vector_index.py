"""Test cho semantic layer optional (embedding tieng Viet + FAISS, D-013).

Moi truong test KHONG cai sentence-transformers/faiss (xem requirements.txt:
day la dependency optional) — nen phan lon test o day xac nhan hanh vi
fail-closed (tu dong ve lexical-only) khi thieu dependency, va dung
monkeypatch de gia lap semantic layer "co san" ma khong can download model
thuc, dam bao logic blend o retrieval.py dung ma khong phu thuoc network.
"""

import pytest

from app.config import get_settings
from app.services.rag.retrieval import RetrievalService, _blend
from app.services.rag.schemas import EvidenceChunk, RetrievalQuery
from app.services.rag.vector_index import SemanticIndex


def _has_source_data() -> bool:
    source_path = get_settings().rag_source_path
    return source_path.exists() and any(source_path.glob("*.txt"))


requires_source_data = pytest.mark.skipif(
    not _has_source_data(), reason="data/Data_DVC khong ton tai trong moi truong nay"
)


def _make_chunk(chunk_id: str, procedure_id: str = "test-procedure") -> EvidenceChunk:
    return EvidenceChunk(
        chunk_id=chunk_id,
        procedure_id=procedure_id,
        procedure_name="Thủ tục kiểm thử",
        section="Mô tả",
        text="Nội dung kiểm thử",
        source_title="Nguồn kiểm thử",
        source_ref="TEST-REF",
        last_verified_at="2026-01-01",
    )


def test_semantic_mode_is_lexical_by_default():
    assert get_settings().rag_semantic_mode == "lexical"


def test_semantic_index_unavailable_when_mode_is_lexical():
    assert SemanticIndex.is_available() is False
    assert SemanticIndex.score_chunks("bất kỳ", [_make_chunk("c1")]) == {}
    assert SemanticIndex.score_text_pairs("bất kỳ", ["a", "b"]) is None


def test_semantic_index_fails_closed_when_dependency_missing(monkeypatch):
    # sentence-transformers khong duoc cai trong moi truong test (dependency
    # optional) -> is_available() phai tra ve False ngay ca khi bat hybrid,
    # khong duoc raise exception len RetrievalService.
    monkeypatch.setattr(
        "app.services.rag.vector_index.get_settings",
        lambda: get_settings().model_copy(update={"rag_semantic_mode": "hybrid"}),
    )
    SemanticIndex.clear_cache()
    try:
        assert SemanticIndex.is_available() is False
        assert SemanticIndex.score_chunks("bất kỳ", [_make_chunk("c1")]) == {}
    finally:
        SemanticIndex.clear_cache()


def test_blend_weight_matches_settings():
    settings = get_settings()
    weight = settings.rag_semantic_weight
    assert _blend(1.0, 0.0) == pytest.approx(1 - weight)
    assert _blend(0.0, 1.0) == pytest.approx(weight)
    assert _blend(1.0, 1.0) == pytest.approx(1.0)


@requires_source_data
def test_retrieve_blends_semantic_score_when_available(monkeypatch):
    """Gia lap semantic layer 'co san' bang monkeypatch (khong download model
    thuc) de xac nhan retrieval.py thuc su blend score, khong chi bo qua no."""

    monkeypatch.setattr(
        "app.services.rag.retrieval.get_settings",
        lambda: get_settings().model_copy(
            update={"rag_semantic_mode": "hybrid", "rag_semantic_weight": 1.0}
        ),
    )
    monkeypatch.setattr(
        "app.services.rag.retrieval.SemanticIndex.is_available", staticmethod(lambda: True)
    )

    def _fake_score_chunks(query_text, chunks):
        # Ep het score semantic ve 0.9 bat ke lexical de kiem tra blend
        # thuc su duoc ap dung (voi weight=1.0, ket qua phai == 0.9 dung).
        return {chunk.chunk_id: 0.9 for chunk in chunks}

    monkeypatch.setattr(
        "app.services.rag.retrieval.SemanticIndex.score_chunks", staticmethod(_fake_score_chunks)
    )
    RetrievalService.clear_cache()
    try:
        evidence = RetrievalService.retrieve(
            RetrievalQuery(text="giấy chứng sinh", procedure_id="dang-ky-khai-sinh")
        )
        assert evidence.chunks
        assert all(chunk.score == pytest.approx(0.9) for chunk in evidence.chunks)
    finally:
        RetrievalService.clear_cache()


@requires_source_data
def test_retrieve_ignores_semantic_when_unavailable_even_in_hybrid_mode(monkeypatch):
    """Trong moi truong test thuc (khong monkeypatch is_available), bat
    hybrid van phai fail-closed ve dung lexical score — khong duoc crash."""

    monkeypatch.setattr(
        "app.services.rag.retrieval.get_settings",
        lambda: get_settings().model_copy(update={"rag_semantic_mode": "hybrid"}),
    )
    RetrievalService.clear_cache()
    try:
        evidence = RetrievalService.retrieve(
            RetrievalQuery(text="giấy chứng sinh", procedure_id="dang-ky-khai-sinh")
        )
        assert evidence.is_grounded is True
        assert evidence.chunks
    finally:
        RetrievalService.clear_cache()
