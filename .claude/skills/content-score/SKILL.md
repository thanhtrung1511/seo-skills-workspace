---
name: content-score
description: Chấm điểm một bài viết nha khoa theo checklist content chuẩn của Dr. Care (65 tiêu chí, thang 100, ≥80 là đạt) và trả về nhận xét ưu điểm / nhược điểm / vấn đề cần cải thiện. Dùng skill này khi user gõ /content-score hoặc đưa một URL bài viết và muốn "chấm điểm bài viết", "chấm content", "đánh giá bài viết theo checklist", "review content nha khoa", "audit bài viết", "kiểm tra bài viết đạt chuẩn chưa", "cho điểm bài", "content này bao nhiêu điểm", "bài này đạt chưa". Kể cả khi user chỉ dán một link bài nha khoa/y khoa và hỏi "được chưa" hay "ổn chưa", hãy dùng skill này để chấm theo checklist.
---

# Content Score — Chấm điểm content nha khoa theo checklist Dr. Care

Khi user gọi `/content-score` hoặc đưa URL bài viết cần chấm, thực hiện đúng workflow dưới đây. Mục tiêu: đọc bài, chấm theo **checklist 65 tiêu chí** (nhúng trong skill), tính **điểm trên thang 100** (≥80 = ĐẠT), và đưa nhận xét hành động được.

Checklist đầy đủ + trọng số + cách chấm nằm ở [references/checklist.md](references/checklist.md). **Đọc file đó trước khi chấm** — đừng chấm theo trí nhớ, vì thang điểm và trọng số nằm trong đó.

---

## Bước 1 — Thu thập đầu vào

Nếu user đã đưa URL thì đi tiếp luôn. Nếu thiếu, hỏi:

```
=== CONTENT SCORE — Chấm điểm bài viết nha khoa ===

[1] URL bài viết cần chấm (bắt buộc)
    →

[2] Keyword chính của bài (nên có — để chấm các tiêu chí keyword)
    Nếu bỏ trống, mình sẽ tự suy từ H1/title/meta.
    →

[3] Keyword phụ (tuỳ chọn)
    →
```

Nếu user không cho keyword, tự suy từ H1/title và **nói rõ giả định** đó trong báo cáo.

---

## Bước 2 — Đọc nội dung bài viết

**Cách nhanh & chuẩn nhất**: chạy script bóc tách có sẵn để lấy toàn bộ tín hiệu định lượng trong một lần (kết nối ra trang web ngoài qua HTTP):

```bash
python3 scripts/extract_seo_signals.py "<URL>" "<keyword chính>"
```

Script trả về: title + độ dài, meta description + độ dài, H1/H2/H3, số chữ, số ảnh + % có ALT, số internal/external link, danh sách nguồn uy tín (Tier 1/2/3), từ tuyệt đối YMYL, ngày cập nhật, byline/disclaimer/FAQ schema, và mật độ keyword. Dùng số liệu này để chấm — khỏi ước lượng bằng mắt.

Nếu script không chạy được (không có Python/mạng), fallback sang `WebFetch` hoặc trình duyệt để tải trang. Dù cách nào, cần lấy được:

- **Phần hiển thị**: H1, các H2/H3/H4, sapo, thân bài, kết bài, FAQ, caption ảnh, disclaimer.
- **Phần HTML/meta**: thẻ `<title>`, `<meta name="description">`, thuộc tính `ALT` của ảnh, các thẻ `<a>` (internal/external link + href), byline/author box.
- **Số liệu định lượng**: tổng số chữ, số ảnh, độ dài câu/đoạn trung bình, số internal link, danh sách domain của external link (để đối chiếu Tier 1/2/3).

Nếu trang chặn fetch hoặc trả về nội dung rỗng, báo cho user và hỏi: dán trực tiếp nội dung bài, hoặc thử URL khác. Không bịa nội dung để chấm.

---

## Bước 3 — Chấm từng tiêu chí

Đi qua **cả 65 tiêu chí** trong checklist, theo từng nhóm. Với mỗi tiêu chí, gán một trong:

- **1 — Đạt**: đáp ứng đầy đủ yêu cầu.
- **0.5 — Đạt một phần**: có nhưng chưa đủ/chưa chuẩn (vd có CTA nhưng không theo 3S; có ảnh nhưng thiếu ALT ở vài ảnh).
- **0 — Không đạt**: thiếu hoặc sai.
- **N/A**: thật sự không kiểm tra được chỉ từ URL (vd % đạo văn, tone màu ảnh, information gain so với top 10). Loại khỏi mẫu số và liệt kê riêng ở mục "Cần kiểm tra thủ công" — **không** đoán bừa thành 0 hay 1.

Nguyên tắc chấm cho chắc tay:
- **Ưu tiên bằng chứng cụ thể.** Khi kết luận một tiêu chí, dẫn ra chi tiết trong bài (vd: "H1 dài 71 ký tự > 63 → 0", "external link toàn blog lạ, không có nguồn Tier 1/2/3 → 0").
- Các tiêu chí YMYL nhóm B đặc biệt quan trọng — chấm nghiêm. Bài procedural (implant, nhổ răng, phẫu thuật…) mà **thiếu phần rủi ro/chống chỉ định** thì tiêu chí #19 và #40 phải 0, và nêu đây là lỗi nghiêm trọng.
- Từ tuyệt đối ("100% an toàn", "bền vĩnh viễn", "chắc chắn thành công") xuất hiện trong bài → #19 và #41 bị trừ.
- Đo định lượng thật (đếm ký tự H1, đếm số câu >30 từ, đếm ảnh/1000 chữ), đừng ước lượng cảm tính.

---

## Bước 4 — Tính điểm

Theo đúng công thức trong checklist:

1. Với mỗi nhóm: `điểm nhóm = (tổng điểm đạt của tiêu chí áp dụng ÷ số tiêu chí áp dụng) × trọng số nhóm`. (Tiêu chí N/A không tính vào mẫu số.)
2. `Tổng điểm = cộng điểm 9 nhóm` (làm tròn tới 1 chữ số thập phân, tối đa 100).
3. **≥ 80 → ĐẠT; < 80 → CHƯA ĐẠT.**

Tự kiểm tra lại phép cộng trước khi xuất — điểm phải khớp với bảng nhóm.

---

## Bước 5 — Xuất báo cáo

Luôn dùng đúng cấu trúc này:

```
════════════════════════════════════════
  BÁO CÁO CHẤM ĐIỂM CONTENT — DR. CARE
════════════════════════════════════════
URL:      <url>
Keyword:  <keyword chính>  (nguồn: user cung cấp / suy từ H1)
Số chữ:   <n> từ   |   Số ảnh: <n>   |   Internal link: <n>

┌────────────────────────────────────────┐
│  TỔNG ĐIỂM:  <X.X> / 100   →  <ĐẠT ✅ / CHƯA ĐẠT ❌>  │
└────────────────────────────────────────┘

── ĐIỂM THEO NHÓM ────────────────────────
 Nhóm                          Đạt/Áp dụng   Điểm/Trọng số
 A. Tổng thể nội dung             .../...        .../15
 B. Thương hiệu & độ tin cậy      .../...        .../20
 C. Cấu trúc bài viết             .../...        .../15
 D. Trải nghiệm người đọc         .../...        .../10
 E. Media                         .../...        .../10
 F. Internal Link                 .../...        .../10
 G. Keyword                       .../...        .../8
 H. Technical                     .../...        .../5
 I. Tối ưu AI Search              .../...        .../7

── ✅ ƯU ĐIỂM ─────────────────────────────
• <những tiêu chí làm tốt, nêu 3-6 điểm nổi bật>

── ⚠️ NHƯỢC ĐIỂM ──────────────────────────
• <các tiêu chí 0 hoặc 0.5, kèm dẫn chứng cụ thể trong bài>

── 🔧 VẤN ĐỀ CẦN CẢI THIỆN (ưu tiên) ──────
1. [Ảnh hưởng lớn] <việc cần làm + tiêu chí # liên quan>
2. [Ảnh hưởng vừa] <...>
3. <...>
   → Sắp xếp theo mức tác động tới điểm & tới E-E-A-T/YMYL.

── 📋 CẦN KIỂM TRA THỦ CÔNG (N/A) ─────────
• <các tiêu chí không tự chấm được từ URL, để user tự soát>
════════════════════════════════════════
```

Sau báo cáo, hỏi: "Bạn muốn mình xem chi tiết bảng chấm từng tiêu chí, hay gợi ý cách sửa từng lỗi để nâng điểm lên ≥80 không?"

Nếu user muốn xem chi tiết, in bảng đầy đủ 65 tiêu chí (# | tên | điểm | lý do).

---

## Lưu ý

- **Chấm nhiều URL cùng lúc**: nếu user đưa danh sách, chấm từng bài và cuối cùng in bảng xếp hạng điểm.
- **Trung thực về giới hạn**: nêu rõ tiêu chí nào là N/A vì không đọc được từ trang, đừng để điểm ảo. Nếu số tiêu chí N/A nhiều bất thường (vd trang chặn fetch), cảnh báo là điểm chỉ mang tính tham khảo.
- **Không dễ dãi**: đây là content y khoa YMYL — thà chấm nghiêm còn hơn cho đạt một bài thiếu bác sĩ chịu trách nhiệm hoặc thiếu cảnh báo rủi ro.
- Checklist là của Dr. Care (nha khoa); nếu user đưa bài ngoài lĩnh vực nha khoa, vẫn chấm được nhưng nói rõ một số tiêu chí (chuyên khoa, nguồn y khoa) có thể không hoàn toàn phù hợp.
