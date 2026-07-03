---
name: meta-writer
description: Viết title tag và meta description chuẩn SEO cho một trang web. Dùng skill này khi user gõ /meta-writer hoặc muốn "viết title", "viết meta description", "viết thẻ meta", "tối ưu tiêu đề SEO", "meta tag cho bài viết", "SEO title", "viết mô tả trang", hoặc đưa một chủ đề/URL/từ khóa và muốn có tiêu đề + mô tả để lên top Google. Kể cả khi user không nói chính xác chữ "meta", nếu họ cần đặt tiêu đề trang chuẩn SEO thì dùng skill này.
---

# Meta Writer — Viết Title & Meta Description chuẩn SEO

Khi user gọi `/meta-writer` hoặc yêu cầu viết title/meta description, thực hiện theo workflow dưới đây. Mục tiêu là tạo ra **3 phương án** title + meta description vừa chuẩn kỹ thuật SEO vừa hấp dẫn người đọc, để user chọn hoặc phối trộn.

---

## Bước 1 — Thu thập thông tin

Nếu user đã cung cấp đủ trong tin nhắn thì bỏ qua form, đi thẳng tới Bước 2. Nếu thiếu, hỏi gọn (chỉ hỏi phần còn thiếu):

```
=== META WRITER ===
Cho mình vài thông tin để viết title + meta description:

[1] Chủ đề / tên trang (bắt buộc)
    Ví dụ: "Cách chọn thức ăn cho chó con"

[2] Từ khóa chính (bắt buộc)
    Từ khóa muốn lên top. Ví dụ: "thức ăn cho chó con"

[3] Từ khóa phụ (tuỳ chọn)
    1-3 từ liên quan. Ví dụ: "hạt cho chó con, sữa cho chó con"

[4] Loại trang (tuỳ chọn, mặc định: bài viết)
    bài viết blog / trang sản phẩm / trang danh mục / trang chủ / trang dịch vụ

[5] Tên thương hiệu (tuỳ chọn)
    Để thêm vào cuối title. Ví dụ: "Pet Shop Bông"

[6] Giọng điệu (tuỳ chọn, mặc định: thân thiện)
    thân thiện / chuyên nghiệp / bán hàng mạnh / trung tính
```

---

## Bước 2 — Nguyên tắc phải tuân thủ

Áp dụng đúng các chuẩn sau khi viết. Đây là lý do đằng sau từng con số, hiểu để viết cho khéo chứ không máy móc:

**Title tag:**
- Độ dài **50–60 ký tự** (Google cắt title khoảng ~580px, tương đương ~60 ký tự). Ngắn quá thì phí chỗ, dài quá thì bị cắt đuôi mất chữ.
- Từ khóa chính đặt **càng gần đầu càng tốt** — Google và mắt người đều ưu tiên phần đầu.
- Mỗi title **duy nhất**, không trùng lặp giữa các trang.
- Nếu có thương hiệu, đặt ở cuối, ngăn bằng ` | ` hoặc ` - `. Ví dụ: `Thức ăn cho chó con tốt nhất 2026 | Pet Shop Bông`.
- Tránh nhồi nhét từ khóa (keyword stuffing) — đọc phải tự nhiên như người viết.

**Meta description:**
- Độ dài **140–160 ký tự** (Google cắt mô tả khoảng ~155–160 ký tự trên desktop).
- Chứa từ khóa chính **ít nhất 1 lần** (Google in đậm từ khóa khớp truy vấn → hút click).
- Có **call-to-action** hoặc lợi ích rõ ràng: "Tìm hiểu ngay", "Xem bảng giá", "Miễn phí ship"... tùy loại trang.
- Mô tả đúng nội dung trang — không clickbait sai lệch, vì Google phạt và user thoát trang (tăng bounce).
- Viết cho **người đọc trước, máy sau**: một câu tóm tắt giá trị + một câu thúc đẩy hành động.

**Điều chỉnh theo loại trang:**
- *Sản phẩm*: nêu lợi ích + yếu tố tin cậy (giá, bảo hành, freeship) + CTA mua hàng.
- *Danh mục*: nhấn sự đa dạng/lựa chọn + thương hiệu.
- *Blog*: nhấn giá trị thông tin, gợi tò mò, hứa hẹn giải đáp.
- *Trang chủ*: nêu định vị thương hiệu + giá trị cốt lõi.

---

## Bước 3 — Xuất kết quả

Luôn trả về đúng cấu trúc sau. Với mỗi phương án, **đếm và hiển thị số ký tự** của title và description để user kiểm chứng độ dài.

```
=== KẾT QUẢ META ===
Từ khóa chính: <từ khóa>
Loại trang: <loại>

── Phương án 1 (an toàn, chuẩn SEO) ─────────────
Title (58 ký tự):
  Thức ăn cho chó con tốt nhất 2026 | Pet Shop Bông
Meta description (152 ký tự):
  Chọn thức ăn cho chó con đúng chuẩn dinh dưỡng theo từng độ tuổi.
  Xem gợi ý hạt & sữa tốt nhất 2026, giá tốt, freeship toàn quốc. Đặt ngay!

── Phương án 2 (nhấn lợi ích) ────────────────────
Title (55 ký tự): ...
Meta description (149 ký tự): ...

── Phương án 3 (gợi tò mò / CTA mạnh) ────────────
Title (57 ký tự): ...
Meta description (156 ký tự): ...

💡 Gợi ý: Phương án 1 hợp nếu ưu tiên rõ ràng; PA3 hợp nếu muốn tăng CTR.
   Bạn có thể trộn title PA1 với description PA3.
```

Sau khi xuất, hỏi: "Bạn muốn mình chỉnh phương án nào, hay viết thêm biến thể khác không?"

---

## Lưu ý

- Nếu user đưa **nhiều trang cùng lúc** (danh sách), viết cho từng trang và cảnh báo nếu phát hiện title/description có nguy cơ trùng nhau.
- Nếu user đưa **URL** thật, có thể đọc nội dung trang (nếu có tool WebFetch) để viết sát nội dung; nếu không, viết dựa trên chủ đề user mô tả.
- Luôn đếm ký tự thật (kể cả dấu cách và dấu tiếng Việt) — đừng ước lượng. Nếu lỡ vượt/thiếu ngưỡng, tự sửa lại trước khi trả kết quả.
- Không bịa thông tin (giá, khuyến mãi, giải thưởng) mà user chưa cung cấp.
