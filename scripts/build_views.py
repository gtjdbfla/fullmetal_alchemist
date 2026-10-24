import json
import re
import shutil
from copy import deepcopy
from pathlib import Path

from export_txt import export as export_txt

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
AUTHOR_SITE = ROOT / "author-site"
CONFIG = ROOT / "private" / "dashboard-config.json"
LEGACY = ROOT / "private" / "archive" / "project-before-dashboard-reset.json"
CHAPTER_TARGET = (5000, 9000)  # 7,000자는 권장일 뿐, 작가 지시로 9,000자까지 허용

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
                heading_index += 1
            text = "\n".join(lines[heading_index:]).strip()
        text = re.sub(r"(\n\s*(?:---|-|\*))+\s*$", "", text).strip()
        item["text"] = text
        counted = text.replace("==", "").replace("~~", "")
        item["characters"] = len(counted)
        review = reviews.get(item.get("episode"))
        if review is not None:
            length_ok = CHAPTER_TARGET[0] <= len(counted) <= CHAPTER_TARGET[1]
            review["length"] = {
                "characters": len(counted),
                "status": "O" if length_ok else "△",
                "target": "5,000–7,000자 권장 (9,000자까지 허용)",
                "reason": f"공백 포함 {len(counted):,}자 · 권장 범위 {'충족' if length_ok else '밖'}",
            }
            statuses = {category.get("status", "△") for category in review.get("categories", [])}
            review["overallStatus"] = "X" if "X" in statuses else "△" if not length_ok or "△" in statuses else "O"
            review["overallReason"] = review["length"]["reason"]
        for chapter in payload.get("storyBible", {}).get("chapters", []):
            if chapter.get("label") == item.get("episode"):
                chapter["characterCount"] = len(counted)
                break

def attach_portraits(payload: dict) -> None:
    for person in payload.get("publicCharacters", []):
        person.pop("portrait", None)
        for ext in ("jpg", "jpeg", "png", "webp"):
            if (SITE / "portraits" / f"{person.get('slug', '')}.{ext}").exists():
                person["portrait"] = f"portraits/{person['slug']}.{ext}"
                break


def main() -> None:
    base = json.loads(CONFIG.read_text(encoding="utf-8"))
    hydrate_manuscripts(base)
    attach_portraits(base)
    # User-requested unified author workspace at both existing URLs.
    author = deepcopy(base)
    author["audience"] = "author"
    author["history"] = legacy_history()
    write_json(SITE / "data" / "project.json", author)
    private_maps = ROOT / "private" / "maps"
    if private_maps.exists():
        shutil.copytree(private_maps, SITE / "maps", dirs_exist_ok=True)
    AUTHOR_SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SITE, AUTHOR_SITE, dirs_exist_ok=True)
    public = author
    export_txt()
    print(f"workspace manuscripts={len(public.get('manuscripts', []))} author history={len(author['history'])}")

if __name__ == "__main__":
    main()
