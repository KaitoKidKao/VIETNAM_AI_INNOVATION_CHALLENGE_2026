"""Deterministic ingestion primitives for approved RAG sources."""

from .chunking import (
    ChunkBuildReport,
    ChunkSourceMetadata,
    EvidenceChunk,
    build_evidence_chunks,
    build_report,
)
from .normalization import NormalizedDocument, normalize_document
from .parsing import ParsedSection, parse_sections

__all__ = [
    "ChunkBuildReport",
    "ChunkSourceMetadata",
    "EvidenceChunk",
    "NormalizedDocument",
    "ParsedSection",
    "build_evidence_chunks",
    "build_report",
    "normalize_document",
    "parse_sections",
]
