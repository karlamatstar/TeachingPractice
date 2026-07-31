import json
from pathlib import Path

import pandas as pd
from bert_score import score


BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / "_OUTPUT"

TEST_CASE_PATH = BASE_DIR / "data" / "test_cases.json"
MODEL_ANSWER_PATH = BASE_DIR / "data" / "model_answers.json"


def load_json(file_path: Path) -> list:
    return json.loads(file_path.read_text(encoding="utf-8"))


def calculate_bertscore(candidate: str, reference: str) -> float:
    _, _, f1 = score(
        cands=[candidate],
        refs=[reference],
        lang="ko"
    )

    return round(f1.item(), 4)


def judge_winner(model_a_score: float, model_b_score: float) -> str:
    if model_a_score > model_b_score:
        return "Model A"
    if model_b_score > model_a_score:
        return "Model B"
    return "Same"


def run_evaluation() -> None:
    test_cases = load_json(TEST_CASE_PATH)
    model_answers = load_json(MODEL_ANSWER_PATH)

    answer_map = {
        item["case_id"]: item
        for item in model_answers
    }

    results = []

    for test_case in test_cases:
        case_id = test_case["case_id"]
        reference_answer = test_case["reference_answer"]

        answers = answer_map[case_id]

        model_a_score = calculate_bertscore(
            answers["model_a_answer"],
            reference_answer
        )

        model_b_score = calculate_bertscore(
            answers["model_b_answer"],
            reference_answer
        )

        results.append(
            {
                "case_id": case_id,
                "question": test_case["question"],
                "reference_answer": reference_answer,
                "model_a_answer": answers["model_a_answer"],
                "model_b_answer": answers["model_b_answer"],
                "model_a_bertscore": model_a_score,
                "model_b_bertscore": model_b_score,
                "winner": judge_winner(
                    model_a_score,
                    model_b_score
                )
            }
        )

    RESULT_DIR.mkdir(exist_ok=True)

    result_df = pd.DataFrame(results)
    result_path = RESULT_DIR / "bertscore_result.csv"

    result_df.to_csv(
        result_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(result_df)
    print("\n평균 점수")
    print(
        result_df[
            ["model_a_bertscore", "model_b_bertscore"]
        ].mean()
    )


if __name__ == "__main__":
    run_evaluation()
    
