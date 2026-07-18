# Procedure Family Registry

Registry này mở rộng ba anchor procedure thành các family có variant, workflow
liên thông và thủ tục hỗ trợ mà không trộn checklist/rules giữa các mã.

## Contract

Nguồn tracked:
[`data/registry/procedure-family-registry.csv`](../../data/registry/procedure-family-registry.csv).

- Registry version: `vaic-procedure-family-registry-v1`.
- Family K1 manifest version: `vaic-family-k1-review-v1`.
- Ba anchor không đổi: `1.001193`, `1.004222`, `1.001612`.
- Registry hiện có 25 source duy nhất và 26 quan hệ. `2.000986` là một source
  có quan hệ bundled với cả khai sinh và thường trú.

### Relation types

| Loại | Ý nghĩa runtime tương lai |
| --- | --- |
| `anchor` | Thủ tục chuẩn đang đại diện family. |
| `direct_variant` | Biến thể cần hỏi làm rõ và chọn exact procedure code. |
| `bundled_workflow` | Workflow liên thông nhiều family, không nhập vào anchor. |
| `supporting_prerequisite` | Thủ tục/giấy xác nhận hỗ trợ trước thủ tục chính. |
| `post_registration` | Cấp lại, thay đổi, xóa hoặc ghi nhận sau đăng ký. |
| `lifecycle_operation` | Thao tác dừng/chuyển trạng thái quy trình. |
| `adjacent_broad` | Nguồn liên quan rộng, mặc định deferred để tránh retrieval nhiễu. |

Release tier `anchor`, `tier_1`, `tier_2`, `deferred` chỉ là thứ tự review;
không phải approval status.

## Dual-Source Discovery

- Mã `1.*` trong task này được đọc từ tracked `data/Data_DVC`.
- Mã `2.*` được đọc trực tiếp từ ignored `dataset_raw` qua path cấu hình.
- Tool không sao chép raw file vào worktree, Git hoặc report.
- Manifest chỉ lưu logical path, checksum và metadata đã parse; không lưu raw text.

Trong repository root có `dataset_raw`:

```powershell
python scripts/data/prepare_family_k1_review_package.py
```

Trong worktree riêng, truyền path của corpus local hiện có:

```powershell
python scripts/data/prepare_family_k1_review_package.py `
  --dataset-raw-dir C:\path\to\workspace\dataset_raw
```

Output local dưới `artifacts/family-k1-review/`:

- `candidate-family-sources.csv`
- `family-provenance-report.json`
- `family-review-checklist.md`

Prepare fail closed nếu registry drift, thiếu source, sai collection, title/code
không khớp, lỗi strict UTF-8 hoặc checksum/normalization lỗi. Tất cả 25 source
luôn bắt đầu bằng `review_status=needs_review`.

## Ranh Giới Runtime

Registry/package này chưa thay đổi router, retrieval hoặc Procedure Pack runtime.
Task intent router tiếp theo phải:

1. Chọn family trước.
2. Hỏi làm rõ để chọn exact procedure code.
3. Chỉ retrieval chunks của code đã chọn.
4. Không phát guidance cho variant chưa qua K1.
5. Không nhân đôi source/chunks của workflow liên thông đa family.

Human K1 review và family manifest validator/release là gate riêng trước khi nối
bất kỳ variant nào vào runtime.
