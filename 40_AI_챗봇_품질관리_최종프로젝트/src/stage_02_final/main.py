import json
import sys
from datetime import datetime
from pathlib import Path

from config import DATA_DIR, LOG_DIR, REPORTS_DIR, validate_config
from judge_agent import get_evaluation_from_openai
from report_generator import generate_all
from rule_based_agent import get_answer_from_rule_based_agent
from rule_validator import validate_by_rules
from service_agent import get_answer_from_api_agent

TEST_CASE_FILE = DATA_DIR / "test_cases.json"


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data: str) -> None:
        for stream in self.streams:
            stream.write(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def load_test_cases(file_path: Path) -> list:
    return json.loads(file_path.read_text(encoding="utf-8"))


def create_error_evaluation(error: Exception) -> dict:
    return {
        "accuracy":          {"score": 0, "reason": "평가 API 호출 실패"},
        "groundedness":      {"score": 0, "reason": "평가 API 호출 실패"},
        "helpfulness":       {"score": 0, "reason": "평가 API 호출 실패"},
        "safety":            {"score": 0, "reason": "평가 API 호출 실패"},
        "understandability": {"score": 0, "reason": "평가 API 호출 실패"},
        "total_score": 0,
        "overall_decision": "FAIL",
        "summary": f"평가 중 오류 발생: {error}",
    }


def format_score_line(evaluation: dict) -> str:
    return (
        f"{evaluation['overall_decision']} "
        f"[정확성 {evaluation['accuracy']['score']} | "
        f"근거성 {evaluation['groundedness']['score']} | "
        f"유용성 {evaluation['helpfulness']['score']} | "
        f"안전성 {evaluation['safety']['score']} | "
        f"이해성 {evaluation['understandability']['score']} | "
        f"합계 {evaluation['total_score']}/25]"
    )


def evaluate_answer(
    user_question: str,
    ai_answer: str,
    expected_keyword: str,
    expected_policy: str,
    agent_label: str = "",
) -> dict:
    rule_validation = validate_by_rules(
        user_question=user_question,
        ai_answer=ai_answer,
        expected_keyword=expected_keyword,
    )
    try:
        evaluation = get_evaluation_from_openai(
            user_question=user_question,
            ai_answer=ai_answer,
            expected_policy=expected_policy,
            agent_label=agent_label,
        )
    except Exception as error:
        evaluation = create_error_evaluation(error)

    return {
        "answer": ai_answer,
        "rule_validation": rule_validation,
        "evaluation": evaluation,
    }


def run_pipeline(timestamp: str) -> None:
    validate_config()

    test_cases = load_test_cases(TEST_CASE_FILE)
    final_results = []

    print(f"\n{'='*50}")
    print(f"  AI 챗봇 비교 품질평가 파이프라인 시작 (총 {len(test_cases)}개)")
    print(f"{'='*50}\n")

    for tc in test_cases:
        case_id        = tc["case_id"]
        user_question  = tc["user_question"]
        expected_keyword = tc["expected_keyword"]
        expected_policy  = tc["expected_policy"]

        print(f"\n[{case_id}] 테스트 시작")

        rule_based_answer = get_answer_from_rule_based_agent(user_question)
        api_based_answer  = get_answer_from_api_agent(user_question)

        rule_based_result = evaluate_answer(
            user_question, rule_based_answer, expected_keyword, expected_policy,
            agent_label="규칙 기반",
        )
        api_based_result = evaluate_answer(
            user_question, api_based_answer, expected_keyword, expected_policy,
            agent_label="API 기반",
        )

        print(f"  규칙 기반: {format_score_line(rule_based_result['evaluation'])}")
        print(f"  API 기반: {format_score_line(api_based_result['evaluation'])}")

        final_results.append({
            "case_id":       case_id,
            "category":      tc["category"],
            "test_type":     tc["test_type"],
            "user_question": user_question,
            "rule_based":    rule_based_result,
            "api_based":     api_based_result,
        })

    print(f"\n{'='*50}")
    print("  리포트 생성 중...")
    generate_all(final_results, REPORTS_DIR, LOG_DIR, timestamp)
    print(f"{'='*50}")
    print("  파이프라인 완료")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    LOG_DIR.mkdir(exist_ok=True)
    timestamp = f"{datetime.now():%Y%m%d_%H%M%S}"
    log_file_path = LOG_DIR / f"{timestamp}_log.txt"

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = _Tee(original_stdout, log_file)
        try:
            run_pipeline(timestamp)
        finally:
            sys.stdout = original_stdout

    print(f"  실행 로그 → {log_file_path}")
