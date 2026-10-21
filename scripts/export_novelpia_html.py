"""노벨피아 에디터(굵게 B·기울임 I·밑줄 U·취소선 S 버튼)에 서식째 붙여 넣을 HTML을 manuscripts/current/*.md에서 만들어 publish/html-novelpia/에 둔다.

사용법: 회차 HTML을 크롬에서 열고 Ctrl+A → Ctrl+C → 노벨피아 본문 칸에 붙여넣기(붙여넣기 방식은 에디터 위 드롭다운에서 서식을 유지하는 쪽).
제목은 에디터의 제목 칸에 따로 넣으므로 HTML 본문에는 제목 줄이 없다. 원고 본문은 건드리지 않고 출력만 바꾼다.

표기 규칙(원고 → 에디터 서식):
  **…**  → 굵게(B)        원고가 굵게 쓴 곳(문서·기록 문구, 화 도입 장소 표시, 강조)을 그대로 살린다
  ~~…~~  → 취소선(S)      에드가 그어 지운 수첩 글
  ==…==  → 기울임(I)      에드의 수첩·생각
  `…`    → 「…」          편지·적힌 글(길어서 기울임 대신 낫표. 서식이 사라져도 구분됨)
  > …    → '>'만 제거
  ---    → ───  (장면 구분 기호. '* * *'는 쓰지 않는다)
STYLE만 고치면 전체에 반영된다."""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_txt import CONFIG, ROOT, SCENE_BREAK, strip_heading  # noqa: E402

OUTPUT = ROOT / "publish" / "html-novelpia"
STYLE = {"bold": "b", "strike": "s", "note": "i"}
LETTER = ("「", "」")


def inline(text: str) -> str:
    """한 줄의 마크다운 서식을 HTML 태그로. 순서: 이스케이프 → 겹친 서식 → 편지 낫표."""
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", lambda m: f"{LETTER[0]}{m.group(1)}{LETTER[1]}", t)
    t = re.sub(r"\*\*(.+?)\*\*", lambda m: f"<{STYLE['bold']}>{m.group(1)}</{STYLE['bold']}>", t)
    t = re.sub(r"~~(.+?)~~", lambda m: f"<{STYLE['strike']}>{m.group(1)}</{STYLE['strike']}>", t)
    t = re.sub(r"==(.+?)==", lambda m: f"<{STYLE['note']}>{m.group(1)}</{STYLE['note']}>", t)
    return t


BREAK_HTML = "<p>───</p>"   # 장면 구분 기호(작가 지정)
BLANK_HTML = "<p><br></p>"
SPACED = True                # True: 원고의 빈 줄을 빈 문단으로 옮겨 문단 사이를 넓게(작가가 고른 '기존' 간격). False: 문단 간격만 자동


def convert(lines: list[str]) -> str:
    out = []
    for line in strip_heading(lines):
        s = line.strip()
        if s in ("---", "-", "*"):
            out.append(BREAK_HTML)
        elif not s:
            if SPACED:
                out.append(BLANK_HTML)
        else:
            out.append(f"<p>{inline(re.sub(r'^>\s?', '', s))}</p>")
    text = "\n".join(out).strip()
    text = re.sub(r"(<p><br></p>\n?){2,}", BLANK_HTML + "\n", text)
    while text.endswith(BREAK_HTML) or text.endswith(BLANK_HTML):
        text = re.sub(r"(<p>───</p>|<p><br></p>)$", "", text).rstrip()
    return text


def export() -> list[tuple[str, str]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT.glob("*.html"):
        stale.unlink()
    rows = []
    for item in json.loads(CONFIG.read_text(encoding="utf-8"))["manuscripts"]:
        source = ROOT / item["file"]
        title = f"{item['episode']} {item['title']}"
        body = convert(source.read_text(encoding="utf-8").strip().splitlines())
        number = source.name.split("-")[0]
        page = f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><title>{html.escape(title)}</title></head>\n<body>\n{body}\n</body></html>\n'
        (OUTPUT / f"{number}_{title.replace(' ', '_')}.html").write_text(page, encoding="utf-8", newline="\n")
        rows.append((number, title))
    return rows


if __name__ == "__main__":
    print(f"html files={len(export())} -> {OUTPUT.relative_to(ROOT)}")
