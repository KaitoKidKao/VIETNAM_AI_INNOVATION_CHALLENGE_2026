from __future__ import annotations

import re
import unicodedata
from enum import Enum


class IntakeDisposition(str, Enum):
    CONTINUE = "continue"
    GREETING = "greeting"
    OUT_OF_SCOPE = "out_of_scope"
    UNSUPPORTED_NEAR_INTENT = "unsupported_near_intent"


def normalize_intent_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    without_marks = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    ascii_words = re.sub(r"[^a-z0-9]+", " ", without_marks.replace("đ", "d"))
    return re.sub(r"\s+", " ", ascii_words).strip()


def _contains_all(text: str, phrases: tuple[str, ...]) -> bool:
    return all(phrase in text for phrase in phrases)


GREETING_PREFIXES = ("xin chao", "chao ban", "hello", "hi")

OUT_OF_SCOPE_PATTERNS = (
    ("giay phep lai xe",),
    ("ho chieu",),
    ("thue thu nhap",),
    ("doi", "can cuoc"),
    ("cap", "can cuoc"),
    ("can cuoc", "het han"),
    ("bao hiem xa hoi",),
    ("giay phep xay dung",),
)

UNSUPPORTED_NEAR_INTENT_PATTERNS = (
    ("cap lai", "khai sinh"),
    ("ban sao", "khai sinh"),
    ("cai chinh", "khai sinh"),
    ("nhan cha me con",),
    ("tam tru",),
    ("luu tru",),
    ("xoa", "thuong tru"),
    ("thanh lap cong ty",),
    ("dang ky doanh nghiep",),
    ("thay doi", "ho kinh doanh"),
)


def classify_intake_text(value: str) -> IntakeDisposition:
    normalized = normalize_intent_text(value)
    if any(
        normalized == greeting or normalized.startswith(f"{greeting} ")
        for greeting in GREETING_PREFIXES
    ):
        return IntakeDisposition.GREETING
    if any(_contains_all(normalized, pattern) for pattern in OUT_OF_SCOPE_PATTERNS):
        return IntakeDisposition.OUT_OF_SCOPE
    if any(_contains_all(normalized, pattern) for pattern in UNSUPPORTED_NEAR_INTENT_PATTERNS):
        return IntakeDisposition.UNSUPPORTED_NEAR_INTENT
    return IntakeDisposition.CONTINUE


def disposition_message(disposition: IntakeDisposition) -> str:
    return {
        IntakeDisposition.GREETING: (
            "Xin chào! 👋 Tôi là VNGov, trợ lý giúp bạn chuẩn bị hồ sơ hành chính. "
            "Hiện tôi hỗ trợ 3 thủ tục: đăng ký khai sinh, đăng ký thường trú và "
            "đăng ký thành lập hộ kinh doanh. Bạn cứ kể tự nhiên việc mình cần làm nhé — "
            "ví dụ: “vợ tôi mới sinh bé, giờ cần làm giấy tờ gì?”"
        ),
        IntakeDisposition.OUT_OF_SCOPE: (
            "Rất tiếc, thủ tục này chưa nằm trong phạm vi bản thử nghiệm "
            "(hiện tôi chỉ hỗ trợ khai sinh, thường trú và hộ kinh doanh). "
            "Bạn có thể tra cứu đầy đủ trên Cổng Dịch vụ công Quốc gia: https://dichvucong.gov.vn nhé."
        ),
        IntakeDisposition.UNSUPPORTED_NEAR_INTENT: (
            "Trường hợp của bạn khá gần với thủ tục tôi hỗ trợ nhưng chưa đúng phạm vi "
            "bản thử nghiệm. Để chắc chắn không mất công chuẩn bị nhầm, bạn vui lòng "
            "kiểm tra thủ tục tương ứng trên Cổng Dịch vụ công Quốc gia (dichvucong.gov.vn) nhé."
        ),
        IntakeDisposition.CONTINUE: "",
    }[disposition]
