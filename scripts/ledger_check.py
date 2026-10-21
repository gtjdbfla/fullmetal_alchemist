"""Check that the foreshadowing ledger matches what is actually on the page.

Each foreshadowing item may carry `verify`: a list of {"chapter": N, "term": "..."}.
The term must appear in that chapter's manuscript (43 = epilogue). The ledger is
also checked for status/payoff consistency.

Run:  python scripts/ledger_check.py      (exit code 1 on problems)
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "private" / "dashboard-config.json"
STATUSES = {"PLANTED", "REINFORCED", "PARTIALLY_REVEALED", "PAYOFF", "UNRESOLVED_BY_DESIGN", "OPEN_BY_DESIGN"}


def chapter_text(number: int) -> str:
    files = glob.glob(str(ROOT / "manuscripts" / "current" / f"{number:03d}-*.md"))
    if not files:
        return ""
    return Path(files[0]).read_text(encoding="utf-8")


def check(config: dict) -> list[str]:
    problems: list[str] = []
    for item in config["storyBible"]["foreshadowing"]:
        fid = item["id"]
        status = item.get("status")
        if status not in STATUSES:
            problems.append(f"{fid}: 알 수 없는 상태 {status}")
        payoff = item.get("payoff", "")
        if status == "PAYOFF" and (not payoff or "미정" in payoff or "예정" in payoff):
            problems.append(f"{fid}: PAYOFF인데 회수 내용이 비었거나 미정/예정이다")
        if status in {"PLANTED", "REINFORCED"} and "회수 완료" in payoff:
            problems.append(f"{fid}: {status}인데 회수 완료라고 적혀 있다")
        if status in {"UNRESOLVED_BY_DESIGN", "OPEN_BY_DESIGN"} and "의도" not in payoff and "열어" not in payoff:
            problems.append(f"{fid}: {status}인데 회수 내용에 의도/열어 둠 설명이 없다")
        for check_ in item.get("verify", []):
            text = chapter_text(check_["chapter"])
            if not text:
                problems.append(f"{fid}: {check_['chapter']}화 원고를 찾을 수 없다")
            elif check_["term"] not in text:
                problems.append(f"{fid}: {check_['chapter']}화에 '{check_['term']}'이(가) 없다")
    return problems


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    problems = check(config)
    total = len(config["storyBible"]["foreshadowing"])
    verified = sum(1 for i in config["storyBible"]["foreshadowing"] if i.get("verify"))
    if problems:
        print(f"ledger problems={len(problems)} (items={total}, verified={verified})")
        for line in problems:
            print(" -", line)
        return 1
    print(f"ledger ok: items={total}, verified={verified}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
