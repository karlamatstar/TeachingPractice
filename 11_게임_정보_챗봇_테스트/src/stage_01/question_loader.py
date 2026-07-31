
# 게임 가챠 테스트 케이스 로더

import json
from pathlib import Path


REQUIRED_FIELDS = [
    "TC_ID",
    "품질지표",
    "유형",
    "난이도",
    "질문",
    "기대결과"
]

OPTIONAL_FIELDS = [
    "검색형태",
    "검증주요요소"
]


def validate_testcase(tc: dict, line_no: int) -> bool:
    """
    테스트케이스 필수 컬럼 검증
    """

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in tc
    ]

    if missing_fields:
        print(
            f"[WARNING] Line {line_no} "
            f"누락 필수 컬럼: {missing_fields}"
        )
        return False

    return True


def load_testcases(file_path: Path | str) -> list[dict]:
    """
    JSONL 파일 로드

    Returns:
        List[dict]
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"파일이 존재하지 않습니다.\n{file_path}"
        )

    testcases = []

    with open(
        file_path,
        mode="r",
        encoding="utf-8"
    ) as f:

        for line_no, line in enumerate(
            f,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                tc = json.loads(line)

                if validate_testcase(
                    tc,
                    line_no
                ):
                    testcases.append(tc)

            except json.JSONDecodeError as e:

                print(
                    f"[ERROR] JSON 파싱 실패 "
                    f"(Line {line_no})"
                )

                print(str(e))

    print(
        f"[INFO] "
        f"{len(testcases)}건 로드 완료"
    )

    return testcases


if __name__ == "__main__":

    sample_path = Path(__file__).resolve().parent / "Input" / "testcases_questions.jsonl"

    tcs = load_testcases(sample_path)

    print(f"총 {len(tcs)}건")
