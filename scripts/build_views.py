import json
import shutil
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
AUTHOR_SITE = ROOT / "author-site"
CONFIG = ROOT / "private" / "dashboard-config.json"
LEGACY = ROOT / "private" / "archive" / "project-before-dashboard-reset.json"

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
    for item in payload.get("manuscripts", []):
        source = ROOT / item.pop("file")
        text = source.read_text(encoding="utf-8").strip()
        lines = text.splitlines()
        if len(lines) >= 2 and lines[0].startswith("# ") and lines[1].startswith("## "):
            text = "\n".join(lines[2:]).strip()
        item["text"] = text
        item["characters"] = len(text)

def main() -> None:
    base = json.loads(CONFIG.read_text(encoding="utf-8"))
    hydrate_manuscripts(base)
    public = deepcopy(base)
    public["audience"] = "reader"
    public.pop("admin", None)
    public.pop("history", None)
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
    print(f"reader manuscripts={len(public.get('manuscripts', []))} author history={len(author['history'])}")

if __name__ == "__main__":
    main()
