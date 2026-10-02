"""전용 연습 폴더의 Stop 훅. 외부 전송을 허가하는 검사가 아니다."""
import json
import sys
from pathlib import Path
from check_report import check


def main():
    event = json.load(sys.stdin)
    # 한 차례 보완 이후에는 계속 붙잡지 않는다. 미달 결과는 사람이 확인한다.
    if event.get("stop_hook_active"):
        return
    draft = Path(__file__).resolve().parent / "reports" / "draft.md"
    try:
        failures = check(draft.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        failures = ["reports/draft.md를 읽을 수 없음"]
    if failures:
        print(json.dumps({
            "decision": "block",
            "reason": "형식 검사 미달: " + "; ".join(failures)
                      + ". 원문에 있는 내용만 보완하세요. 원문이 부족하면 확인을 요청하고,"
                      + " 최종본 저장이나 외부 전송은 하지 마세요."
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
