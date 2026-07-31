import json
import shutil
from pathlib import Path

import pandas as pd


def save_json_report(results: list, file_path: Path) -> None:
    file_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_rule_status(rule_validation: dict) -> str:
    if "rule_status" in rule_validation:
        return str(rule_validation["rule_status"])
    if "keyword_found" in rule_validation:
        return "PASS" if rule_validation["keyword_found"] else "FAIL"
    return "CHECK"


def _results_to_rows(results: list) -> list:
    """결과 리스트를 CSV/요약 통계에 공용으로 쓸 평평한(flat) 행 리스트로 변환합니다."""
    rows = []
    for result in results:
        for model_type in ["rule_based", "api_based"]:
            model_result = result[model_type]
            evaluation = model_result["evaluation"]
            rule_validation = model_result["rule_validation"]
            rows.append({
                "case_id":                result["case_id"],
                "category":               result["category"],
                "test_type":              result["test_type"],
                "model_type":             model_type,
                "user_question":          result["user_question"],
                "ai_answer":              model_result["answer"],
                "rule_status":            get_rule_status(rule_validation),
                "accuracy_score":         evaluation["accuracy"]["score"],
                "groundedness_score":     evaluation["groundedness"]["score"],
                "helpfulness_score":      evaluation["helpfulness"]["score"],
                "safety_score":           evaluation["safety"]["score"],
                "understandability_score": evaluation.get("understandability", {}).get("score", 0),
                "total_score":            evaluation.get("total_score", 0),
                "overall_decision":       evaluation["overall_decision"],
                "summary":                evaluation["summary"],
            })
    return rows


def save_csv_report(results: list, file_path: Path) -> None:
    pd.DataFrame(_results_to_rows(results)).to_csv(file_path, index=False, encoding="utf-8-sig")


# ---------------------------------------------------------------------------
# 마크다운 리포트에서 PASS/REVIEW/FAIL을 시각적으로 구분하기 위한 색상 배지.
# PASS=파랑, REVIEW=노랑, FAIL=빨강 (요청에 따른 색상 매핑).
# ---------------------------------------------------------------------------
DECISION_BADGE_STYLES = {
    "PASS":   ("#2563eb", "#ffffff"),
    "REVIEW": ("#eab308", "#3f2d03"),
    "FAIL":   ("#dc2626", "#ffffff"),
}


def decision_badge(decision: str) -> str:
    bg, fg = DECISION_BADGE_STYLES.get(decision, ("#6b7280", "#ffffff"))
    return (
        f'<span style="display:inline-block;background:{bg};color:{fg};'
        f'padding:3px 12px;border-radius:999px;font-weight:700;font-size:0.95em;">'
        f'{decision}</span>'
    )


# 테스트 유형(Happy/Edge/Negative) 구분용 파스텔톤 배지.
# 판정 배지(진한 원색)와 대비되도록 채도를 낮춘 파스텔 색을 사용한다.
TEST_TYPE_BADGE_STYLES = {
    "Happy":    ("#d1fae5", "#065f46"),  # 파스텔 그린
    "Edge":     ("#fde8cc", "#92400e"),  # 파스텔 피치/오렌지
    "Negative": ("#fbcfe8", "#9d174d"),  # 파스텔 핑크
}


def test_type_badge(test_type: str) -> str:
    bg, fg = TEST_TYPE_BADGE_STYLES.get(test_type, ("#e5e7eb", "#374151"))
    return (
        f'<span style="display:inline-block;background:{bg};color:{fg};'
        f'padding:3px 12px;border-radius:999px;font-weight:700;font-size:0.95em;">'
        f'{test_type}</span>'
    )


SCORE_COLS_MD = ["accuracy_score", "groundedness_score", "helpfulness_score", "safety_score", "understandability_score"]
AXIS_LABELS_MD = {
    "accuracy_score": "정확성", "groundedness_score": "근거성", "helpfulness_score": "유용성",
    "safety_score": "안전성", "understandability_score": "이해가능성",
}
MODEL_LABELS_MD = {"rule_based": "규칙 기반 챗봇", "api_based": "API 기반 챗봇"}

TEST_TYPE_ORDER = ["Happy", "Edge", "Negative"]


def wrap_details(body_lines: list) -> list:
    """큰 번호(## N.) 제목은 항상 보이게 두고, 그 아래 본문만 접었다 펼치는 형태로 감싼다.
    <summary> 뒤에는 표/리스트가 마크다운으로 정상 렌더링되도록 빈 줄을 둔다."""
    return ["<details>", "", "<summary> </summary>", ""] + body_lines + ["", "</details>", ""]


def save_markdown_report(results: list, file_path: Path) -> None:
    lines = ["# AI 챗봇 품질관리 최종 비교 보고서", ""]

    # -----------------------------------------------------------------
    # 1. 평가 목적
    # -----------------------------------------------------------------
    lines.append("## 1. 평가 목적")
    lines.append("")
    lines.append("### 규칙 기반 챗봇과 API 기반 챗봇의 품질을 동일한 테스트 케이스로 비교 평가합니다.")
    lines.append("")

    # -----------------------------------------------------------------
    # 2. 비교 결과
    # -----------------------------------------------------------------
    section2 = [
        "| 테스트 ID | 유형 | 규칙 기반 판정 | API 기반 판정 |",
        "|---|---|---|---|",
    ]
    for result in results:
        section2.append(
            f"| **{result['case_id']}** | "
            f"{test_type_badge(result['test_type'])} | "
            f"{decision_badge(result['rule_based']['evaluation']['overall_decision'])} | "
            f"{decision_badge(result['api_based']['evaluation']['overall_decision'])} |"
        )
    lines.append("## 2. 비교 결과")
    lines.append("")
    lines.extend(wrap_details(section2))

    # -----------------------------------------------------------------
    # 3. 케이스별 상세 비교
    # -----------------------------------------------------------------
    section3 = []
    for i, result in enumerate(results, start=1):
        def score_line(ev: dict) -> str:
            return (
                f"정확성 {ev['accuracy']['score']} | "
                f"근거성 {ev['groundedness']['score']} | "
                f"유용성 {ev['helpfulness']['score']} | "
                f"안전성 {ev['safety']['score']} | "
                f"이해성 {ev.get('understandability', {}).get('score', 0)} | "
                f"합계 {ev.get('total_score', 0)}/25"
            )

        rb_ev = result['rule_based']['evaluation']
        ab_ev = result['api_based']['evaluation']

        # 케이스마다 번호 매긴 제목(3.1, 3.2, ...)으로 구분해 접지 않고 바로 펼쳐 보이게 한다.
        heading_label = (
            f"{result['case_id']} · {result['test_type']} · {result['category']} · "
            f"규칙기반 {rb_ev['overall_decision']} / API기반 {ab_ev['overall_decision']}"
        )
        section3.extend([
            f"### 3.{i} {heading_label}",
            "",
            f"- 사용자 질문: {result['user_question']}",
            "",
            "#### 규칙 기반 챗봇",
            f"- 답변: {result['rule_based']['answer']}",
            f"- 규칙 점검: {get_rule_status(result['rule_based']['rule_validation'])}",
            f"- 점수: {score_line(rb_ev)}",
            f"- 종합 판정: {decision_badge(rb_ev['overall_decision'])}",
            f"- 평가 의견: {rb_ev['summary']}",
            "",
            "#### API 기반 챗봇",
            f"- 답변: {result['api_based']['answer']}",
            f"- 규칙 점검: {get_rule_status(result['api_based']['rule_validation'])}",
            f"- 점수: {score_line(ab_ev)}",
            f"- 종합 판정: {decision_badge(ab_ev['overall_decision'])}",
            f"- 평가 의견: {ab_ev['summary']}",
            "",
        ])
    lines.append("## 3. 케이스별 상세 비교")
    lines.append("")
    lines.extend(wrap_details(section3))

    # -----------------------------------------------------------------
    # 4. 종합 요약 — flat 행 데이터를 집계해 표를 자동 생성
    # -----------------------------------------------------------------
    df = pd.DataFrame(_results_to_rows(results))

    total_cases = df["case_id"].nunique()
    total_rows = len(df)
    overall_pass = int((df["overall_decision"] == "PASS").sum())
    overall_review = int((df["overall_decision"] == "REVIEW").sum())
    overall_fail = int((df["overall_decision"] == "FAIL").sum())
    overall_pass_rate = round(overall_pass / total_rows * 100, 1) if total_rows else 0.0
    overall_avg_total = round(df["total_score"].mean(), 2) if total_rows else 0.0

    model_stats = {}
    for model_type, g in df.groupby("model_type"):
        n = len(g)
        model_stats[model_type] = {
            "n": n,
            "pass": int((g["overall_decision"] == "PASS").sum()),
            "review": int((g["overall_decision"] == "REVIEW").sum()),
            "fail": int((g["overall_decision"] == "FAIL").sum()),
            "pass_rate": round((g["overall_decision"] == "PASS").sum() / n * 100, 1) if n else 0.0,
            "avg_total": round(g["total_score"].mean(), 2) if n else 0.0,
            "axis_avg": {c: round(g[c].mean(), 2) for c in SCORE_COLS_MD},
        }

    test_type_stats = {}
    for test_type, g in df.groupby("test_type"):
        n = len(g)
        test_type_stats[test_type] = {
            "n": n,
            "pass": int((g["overall_decision"] == "PASS").sum()),
            "review": int((g["overall_decision"] == "REVIEW").sum()),
            "fail": int((g["overall_decision"] == "FAIL").sum()),
            "pass_rate": round((g["overall_decision"] == "PASS").sum() / n * 100, 1) if n else 0.0,
            "avg_total": round(g["total_score"].mean(), 2) if n else 0.0,
            "axis_avg": {c: round(g[c].mean(), 2) for c in SCORE_COLS_MD},
        }
    ordered_test_types = [t for t in TEST_TYPE_ORDER if t in test_type_stats] + \
        [t for t in test_type_stats if t not in TEST_TYPE_ORDER]

    section4 = [f"- 전체 테스트 케이스: **{total_cases}건** (모델 2종 × 케이스 → 평가 행 {total_rows}건)"]
    section4.append(
        f"- 전체 판정 분포: {decision_badge('PASS')} {overall_pass}건 · "
        f"{decision_badge('REVIEW')} {overall_review}건 · "
        f"{decision_badge('FAIL')} {overall_fail}건 (통과율 {overall_pass_rate}%)"
    )
    section4.append(f"- 전체 평균 종합점수: **{overall_avg_total} / 25**")
    section4.append("")

    section4.append("| 모델 | 케이스 | PASS | REVIEW | FAIL | 통과율 | 평균 종합점수 |")
    section4.append("|---|---|---|---|---|---|---|")
    for model_type in ["rule_based", "api_based"]:
        s = model_stats.get(model_type)
        if not s:
            continue
        section4.append(
            f"| {MODEL_LABELS_MD[model_type]} | {s['n']} | {s['pass']} | {s['review']} | {s['fail']} | "
            f"{s['pass_rate']}% | {s['avg_total']} / 25 |"
        )
    section4.append("")

    if "rule_based" in model_stats and "api_based" in model_stats:
        rb_rate = model_stats["rule_based"]["pass_rate"]
        ab_rate = model_stats["api_based"]["pass_rate"]
        if ab_rate > rb_rate:
            section4.append(
                f"- API 기반 챗봇이 규칙 기반 챗봇보다 통과율이 **{round(ab_rate - rb_rate, 1)}%p 높아** "
                "전반적으로 더 우수한 응답 품질을 보였습니다."
            )
        elif rb_rate > ab_rate:
            section4.append(
                f"- 규칙 기반 챗봇이 API 기반 챗봇보다 통과율이 **{round(rb_rate - ab_rate, 1)}%p 높아** "
                "전반적으로 더 우수한 응답 품질을 보였습니다."
            )
        else:
            section4.append("- 두 모델의 통과율이 동일하여 우열을 가리기 어렵습니다.")
    section4.append("")

    axis_header = " | ".join(AXIS_LABELS_MD[c] for c in SCORE_COLS_MD)
    section4.append(f"| 모델 | {axis_header} |")
    section4.append("|---|" + "---|" * len(SCORE_COLS_MD))
    for model_type in ["rule_based", "api_based"]:
        s = model_stats.get(model_type)
        if not s:
            continue
        scores = " | ".join(str(s["axis_avg"][c]) for c in SCORE_COLS_MD)
        section4.append(f"| {MODEL_LABELS_MD[model_type]} | {scores} |")
    section4.append("")

    # 테스트 유형별 항목 평균 점수
    section4.append("**테스트 유형별 항목 평균 점수**")
    section4.append("")
    section4.append(f"| 테스트 유형 | 평가 행 | {axis_header} | 평균 종합점수 |")
    section4.append("|---|---|" + "---|" * len(SCORE_COLS_MD) + "---|")
    for test_type in ordered_test_types:
        s = test_type_stats[test_type]
        scores = " | ".join(str(s["axis_avg"][c]) for c in SCORE_COLS_MD)
        section4.append(
            f"| {test_type_badge(test_type)} | {s['n']} | {scores} | {s['avg_total']} / 25 |"
        )
    section4.append("")

    # 테스트 유형별 판정 분포
    section4.append("**테스트 유형별 판정 분포**")
    section4.append("")
    section4.append("| 테스트 유형 | 평가 행 | PASS | REVIEW | FAIL | 통과율 |")
    section4.append("|---|---|---|---|---|---|")
    for test_type in ordered_test_types:
        s = test_type_stats[test_type]
        section4.append(
            f"| {test_type_badge(test_type)} | {s['n']} | {s['pass']} | {s['review']} | {s['fail']} | {s['pass_rate']}% |"
        )

    lines.append("## 4. 종합 요약")
    lines.append("")
    lines.extend(wrap_details(section4))

    file_path.write_text("\n".join(lines), encoding="utf-8")


def generate_all(results: list, reports_dir: Path, log_dir: Path, timestamp: str) -> None:
    log_json = log_dir / f"{timestamp}_evaluation_result.json"
    log_csv  = log_dir / f"{timestamp}_evaluation_result.csv"
    log_md   = log_dir / f"{timestamp}_final_quality_report.md"

    save_json_report(results, log_json)
    save_csv_report(results, log_csv)
    save_markdown_report(results, log_md)

    latest_json = reports_dir / "evaluation_result.json"
    latest_csv  = reports_dir / "evaluation_result.csv"
    latest_md   = reports_dir / "final_quality_report.md"

    shutil.copy2(log_json, latest_json)
    shutil.copy2(log_csv, latest_csv)
    shutil.copy2(log_md, latest_md)

    print(f"  JSON    → {log_json} (최신본 → {latest_json})")
    print(f"  CSV     → {log_csv} (최신본 → {latest_csv})")
    print(f"  Markdown→ {log_md} (최신본 → {latest_md})")


if __name__ == "__main__":
    # OpenAI API를 다시 호출하지 않고, reports/evaluation_result.json에 저장된
    # 기존 평가 결과만 다시 읽어 CSV/Markdown을 재생성한다.
    # (리포트 서식만 바뀌었을 때 전체 파이프라인(main.py)을 재실행할 필요가 없도록 하기 위함)
    from config import REPORTS_DIR

    existing_json = REPORTS_DIR / "evaluation_result.json"
    if not existing_json.exists():
        raise SystemExit(
            f"{existing_json} 파일이 없습니다. 먼저 `python main.py`를 한 번 실행해 "
            "평가 결과를 생성한 뒤 다시 시도하세요."
        )

    existing_results = json.loads(existing_json.read_text(encoding="utf-8"))
    save_json_report(existing_results, REPORTS_DIR / "evaluation_result.json")
    save_csv_report(existing_results, REPORTS_DIR / "evaluation_result.csv")
    save_markdown_report(existing_results, REPORTS_DIR / "final_quality_report.md")
    print("\n기존 평가 결과(JSON)를 바탕으로 리포트를 재생성했습니다. (OpenAI API 재호출 없음, log/ 에는 남기지 않음)")
