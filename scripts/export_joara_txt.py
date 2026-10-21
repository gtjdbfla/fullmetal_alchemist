"""조아라 업로드용 평문 txt를 만든다. 조아라 에디터는 굵게·기울임·취소선·HTML을 받지 않고 프롤로그 지정도 없어서
  - 본문만 담고(제목은 조아라의 제목 칸에 따로 붙여 넣는다)
  - 프롤로그를 1편으로 두고 이후 화를 한 편씩 미룬다(제1화 = 2편)
  - 서식은 export_platform_txt.py와 같은 기호(「」 편지, 『』 수첩, 〈〉 문서, ─── 장면 구분)로 구분한다.
원고 본문은 건드리지 않고 출력만 만든다."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_txt import CONFIG, ROOT  # noqa: E402
from export_platform_txt import convert  # noqa: E402

OUTPUT = ROOT / "publish" / "txt-joara"


def export() -> list[tuple[int, str, int]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT.glob("*.txt"):
        stale.unlink()
    rows = []
    for order, item in enumerate(json.loads(CONFIG.read_text(encoding="utf-8"))["manuscripts"], start=1):
        source = ROOT / item["file"]
        body = convert(source.read_text(encoding="utf-8").strip().splitlines())
        title = f"{item['episode']} {item['title']}"
        (OUTPUT / f"{order:02d}편_{title.replace(' ', '_')}.txt").write_text(body + "\n", encoding="utf-8", newline="\n")
        rows.append((order, title, len(body)))
    lines = ["조아라 제목 칸에 붙여 넣을 제목 (프롤로그가 1편, 제1화가 2편)", ""]
    lines += [f"{order}편\t{title}\t{chars}자" for order, title, chars in rows]
    (OUTPUT / "_제목목록.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return rows


if __name__ == "__main__":
    print(f"txt files={len(export())} -> {OUTPUT.relative_to(ROOT)}")
