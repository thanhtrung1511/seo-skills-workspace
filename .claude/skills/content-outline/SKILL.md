---
name: content-outline
description: Dựng dàn ý bài viết chuẩn SEO từ một từ khóa chính. Dùng skill này khi user gõ /content-outline hoặc muốn "lên dàn ý bài viết", "outline bài SEO", "cấu trúc bài viết chuẩn SEO", "dàn ý content", "viết outline blog", "brief bài viết", "H1 H2 H3 cho bài", "làm sườn bài viết", hoặc đưa một từ khóa và muốn có bố cục bài viết để lên top Google. Kể cả khi user chỉ nói "viết cho tôi cái sườn bài về X" mà không nói chữ SEO, nếu mục đích là bài chuẩn SEO thì dùng skill này.
---

# Content Outline — Dàn ý bài viết chuẩn SEO

Khi user gọi `/content-outline` hoặc yêu cầu lên dàn ý/sườn bài viết SEO, thực hiện theo workflow dưới đây. Kết quả là một **brief dàn ý hoàn chỉnh** mà người viết có thể ngồi vào viết ngay: cấu trúc heading, search intent, câu hỏi cần trả lời, và các gợi ý tối ưu.

---

## Bước 1 — Thu thập thông tin

Nếu user đã cung cấp đủ thì bỏ qua, đi thẳng Bước 2. Nếu thiếu, hỏi gọn phần còn thiếu:

```
=== CONTENT OUTLINE ===
Cho mình vài thông tin để dựng dàn ý:

[1] Từ khóa chính (bắt buộc)
    Ví dụ: "cách nuôi mèo con"

[2] Đối tượng đọc (tuỳ chọn, mặc định: người mới tìm hiểu)
    Ví dụ: "người lần đầu nuôi mèo"

[3] Mục tiêu bài viết (tuỳ chọn, mặc định: cung cấp thông tin)
    thông tin/hướng dẫn / so sánh / review sản phẩm / bán hàng

[4] Độ dài mong muốn (tuỳ chọn, mặc định: 1500-2000 từ)
```

---

## Bước 1.5 — Lấy từ khóa liên quan THẬT từ Google (kết nối API ngoài)

Trước khi tự suy nghĩ, chạy script để lấy gợi ý tìm kiếm thật từ **Google Suggest API** — dữ liệu này phản ánh đúng thứ người dùng đang gõ, giúp mục FAQ và phần "keyword phụ" bám sát nhu cầu thực tế thay vì đoán:

```bash
python3 scripts/fetch_related_keywords.py "<từ khóa chính>"
```

(Script chỉ dùng thư viện chuẩn, không cần API key — endpoint công khai `suggestqueries.google.com`.)

Kết quả trả về 2 nhóm: **từ khóa liên quan** và **câu hỏi kiểu PAA**. Dùng chúng làm nguyên liệu cho Bước 3 (chọn lọc, không bê nguyên si tất cả). Nếu script báo lỗi mạng/không lấy được, cứ tiếp tục và tự đề xuất dựa trên kiến thức — nói rõ là đã fallback.

---

## Bước 2 — Xác định search intent

Trước khi dựng heading, xác định **ý định tìm kiếm** của từ khóa — đây là bước quan trọng nhất, vì cấu trúc bài phải khớp thứ Google muốn xếp hạng cho truy vấn đó. Phân loại vào 1 trong 4 nhóm và nêu rõ:

- **Informational** (tìm thông tin): "cách...", "là gì", "tại sao" → bài hướng dẫn/giải thích.
- **Commercial** (cân nhắc mua): "tốt nhất", "so sánh", "review", "top" → bài so sánh/đánh giá.
- **Transactional** (muốn mua/hành động): "mua", "giá", "ở đâu", "khuyến mãi" → trang bán hàng/landing.
- **Navigational** (tìm thương hiệu cụ thể): tên brand → không cần bài blog dài.

Nêu một câu: "Từ khóa này thuộc intent <loại> → nên viết dạng <kiểu bài>." Nếu intent không rõ, chọn hướng phổ biến nhất và nói giả định.

---

## Bước 3 — Dựng dàn ý

Áp dụng các nguyên tắc sau (giải thích lý do để linh hoạt, không máy móc):

- **Chỉ 1 thẻ H1** = tiêu đề bài, chứa từ khóa chính. Google dùng H1 để hiểu chủ đề chính.
- **H2** cho các phần lớn; **H3** cho ý nhỏ trong H2. Cấu trúc phân cấp giúp Google (và người đọc lướt) nắm bố cục — cũng là cơ sở để ăn *featured snippet*.
- **Rải từ khóa chính + biến thể** tự nhiên vào một vài heading, đừng nhồi vào tất cả.
- Mở bài nên trả lời nhanh câu hỏi cốt lõi ngay 100 từ đầu (giữ chân người đọc + tăng cơ hội snippet).
- Phủ **các câu hỏi liên quan** (kiểu "People Also Ask") → thường gom thành mục FAQ ở cuối.
- Có phần **kết luận + CTA** phù hợp mục tiêu bài.
- Cân nhắc chỗ nên chèn: bảng so sánh, danh sách bước, hình ảnh/infographic, liên kết nội bộ.

---

## Bước 4 — Xuất kết quả

Luôn dùng đúng template này:

```
=== DÀN Ý BÀI VIẾT: <từ khóa chính> ===
Search intent: <loại> → <kiểu bài>
Đối tượng: <...>   |   Độ dài đề xuất: <...> từ

── META (gợi ý) ──────────────────────────
Title đề xuất: <tiêu đề chuẩn SEO ~55-60 ký tự>
Meta description: <~150 ký tự>
URL slug đề xuất: /tu-khoa-chinh

── CẤU TRÚC BÀI ───────────────────────────
H1: <tiêu đề chứa từ khóa chính>

  Mở bài (~100 từ): <1 câu tóm tắt bài sẽ trả lời gì>

H2: <phần 1>
   - ý cần nêu / dữ liệu cần có
   H3: <ý nhỏ>
H2: <phần 2>
   ...
H2: <phần N>

H2: Câu hỏi thường gặp (FAQ)
   - <câu hỏi 1 dạng People Also Ask>
   - <câu hỏi 2>
   - <câu hỏi 3>

H2: Kết luận
   - tóm tắt + CTA: <hành động mong muốn>

── GỢI Ý TỐI ƯU ───────────────────────────
• Từ khóa phụ nên rải: <danh sách 3-6 từ liên quan>
• Yếu tố nên chèn: <bảng / danh sách bước / ảnh / video...>
• Liên kết nội bộ gợi ý: <chủ đề bài nên link tới>
• Từ khóa LSI / thực thể liên quan: <vài từ ngữ cảnh>
```

Sau khi xuất, hỏi: "Bạn muốn mình đào sâu phần nào thành nội dung chi tiết, hay thêm/bớt mục nào không?"

---

## Lưu ý

- **Từ khóa phụ và câu hỏi liên quan**: ưu tiên dùng kết quả từ `scripts/fetch_related_keywords.py` (Bước 1.5) — đó là dữ liệu tìm kiếm thật. Bổ sung thêm bằng kiến thức về chủ đề nếu cần. Nếu script không chạy được thì tự đề xuất và nói rõ là fallback.
- Số lượng H2 nên tương xứng độ dài bài: ~1500 từ ≈ 4-6 H2; bài dài hơn thì nhiều hơn.
- Không dựng dàn ý sáo rỗng — mỗi heading phải có lý do tồn tại và phục vụ intent.
- Nếu từ khóa quá rộng (vd "chó mèo"), gợi ý user thu hẹp để bài có tiêu điểm rõ, hoặc đề xuất tách thành cụm nhiều bài (topic cluster).
