import json
import shutil
from copy import deepcopy
from pathlib import Path

from export_txt import export as export_txt

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
AUTHOR_SITE = ROOT / "author-site"
CONFIG = ROOT / "private" / "dashboard-config.json"
LEGACY = ROOT / "private" / "archive" / "project-before-dashboard-reset.json"
CHAPTER_TARGET = (4800, 5000)

def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def legacy_history() -> list[dict]:
    if not LEGACY.exists():
        return []
    payload = json.loads(LEGACY.read_text(encoding="utf-8"))
    return [{
        "id": item["id"], "episode": item["episode"], "title": item["title"],
        "version": item.get("version", 1), "text": item["text"],
        "archivedReason": "대시보드 구조 개편 전 보관본",
    } for item in payload.get("manuscripts", [])]

def hydrate_manuscripts(payload: dict) -> None:
    reviews = {item["episode"]: item for item in payload.get("chapterReviews", [])}
    for item in payload.get("manuscripts", []):
        source = ROOT / item.pop("file")
        text = source.read_text(encoding="utf-8").strip()
        lines = text.splitlines()
        if lines and lines[0].startswith("# "):
            heading_index = 1
            while heading_index < len(lines) and not lines[heading_index].strip():
                heading_index += 1
            if heading_index < len(lines) and lines[heading_index].startswith("## "):
                text = "\n".join(lines[heading_index + 1:]).strip()
        item["text"] = text
        item["characters"] = len(text)
        review = reviews.get(item.get("episode"))
        if review is not None:
            length_ok = CHAPTER_TARGET[0] <= len(text) <= CHAPTER_TARGET[1]
            review["length"] = {
                "characters": len(text),
                "status": "O" if length_ok else "△",
                "target": "4,800–5,000자",
                "reason": f"공백 포함 {len(text):,}자 · 목표 {'충족' if length_ok else '범위 밖'}",
            }
            statuses = {category.get("status", "△") for category in review.get("categories", [])}
            review["overallStatus"] = "X" if "X" in statuses else "△" if not length_ok or "△" in statuses else "O"
            review["overallReason"] = review["length"]["reason"]
        for chapter in payload.get("storyBible", {}).get("chapters", []):
            if chapter.get("label") == item.get("episode"):
                chapter["characterCount"] = len(text)
                break

def main() -> None:
    base = json.loads(CONFIG.read_text(encoding="utf-8"))
    hydrate_manuscripts(base)
    public = deepcopy(base)
    public["audience"] = "reader"
    public.pop("admin", None)
    public.pop("history", None)
    public.pop("analysis", None)
    public.pop("chapterReviews", None)
    public.pop("storyline", None)
    public.pop("storyBible", None)
    public.pop("sourceDocuments", None)
    write_json(SITE / "data" / "project.json", public)

    if AUTHOR_SITE.exists():
        for child in AUTHOR_SITE.iterdir():
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    else:
        AUTHOR_SITE.mkdir(parents=True)
    shutil.copytree(SITE, AUTHOR_SITE, dirs_exist_ok=True)
    author = deepcopy(base)
    author["audience"] = "author"
    author["history"] = legacy_history()
    write_json(AUTHOR_SITE / "data" / "project.json", author)
    export_txt()
    print(f"reader manuscripts={len(public.get('manuscripts', []))} author history={len(author['history'])}")

if __name__ == "__main__":
    main()
