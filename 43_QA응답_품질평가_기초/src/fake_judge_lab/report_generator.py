import csv
import json
from dataclasses import asdict
from pathlib import Path

from evaluator import EvaluationResult


def save_reports(
    results: list[EvaluationResult],
    output_dir: str = "reports",
) -> dict[str, Path]:
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "evaluation_result.json"
    csv_path = report_dir / "evaluation_result.csv"
    md_path = report_dir / "evaluation_report.md"

    json_path.write_text(
        json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["case_id", "answer_name", "score", "verdict", "reason"]
        )
        for result in results:
            writer.writerow(
                [
                    result.case_id,
                    result.answer_name,
                    result.score,
                    result.verdict,
                    result.reason,
                ]
            )

    lines = [
        "# 가짜 Judge 자동 평가 보고서",
        "",
        "| 사례 | 답변 | 점수 | 판정 | 평가 근거 |",
        "|---|---|---:|---|---|",
    ]

    for result in results:
        lines.append(
            f"| {result.case_id} | {result.answer_name} | "
            f"{result.score} | {result.verdict} | {result.reason} |"
        )

    lines.extend(["", "## 세부 평가"])

    for result in results:
        lines.extend(
            [
                "",
                f"### {result.answer_name}",
                "",
                "| 평가항목 | 점수 |",
                "|---|---:|",
            ]
        )
        for criterion, score in result.criteria.items():
            lines.append(f"| {criterion} | {score} / 5 |")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "json": json_path,
        "csv": csv_path,
        "markdown": md_path,
    }
