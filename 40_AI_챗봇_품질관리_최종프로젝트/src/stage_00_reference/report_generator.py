import json
from pathlib import Path

import pandas as pd


def save_json_report(results: list, file_path: Path) -> None:
    file_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_rule_status(rule_validation: dict) -> str:
    """rule_validator.py의 반환 형식 차이를 안전하게 처리합니다."""

    if "status" in rule_validation:
        return str(rule_validation["status"])

    if "rule_passed" in rule_validation:
        return "PASS" if rule_validation["rule_passed"] else "FAIL"

    if "passed" in rule_validation:
        return "PASS" if rule_validation["passed"] else "FAIL"

    if "keyword_found" in rule_validation:
        return "PASS" if rule_validation["keyword_found"] else "FAIL"

    return "CHECK"


def save_csv_report(results: list, file_path: Path) -> None:
    rows = []

    for result in results:
        for model_type in ["rule_based", "api_based"]:
            model_result = result[model_type]
            evaluation = model_result["evaluation"]
            rule_validation = model_result["rule_validation"]

            rows.append(
                {
                    "case_id": result["case_id"],
                    "category": result["category"],
                    "test_type": result["test_type"],
                    "model_type": model_type,
                    "user_question": result["user_question"],
                    "ai_answer": model_result["answer"],
                    "rule_status": get_rule_status(rule_validation),
                    "accuracy_score": evaluation["accuracy"]["score"],
                    "groundedness_score": evaluation["groundedness"]["score"],
                    "helpfulness_score": evaluation["helpfulness"]["score"],
                    "safety_score": evaluation["safety"]["score"],
                    "overall_decision": evaluation["overall_decision"],
                    "summary": evaluation["summary"],
                }
            )

    pd.DataFrame(rows).to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )


def save_markdown_report(results: list, file_path: Path) -> None:
    lines = [
        "# AI 챗봇 품질관리 최종 비교 보고서",
        "",
        "## 1. 평가 목적",
        "",
        "규칙 기반 챗봇과 API 기반 챗봇의 품질을 동일한 테스트 케이스로 비교 평가합니다.",
        "",
        "## 2. 비교 결과",
        "",
        "| 테스트 ID | 유형 | 규칙 기반 판정 | API 기반 판정 |",
        "|---|---|---|---|"
    ]

    for result in results:
        lines.append(
            f"| {result['case_id']} | "
            f"{result['test_type']} | "
            f"{result['rule_based']['evaluation']['overall_decision']} | "
            f"{result['api_based']['evaluation']['overall_decision']} |"
        )

    lines.extend([
        "",
        "## 3. 케이스별 상세 비교",
        ""
    ])

    for result in results:
        lines.extend([
            f"### {result['case_id']}",
            "",
            f"- 사용자 질문: {result['user_question']}",
            "",
            "#### 규칙 기반 챗봇",
            f"- 답변: {result['rule_based']['answer']}",
            f"- 규칙 점검: {get_rule_status(result['rule_based']['rule_validation'])}",
            f"- 종합 판정: {result['rule_based']['evaluation']['overall_decision']}",
            f"- 평가 의견: {result['rule_based']['evaluation']['summary']}",
            "",
            "#### API 기반 챗봇",
            f"- 답변: {result['api_based']['answer']}",
            f"- 규칙 점검: {get_rule_status(result['api_based']['rule_validation'])}",
            f"- 종합 판정: {result['api_based']['evaluation']['overall_decision']}",
            f"- 평가 의견: {result['api_based']['evaluation']['summary']}",
            ""
        ])

    file_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )