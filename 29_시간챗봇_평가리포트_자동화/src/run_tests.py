import csv
import json
import logging
import time
from pathlib import Path

from dotenv import load_dotenv

from chatbot import get_chatbot_answer
from evaluator_agent import get_evaluation
from generate_report import generate_markdown_report

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "_OUTPUT"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

load_dotenv(PROJECT_DIR / ".env")

CSV_FIELDNAMES = [
    "case_id",
    "type",
    "group",
    "user_question",
    "ai_answer",
    "expected_result",
    "accuracy_score",
    "usefulness_score",
    "safety_score",
    "reliability_score",
    "tool_score",
    "total_score",
    "pass_fail",
    "defect_location",
    "response_time_sec",
    "reason",
]


def load_test_cases(path: str = BASE_DIR / "test_cases" / "test_cases.json") -> list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_one_case(case_id: str, test_type: str, user_question: str, expected_result: str, group: str = "") -> dict:
    start = time.perf_counter()
    try:
        result = get_chatbot_answer(user_question)
        ai_answer = result["answer"]
        tool_calls = result["tool_calls"]
        elapsed = round(time.perf_counter() - start, 2)

        evaluation = get_evaluation(test_type, user_question, expected_result, ai_answer, tool_calls)

        return {
            "case_id": case_id,
            "type": test_type,
            "group": group,
            "user_question": user_question,
            "ai_answer": ai_answer,
            "expected_result": expected_result,
            "accuracy_score": evaluation["Accuracy"]["score"],
            "usefulness_score": evaluation["Usefulness"]["score"],
            "safety_score": evaluation["Safety"]["score"],
            "reliability_score": evaluation["Reliability"]["score"],
            "tool_score": evaluation["Tool"]["score"],
            "total_score": evaluation["total_score"],
            "pass_fail": "PASS" if evaluation["pass"] else "FAIL",
            "defect_location": evaluation.get("defect_location", ""),
            "response_time_sec": elapsed,
            "reason": evaluation.get("reason", ""),
        }

    except Exception as error:
        elapsed = round(time.perf_counter() - start, 2)
        logging.error(f"[오류 발생] {case_id}: {error}")
        return {
            "case_id": case_id,
            "type": test_type,
            "group": group,
            "user_question": user_question,
            "ai_answer": "",
            "expected_result": expected_result,
            "accuracy_score": 0,
            "usefulness_score": 0,
            "safety_score": 0,
            "reliability_score": 0,
            "tool_score": 0,
            "total_score": 0,
            "pass_fail": "FAIL",
            "defect_location": "API 결함",
            "response_time_sec": elapsed,
            "reason": f"실행 오류: {error}",
        }


def run_tests(input_path: str = BASE_DIR / "test_cases" / "test_cases.json", output_path: str = OUTPUT_DIR / "test_results" / "test_results.csv") -> list:
    test_cases = load_test_cases(input_path)
    rows = []

    logging.info(f"자동 테스트를 시작합니다. (총 {len(test_cases)}개, 입력: {input_path})")

    for test_case in test_cases:
        case_id = test_case["case_id"]
        logging.info(f"[{case_id}] 실행 중...")

        row = run_one_case(
            case_id=case_id,
            test_type=test_case["type"],
            user_question=test_case["user_question"],
            expected_result=test_case["expected_result"],
            group=test_case.get("group", ""),
        )
        rows.append(row)
        logging.info(f"  -> {row['pass_fail']} (총점 {row['total_score']}/25, 결함위치: {row['defect_location']})")

    save_csv(rows, output_path)

    passed = sum(1 for row in rows if row["pass_fail"] == "PASS")
    logging.info(f"\n테스트 완료: {passed}/{len(rows)} PASS")
    logging.info(f"{output_path} 파일이 생성되었습니다.")

    generate_markdown_report()
    
    return rows


def save_csv(rows: list, output_path: str = OUTPUT_DIR / "test_results" / "test_results.csv") -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    run_tests()
