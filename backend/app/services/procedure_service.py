from typing import Dict, Any, List, Optional
from app.models.checklist import ChecklistResponse, ChecklistItem, Step
from app.models.common import Citation

PROCEDURES_DB = {
    "dang-ky-khai-sinh": {
        "id": "dang-ky-khai-sinh",
        "name": "Đăng ký khai sinh",
        "jurisdiction": "Cấp xã/phường/thị trấn",
        "authority": "Ủy ban nhân dân cấp xã",
        "effective_from": "2024-01-01",
        "effective_to": None,
        "last_verified_at": "2026-07-17",
        "trust_state": "verified_guidance"
    },
    "dang-ky-thuong-tru": {
        "id": "dang-ky-thuong-tru",
        "name": "Đăng ký thường trú",
        "jurisdiction": "Cấp xã/phường/thị trấn",
        "authority": "Công an cấp xã",
        "effective_from": "2024-01-01",
        "effective_to": None,
        "last_verified_at": "2026-07-17",
        "trust_state": "verified_guidance"
    },
    "dang-ky-ho-kinh-doanh": {
        "id": "dang-ky-ho-kinh-doanh",
        "name": "Đăng ký thành lập hộ kinh doanh",
        "jurisdiction": "Cấp huyện/quận/thị xã",
        "authority": "Phòng Tài chính - Kế hoạch cấp huyện",
        "effective_from": "2024-01-01",
        "effective_to": None,
        "last_verified_at": "2026-07-17",
        "trust_state": "verified_guidance"
    }
}

class ProcedureService:
    @staticmethod
    def list_procedures() -> List[Dict[str, Any]]:
        return list(PROCEDURES_DB.values())

    @staticmethod
    def get_procedure(procedure_id: str) -> Optional[Dict[str, Any]]:
        return PROCEDURES_DB.get(procedure_id)

    @staticmethod
    def get_checklist(procedure_id: str) -> ChecklistResponse:
        citations = [
            Citation(title="Luật Hộ tịch số 60/2014/QH13", url="https://chinhphu.vn", ref_code="LUAT-HOTICH-2014"),
            Citation(title="Nghị định 123/2015/NĐ-CP", url="https://chinhphu.vn", ref_code="ND-123-2015")
        ]

        if procedure_id == "dang-ky-khai-sinh":
            return ChecklistResponse(
                procedure_id=procedure_id,
                procedure_name=PROCEDURES_DB[procedure_id]["name"],
                required_documents=[
                    ChecklistItem(
                        id="giay-chung-sinh",
                        title="Giấy chứng sinh",
                        required=True,
                        description="Bản chính do cơ sở y tế nơi trẻ sinh ra cấp. Nếu không có giấy chứng sinh thì nộp văn bản xác nhận của người làm chứng.",
                        citations=[citations[1]]
                    ),
                    ChecklistItem(
                        id="cccd-cha-me",
                        title="Căn cước công dân của cha và mẹ",
                        required=True,
                        description="Bản chụp xuất trình kèm bản chính để đối chiếu.",
                        citations=[citations[0]]
                    )
                ],
                optional_documents=[
                    ChecklistItem(
                        id="giay-dang-ky-ket-hon",
                        title="Giấy chứng nhận kết hôn",
                        required=False,
                        description="Xuất trình nếu cha mẹ có đăng ký kết hôn để xác định quan hệ cha, mẹ, con.",
                        citations=[citations[0]]
                    )
                ],
                steps=[
                    Step(
                        step_number=1,
                        title="Chuẩn bị và nộp hồ sơ",
                        description="Người đi đăng ký chuẩn bị đầy đủ giấy tờ và nộp tại UBND cấp xã nơi cư trú của cha hoặc mẹ.",
                        processing_time="Giải quyết ngay trong ngày",
                        fees="Miễn phí"
                    )
                ],
                form_schema={
                    "type": "object",
                    "properties": {
                        "ho_ten_tre": {"type": "string", "title": "Họ và tên trẻ", "minLength": 2},
                        "ngay_sinh_tre": {"type": "string", "title": "Ngày sinh của trẻ", "format": "date"},
                        "ho_ten_cha": {"type": "string", "title": "Họ và tên cha"},
                        "ho_ten_me": {"type": "string", "title": "Họ và tên mẹ"}
                    },
                    "required": ["ho_ten_tre", "ngay_sinh_tre", "ho_ten_me"]
                },
                effective_date="2024-01-01",
                sources=citations
            )

        return ChecklistResponse(
            procedure_id=procedure_id,
            procedure_name=PROCEDURES_DB[procedure_id]["name"],
            required_documents=[
                ChecklistItem(
                    id="doc-required-1",
                    title="Tờ khai theo mẫu quy định",
                    required=True,
                    description="Điền đầy đủ thông tin vào biểu mẫu do nhà nước ban hành.",
                    citations=[citations[0]]
                )
            ],
            optional_documents=[],
            steps=[
                Step(
                    step_number=1,
                    title="Nộp hồ sơ trực tuyến hoặc trực tiếp",
                    description="Nộp hồ sơ qua Cổng dịch vụ công hoặc tại bộ phận Một cửa.",
                    processing_time="3-5 ngày làm việc",
                    fees="Tùy trường hợp"
                )
            ],
            form_schema={
                "type": "object",
                "properties": {
                    "ho_ten_nguoi_khai": {"type": "string", "title": "Họ và tên người khai", "minLength": 2},
                    "so_dien_thoai": {"type": "string", "title": "Số điện thoại"}
                },
                "required": ["ho_ten_nguoi_khai"]
            },
            effective_date="2024-01-01",
            sources=citations
        )
