"""Optional semantic layer (embedding tieng Viet + FAISS) tren tren EvidenceChunk.

Day la lop BO SUNG cho lexical retrieval trong retrieval.py, KHONG thay the:
neu `sentence-transformers`/`faiss` chua duoc cai, model chua download duoc
(offline/khong network), hoac `Settings.rag_semantic_mode != "hybrid"`, moi
ham public o day tra ve rong/None mot cach an toan (fail-closed) va
`RetrievalService` se tu dong chi dung lexical score nhu truoc (xem D-013).

Chon `bkai-foundation-models/vietnamese-bi-encoder` lam mac dinh vi model
nay duoc fine-tune tren Zalo Legal Text Retrieval — gan voi domain van ban
hanh chinh/phap ly cua du an nay hon cac model embedding tieng Viet tong
quat khac.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Dict, List, Optional, Sequence

from app.config import get_settings
from app.services.rag.schemas import EvidenceChunk

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_encoder(model_name: str):
    """Tra ve SentenceTransformer da load, hoac None neu thieu dependency
    hay khong tai duoc model (vi du khong co network lan dau download)."""

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        logger.warning(
            "sentence-transformers chua duoc cai — semantic layer fail-closed "
            "ve lexical-only. Cai `pip install -r requirements.txt` de bat hybrid."
        )
        return None

    try:
        return SentenceTransformer(model_name)
    except Exception:  # noqa: BLE001 - bat ky loi tai model (network/disk...) deu fail-closed
        logger.warning(
            "Khong tai duoc embedding model '%s' — fail-closed ve lexical-only.", model_name
        )
        return None


def _encode(model_name: str, texts: Sequence[str]):
    encoder = _load_encoder(model_name)
    if encoder is None or not texts:
        return None
    return encoder.encode(list(texts), normalize_embeddings=True, show_progress_bar=False)


@lru_cache(maxsize=8)
def _build_faiss_index(model_name: str, procedure_id: str, chunk_ids: tuple, texts: tuple):
    """Build FAISS index (in-process, khong persist ra disk) cho 1 procedure.

    `chunk_ids`/`texts` duoc truyen vao (thay vi tu load lai) de cache key
    tu dong invalidate dung luc source data thay doi trong test/dev.
    """

    try:
        import faiss
    except ImportError:
        logger.warning("faiss chua duoc cai — semantic layer fail-closed ve lexical-only.")
        return None

    embeddings = _encode(model_name, texts)
    if embeddings is None:
        return None

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # embeddings da normalize -> inner product = cosine
    index.add(embeddings)
    return index


class SemanticIndex:
    """Facade fail-closed cho semantic search; RetrievalService goi qua day
    thay vi dung truc tiep sentence-transformers/faiss de giu retrieval.py
    khong bi crash khi thieu dependency."""

    @staticmethod
    def clear_cache() -> None:
        _load_encoder.cache_clear()
        _build_faiss_index.cache_clear()

    @staticmethod
    def is_available() -> bool:
        settings = get_settings()
        if settings.rag_semantic_mode != "hybrid":
            return False
        return _load_encoder(settings.rag_embedding_model) is not None

    @staticmethod
    def score_chunks(query_text: str, chunks: List[EvidenceChunk]) -> Dict[str, float]:
        """Tra ve {chunk_id: cosine_similarity trong [0, 1]} hoac {} neu
        semantic layer khong san sang / danh sach chunk rong."""

        settings = get_settings()
        if settings.rag_semantic_mode != "hybrid" or not chunks or not query_text.strip():
            return {}

        model_name = settings.rag_embedding_model
        chunk_ids = tuple(c.chunk_id for c in chunks)
        texts = tuple(f"{c.procedure_name} {c.section} {c.text}" for c in chunks)

        index = _build_faiss_index(model_name, chunks[0].procedure_id, chunk_ids, texts)
        if index is None:
            return {}

        query_embedding = _encode(model_name, [query_text])
        if query_embedding is None:
            return {}

        top_k = min(len(chunk_ids), index.ntotal)
        scores, indices = index.search(query_embedding, top_k)
        result: Dict[str, float] = {}
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            # Inner product tren vector da normalize nam trong [-1, 1]; ep ve
            # [0, 1] de blend truc tiep voi lexical cosine score hien tai.
            result[chunk_ids[idx]] = max(0.0, min(1.0, (float(score) + 1.0) / 2.0))
        return result

    @staticmethod
    def score_text_pairs(query_text: str, candidate_texts: Sequence[str]) -> Optional[List[float]]:
        """Tra ve list similarity (cung thu tu candidate_texts) hoac None
        neu semantic layer khong san sang — dung cho recommend_procedure
        (so sanh 1 query voi nhieu procedure-level representative text)."""

        settings = get_settings()
        if settings.rag_semantic_mode != "hybrid" or not candidate_texts:
            return None

        model_name = settings.rag_embedding_model
        embeddings = _encode(model_name, [query_text, *candidate_texts])
        if embeddings is None:
            return None

        query_vec, candidate_vecs = embeddings[0], embeddings[1:]
        return [max(0.0, min(1.0, (float(query_vec @ vec) + 1.0) / 2.0)) for vec in candidate_vecs]
