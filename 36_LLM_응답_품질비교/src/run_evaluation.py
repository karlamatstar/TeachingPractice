import json
from pathlib import Path

import pandas as pd
from bert_score import score


BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / "_OUTPUT"

TEST_CASE_PATH = BASE_DIR / "data" / "test_cases.json"
MODEL_ANSWER_PATH = BASE_DIR / "data" / "model_answers.json"

CSV_RESULT_PATH = RESULT_DIR / "baseline_comparison_result.csv"
MD_RESULT_PATH = RESULT_DIR / "baseline_comparison_report.md"


def load_json(file_path: Path) -> list:
    return json.loads(file_path.read_text(encoding="utf-8"))


def judge_status(f1_score: float) -> str:
    """
    BERTScore F1 기준으로 상태를 판정합니다.
    점수 기준은 조직과 서비스 특성에 따라 조정해야 합니다.
    """

    if f1_score >= 0.95:
        return "안정적 유지"

    if f1_score >= 0.85:
        return "검토 필요"

    return "성능 저하 의심"


def create_opinion(status: str, case_id: str) -> str:
    """
    각 테스트 케이스의 1차 평가 의견을 생성합니다.
    """

    if status == "안정적 유지":
        return (
            f"{case_id}은(는) 기준 모델 A와 의미 및 응답 방향이 "
            "대체로 유사합니다. 회귀 문제 가능성은 낮습니다."
        )

    if status == "검토 필요":
        return (
            f"{case_id}은(는) 기준 모델 A와 일부 표현 또는 답변 범위의 "
            "차이가 확인됩니다. 실제 품질 저하인지 사람의 검토가 필요합니다."
        )

    return (
        f"{case_id}은(는) 기준 모델 A와 의미적 차이가 비교적 큽니다. "
        "의도, 정확성, 안전성, 사실성 관점에서 우선 검토해야 합니다."
    )


def create_final_opinion(result_df: pd.DataFrame) -> str:
    """
    전체 모델 B에 대한 종합 평가 의견을 만듭니다.
    """

    average_f1 = result_df["bert_score_f1"].mean()

    stable_count = (result_df["status"] == "안정적 유지").sum()
    review_count = (result_df["status"] == "검토 필요").sum()
    regression_count = (result_df["status"] == "성능 저하 의심").sum()

    if average_f1 >= 0.95 and regression_count == 0:
        conclusion = (
            "모델 B는 기준 모델 A의 응답 특성과 전반적으로 유사하며, "
            "뚜렷한 회귀 현상은 발견되지 않았습니다."
        )
    elif average_f1 >= 0.85:
        conclusion = (
            "모델 B는 전반적으로 기준 모델 A와 유사하지만, "
            "일부 테스트 케이스에서 응답 방향 또는 답변 범위 차이가 확인되었습니다. "
            "배포 전 사람 검토를 권장합니다."
        )
    else:
        conclusion = (
            "모델 B는 기준 모델 A 대비 의미적 차이가 비교적 크게 나타났습니다. "
            "성능 저하 또는 응답 정책 변경 가능성이 있으므로 배포 전 상세 분석이 필요합니다."
        )

    return f"""
## 최종 평가 의견

- 전체 테스트 케이스 수: {len(result_df)}건
- 평균 BERTScore F1: {average_f1:.4f}
- 안정적 유지: {stable_count}건
- 검토 필요: {review_count}건
- 성능 저하 의심: {regression_count}건

### 종합 판정

{conclusion}

### QA 권고 사항

1. BERTScore가 낮은 케이스는 반드시 사람이 원문 답변을 비교 검토합니다.
2. 안전성, 환각, 숫자, 날짜, 금액, 법률 정보는 BERTScore만으로 판정하지 않습니다.
3. 기준 모델 A가 잘못 답한 경우 B 모델이 더 좋은 답을 하더라도 낮은 점수가 나올 수 있습니다.
4. 실제 운영 전에는 Golden Set 기반 정확성 평가와 기준 모델 기반 회귀 평가를 함께 수행해야 합니다.
"""


def save_markdown_report(result_df: pd.DataFrame, final_opinion: str) -> None:
    """
    결과를 Markdown 보고서로 저장합니다.
    """

    markdown_table = result_df.to_markdown(index=False)

    report = f"""# 기준 모델 기반 BERTScore 평가 보고서

## 평가 개요

- 기준 모델: Model A
- 비교 모델: Model B
- 평가 방식: 기준 모델 A 응답을 Reference로 사용
- 비교 지표: BERTScore Precision / Recall / F1
- 목적: 모델 B가 모델 A의 응답 특성을 유지하는지 확인

## 상세 평가 결과

{markdown_table}

{final_opinion}
"""

    MD_RESULT_PATH.write_text(report, encoding="utf-8")


def run_evaluation() -> None:
    RESULT_DIR.mkdir(exist_ok=True)

    test_cases = load_json(TEST_CASE_PATH)
    model_answers = load_json(MODEL_ANSWER_PATH)

    question_map = {
        item["case_id"]: {
            "category": item["category"],
            "question": item["question"]
        }
        for item in test_cases
    }

    case_ids = []
    references = []
    candidates = []

    for answer in model_answers:
        case_ids.append(answer["case_id"])
        references.append(answer["model_a_answer"])
        candidates.append(answer["model_b_answer"])

    precision, recall, f1 = score(
        cands=candidates,
        refs=references,
        lang="ko",
        verbose=True
    )

    results = []

    for index, case_id in enumerate(case_ids):
        f1_score = round(f1[index].item(), 4)
        status = judge_status(f1_score)

        results.append(
            {
                "case_id": case_id,
                "category": question_map[case_id]["category"],
                "question": question_map[case_id]["question"],
                "model_a_answer": references[index],
                "model_b_answer": candidates[index],
                "bert_score_precision": round(precision[index].item(), 4),
                "bert_score_recall": round(recall[index].item(), 4),
                "bert_score_f1": f1_score,
                "status": status,
                "evaluation_opinion": create_opinion(status, case_id)
            }
        )

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        CSV_RESULT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    final_opinion = create_final_opinion(result_df)

    save_markdown_report(
        result_df=result_df,
        final_opinion=final_opinion
    )

    print("평가가 완료되었습니다.")
    print(f"CSV 결과 파일: {CSV_RESULT_PATH}")
    print(f"Markdown 보고서 파일: {MD_RESULT_PATH}")


if __name__ == "__main__":
    run_evaluation()
