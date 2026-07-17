from typing import Dict, Any
from app.models.validation import ValidationResponse, Finding

class ValidationService:
    @staticmethod
    def validate(procedure_id: str, form_data: Dict[str, Any]) -> ValidationResponse:
        findings = []
        is_valid = True

        if procedure_id == "dang-ky-khai-sinh":
            # Required checks
            if not form_data.get("ho_ten_tre"):
                findings.append(Finding(
                    field="ho_ten_tre",
                    severity="error",
                    message="Họ và tên trẻ là bắt buộc và không được để trống.",
                    fix_suggestion="Vui lòng điền họ và tên đầy đủ của trẻ.",
                    rule_id="R-BIRTH-001"
                ))
                is_valid = False

            if not form_data.get("ngay_sinh_tre"):
                findings.append(Finding(
                    field="ngay_sinh_tre",
                    severity="error",
                    message="Ngày sinh của trẻ là bắt buộc.",
                    fix_suggestion="Vui lòng chọn ngày sinh của trẻ.",
                    rule_id="R-BIRTH-002"
                ))
                is_valid = False

            # Logical / cross-field check
            ho_ten_tre = form_data.get("ho_ten_tre", "")
            if ho_ten_tre and not any(char.isalpha() for char in ho_ten_tre):
                findings.append(Finding(
                    field="ho_ten_tre",
                    severity="error",
                    message="Họ tên của trẻ chứa ký tự không hợp lệ.",
                    fix_suggestion="Vui lòng chỉ sử dụng chữ cái tiếng Việt và khoảng trắng.",
                    rule_id="R-BIRTH-003"
                ))
                is_valid = False

            # Warning checks
            if not form_data.get("ho_ten_cha"):
                findings.append(Finding(
                    field="ho_ten_cha",
                    severity="warning",
                    message="Thiếu thông tin người cha có thể ảnh hưởng nếu muốn ghi tên cha vào giấy khai sinh ngay lập tức.",
                    fix_suggestion="If there is father information, please fill it in to do identification at the same time.",
                    rule_id="R-BIRTH-004"
                ))

        else:
            # Default validator for other forms
            if not form_data.get("ho_ten_nguoi_khai"):
                findings.append(Finding(
                    field="ho_ten_nguoi_khai",
                    severity="error",
                    message="Họ và tên người khai là bắt buộc.",
                    fix_suggestion="Vui lòng điền họ tên của bạn.",
                    rule_id="R-GEN-001"
                ))
                is_valid = False

        summary = "Hồ sơ của bạn đã đạt các kiểm tra sơ bộ." if is_valid else "Phát hiện một số lỗi cần khắc phục trước khi nộp hồ sơ."

        return ValidationResponse(
            procedure_id=procedure_id,
            is_valid=is_valid,
            findings=findings,
            summary_message=summary
        )
