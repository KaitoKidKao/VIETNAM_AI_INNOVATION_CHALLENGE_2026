---
name: AI Procedure Copilot
description: Hệ thống trợ lý hướng dẫn và tiền kiểm hồ sơ hành chính công
colors:
  primary: "#0F172A"       # Deep Slate (Chữ chính & Header)
  neutral-bg: "#F8FAFC"    # Slate Tint (Màu nền body)
  accent: "#2563EB"        # Trusted Blue (CTA chính & Link)
  warning: "#D97706"       # Amber (Cảnh báo vàng)
  error: "#DC2626"         # Red (Lỗi đỏ)
  success: "#16A34A"       # Green (Đạt chuẩn xanh)
typography:
  display:
    fontFamily: "Outfit, Inter, sans-serif"
    fontSize: "clamp(2rem, 5vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "4px"
  md: "8px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: "12px 24px"
  card:
    backgroundColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: "24px"
---

# Design System: AI Procedure Copilot

## 1. Overview

**Creative North Star: "The Digital Registry Bureau"**

Hệ thống thiết kế tập trung hoàn toàn vào tính **thực dụng (utilitarian)** và **sự rõ ràng (clarity)**. Mọi quyết định thiết kế đều hướng tới việc giảm thiểu tải thức nhận của người dân khi phải đối mặt với các biểu mẫu hành chính phức tạp. Chúng tôi từ chối các xu hướng thiết kế SaaS bóng bẩy, gradient màu mè, hay kính mờ (glassmorphic) để đổi lấy sự tập trung, đáng tin cậy như một cơ quan một cửa hiện đại và sạch sẽ.

**Key Characteristics:**
- Giao diện hai cột rõ ràng: Cột trái là Trợ lý hướng dẫn (Chat/Checklist), cột phải là biểu mẫu động kê khai (Form).
- Sử dụng màu sắc làm tín hiệu điều hướng lỗi (Đỏ, Vàng, Xanh) cực kỳ rõ ràng và có độ tương phản cao.
- Độ rộng dòng văn bản giới hạn ở mức dễ đọc (65-75ch).

## 2. Colors

Bảng màu sử dụng cấu trúc tương phản cao và rõ ràng, sử dụng các tông màu lạnh của Slate và Blue để gợi lên sự an tâm, tin cậy.

### Primary
- **Deep Slate** (#0F172A): Dùng cho văn bản chính, tiêu đề và các phần tử quan trọng cần sự vững chãi.

### Neutral
- **Slate Tint** (#F8FAFC): Màu nền body của trang web, giảm mỏi mắt cho người dùng.
- **Pure White** (#FFFFFF): Màu nền cho các thẻ card, container biểu mẫu và khung chat.
- **Border Slate** (#E2E8F0): Màu đường viền mảnh phân chia các khu vực nội dung.

### Semantic
- **Amber Warning** (#D97706): Chỉ định các cảnh báo thiếu thông tin hoặc cần lưu ý.
- **Red Error** (#DC2626): Chỉ định các lỗi định dạng hoặc mâu thuẫn bắt buộc phải sửa.
- **Green Success** (#16A34A): Chỉ định các trường dữ liệu và hồ sơ đã đạt kiểm tra sơ bộ.

**The Contrast Rule.** Màu sắc tín hiệu (Đỏ/Vàng/Xanh) phải luôn đi kèm biểu tượng hoặc nhãn văn bản; không bao giờ dùng duy nhất màu sắc để biểu đạt trạng thái đạt/lỗi.

## 3. Typography

**Display Font:** Outfit (hoặc sans-serif dự phòng)
**Body Font:** Inter (hoặc sans-serif dự phòng)

Giao diện kết hợp tính hình học sắc nét của Outfit cho tiêu đề lớn và tính dễ đọc cao của Inter cho nội dung dài hoặc nhãn form.

### Hierarchy
- **Display** (700, clamp(2rem, 5vw, 3rem), 1.2): Dùng cho tiêu đề trang chính và chào hỏi đầu trang.
- **Headline** (600, 1.5rem, 1.3): Dùng cho tiêu đề các phần lớn (Checklist, Form).
- **Title** (600, 1.125rem, 1.4): Dùng cho tên các trường, các bước trong quy trình.
- **Body** (400, 1rem, 1.6): Dùng cho văn bản hướng dẫn, mô tả hồ sơ.
- **Label** (500, 0.875rem, 1.2): Dùng cho nhãn phụ, ngày tháng, và trích dẫn nguồn luật.

**The Reading Rhythm Rule.** Khoảng cách giữa các đoạn văn bản hướng dẫn phải bằng chính xác một nửa chiều cao dòng của font chữ đó để duy trì mạch đọc tốt.

## 4. Elevation

Hệ thống thiết kế này sử dụng triết lý **phẳng theo mặc định (flat by default)**. Chiều sâu được phân tách bằng màu nền và các đường viền mảnh (border), thay vì sử dụng các đổ bóng (drop shadow) mềm lớn mang tính trang trí.

### Shadow Vocabulary
- **Interactive Focus** (`box-shadow: 0 0 0 2px #2563EB`): Sử dụng làm vòng sáng tập trung (focus ring) khi người dùng di chuyển bằng bàn phím hoặc nhấn vào input.

**The Border Priority Rule.** Ưu tiên sử dụng đường viền mảnh (1px solid #E2E8F0) để phân tách các khu vực thẻ card. Chỉ dùng bóng mờ rất nhẹ khi cần phân tách một modal nổi lên trên bề mặt.

## 5. Components

### Buttons
- **Shape:** Bo góc vừa phải (8px) mang lại cảm giác thân thiện nhưng vẫn nghiêm túc.
- **Primary:** Sử dụng màu Trusted Blue (#2563EB), chữ trắng (#FFFFFF), padding (12px 24px).
- **Hover / Focus:** Hover chuyển màu đậm hơn (#1D4ED8), focus-visible hiển thị vòng viền focus.

### Cards / Containers
- **Corner Style:** 8px radius.
- **Background:** Màu trắng tinh khiết (#FFFFFF) nổi bật trên nền Slate Tint.
- **Border:** Viền mờ mảnh (1px solid #E2E8F0).

### Inputs / Fields
- **Style:** Nền trắng, viền xám (#CBD5E1), góc bo 8px.
- **Focus:** Viền đổi sang Trusted Blue và có bóng bao quanh 2px để báo trạng thái hoạt động.

### Navigation
- **Style:** Thanh điều hướng tối giản trên đầu hoặc bên hông, sử dụng màu chữ Deep Slate, hover có gạch chân mảnh.

## 6. Do's and Don'ts

### Do:
- **Do** Luôn trích dẫn nguồn luật đi kèm các hướng dẫn checklist (Ví dụ: "Theo Điều 15 Luật Hộ tịch").
- **Do** Đảm bảo độ tương phản màu chữ luôn đạt WCAG AA trở lên (đặc biệt là chữ xám trên nền trắng).
- **Do** Thiết kế các trạng thái rỗng (empty states) thân thiện cho khung chat khi mới bắt đầu.

### Don't:
- **Don't** Sử dụng các đổ bóng mờ ảo (drop shadow) quá lớn gây cảm giác bồng bềnh thiếu nghiêm túc.
- **Don't** Sử dụng chữ gradient hoặc các hình nền chuyển động nhiều màu sắc.
- **Don't** Để các chữ tiêu đề quá lớn bị tràn khỏi khung chứa trên thiết bị di động.
