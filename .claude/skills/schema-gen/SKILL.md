---
name: schema-gen
description: Sinh mã Schema markup JSON-LD chuẩn schema.org để gắn vào website giúp SEO và hiển thị rich result trên Google. Dùng skill này khi user gõ /schema-gen hoặc muốn "tạo schema", "viết structured data", "JSON-LD cho trang", "schema markup", "gắn dữ liệu có cấu trúc", "tạo rich snippet", "schema sản phẩm/bài viết/FAQ/doanh nghiệp", "markup cho Google", hoặc mô tả một trang (sản phẩm, bài viết, FAQ, doanh nghiệp, breadcrumb…) và muốn có đoạn code schema dán vào web. Kể cả khi user không nói chữ "schema" mà muốn "cho Google hiểu trang" hoặc "hiện sao/giá/FAQ trên kết quả tìm kiếm", hãy dùng skill này.
---

# Schema Gen — Sinh JSON-LD Schema markup chuẩn schema.org

Khi user gọi `/schema-gen` hoặc yêu cầu tạo structured data, thực hiện theo workflow dưới đây. Kết quả là **đoạn JSON-LD hợp lệ** (đặt trong `<script type="application/ld+json">`) mà user dán thẳng vào `<head>` hoặc `<body>` của trang.

Tại sao JSON-LD: Google khuyến nghị JSON-LD hơn Microdata/RDFa vì tách khỏi HTML hiển thị, dễ chèn và bảo trì. Schema đúng giúp Google hiểu nội dung và có cơ hội hiện *rich result* (sao đánh giá, giá, FAQ, breadcrumb, ảnh…), tăng CTR.

---

## Bước 1 — Xác định loại schema

Hỏi (hoặc suy từ mô tả của user) trang thuộc loại nào. Các loại phổ biến và khi nào dùng:

```
=== SCHEMA GEN ===
Trang bạn cần đánh schema thuộc loại nào?

[1] Article / BlogPosting   — bài viết, tin tức, blog
[2] Product                 — trang sản phẩm (có giá, tồn kho, đánh giá)
[3] FAQPage                 — trang/khối câu hỏi thường gặp
[4] LocalBusiness           — doanh nghiệp có địa điểm (shop, phòng khám…)
[5] Organization            — thông tin tổ chức/thương hiệu (thường cho trang chủ)
[6] BreadcrumbList          — đường dẫn phân cấp
[7] HowTo                   — bài hướng dẫn theo bước
[8] Review / AggregateRating— đánh giá, xếp hạng
[9] Loại khác / kết hợp nhiều loại (mô tả giúp mình)
```

Một trang có thể cần **nhiều schema** cùng lúc (vd Product + BreadcrumbList + FAQPage). Nếu vậy, sinh từng khối hoặc gộp bằng mảng `@graph`.

---

## Bước 2 — Thu thập trường dữ liệu

Với mỗi loại, chỉ hỏi các trường **cần & nên có** (đừng hỏi tràn lan). Các trường bắt buộc theo yêu cầu rich result của Google:

- **Article/BlogPosting**: `headline` (≤110 ký tự), `image`, `author` (Person/Organization), `publisher` (kèm logo), `datePublished`, `dateModified`, `mainEntityOfPage` (URL).
- **Product**: `name`, `image`, `description`, `brand`, `sku`/`gtin`, và `offers` (`price`, `priceCurrency`, `availability`, `url`); nếu có đánh giá thêm `aggregateRating` (`ratingValue`, `reviewCount`) hoặc `review`.
- **FAQPage**: danh sách `mainEntity` gồm các `Question` → mỗi câu có `acceptedAnswer` (Answer/text). Chỉ dùng cho FAQ thật hiển thị trên trang (không nhồi FAQ ẩn — Google phạt).
- **LocalBusiness**: `name`, `address` (PostalAddress đầy đủ), `telephone`, `openingHoursSpecification`, `geo` (lat/long nếu có), `priceRange`, `url`, `image`. Chọn subtype sát nhất (vd `Dentist`, `Restaurant`, `Store`).
- **Organization**: `name`, `url`, `logo`, `sameAs` (mảng link mạng xã hội), `contactPoint`.
- **BreadcrumbList**: danh sách `itemListElement` gồm các `ListItem` (`position`, `name`, `item`=URL).
- **HowTo**: `name`, `step` (mảng HowToStep có `name` + `text` + ảnh nếu có), `totalTime` tuỳ chọn.

Trường nào user không có thì **bỏ hẳn khỏi JSON** — không điền giá trị giả. Không bịa rating, giá, ngày tháng.

---

## Bước 3 — Sinh JSON-LD

Nguyên tắc:
- Luôn mở đầu bằng `"@context": "https://schema.org"` và `"@type"` đúng loại.
- Định dạng ngày theo **ISO 8601** (`2026-07-03` hoặc có giờ `2026-07-03T09:00:00+07:00`).
- URL để dạng tuyệt đối (có `https://`).
- Giá là chuỗi số không kèm ký hiệu tiền (`"price": "1500000"`, `"priceCurrency": "VND"`).
- Bọc kết quả trong thẻ script để user dán thẳng.
- Nếu nhiều schema, dùng `@graph` để gộp trong 1 script.

Ví dụ khung (Article):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://vd.com/bai-viet" },
  "headline": "Tiêu đề bài viết ≤110 ký tự",
  "image": "https://vd.com/anh.jpg",
  "author": { "@type": "Person", "name": "BS. Nguyễn Văn A" },
  "publisher": {
    "@type": "Organization",
    "name": "Pet Shop Bông",
    "logo": { "@type": "ImageObject", "url": "https://vd.com/logo.png" }
  },
  "datePublished": "2026-07-01",
  "dateModified": "2026-07-03"
}
</script>
```

---

## Bước 4 — Xuất kết quả + hướng dẫn kiểm tra

Sau khi in code, luôn kèm:

```
── CÁCH DÙNG ──────────────────────────────
• Dán đoạn <script> trên vào trong <head> (hoặc cuối <body>) của trang.
• Kiểm tra hợp lệ tại:
   - Google Rich Results Test: https://search.google.com/test/rich-results
   - Schema Markup Validator:  https://validator.schema.org
• Đảm bảo dữ liệu trong schema KHỚP với nội dung hiển thị trên trang
  (Google phạt schema khai khác với nội dung thấy được).

── TRƯỜNG CÒN THIẾU (nên bổ sung để mạnh hơn) ──
• <liệt kê các trường tuỳ chọn user chưa cung cấp, vd aggregateRating, sameAs...>
```

Hỏi tiếp: "Bạn muốn mình thêm loại schema nào nữa cho trang này (vd Breadcrumb, FAQ) hay chỉnh trường nào không?"

---

## Lưu ý

- **Chỉ markup thứ có thật trên trang.** FAQ, review, giá… phải đang hiển thị cho người dùng; markup nội dung ẩn hoặc sai lệch vi phạm chính sách của Google và có thể bị phạt thủ công.
- Chọn `@type` **cụ thể nhất** có thể (vd `Dentist` thay vì `LocalBusiness` chung) để Google hiểu rõ hơn.
- Nếu user đưa **URL thật** và có tool đọc trang, có thể trích sẵn dữ liệu (title, ảnh, giá…) để điền, rồi để user xác nhận.
- Trả về **JSON hợp lệ 100%**: kiểm tra dấu phẩy, ngoặc, escape ký tự đặc biệt trong chuỗi (vd dấu ngoặc kép bên trong phải `\"`). Nếu không chắc, tự rà lại cú pháp trước khi đưa.
- Với schema tiếng Việt, giữ nguyên dấu tiếng Việt trong giá trị chuỗi (JSON hỗ trợ UTF-8).
