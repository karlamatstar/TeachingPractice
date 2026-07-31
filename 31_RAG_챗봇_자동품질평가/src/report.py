from pathlib import Path


def score_to_text(value) -> str:
    """점수 값이 없을 때도 오류 없이 출력합니다."""

    if value is None:
        return "-"

    return str(value)


def save_markdown_report(final_report: dict, output_path: str):
    """
    평가 결과를 사람이 읽기 쉬운 Markdown 보고서로 저장합니다.

    final_report 예시:
    {
        "results": [
            {
                "case_id": "RAG-001",
                "category": "정상 질문",
                "user_question": "...",
                "ai_answer": "...",
                "retrieved_sources": [],
                "evaluation": {},
                "correction": {}
            }
        ]
    }
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    results = final_report.get("results", [])

    # ----------------------------
    # 1. 보고서 제목 및 요약
    # ----------------------------
    lines.append("# RAG 챗봇 품질평가 보고서")
    lines.append("")

    created_at = final_report.get("created_at", "")
    if created_at:
        lines.append(f"- 평가 일시: {created_at}")

    lines.append(f"- 총 테스트 건수: {len(results)}")

    valid_scores = []

    for result in results:
        evaluation = result.get("evaluation", {})
        final_score = evaluation.get("final_score")

        if isinstance(final_score, (int, float)):
            valid_scores.append(final_score)

    if valid_scores:
        average_score = sum(valid_scores) / len(valid_scores)
        lines.append(f"- 평균 최종 점수: **{average_score:.2f} / 5.00**")
    else:
        lines.append("- 평균 최종 점수: 계산 불가")

    lines.append("")
    lines.append("---")
    lines.append("")

    rubric_labels = {
        "understanding": "이해도",
        "accuracy": "정확성",
        "relevance": "관련성",
        "expression": "표현성"
    }

    # ----------------------------
    # 2. 테스트 케이스별 상세 결과
    # ----------------------------
    for result in results:
        case_id = result.get("case_id", "CASE-ID 없음")
        category = result.get("category", "분류 없음")
        question = result.get("user_question", "")
        ai_answer = result.get("ai_answer", "")
        sources = result.get("retrieved_sources", [])
        evaluation = result.get("evaluation", {})
        correction = result.get("correction", {})
        error = result.get("error")

        lines.append(f"## {case_id} - {category}")
        lines.append("")

        lines.append("### 사용자 질문")
        lines.append(question)
        lines.append("")

        # 실행 오류가 있으면 나머지 평가는 생략
        if error:
            lines.append("### 실행 오류")
            lines.append("```text")
            lines.append(error)
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue

        lines.append("### RAG 챗봇 답변")
        lines.append(ai_answer)
        lines.append("")

        lines.append("### 검색 출처")

        if sources:
            for source in sources:
                lines.append(f"- {source}")
        else:
            lines.append("- 검색 출처 없음")

        lines.append("")

        # ----------------------------
        # 1단계: 루브릭 평가
        # ----------------------------
        rubric = evaluation.get("rubric_evaluation", {})

        lines.append("### 1단계: 루브릭 평가")
        lines.append("")
        lines.append("| 평가 항목 | 점수 | 평가 근거 |")
        lines.append("|---|---:|---|")

        for key, label in rubric_labels.items():
            item = rubric.get(key, {})

            score = score_to_text(item.get("score"))
            reason = item.get("reason", "-")

            lines.append(
                f"| {label} | {score} | {reason} |"
            )

        lines.append("")

        # ----------------------------
        # 2단계: 감점 평가
        # ----------------------------
        deductions = evaluation.get("deductions", {})

        lines.append("### 2단계: 감점 평가")
        lines.append("")
        lines.append("| 평가 항목 | 감점 | 감점 사유 |")
        lines.append("|---|---:|---|")

        for key, label in rubric_labels.items():
            item = deductions.get(key, {})

            deduction = score_to_text(item.get("deduction"))
            reason = item.get("reason", "-")

            lines.append(
                f"| {label} | {deduction} | {reason} |"
            )

        lines.append("")

        # ----------------------------
        # 3단계: 최종 점수
        # ----------------------------
        final_scores = evaluation.get("final_scores", {})

        lines.append("### 3단계: 최종 항목 점수")
        lines.append("")
        lines.append("| 이해도 | 정확성 | 관련성 | 표현성 |")
        lines.append("|---:|---:|---:|---:|")

        lines.append(
            "| "
            f"{score_to_text(final_scores.get('understanding'))} | "
            f"{score_to_text(final_scores.get('accuracy'))} | "
            f"{score_to_text(final_scores.get('relevance'))} | "
            f"{score_to_text(final_scores.get('expression'))} |"
        )

        lines.append("")

        lines.append(
            "### 최종 점수: "
            f"**{score_to_text(evaluation.get('final_score'))} / 5.00**"
        )

        lines.append("")

        lines.append("### 종합 의견")
        lines.append(
            evaluation.get(
                "overall_comment",
                "종합 의견이 생성되지 않았습니다."
            )
        )

        lines.append("")

        # ----------------------------
        # 4단계: 수정 모범답안
        # ----------------------------
        lines.append("### 수정 모범답안")
        lines.append(
            correction.get(
                "corrected_answer",
                "수정 모범답안이 생성되지 않았습니다."
            )
        )

        lines.append("")

        lines.append("### 수정 이유")
        lines.append(
            correction.get(
                "reason_for_correction",
                "-"
            )
        )

        lines.append("")

        lines.append("### 반영한 개선 사항")

        improvements = correction.get(
            "applied_improvements",
            []
        )

        if improvements:
            for item in improvements:
                lines.append(f"- {item}")
        else:
            lines.append("- 해당 없음")

        lines.append("")
        lines.append("---")
        lines.append("")

    # ----------------------------
    # 3. 파일 저장: 반드시 반복문 밖에서 한 번만 실행
    # ----------------------------
    path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )