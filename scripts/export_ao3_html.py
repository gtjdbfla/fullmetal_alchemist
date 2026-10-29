"""AO3(Archive of Our Own) 업로드용 HTML을 translations/en/*.md에서 만들어 publish/en-ao3/에 둔다.

사용법: AO3 새 회차 화면에서 본문 편집기를 'HTML'로 바꾸고, 회차 .html 파일의 내용을 통째로 붙여 넣는다.
제목(Chapter Title)은 AO3의 제목 칸에 따로 넣으므로 HTML 본문에는 제목이 없다. 제목 목록은 _titles.txt에 있다.
원고(manuscripts/)는 건드리지 않는다. 영어 번역 원문은 translations/en/에 두고, 한국어 원고가 바뀌면 번역도 같이 고친다.

번역 원문 표기(마크다운):
  빈 줄          단락 구분
  *…*  / **…**   기울임 / 굵게 (에드의 수첩·강조 / 문서·기록 문구)
  > …           편지·노트·기도문 (연속된 > 줄은 하나의 인용 블록, 빈 '>' 줄은 단락 구분)
  * * *         장면 구분 → <hr />
출력 따옴표는 AO3에서 읽기 좋게 둥근 따옴표(“ ” ‘ ’)와 말줄임표(…)로 바꾼다."""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_txt import ROOT  # noqa: E402

SOURCE = ROOT / "translations" / "en"
OUTPUT = ROOT / "publish" / "en-ao3"
SCENE_BREAK = "* * *"


def smart_quotes(text: str) -> str:
    """직선 따옴표를 둥근 따옴표로. 여는 따옴표는 문장 시작·공백·괄호·줄표 뒤에 온 것."""
    out = []
    for i, ch in enumerate(text):
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < len(text) else ""
        opening = (not prev) or prev.isspace() or prev in "([{“‘"
        if prev and prev in "—*":  # 줄표·기울임 표시 뒤의 따옴표는 뒤에 글자가 이어질 때만 여는 따옴표
            opening = nxt.isalnum()
        if ch == '"':
            out.append("“" if opening else "”")
        elif ch == "'":
            out.append("‘" if opening else "’")
        else:
            out.append(ch)
    return "".join(out).replace("...", "…")


def inline(text: str) -> str:
    t = html.escape(text, quote=False)
    t = smart_quotes(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def convert(lines: list[str]) -> str:
    out, quote = [], []

    def flush_quote():
        if quote:
            paras = [p for p in "\n".join(quote).split("\n\n") if p.strip()]
            out.append("<blockquote>" + "".join(f"<p>{inline(' '.join(p.split()))}</p>" for p in paras) + "</blockquote>")
            quote.clear()

    for line in lines:
        s = line.rstrip()
        if s.startswith(">"):
            quote.append(s[1:].strip())
            continue
        if quote and not s.strip():
            # 인용 블록은 빈 줄이 아니라 '>' 줄이 끊는다. 빈 줄은 블록 끝으로 본다.
            flush_quote()
            continue
        flush_quote()
        if not s.strip():
            continue
        if s.strip() == SCENE_BREAK:
            out.append("<hr />")
        else:
            out.append(f"<p>{inline(s.strip())}</p>")
    flush_quote()
    return "\n".join(out)


def split_title(lines: list[str]) -> tuple[str, list[str]]:
    for index, line in enumerate(lines):
        if line.startswith("# "):
            return line[2:].strip(), lines[index + 1:]
    raise ValueError("제목 줄('# …')이 없다")


def export() -> list[tuple[str, str, int]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT.glob("*.html"):
        stale.unlink()
    rows = []
    for source in sorted(SOURCE.glob("[0-9][0-9][0-9]-*.md")):
        title, body_lines = split_title(source.read_text(encoding="utf-8").splitlines())
        body = convert(body_lines)
        (OUTPUT / f"{source.stem}.html").write_text(body + "\n", encoding="utf-8", newline="\n")
        words = len(re.findall(r"[A-Za-z0-9’']+", re.sub(r"<[^>]+>", " ", body)))
        rows.append((source.stem, title, words))
    # AO3가 'Chapter N'을 자동으로 붙이므로 제목 칸에는 'Chapter N:'을 뺀 이름을 넣는다. 프롤로그를 1회차로 올리면 AO3 번호는 한 칸씩 밀린다.
    lines = ["AO3 'Chapter Title' 칸에 넣을 제목 / 영어 단어 수", ""]
    lines += [f"{stem}\t{re.sub(r'^Chapter \d+:\s*', '', title)}\t{words}words" for stem, title, words in rows]
    (OUTPUT / "_titles.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return rows


if __name__ == "__main__":
    print(f"ao3 html files={len(export())} -> {OUTPUT.relative_to(ROOT)}")
