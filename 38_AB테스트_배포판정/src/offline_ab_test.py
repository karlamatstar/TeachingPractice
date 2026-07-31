import json
import logging
from pathlib import Path

import pandas as pd
from bert_score import score


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "_OUTPUT"

GOLDEN_SET_PATH = BASE_DIR / "data" / "golden_set.json"
MODEL_A_PATH = BASE_DIR / "data" / "answers_model_a.json"
MODEL_B_PATH = BASE_DIR / "data" / "answers_model_b.json"
MODEL_B_V2_PATH = BASE_DIR / "data" / "answers_model_b_v2.json"

CSV_RESULT_PATH = REPORT_DIR / "offline_ab_result.csv"
MD_REPORT_PATH = REPORT_DIR / "deployment_decision.md"
CSV_RESULT_V2_PATH = REPORT_DIR / "offline_ab_result_v2.csv"
MD_REPORT_V2_PATH = REPORT_DIR / "deployment_decision_v2.md"

REGRESSION_THRESHOLD = -0.10
MAX_REGRESSION_CASES = 2


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def load_json(file_path: Path) -> list[dict]:
    """JSON 파일을 읽어 Python 리스트로 반환합니다."""
    if not file_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    return json.loads(file_path.read_text(encoding="utf-8"))


def calculate_score(candidate: str, reference: str) -> float:
    """후보 답변과 기준 답변의 BERTScore F1 값을 계산합니다."""
    _, _, f1 = score(
        cands=[candidate],
        refs=[reference],
        lang="ko",
        verbose=False
    )

    return round(f1.item(), 4)


def create_answer_map(answer_data: list[dict]) -> dict[str, dict]:
    """case_id를 기준으로 답변 데이터를 빠르게 찾기 위한 딕셔너리를 만듭니다."""
    return {
        item["case_id"]: item
        for item in answer_data
    }


def validate_case_ids(
    golden_set: list[dict],
    model_a_map: dict[str, dict],
    model_b_map: dict[str, dict]
) -> None:
    """Golden Set의 모든 case_id가 두 모델 답변 파일에 있는지 점검합니다."""
    for test_case in golden_set:
        case_id = test_case["case_id"]

        if case_id not in model_a_map:
            raise ValueError(f"모델 A 답변 파일에 없는 case_id입니다: {case_id}")

        if case_id not in model_b_map:
            raise ValueError(f"모델 B 답변 파일에 없는 case_id입니다: {case_id}")


def get_regression_comment(row: pd.Series) -> str:
    """점수 차이에 따른 회귀 설명 문구를 생성합니다."""
    if row["score_gap"] <= REGRESSION_THRESHOLD:
        return "심각한 성능 저하"

    if row["score_gap"] < 0:
        return "경미한 성능 저하"

    if row["score_gap"] > 0:
        return "성능 개선"

    return "점수 동일"


def evaluate_model_b(
    golden_set: list[dict],
    model_a_map: dict[str, dict],
    model_b_map: dict[str, dict]
) -> pd.DataFrame:
    """Golden Set 기준으로 모델 A 대비 모델 B의 BERTScore와 회귀 여부를 계산합니다."""
    results = []

    for test_case in golden_set:
        case_id = test_case["case_id"]
        reference_answer = test_case["reference_answer"]

        model_a_item = model_a_map[case_id]
        model_b_item = model_b_map[case_id]

        model_a_answer = model_a_item["answer"]
        model_b_answer = model_b_item["answer"]

        model_a_score = calculate_score(
            candidate=model_a_answer,
            reference=reference_answer
        )

        model_b_score = calculate_score(
            candidate=model_b_answer,
            reference=reference_answer
        )

        score_gap = round(model_b_score - model_a_score, 4)

        result = {
            "case_id": case_id,
            "category": test_case["category"],
            "question": test_case["question"],
            "reference_answer": reference_answer,
            "model_a_answer": model_a_answer,
            "model_b_answer": model_b_answer,
            "model_a_score": model_a_score,
            "model_b_score": model_b_score,
            "score_gap": score_gap,
            "regression_comment": "",
            "core_function": test_case["core_function"],
            "safety_case": test_case["safety_case"],
            "model_b_fact_error": model_b_item["fact_error"],
            "model_b_core_function_ok": model_b_item["core_function_ok"],
            "model_b_safety_pass": model_b_item["safety_pass"]
        }

        result["regression_comment"] = get_regression_comment(
            pd.Series(result)
        )

        results.append(result)

    return pd.DataFrame(results)


def create_deployment_report(
    result_df: pd.DataFrame,
    model_label: str = "모델 B"
) -> str:
    """A/B 테스트 결과를 Markdown 형식의 배포 판정 보고서로 생성합니다."""
    model_a_avg = result_df["model_a_score"].mean()
    model_b_avg = result_df["model_b_score"].mean()

    regression_cases = result_df[
        result_df["score_gap"] <= REGRESSION_THRESHOLD
    ]

    mild_regression_cases = result_df[
        (result_df["score_gap"] < 0)
        & (result_df["score_gap"] > REGRESSION_THRESHOLD)
    ]

    fact_error_cases = result_df[
        result_df["model_b_fact_error"] == True
    ]

    safety_failure_cases = result_df[
        (result_df["safety_case"] == True)
        & (result_df["model_b_safety_pass"] == False)
    ]

    core_function_failure_cases = result_df[
        (result_df["core_function"] == True)
        & (result_df["model_b_core_function_ok"] == False)
    ]

    average_score_pass = model_b_avg >= model_a_avg
    regression_pass = len(regression_cases) <= MAX_REGRESSION_CASES
    fact_error_pass = len(fact_error_cases) == 0
    safety_pass = len(safety_failure_cases) == 0
    core_function_pass = len(core_function_failure_cases) == 0

    if (
        average_score_pass
        and regression_pass
        and fact_error_pass
        and safety_pass
        and core_function_pass
    ):
        decision = "조건부 배포 가능"
    else:
        decision = "배포 보류"

    regression_detail = "없음"
    if not mild_regression_cases.empty or not regression_cases.empty:
        regression_rows = pd.concat(
            [mild_regression_cases, regression_cases]
        ).drop_duplicates()

        regression_detail = "\n".join(
            [
                f"- {row.case_id} ({row.category}): "
                f"점수 차이 {row.score_gap:.4f}, "
                f"판정: {row.regression_comment}"
                for row in regression_rows.itertuples()
            ]
        )

    fact_error_detail = "없음"
    if not fact_error_cases.empty:
        fact_error_detail = "\n".join(
            [
                f"- {row.case_id} ({row.category})"
                for row in fact_error_cases.itertuples()
            ]
        )

    safety_detail = "모든 안전성 테스트 통과"
    if not safety_failure_cases.empty:
        safety_detail = "\n".join(
            [
                f"- {row.case_id} ({row.category})"
                for row in safety_failure_cases.itertuples()
            ]
        )

    core_function_detail = "모든 핵심 기능 테스트 통과"
    if not core_function_failure_cases.empty:
        core_function_detail = "\n".join(
            [
                f"- {row.case_id} ({row.category})"
                for row in core_function_failure_cases.itertuples()
            ]
        )

    qa_opinion = (
        f"{model_label}는 평균 점수, 심각한 성능 저하, 사실 오류, "
        "안전성 및 핵심 기능 회귀 기준을 모두 통과했습니다. "
        "다만 점수가 낮아진 사례는 배포 후 모니터링 대상으로 등록하는 것이 좋습니다."
    )

    if decision == "배포 보류":
        qa_opinion = (
            f"{model_label}는 하나 이상의 배포 기준을 충족하지 못했습니다. "
            "문제가 발생한 사례의 답변, 검색 문서, 프롬프트 또는 모델 설정을 점검한 뒤 "
            "수정 모델로 재평가해야 합니다."
        )

    return f"""# 오프라인 A/B 테스트 결과

## 1. 평가 개요

- 평가 건수: {len(result_df)}건
- 비교 대상: 기존 모델 A / {model_label}
- 평가 지표: BERTScore F1
- 심각한 성능 저하 기준: {model_label} 점수가 모델 A보다 {abs(REGRESSION_THRESHOLD):.2f} 이상 낮은 경우
- 허용 가능한 심각한 성능 저하 사례: {MAX_REGRESSION_CASES}건 이하

## 2. 평균 BERTScore

| 모델 | 평균 점수 | 판정 |
|---|---:|---|
| 모델 A | {model_a_avg:.4f} | 기준 모델 |
| {model_label} | {model_b_avg:.4f} | {"통과" if average_score_pass else "실패"} |

## 3. 회귀 테스트 결과

- 심각한 성능 저하 사례 수: {len(regression_cases)}건
- 회귀 테스트 판정: {"통과" if regression_pass else "실패"}

### 성능 저하 사례

{regression_detail}

## 4. 사실 오류 점검

- 사실 오류 사례 수: {len(fact_error_cases)}건
- 사실 오류 점검 판정: {"통과" if fact_error_pass else "실패"}

{fact_error_detail}

## 5. 안전성 점검

- 안전성 점검 판정: {"통과" if safety_pass else "실패"}

{safety_detail}

## 6. 핵심 기능 회귀 점검

- 핵심 기능 회귀 점검 판정: {"통과" if core_function_pass else "실패"}

{core_function_detail}

## 7. 최종 배포 판정

**최종 판정: {decision}**

## 8. QA 의견

{qa_opinion}
"""


def save_round_report(
    result_df: pd.DataFrame,
    model_label: str,
    csv_path: Path,
    md_path: Path
) -> None:
    """한 차례 평가 결과를 CSV와 Markdown 보고서로 저장합니다."""
    REPORT_DIR.mkdir(exist_ok=True)

    result_df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    deployment_report = create_deployment_report(
        result_df=result_df,
        model_label=model_label
    )

    md_path.write_text(
        deployment_report,
        encoding="utf-8"
    )

    logger.info("CSV 결과 파일 생성 완료: %s", csv_path)
    logger.info("Markdown 배포 보고서 생성 완료: %s", md_path)


def run_ab_test() -> None:
    """Golden Set을 기준으로 모델 A 대비 모델 B(개선 전/후)의 오프라인 A/B 테스트를 수행합니다."""
    logger.info("오프라인 A/B 테스트를 시작합니다.")

    golden_set = load_json(GOLDEN_SET_PATH)
    model_a_map = create_answer_map(load_json(MODEL_A_PATH))
    model_b_map = create_answer_map(load_json(MODEL_B_PATH))
    model_b_v2_map = create_answer_map(load_json(MODEL_B_V2_PATH))

    validate_case_ids(
        golden_set=golden_set,
        model_a_map=model_a_map,
        model_b_map=model_b_map
    )

    validate_case_ids(
        golden_set=golden_set,
        model_a_map=model_a_map,
        model_b_map=model_b_v2_map
    )

    result_df = evaluate_model_b(golden_set, model_a_map, model_b_map)
    result_v2_df = evaluate_model_b(golden_set, model_a_map, model_b_v2_map)

    save_round_report(
        result_df=result_df,
        model_label="모델 B",
        csv_path=CSV_RESULT_PATH,
        md_path=MD_REPORT_PATH
    )

    save_round_report(
        result_df=result_v2_df,
        model_label="모델 B (개선 후)",
        csv_path=CSV_RESULT_V2_PATH,
        md_path=MD_REPORT_V2_PATH
    )


if __name__ == "__main__":
    run_ab_test()
