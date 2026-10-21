"""회차별 연재용 txt를 manuscripts/current/*.md에서 만들어 publish/txt/에 둔다."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "private" / "dashboard-config.json"
OUTPUT = ROOT / "publish" / "txt"
SCENE_BREAK = "───"  # 장면 구분 기호(작가 지정, 업로드용과 같게)


def strip_heading(lines: list[str]) -> list[str]:
    index = 0
    if lines and lines[0].startswith("# "):
        index = 1
        while index < len(lines) and not lines[index].strip():
            index += 1
        if index < len(lines) and lines[index].startswith("## "):
            index += 1
    return lines[index:]


def plain_body(lines: list[str]) -> str:
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped in ("---", "-", "*"):
            out.append(SCENE_BREAK)
            continue
        stripped = re.sub(r"^>\s?", "", stripped)
        stripped = stripped.replace("**", "").replace("==", "").replace("~~", "")
        out.append(stripped)
    text = "\n".join(out).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    while text.endswith(SCENE_BREAK):
        text = text[: -len(SCENE_BREAK)].rstrip()
    return text


def export() -> list[tuple[str, str, int]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT.glob("*.txt"):
        stale.unlink()
    rows = []
    for item in json.loads(CONFIG.read_text(encoding="utf-8"))["manuscripts"]:
        source = ROOT / item["file"]
        body = plain_body(strip_heading(source.read_text(encoding="utf-8").strip().splitlines()))
        title = f"{item['episode']} {item['title']}"
        number = source.name.split("-")[0]
        target = OUTPUT / f"{number}_{title.replace(' ', '_')}.txt"
        target.write_text(f"{title}\n\n{body}\n", encoding="utf-8", newline="\n")
        rows.append((number, title, len(body)))
    index = "\n".join(f"{number}\t{title}\t{count}자" for number, title, count in rows)
    (OUTPUT / "_INDEX.tsv").write_text(index + "\n", encoding="utf-8", newline="\n")
    return rows


if __name__ == "__main__":
    print(f"txt files={len(export())} -> {OUTPUT.relative_to(ROOT)}")
