from fastapi import APIRouter, HTTPException
from app.models.intake import IntakeRequest, IntakeResponse
from app.services.procedure_service import PROCEDURES_DB

router = APIRouter(prefix="/v1")

@router.post("/intake/turn", response_model=IntakeResponse)
def intake_turn(request: IntakeRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")

    last_user_message = request.messages[-1].content.lower()

    # Simple mock intent classification
    detected_id = request.current_procedure_id
    if not detected_id:
        if "khai sinh" in last_user_message or "sinh con" in last_user_message:
            detected_id = "dang-ky-khai-sinh"
        elif "thuong tru" in last_user_message or "ho khau" in last_user_message:
            detected_id = "dang-ky-thuong-tru"
        elif "ho kinh doanh" in last_user_message or "mo cua hang" in last_user_message:
            detected_id = "dang-ky-ho-kinh-doanh"

    if not detected_id:
        return IntakeResponse(
            detected_procedure_id=None,
            message="Xin chào! Tôi có thể hỗ trợ bạn chuẩn bị hồ sơ cho các thủ tục hành chính sau: Đăng ký khai sinh, Đăng ký thường trú, hoặc Đăng ký thành lập hộ kinh doanh. Bạn đang cần thực hiện thủ tục nào?",
            trust_state="need_more_information",
            required_clarifications=["procedure_selection"],
            sources=[]
        )

    proc_name = PROCEDURES_DB[detected_id]["name"]
    return IntakeResponse(
        detected_procedure_id=detected_id,
        message=f"Tôi đã nhận diện nhu cầu làm thủ tục: **{proc_name}**. Để hướng dẫn chính xác nhất, bạn có thể trả lời một số câu hỏi sau không?",
        trust_state="need_more_information",
        required_clarifications=["jurisdiction_detail", "relationship_to_subject"],
        sources=[{
            "title": "Cổng Dịch vụ công Quốc gia",
            "url": "https://dichvucong.gov.vn",
            "type": "official_portal"
        }]
    )
