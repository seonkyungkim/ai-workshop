"""교육용 Markdown 형식 검사. 사실 여부는 원문과 별도로 대조한다."""
import re
import sys
from datetime import datetime
from pathlib import Path


def check(text):
    lines = text.strip().splitlines()
    failures = []
    title = re.fullmatch(r"# ([0-9]{8})_(\S.*)", lines[0]) if lines else None
    try:
        if not title:
            raise ValueError()
        datetime.strptime(title[1], "%Y%m%d")
    except ValueError:
        failures.append("제목: # YYYYMMDD_주제와 실제 날짜 필요")

    expected = ["한 일", "다음 주 계획", "이슈"]
    sections = {}
    current = None
    for line in lines[1:]:
        if line.startswith("## "):
            current = line[3:].strip()
            if current not in expected or current in sections:
                failures.append("알 수 없거나 중복된 절: " + current)
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
        elif line.strip():
            failures.append("절 밖의 본문")

    def content(name):
        # 목록 기호나 공백만 있는 칸은 내용으로 세지 않는다.
        return "\n".join(re.sub(r"^\s*[-*+]\s*", "", s).strip()
                         for s in sections.get(name, [])).strip()

    for name in expected:
        if not re.search(r"[가-힣A-Za-z0-9]", content(name)):
            failures.append("빈 칸 또는 누락: " + name)
    if not re.search(r"[0-9]", content("한 일")):
        failures.append("한 일에 숫자 없음")
    return failures


def main():
    if len(sys.argv) != 2:
        print("사용법: python3 check_report.py 보고서.md", file=sys.stderr)
        return 2
    try:
        failures = check(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 2
    print("PASS" if not failures else "FAIL: " + "; ".join(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
