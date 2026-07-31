# RAG 챗봇 답변을 자동 채점하는 Judge 스크립트
# 평가 항목: 정확성, 근거성, 환각여부, 검색성능 (각 1~5점)
# run_test_cases.py 가 만든 logs/test_log_*.json 을 입력으로 사용한다.
import sys
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parents[1]
load_dotenv(PROJECT_DIR / ".env")

LOG_DIR = PROJECT_DIR / "_OUTPUT" / "stage_01"

# 평가 항목 정의 (라벨: 설명)
CRITERIA = {
    "accuracy": ("정확성", "검색된 문서 내용에 비추어 답변이 사실적으로 정확한가"),
    "grounding": ("근거성", "답변이 제공된 문서(context)에 실제로 근거하고 있는가"),
    "hallucination": ("환각여부", "문서에 없는 내용을 지어내지 않았는가 (점수 높을수록 환각 없음)"),
    "retrieval": ("검색성능", "검색된 문서 조각이 질문에 답하기에 충분/적절한가"),
}

PASS_THRESHOLD = 3  # 모든 항목이 이 점수 이상이면 합격


def get_judge_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )


def build_judge_prompt(question, context_items, answer):
    if context_items:
        context = "\n\n".join(
            [
                f"[출처: {item.get('source', '알 수 없음')}]\n{item.get('content', '')}"
                for item in context_items
            ]
        )
    else:
        context = "(검색된 문서 없음)"

    return f"""
당신은 RAG 챗봇의 답변 품질을 채점하는 엄격한 평가자입니다.

아래 [질문], [검색된 문서], [챗봇 답변]을 보고 4개 항목을 각각 1~5점으로 채점하십시오.
반드시 [검색된 문서]에 적힌 내용만을 사실 기준으로 삼으십시오.
당신의 사전 지식이나 추측으로 채점하지 마십시오.

[평가 항목]
- accuracy(정확성): 검색된 문서 내용에 비추어 답변이 사실적으로 정확한가.
- grounding(근거성): 답변이 검색된 문서에 실제로 근거하며 출처를 올바르게 반영하는가.
- hallucination(환각여부): 문서에 없는 내용을 지어내지 않았는가. 환각이 없을수록 높은 점수.
  (문서에 근거가 없을 때 "확인할 수 없습니다"라고 답하면 5점, 없는 내용을 만들어 내면 1점)
- retrieval(검색성능): 검색된 문서 조각이 질문에 답하기에 충분하고 관련성이 높은가.

[점수 기준]
5 = 매우 우수, 4 = 우수, 3 = 보통, 2 = 미흡, 1 = 매우 미흡

[질문]
{question}

[검색된 문서]
{context}

[챗봇 답변]
{answer}

아래 JSON 형식으로만 답하십시오. 다른 텍스트는 출력하지 마십시오.
{{
  "accuracy": {{"score": <1-5>, "reason": "<간단한 근거>"}},
  "grounding": {{"score": <1-5>, "reason": "<간단한 근거>"}},
  "hallucination": {{"score": <1-5>, "reason": "<간단한 근거>"}},
  "retrieval": {{"score": <1-5>, "reason": "<간단한 근거>"}}
}}
"""


def find_latest_log():
    candidates = sorted(LOG_DIR.glob("test_log_*.json"))
    if not candidates:
        raise FileNotFoundError(
            "logs 폴더에 test_log_*.json 이 없습니다. 먼저 run_test_cases.py 를 실행하세요."
        )
    return candidates[-1]


def judge_one(llm, case):
    prompt = build_judge_prompt(
        case.get("user_question", ""),
        case.get("context", []),
        case.get("answer", "")
    )

    response = llm.invoke(prompt)
    evaluation = json.loads(response.content)

    scores = {key: int(evaluation[key]["score"]) for key in CRITERIA}
    reasons = {key: evaluation[key].get("reason", "") for key in CRITERIA}
    passed = all(score >= PASS_THRESHOLD for score in scores.values())

    return scores, reasons, passed


# case_id 안의 평가 항목 / 시나리오 유형 분류 기준
CATEGORY_LABELS = [
    ("Accuracy", "정확성"),
    ("Grounding", "근거성"),
    ("Hallucination", "환각여부"),
    ("Retrieval", "검색성능"),
]

SCENARIO_LABELS = [
    ("Happy", "Happy"),
    ("Edge", "Edge"),
    ("Negative", "Negative"),
]


def count_by_keyword(results, label_pairs):
    # case_id 에 포함된 키워드로 분류하여 (라벨, 개수) 집계
    counts = {label: 0 for _, label in label_pairs}
    for result in results:
        case_id = result.get("case_id", "")
        for keyword, label in label_pairs:
            if keyword in case_id:
                counts[label] += 1
                break
    return counts


def build_distribution_table(title, counts, total):
    lines = [f"### {title}", ""]
    lines.append("| 구분 | 개수 | 비율 |")
    lines.append("|---|---:|---:|")
    for label, count in counts.items():
        percent = (count / total * 100) if total else 0
        lines.append(f"| {label} | {count}건 | {percent:.1f}% |")
    lines.append(f"| 합계 | {sum(counts.values())}건 | 100.0% |")
    lines.append("")

    # 비율을 텍스트 막대그래프로 표현 (100% = 막대 20칸)
    label_width = max(len(label) for label in counts)
    lines.append("```")
    for label, count in counts.items():
        percent = (count / total * 100) if total else 0
        bar = "█" * round(percent / 5)
        lines.append(f"{label.ljust(label_width)} | {bar} {percent:.1f}%")
    lines.append("```")
    lines.append("")
    return lines


def build_evaluation_object(scores, reasons):
    # 평가 결과를 한글 항목명 기준 JSON 객체로 구성한다.
    evaluation = {}
    for key, (label, _) in CRITERIA.items():
        evaluation[label] = {
            "score": scores[key],
            "reason": reasons[key]
        }
    return evaluation


def write_markdown_report(path, results):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# LLM AI 서비스 품질평가 보고서")
    lines.append("")
    lines.append(f"- 생성일시: {created_at}")
    lines.append(f"- 총 테스트 케이스 수: {len(results)}건")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. 평가 결과 요약 표
    lines.append("## 1. 평가 결과 요약")
    lines.append("")
    lines.append("| 번호 | 테스트 ID | 사용자 질문 | 평가 결과 |")
    lines.append("|---:|---|---|---|")

    for index, result in enumerate(results, start=1):
        case_id = result.get("case_id", f"CASE_{index}")
        question = result.get("user_question", "")

        if "scores" in result:
            evaluation = build_evaluation_object(result["scores"], result["reasons"])
            cell = json.dumps(evaluation, ensure_ascii=False)
        else:
            cell = f"[채점 오류] {result.get('error', '')}"

        # 표가 깨지지 않도록 셀 내 줄바꿈/파이프 문자 정리
        question_cell = question.replace("|", "\\|").replace("\n", " ")
        cell = cell.replace("|", "\\|").replace("\n", " ")

        lines.append(f"| {index} | {case_id} | {question_cell} | {cell} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # 2. 테스트 케이스별 상세 결과
    lines.append("## 2. 테스트 케이스별 상세 결과")
    lines.append("")

    for index, result in enumerate(results, start=1):
        case_id = result.get("case_id", f"CASE_{index}")
        question = result.get("user_question", "")
        answer = result.get("answer", "")

        lines.append(f"### {index}. {case_id}")
        lines.append("")
        lines.append("#### 사용자 질문")
        lines.append("")
        lines.append(question)
        lines.append("")
        lines.append("#### AI 답변")
        lines.append("")
        lines.append(answer)
        lines.append("")
        lines.append("#### 평가 결과")
        lines.append("")
        lines.append("```json")
        if "scores" in result:
            evaluation = build_evaluation_object(result["scores"], result["reasons"])
            lines.append(json.dumps(evaluation, ensure_ascii=False, indent=2))
        else:
            lines.append(json.dumps({"error": result.get("error", "")}, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # 3. 결과 요약
    graded = [r for r in results if "scores" in r]
    pass_count = sum(1 for r in graded if r.get("passed"))
    fail_count = len(graded) - pass_count

    lines.append("## 3. 결과 요약")
    lines.append("")
    lines.append(f"- 총 테스트 케이스: {len(results)}건")
    lines.append(f"- 채점 완료: {len(graded)}건")
    lines.append(f"- 합격: {pass_count}건 / 실패: {fail_count}건 "
                 f"(합격 기준: 모든 항목 {PASS_THRESHOLD}점 이상)")
    lines.append("")
    lines.append("### 항목별 평균 점수")
    lines.append("")
    lines.append("| 평가 항목 | 평균 점수 |")
    lines.append("|---|---:|")
    for key, (label, _) in CRITERIA.items():
        avg = (sum(r["scores"][key] for r in graded) / len(graded)) if graded else 0
        lines.append(f"| {label}({key}) | {avg:.2f} |")
    lines.append("")

    # 평가 항목별 / 시나리오 유형별 케이스 분포
    total = len(results)
    category_counts = count_by_keyword(results, CATEGORY_LABELS)
    scenario_counts = count_by_keyword(results, SCENARIO_LABELS)

    lines.extend(build_distribution_table("평가 항목별 케이스 분포", category_counts, total))
    lines.extend(build_distribution_table("시나리오 유형별 케이스 분포", scenario_counts, total))

    # 실패한 케이스 목록
    failed = [r for r in graded if not r.get("passed")]
    if failed:
        lines.append("### 실패(FAIL) 케이스")
        lines.append("")
        lines.append("| 테스트 ID | 사용자 질문 | 정확성 | 근거성 | 환각여부 | 검색성능 |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for r in failed:
            question_cell = r.get("user_question", "").replace("|", "\\|").replace("\n", " ")
            s = r["scores"]
            lines.append(
                f"| {r['case_id']} | {question_cell} | "
                f"{s['accuracy']} | {s['grounding']} | "
                f"{s['hallucination']} | {s['retrieval']} |"
            )
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = find_latest_log()

    with open(input_path, encoding="utf-8") as f:
        cases = json.load(f)

    llm = get_judge_llm()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_txt = LOG_DIR / f"judge_report_{timestamp}.txt"
    report_json = LOG_DIR / f"judge_report_{timestamp}.json"

    results = []
    totals = {key: 0 for key in CRITERIA}
    pass_count = 0

    with open(report_txt, "w", encoding="utf-8") as report:
        report.write("RAG 챗봇 자동 채점 리포트\n")
        report.write(f"채점 시각: {timestamp}\n")
        report.write(f"입력 로그: {input_path.name}\n")
        report.write(f"총 케이스: {len(cases)}건 (합격 기준: 모든 항목 {PASS_THRESHOLD}점 이상)\n")
        report.write("=" * 72 + "\n\n")

        for index, case in enumerate(cases, start=1):
            case_id = case.get("case_id", f"CASE_{index}")
            question = case.get("user_question", "")

            print(f"[{index}/{len(cases)}] {case_id} 채점 중...")

            try:
                scores, reasons, passed = judge_one(llm, case)
            except Exception as error:
                report.write(f"[{index}] {case_id}\n")
                report.write(f"질문: {question}\n")
                report.write(f"[채점 오류] {error}\n")
                report.write("-" * 72 + "\n\n")
                results.append({"case_id": case_id, "error": str(error)})
                continue

            for key in CRITERIA:
                totals[key] += scores[key]
            if passed:
                pass_count += 1

            verdict = "PASS" if passed else "FAIL"
            report.write(f"[{index}] {case_id}  →  {verdict}\n")
            report.write(f"질문: {question}\n")
            for key, (label, _) in CRITERIA.items():
                report.write(f"  - {label}({key}): {scores[key]}점  | {reasons[key]}\n")
            report.write("-" * 72 + "\n\n")
            report.flush()

            results.append(
                {
                    "case_id": case_id,
                    "user_question": question,
                    "answer": case.get("answer", ""),
                    "scores": scores,
                    "reasons": reasons,
                    "passed": passed
                }
            )

        # 요약 통계
        graded = [r for r in results if "scores" in r]
        report.write("=" * 72 + "\n")
        report.write("요약\n")
        report.write(f"채점 완료: {len(graded)}건 / 전체 {len(cases)}건\n")
        report.write(f"합격: {pass_count}건  실패: {len(graded) - pass_count}건\n")
        if graded:
            report.write("항목별 평균 점수:\n")
            for key, (label, _) in CRITERIA.items():
                avg = totals[key] / len(graded)
                report.write(f"  - {label}({key}): {avg:.2f}점\n")

    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "input_log": input_path.name,
                "pass_threshold": PASS_THRESHOLD,
                "pass_count": pass_count,
                "total": len(cases),
                "averages": {
                    key: (totals[key] / len(graded) if graded else 0)
                    for key in CRITERIA
                },
                "results": results,
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    # final_report.md 형식의 마크다운 보고서 생성
    report_md = LOG_DIR / f"final_report_{timestamp}.md"
    write_markdown_report(report_md, results)

    print()
    print(f"채점 완료: 합격 {pass_count} / {len(graded)}건")
    print(f"리포트(txt): {report_txt}")
    print(f"리포트(json): {report_json}")
    print(f"리포트(md): {report_md}")


if __name__ == "__main__":
    main()
