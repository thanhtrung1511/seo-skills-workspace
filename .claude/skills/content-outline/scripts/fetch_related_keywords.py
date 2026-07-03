#!/usr/bin/env python3
"""
fetch_related_keywords.py — Kết nối API GỢI Ý TÌM KIẾM CỦA GOOGLE (Google Suggest)
để lấy từ khóa liên quan và câu hỏi kiểu "People Also Ask" THẬT từ hành vi tìm
kiếm, thay vì đoán. Đây là phần "kết nối nền tảng ngoài (API/CLI)" của skill
content-outline.

Endpoint công khai, không cần API key:
    https://suggestqueries.google.com/complete/search?client=chrome&hl=vi&q=<query>

Cách dùng:
    python3 fetch_related_keywords.py "trồng răng implant"
    python3 fetch_related_keywords.py "trồng răng implant" --gl vn --hl vi

Chỉ dùng thư viện chuẩn của Python.
"""
import sys, json, urllib.request, urllib.parse, urllib.error

UA = "Mozilla/5.0 (compatible; content-outline-skill/1.0)"
# Bộ từ để hoặc thêm để bung ra câu hỏi PAA và các nhánh dài
QUESTION_MODIFIERS = ["", "là gì", "có tốt không", "giá bao nhiêu", "có đau không",
                      "ở đâu", "khi nào", "có nên", "cách", "loại nào tốt", "review",
                      "bao lâu", "kiêng gì", "quy trình"]


def suggest(query, hl="vi", gl="vn"):
    q = urllib.parse.quote(query)
    url = (f"https://suggestqueries.google.com/complete/search?"
           f"client=chrome&hl={hl}&gl={gl}&q={q}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read().decode("utf-8", errors="ignore")
        arr = json.loads(data)
        return arr[1] if len(arr) > 1 else []
    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return []


def main():
    if len(sys.argv) < 2:
        print("Dùng: python3 fetch_related_keywords.py \"<keyword>\" [--hl vi] [--gl vn]")
        sys.exit(1)
    kw = sys.argv[1]
    hl, gl = "vi", "vn"
    for i, a in enumerate(sys.argv):
        if a == "--hl" and i + 1 < len(sys.argv):
            hl = sys.argv[i + 1]
        if a == "--gl" and i + 1 < len(sys.argv):
            gl = sys.argv[i + 1]

    seen = set()
    related, questions = [], []
    for mod in QUESTION_MODIFIERS:
        query = f"{kw} {mod}".strip()
        for s in suggest(query, hl, gl):
            sl = s.lower().strip()
            if sl in seen:
                continue
            seen.add(sl)
            # phân loại: câu hỏi hay từ khóa thường
            if any(w in sl for w in ["là gì", "tại sao", "vì sao", "có nên", "bao nhiêu",
                                     "bao lâu", "khi nào", "ở đâu", "có đau", "có tốt",
                                     "kiêng", "?", "như thế nào", "loại nào"]):
                questions.append(s)
            else:
                related.append(s)

    if not seen:
        print("⚠ Không lấy được gợi ý (có thể do mạng hoặc Google giới hạn). "
              "Skill sẽ tự đề xuất từ khóa liên quan dựa trên kiến thức.")
        sys.exit(3)

    print("=" * 56)
    print(f"GỢI Ý TỪ GOOGLE SUGGEST — \"{kw}\"  (hl={hl}, gl={gl})")
    print("=" * 56)
    print(f"\n🔑 TỪ KHÓA LIÊN QUAN ({len(related)}):")
    for r in related:
        print(f"  • {r}")
    print(f"\n❓ CÂU HỎI / PAA gợi ý ({len(questions)}):")
    for q in questions:
        print(f"  • {q}")
    print("\n→ Dùng các câu hỏi trên cho mục FAQ, các từ khóa cho phần 'rải keyword phụ'.")


if __name__ == "__main__":
    main()
