import json
from pathlib import Path

from config import DATA_DIR, REPORT_DIR, validate_config
from judge_agent import get_evaluation_from_openai
from report_generator import (
    save_csv_report,
    save_json_report,
    save_markdown_report
)
from rule_based_agent import get_answer_from_rule_based_agent
from rule_validator import validate_by_rules
from service_agent import get_answer_from_api_agent


TEST_CASE_FILE = DATA_DIR / "test_cases.json"

JSON_REPORT_FILE = REPORT_DIR / "evaluation_result.json"
CSV_REPORT_FILE = REPORT_DIR / "evaluation_result.csv"
MARKDOWN_REPORT_FILE = REPORT_DIR / "final_quality_report.md"


def load_test_cases(file_path: Path) -> list:
    return json.loads(
        file_path.read_text(encoding="utf-8")
    )


def create_error_evaluation(error: Exception) -> dict:
    return {
        "accuracy": {
            "score": 0,
            "reason": "평가 API 호출 실패"
        },
        "groundedness": {
            "score": 0,
            "reason": "평가 API 호출 실패"
        },
        "helpfulness": {
            "score": 0,
            "reason": "평가 API 호출 실패"
        },
        "safety": {
            "score": 0,
            "reason": "평가 API 호출 실패"
        },
        "overall_decision": "FAIL",
        "summary": f"평가 중 오류 발생: {error}"
    }


def evaluate_answer(
    user_question: str,
    ai_answer: str,
    expected_keyword: str,
    expected_policy: str
) -> dict:
    rule_validation = validate_by_rules(
        user_question=user_question,
        ai_answer=ai_answer,
        expected_keyword=expected_keyword
    )

    try:
        evaluation = get_evaluation_from_openai(
            user_question=user_question,
            ai_answer=ai_answer,
            expected_policy=expected_policy
        )
    except Exception as error:
        evaluation = create_error_evaluation(error)

    return {
        "answer": ai_answer,
        "rule_validation": rule_validation,
        "evaluation": evaluation
    }


def run_pipeline() -> None:
    validate_config()

    test_cases = load_test_cases(TEST_CASE_FILE)
    final_results = []

    for test_case in test_cases:
        case_id = test_case["case_id"]
        category = test_case["category"]
        test_type = test_case["test_type"]
        user_question = test_case["user_question"]
        expected_keyword = test_case["expected_keyword"]
        expected_policy = test_case["expected_policy"]

        print(f"\n[{case_id}] 테스트 시작")

        rule_based_answer = get_answer_from_rule_based_agent(
            user_question
        )

        api_based_answer = get_answer_from_api_agent(
            user_question
        )

        rule_based_result = evaluate_answer(
            user_question=user_question,
            ai_answer=rule_based_answer,
            expected_keyword=expected_keyword,
            expected_policy=expected_policy
        )

        api_based_result = evaluate_answer(
            user_question=user_question,
            ai_answer=api_based_answer,
            expected_keyword=expected_keyword,
            expected_policy=expected_policy
        )

        final_results.append(
            {
                "case_id": case_id,
                "category": category,
                "test_type": test_type,
                "user_question": user_question,
                "rule_based": rule_based_result,
                "api_based": api_based_result
            }
        )

    save_json_report(final_results, JSON_REPORT_FILE)
    save_csv_report(final_results, CSV_REPORT_FILE)
    save_markdown_report(final_results, MARKDOWN_REPORT_FILE)

    print("\nAI 챗봇 비교 품질평가 완료")
    print(f"JSON 결과: {JSON_REPORT_FILE}")
    print(f"CSV 결과: {CSV_REPORT_FILE}")
    print(f"Markdown 보고서: {MARKDOWN_REPORT_FILE}")


if __name__ == "__main__":
    run_pipeline()