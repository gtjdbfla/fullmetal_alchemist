"""노벨피아·조아라 업로드용 평문 txt를 manuscripts/current/*.md에서 만들어 publish/txt-platform/에 둔다.

원고(마크다운)의 서식을 어느 편집기에서도 깨지지 않는 기호로 바꾼다. 굵게·기울임 같은 서식 지원 여부는 플랫폼마다 달라 의존하지 않는다.
원고 본문은 건드리지 않고 출력만 바꾼다. 기본 연재용 txt(scripts/export_txt.py → publish/txt/)는 그대로 둔다.

표기 규칙(원고 → 업로드용):
  `…`   편지·쪽지 글            → 「…」
  ==…==  에드의 수첩·생각       → 『…』   (~~…~~ 지운 수첩 글도 같은 표기)
  **…**  줄 전체가 굵게(문서·기록·되새기는 말) → 〈…〉
         화 도입의 장소 표시(**아메스트리스, 이슈발.**) → 굵게만 제거, 평문
         문장 속 강조 → 굵게만 제거
  > …    회상 인용              → '>'만 제거(앞 문장과 따옴표 대사가 구분해 준다)
  ---    장면 구분              → ───
표기 기호는 아래 MARKS만 바꾸면 전체에 반영된다."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_txt import CONFIG, ROOT, strip_heading  # noqa: E402

OUTPUT = ROOT / "publish" / "txt-platform"
MARKS = {"letter": ("「", "」"), "note": ("『", "』"), "doc": ("〈", "〉")}
SCENE = "───"  # 장면 구분 기호(작가 지정)
LOCATION = re.compile(r"^\*\*[^*]+,\s*[^*]+\.\*\*$")  # **아메스트리스, 이슈발.** 같은 장소 표시


def wrap(kind: str, text: str) -> str:
    a, b = MARKS[kind]
    return f"{a}{text}{b}"


def convert_line(line: str, first_content: bool) -> str:
    s = line.strip()
    if s in ("---", "-", "*"):
        return SCENE
    s = re.sub(r"^>\s?", "", s)
    if first_content and LOCATION.match(s):                       # 화 도입 장소 표시
        return s.replace("**", "")
    if re.fullmatch(r"\*\*[^*]+\*\*", s):                         # 줄 전체가 굵게 = 문서·기록·되새김
        return wrap("doc", s[2:-2].replace("`", ""))
    s = re.sub(r"==\*\*([^*]+)\*\*==", r"==\1==", s)               # ==**…**== 겹침
    s = re.sub(r"~~(.+?)~~", lambda m: wrap("note", m.group(1)), s)
    s = re.sub(r"==(.+?)==", lambda m: wrap("note", m.group(1)), s)
    s = re.sub(r"`([^`]+)`", lambda m: wrap("letter", m.group(1)), s)
    return s.replace("**", "")                                    # 문장 속 강조는 기호만 제거


def convert(lines: list[str]) -> str:
    out, seen = [], False
    for line in strip_heading(lines):
        first = False
        if line.strip() and not seen:
            seen, first = True, True
        out.append(convert_line(line, first))
    text = "\n".join(out).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    while text.endswith(SCENE):
        text = text[: -len(SCENE)].rstrip()
    return text


def export() -> list[tuple[str, str, int]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT.glob("*.txt"):
        stale.unlink()
    rows = []
    for item in json.loads(CONFIG.read_text(encoding="utf-8"))["manuscripts"]:
        source = ROOT / item["file"]
        body = convert(source.read_text(encoding="utf-8").strip().splitlines())
        title = f"{item['episode']} {item['title']}"
        number = source.name.split("-")[0]
        (OUTPUT / f"{number}_{title.replace(' ', '_')}.txt").write_text(f"{title}\n\n{body}\n", encoding="utf-8", newline="\n")
        rows.append((number, title, len(body)))
    return rows


if __name__ == "__main__":
    print(f"txt files={len(export())} -> {OUTPUT.relative_to(ROOT)}")
