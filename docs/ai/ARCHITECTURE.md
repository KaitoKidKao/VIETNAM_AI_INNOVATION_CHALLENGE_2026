# Kiến trúc tối thiểu — AI Procedure Copilot

> Trạng thái: Active
>
> Cập nhật gần nhất: 2026-07-17
> Decision liên quan: D-005

Tài liệu này mô tả chi tiết kiến trúc đang triển khai cho dự án AI Procedure Copilot.

## Mục tiêu kiến trúc

- Phục vụ một demo MVP end-to-end đáng tin cậy trong 48 giờ.
- Tách biệt rõ ràng giữa Frontend (giao diện, widget) và Backend (quy tắc kiểm tra deterministic, gọi LLM).
- Dễ dàng chạy và xác thực độc lập dưới local.

## Tổng quan hệ thống

```text
       [Người dùng / Giám khảo]
                  |
                  v
       [Web FE (Next.js - Port 3000)]
                  |
                  |  (REST API / JSON)
                  v
       [FastAPI Backend - Port 8000]
         /        |        \
        v         v         v
 [RAG Store] [Rule Engine] [LLM Provider]
```

## Thành phần và boundary

| Thành phần | Trách nhiệm | Input / output | Owner tạm thời / Task Record | Rủi ro |
| --- | --- | --- | --- | --- |
| **Web FE** | Giao diện chat hướng dẫn, điền form động, hiển thị checklist và cảnh báo lỗi. Cung cấp file nhúng widget. | Input: Tương tác người dùng. Output: Gọi API và hiển thị kết quả. | Antigravity / `local-20260717-scaffold-vaic` | CSS conflict nếu nhúng trực tiếp, được giảm thiểu bằng iframe / Web Component. |
| **FastAPI Backend** | Tiếp nhận câu hỏi, điều phối luồng (intent clarification, retrieval, deterministic rule checking, LLM response policy). | Input: REST Request JSON. Output: JSON chứa checklist/findings/citations. | Antigravity / `local-20260717-scaffold-vaic` | Lỗi timeout từ mô hình LLM bên ngoài, được xử lý bằng retry và error mapping. |
| **Rule Engine** | Kiểm tra lỗi kê khai (thiếu trường, sai định dạng, mâu thuẫn dữ liệu) một cách deterministic dựa trên schema. | Input: Dữ liệu form. Output: Danh sách findings (lỗi đỏ/vàng/xanh). | Antigravity / `local-20260717-scaffold-vaic` | Schema quá phức tạp cho 3 thủ tục, được giảm thiểu bằng cách tối giản form schema theo đúng pháp lý. |

## Contracts và tích hợp

| Boundary | Producer | Consumer | Contract/version | Validation | Fallback | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `/v1/procedures` | Backend | Frontend | JSON list of procedures | Schema validation | Static fallback lists | D-005 |
| `/v1/intake/turn` | Backend | Frontend | JSON turn session data | Schema validation | Trả lời lỗi hệ thống | D-005 |
| `/v1/applications/validate` | Backend | Frontend | Form payload / Findings | Deterministic rule checking | Trả về thông báo thành công mặc định | D-005 |

### API Routes chi tiết

- **`GET /health`**: Smoke check kiểm tra trạng thái hoạt động của Backend.
- **`GET /v1/procedures`**: Trả về danh sách 3 procedure packs đang được hỗ trợ (khai sinh, thường trú, hộ kinh doanh).
- **`POST /v1/intake/turn`**: Nhận câu hỏi/câu trả lời của phiên hội thoại để xác định nhu cầu hoặc hỏi làm rõ (clarification).
- **`POST /v1/procedures/{id}/checklist`**: Nhận câu trả lời làm rõ, trả về danh mục hồ sơ giấy tờ cần chuẩn bị và quy trình chi tiết cá nhân hóa.
- **`POST /v1/applications/validate`**: Nhận dữ liệu kê khai biểu mẫu, chạy rule engine để phát hiện trường thiếu, sai định dạng hoặc mâu thuẫn, trả về danh sách cảnh báo đỏ/vàng/xanh kèm cách sửa.

## Chạy, quan sát và khôi phục

| Việc | Lệnh hoặc bước đã kiểm chứng | Owner tạm thời / Task Record | Ghi chú |
| --- | --- | --- | --- |
| Cài dependencies | Backend: `pip install -r requirements.txt`<br>Frontend: `npm install` | Antigravity / `local-20260717-scaffold-vaic` | Chạy tại các thư mục tương ứng |
| Chạy local | Backend: `uvicorn main:app --port 8000 --reload`<br>Frontend: `npm run dev` | Antigravity / `local-20260717-scaffold-vaic` | Backend chạy cổng 8000, Frontend chạy cổng 3000 |
| Chạy checks | `python scripts/ci/validate_repo.py` | Antigravity / `local-20260717-scaffold-vaic` | Kiểm tra tính hợp lệ của repo |
| Rollback/fallback | Reset git commit / Hạ cấp xuống mock UI | Antigravity / `local-20260717-scaffold-vaic` | Dùng Git để rollback |
