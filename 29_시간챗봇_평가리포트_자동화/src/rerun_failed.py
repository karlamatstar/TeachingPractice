import csv
import logging
from pathlib import Path

from dotenv import load_dotenv

from run_tests import run_one_case, save_csv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "_OUTPUT"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

load_dotenv(PROJECT_DIR / ".env")


def load_failed_cases(path: str = OUTPUT_DIR / "test_results" / "test_results.csv") -> list:
    rows = csv.DictReader(Path(path).open(encoding="utf-8-sig"))
    return [row for row in rows if row["pass_fail"] == "FAIL"]


def rerun_failed(input_path: str = OUTPUT_DIR / "test_results" / "test_results.csv", output_path: str = OUTPUT_DIR / "test_results" / "retest_results.csv") -> list:
    failed_cases = load_failed_cases(input_path)
    rows = []

    logging.info(f"FAIL 케이스 재테스트를 시작합니다. (총 {len(failed_cases)}개)")

    for case in failed_cases:
        case_id = case["case_id"]
        logging.info(f"[{case_id}] 재실행 중...")

        row = run_one_case(
            case_id=case_id,
            test_type=case["type"],
            user_question=case["user_question"],
            expected_result=case["expected_result"],
            group=case.get("group", ""),
        )
        rows.append(row)
        logging.info(f"  -> {row['pass_fail']} (총점 {row['total_score']}/25, 결함위치: {row['defect_location']})")

    save_csv(rows, output_path)

    passed = sum(1 for row in rows if row["pass_fail"] == "PASS")
    logging.info(f"\n재테스트 완료: {passed}/{len(rows)} PASS")
    logging.info(f"{output_path} 파일이 생성되었습니다.")

    return rows


if __name__ == "__main__":
    rerun_failed()
