import json
import csv
from datetime import datetime
from config import REPORTS_DIR


def save_json(results: list) -> str:
    path = REPORTS_DIR / "evaluation_result.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return str(path)


def save_csv(results: list) -> str:
    path = REPORTS_DIR / "evaluation_result.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "case_id", "category", "test_type",
            "rule_status",
            "accuracy_score", "groundedness_score",
            "helpfulness_score", "safety_score",
            "overall_decision",
        ])
        for r in results:
            ev = r.get("evaluation_result", {})
            rv = r.get("rule_validation", {})
            writer.writerow([
                r["case_id"],
                r["category"],
                r["test_type"],
                rv.get("rule_status", ""),
                ev.get("accuracy", {}).get("score", ""),
                ev.get("groundedness", {}).get("score", ""),
                ev.get("helpfulness", {}).get("score", ""),
                ev.get("safety", {}).get("score", ""),
                ev.get("overall_decision", ""),
            ])
    return str(path)


def save_markdown(results: list) -> str:
    path = REPORTS_DIR / "final_quality_report.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    total = len(results)
    passed = sum(
        1 for r in results
        if r.get("evaluation_result", {}).get("overall_decision") == "PASS"
    )

    lines = [
        "# AI 챗봇 품질 평가 최종 보고서",
        "",
        f"- 평가 일시: {now}",
        f"- 총 케이스: {total}개",
        f"- PASS: {passed}개 / FAIL 또는 REVIEW: {total - passed}개",
        "",
        "---",
        "",
        "## 케이스별 평가 결과",
        "",
        "| case_id | category | rule | acc | grd | hlp | sft | 판정 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for r in results:
        ev = r.get("evaluation_result", {})
        rv = r.get("rule_validation", {})
        lines.append(
            f"| {r['case_id']} | {r['category']} "
            f"| {rv.get('rule_status','')} "
            f"| {ev.get('accuracy',{}).get('score','')} "
            f"| {ev.get('groundedness',{}).get('score','')} "
            f"| {ev.get('helpfulness',{}).get('score','')} "
            f"| {ev.get('safety',{}).get('score','')} "
            f"| {ev.get('overall_decision','')} |"
        )

    lines += ["", "---", "", "## 케이스별 상세 요약", ""]
    for r in results:
        ev = r.get("evaluation_result", {})
        lines += [
            f"### {r['case_id']} — {r['category']}",
            f"- 질문: {r['user_question']}",
            f"- 답변: {r.get('ai_answer', '')}",
            f"- 총평: {ev.get('summary', '')}",
            "",
        ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return str(path)


def generate_all(results: list):
    p1 = save_json(results)
    p2 = save_csv(results)
    p3 = save_markdown(results)
    print(f"  JSON    → {p1}")
    print(f"  CSV     → {p2}")
    print(f"  Markdown→ {p3}")
