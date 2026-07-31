import json
from config import DATA_DIR
from service_agent import get_answer
from rule_validator import validate
from judge_agent import evaluate
from report_generator import generate_all


def run_pipeline():
    test_cases_path = DATA_DIR / "test_cases.json"
    with open(test_cases_path, encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    total = len(test_cases)

    print(f"\n{'='*50}")
    print(f"  AI 챗봇 품질 평가 파이프라인 시작 (총 {total}개)")
    print(f"{'='*50}\n")

    for i, tc in enumerate(test_cases, 1):
        print(f"[{i}/{total}] {tc['case_id']} — {tc['category']}")

        ai_answer = get_answer(tc["user_question"])
        print(f"  챗봇 답변: {ai_answer[:80]}{'...' if len(ai_answer) > 80 else ''}")

        rule_result = validate(ai_answer, tc["expected_keyword"])
        print(f"  규칙 검증: {rule_result['rule_status']}")

        eval_result = evaluate(tc["user_question"], ai_answer)
        decision = eval_result.get("overall_decision", "?")
        print(f"  AI 평가:  {decision} | {eval_result.get('summary', '')}")

        results.append({
            **tc,
            "ai_answer": ai_answer,
            "rule_validation": rule_result,
            "evaluation_result": eval_result,
        })
        print()

    print(f"{'='*50}")
    print("  리포트 생성 중...")
    generate_all(results)
    print(f"{'='*50}")
    print("  파이프라인 완료")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    run_pipeline()
