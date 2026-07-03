# SEO Skills Workspace — Claude Code

Không gian làm việc cá nhân gồm **3 Claude Code Skills** phục vụ công việc SEO,
đặt trong `.claude/skills/`. Dùng cho bài tập: *"Xây 1 không gian làm việc cá
nhân với ít nhất 3 skills"*.

## Danh sách skills

| Skill | Lệnh | Chức năng | Kết nối ngoài | Có files/folder |
|---|---|---|---|---|
| **content-score-nganhnhakhoa** | `/content-score-nganhnhakhoa` | Nhập URL bài nha khoa → chấm 65 tiêu chí checklist Dr. Care → điểm /100 (≥80 đạt) + nhận xét ưu/nhược/cần cải thiện | ✅ HTTP fetch trang ngoài (CLI/API) | ✅ `references/` + `scripts/` |
| **content-outline** | `/content-outline` | Nhập 1 keyword → search intent + dàn ý H1/H2/H3 + FAQ chuẩn SEO | ✅ **Google Suggest API** | ✅ `scripts/` |
| **meta-writer** | `/meta-writer` | Chủ đề + keyword → 3 phương án title & meta description (đếm ký tự, đúng chuẩn độ dài) | — | — |

## Đối chiếu yêu cầu bài tập

- ✅ **≥ 3 skills**: có 3 skills trong `.claude/skills/`.
- ✅ **≥ 1 skill kết nối nền tảng ngoài (API/MCP/CLI)**:
  - `content-outline` gọi **Google Suggest API** qua script Python (`scripts/fetch_related_keywords.py`) để lấy từ khóa & câu hỏi PAA thật.
  - `content-score-nganhnhakhoa` kết nối HTTP tới website ngoài để bóc tách tín hiệu SEO (`scripts/extract_seo_signals.py`).
- ✅ **≥ 1 skill có files & folder bên cạnh SKILL.md**:
  - `content-score-nganhnhakhoa/` có `references/checklist.md` (65 tiêu chí) và `scripts/extract_seo_signals.py`.
  - `content-outline/` có `scripts/fetch_related_keywords.py`.

## Cấu trúc

```
seo-skills-workspace/
├── README.md
├── .claude/
│   └── skills/
│       ├── content-score-nganhnhakhoa/
│       │   ├── SKILL.md
│       │   ├── references/checklist.md
│       │   └── scripts/extract_seo_signals.py
│       ├── content-outline/
│       │   ├── SKILL.md
│       │   └── scripts/fetch_related_keywords.py
│       └── meta-writer/SKILL.md
└── outputs/                # file output mẫu từ việc chạy skill
    ├── content-score_elitedental_implant.md
    ├── content-score_drcare_ngam-rang.md
    └── content-outline_trong-rang-implant.md
```

## Video demo

Video quay màn hình chạy skill (Google Drive):
👉 https://drive.google.com/file/d/1UbrFsxh_nqYqFlRPAimpfZiB7nyNpTwR/view?usp=sharing

## Cách dùng

1. Mở thư mục này bằng Claude Code (`claude` trong terminal tại đây).
2. Gõ `/` để thấy 3 lệnh skill, hoặc gọi trực tiếp, ví dụ:
   - `/content-score-nganhnhakhoa https://…` — chấm điểm một bài viết.
   - `/content-outline "trồng răng implant"` — dựng dàn ý.
   - `/meta-writer` — theo hướng dẫn trong skill.

### Chạy trực tiếp script kết nối ngoài (không qua skill)

```bash
# Google Suggest API — từ khóa & PAA thật
python3 .claude/skills/content-outline/scripts/fetch_related_keywords.py "trồng răng implant"

# Bóc tách tín hiệu SEO on-page của một URL
python3 .claude/skills/content-score-nganhnhakhoa/scripts/extract_seo_signals.py "https://..." "keyword chính"
```

> Yêu cầu: Python 3 (chỉ dùng thư viện chuẩn, không cần cài thêm) và kết nối mạng.

## Nguồn checklist

Checklist chấm điểm trong `content-score-nganhnhakhoa` dựa trên bộ tiêu chí content nha khoa
của Dr. Care (65 tiêu chí, 9 nhóm, trọng số cộng = 100).
