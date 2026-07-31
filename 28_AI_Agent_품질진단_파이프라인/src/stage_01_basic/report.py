import json
from datetime import datetime
from pathlib import Path


def save_report(final_results: list, output_path: str = "final_report.json") -> str:
    """평가 결과를 JSON 파일로 저장합니다."""
    Path(output_path).write_text(
        json.dumps(final_results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return output_path


def _to_text(value) -> str:
    """dict, list, 문자열 등 어떤 값도 Markdown에 안전하게 표시합니다."""
    if value is None:
        return "-"

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)

    return str(value)


def save_markdown_report(
    final_results: list,
    output_path: str = "final_report.md"
) -> str:
    """평가 결과를 사람이 읽기 쉬운 Markdown 보고서로 저장합니다."""

    total_count = len(final_results)

    markdown_lines = [
        "# LLM AI 서비스 품질평가 보고서",
        "",
        f"- 생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 총 테스트 케이스 수: {total_count}건",
        "",
        "---",
        "",
        "## 1. 평가 결과 요약",
        "",
        "| 번호 | 테스트 ID | 사용자 질문 | 평가 결과 |",
        "|---:|---|---|---|",
    ]

    for index, result in enumerate(final_results, start=1):
        case_id = result.get("case_id", "-")
        question = result.get("user_question", "-").replace("\n", " ")
        evaluation = _to_text(result.get("evaluation_result", "-"))
        evaluation_one_line = evaluation.replace("\n", " ").replace("|", "/")

        markdown_lines.append(
            f"| {index} | {case_id} | {question} | {evaluation_one_line} |"
        )

    markdown_lines.extend([
        "",
        "---",
        "",
        "## 2. 테스트 케이스별 상세 결과",
        ""
    ])

    for index, result in enumerate(final_results, start=1):
        case_id = result.get("case_id", "-")
        user_question = result.get("user_question", "-")
        ai_answer = result.get("ai_answer", "-")
        evaluation_result = result.get("evaluation_result", "-")
        error_message = result.get("error")

        markdown_lines.extend([
            f"### {index}. {case_id}",
            "",
            "#### 사용자 질문",
            "",
            user_question,
            "",
            "#### AI 답변",
            "",
            ai_answer,
            "",
            "#### 평가 결과",
            "",
            "```json",
            _to_text(evaluation_result),
            "```",
            ""
        ])

        if error_message:
            markdown_lines.extend([
                "#### 오류 내용",
                "",
                "```text",
                str(error_message),
                "```",
                ""
            ])

        markdown_lines.extend([
            "---",
            ""
        ])

    Path(output_path).write_text(
        "\n".join(markdown_lines),
        encoding="utf-8"
    )

    return output_path

