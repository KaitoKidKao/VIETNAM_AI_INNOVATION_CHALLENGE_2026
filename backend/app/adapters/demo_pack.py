"""Demo-approved procedure packs for the local MVP flow.

Cac pack JSON trong app/data/demo_packs duoc author offline tu nguon cong khai
data/Data_DVC (ma 1.001193 / 1.004222 / 1.001612) va mang
review_status=demo_approved voi demo_pack=true. Day la du lieu ky thuat cho
demo, KHONG phai K1/human legal approval. TrustPolicy gan demo_mode vao moi
response de UI luon hien thi watermark demo.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.adapters.dev_fixture import normalize_text
from app.models.common import SessionContext
from app.models.procedure import (
    ProcedureCandidate,
    ProcedurePack,
    ProcedureSummary,
    ReviewStatus,
)

DEMO_PACK_DIR = Path(__file__).resolve().parents[1] / "data" / "demo_packs"


@lru_cache(maxsize=1)
def load_demo_packs() -> dict[str, ProcedurePack]:
    packs: dict[str, ProcedurePack] = {}
    for path in sorted(DEMO_PACK_DIR.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        pack = ProcedurePack.model_validate(raw)
        if not pack.demo_pack:
            raise ValueError(
                f"Demo pack {path.name} thiếu demo_pack=true; "
                "chỉ pack watermark demo được nạp qua adapter này."
            )
        if pack.review_status != ReviewStatus.DEMO_APPROVED:
            raise ValueError(
                f"Demo pack {path.name} phải dùng review_status=demo_approved."
            )
        packs[pack.procedure_id] = pack
    if not packs:
        raise FileNotFoundError(f"Không tìm thấy demo pack JSON nào trong {DEMO_PACK_DIR}")
    return packs


class DemoPackProcedureRepository:
    async def list_procedures(self) -> list[ProcedureSummary]:
        return [
            ProcedureSummary(
                procedure_id=pack.procedure_id,
                name=pack.name,
                version=pack.version,
                review_status=pack.review_status,
                demo_mode=True,
            )
            for pack in load_demo_packs().values()
        ]

    async def get_procedure(self, procedure_id: str) -> ProcedurePack | None:
        return load_demo_packs().get(procedure_id)


class DemoPackRecommendationProvider:
    async def recommend(
        self, need_text: str, session_context: SessionContext
    ) -> list[ProcedureCandidate]:
        normalized_need = normalize_text(need_text)
        candidates: list[ProcedureCandidate] = []
        for pack in load_demo_packs().values():
            matched = [
                alias for alias in pack.aliases if normalize_text(alias) in normalized_need
            ]
            if matched:
                candidates.append(
                    ProcedureCandidate(
                        procedure_id=pack.procedure_id,
                        name=pack.name,
                        reason=f'Khớp từ khóa "{matched[0]}" trong mô tả nhu cầu.',
                    )
                )
        return candidates[:1]
