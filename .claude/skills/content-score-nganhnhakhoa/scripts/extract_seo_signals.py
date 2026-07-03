#!/usr/bin/env python3
"""
extract_seo_signals.py — Bóc tách tín hiệu SEO on-page từ một URL để phục vụ
skill content-score. Chỉ dùng thư viện chuẩn của Python (không cần cài thêm).

Cách dùng:
    python3 extract_seo_signals.py <URL> [keyword_chính]

Trả về báo cáo dạng text: title, meta description, H1/H2/H3, số chữ, ảnh + ALT,
internal/external link, nguồn y khoa (Tier 1/2/3), từ tuyệt đối (YMYL),
ngày cập nhật, disclaimer, và mật độ keyword (nếu truyền keyword).

Đây chỉ là bước THU THẬP DỮ LIỆU. Việc chấm điểm 65 tiêu chí do skill thực hiện
dựa trên references/checklist.md.
"""
import sys, re, json, urllib.request, urllib.error
from html import unescape

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

# Nguồn uy tín theo checklist Dr. Care
AUTHORITY = {
    "Tier 1 (chuyên sâu)": ["pubmed", "ncbi.nlm.nih.gov", "nih.gov", "ada.org", "who.int", "nidcr"],
    "Tier 2 (triệu chứng/chăm sóc)": ["mayoclinic", "clevelandclinic", "cdc.gov"],
    "Tier 3 (nội địa VN)": ["moh.gov.vn", "medinet", "benhvienranghammat", "syt."],
}
# Từ tuyệt đối cần tránh trong content YMYL (loại trừ cụm hợp lệ "răng vĩnh viễn")
ABSOLUTE_PATTERNS = [
    r"100\s*%\s*an toàn", r"hoàn toàn không đau", r"bền vĩnh viễn",
    r"tồn tại vĩnh viễn", r"chắc chắn (thành công|khỏi)", r"tuyệt đối an toàn",
    r"không bao giờ (hỏng|đau|biến chứng)",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="ignore")


def tag_text(html, tag):
    out = []
    for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.S | re.I):
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = unescape(re.sub(r"\s+", " ", t)).strip()
        if t:
            out.append(t)
    return out


def visible_words(html):
    m = re.search(r'class="[^"]*entry-content[^"]*"(.*?)(</article|<footer)', html, re.S | re.I)
    body = m.group(1) if m else html
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
    text = unescape(re.sub(r"<[^>]+>", " ", body))
    return len(text.split()), text


def main():
    if len(sys.argv) < 2:
        print("Dùng: python3 extract_seo_signals.py <URL> [keyword]")
        sys.exit(1)
    url = sys.argv[1]
    keyword = sys.argv[2].lower() if len(sys.argv) > 2 else None

    try:
        html = fetch(url)
    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
        print(f"❌ Không tải được trang: {e}")
        print("→ Nhờ user dán trực tiếp nội dung bài hoặc thử URL khác.")
        sys.exit(2)

    domain = re.sub(r"^https?://", "", url).split("/")[0].replace("www.", "")

    # Title & meta
    title = (tag_text(html, "title") or [""])[0]
    mdesc = ""
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)', html, re.I)
    if m:
        mdesc = unescape(m.group(1)).strip()

    h1 = tag_text(html, "h1")
    h2 = tag_text(html, "h2")
    h3 = tag_text(html, "h3")
    words, text = visible_words(html)
    text_low = text.lower()

    # Ảnh + ALT
    imgs = re.findall(r"<img[^>]*>", html, re.I)
    alt_ok = sum(1 for i in imgs if re.search(r'alt=["\'][^"\']+["\']', i, re.I))

    # Links
    hrefs = re.findall(r'href=["\'](https?://[^"\']+)["\']', html, re.I)
    internal = [h for h in hrefs if domain in h]
    external = [h for h in hrefs if domain not in h]
    ext_domains = sorted({re.sub(r"^https?://", "", h).split("/")[0].replace("www.", "") for h in external})

    # Nguồn uy tín
    found_authority = {}
    for tier, doms in AUTHORITY.items():
        hits = [d for d in ext_domains if any(k in d for k in doms)]
        if hits:
            found_authority[tier] = hits

    # Từ tuyệt đối
    absolutes = []
    for p in ABSOLUTE_PATTERNS:
        for mm in re.finditer(p, text_low):
            absolutes.append(text_low[max(0, mm.start() - 20):mm.start() + 25].strip())

    # Ngày cập nhật
    dm = ""
    m = re.search(r'"dateModified":"([^"]+)"', html)
    if m:
        dm = m.group(1)

    # Disclaimer
    disclaimer = bool(re.search(r"không thay thế|mang tính (tham khảo|thông tin)|chỉ định trực tiếp của bác sĩ", text_low))
    # Byline / bác sĩ
    byline = bool(re.search(r"tư vấn chuyên môn|cố vấn chuyên môn|tham vấn y khoa", text_low))
    faq_schema = "FAQPage" in html

    # Keyword density
    density = None
    if keyword:
        cnt = len(re.findall(re.escape(keyword), text_low))
        density = (cnt / words * 100) if words else 0

    # In báo cáo
    p = print
    p("=" * 60)
    p(f"TÍN HIỆU SEO — {url}")
    p("=" * 60)
    p(f"Title ({len(title)} ký tự): {title}")
    p(f"Meta desc ({len(mdesc)} ký tự): {mdesc or '(không có)'}")
    p(f"H1 ({len(h1[0]) if h1 else 0} ký tự): {h1[0] if h1 else '(không có)'}")
    p(f"Số H1: {len(h1)} | H2: {len(h2)} | H3: {len(h3)}")
    p(f"Số chữ (body ước tính): ~{words}")
    p(f"Ảnh: {len(imgs)} thẻ <img>, {alt_ok} có ALT ({alt_ok*100//max(1,len(imgs))}%)")
    p(f"Internal link: {len(set(internal))} | External link: {len(set(external))}")
    p(f"Ngày cập nhật (dateModified): {dm or '(không tìm thấy)'}")
    p(f"Byline bác sĩ: {'CÓ' if byline else 'KHÔNG'} | Disclaimer: {'CÓ' if disclaimer else 'KHÔNG'} | FAQPage schema: {'CÓ' if faq_schema else 'KHÔNG'}")
    if keyword:
        p(f"Keyword '{keyword}': xuất hiện {cnt} lần, mật độ ~{density:.2f}%")
    p("-" * 60)
    p("H2:")
    for x in h2:
        p(f"  • {x}")
    p("H3:")
    for x in h3:
        p(f"  • {x}")
    p("-" * 60)
    p("NGUỒN UY TÍN (external authority):")
    if found_authority:
        for tier, hits in found_authority.items():
            p(f"  {tier}: {', '.join(hits)}")
    else:
        p("  ⚠ KHÔNG có nguồn Tier 1/2/3 → tiêu chí #17, #18 nguy cơ 0 điểm")
    p("External domains khác: " + (", ".join(d for d in ext_domains if d != domain) or "(không có)"))
    p("-" * 60)
    p("TỪ TUYỆT ĐỐI (YMYL — cần tránh):")
    if absolutes:
        for a in absolutes:
            p(f"  ⚠ ...{a}...")
    else:
        p("  ✓ Không phát hiện từ tuyệt đối sai (lưu ý: 'răng vĩnh viễn' là thuật ngữ hợp lệ)")
    p("=" * 60)


if __name__ == "__main__":
    main()
