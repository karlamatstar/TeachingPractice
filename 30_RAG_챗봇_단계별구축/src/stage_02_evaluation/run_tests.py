import json
import logging
from datetime import datetime
from pathlib import Path

from evaluator_agent import get_evaluation_from_openai
from agents.correction_agent import create_corrected_answer
from rag_service import answer_question



BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parents[1]
TEST_CASE_PATH = BASE_DIR / "test_cases.json"
REPORT_DIR = PROJECT_DIR / "_OUTPUT" / "stage_02"


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


def load_test_cases() -> list:
    return json.loads(
        TEST_CASE_PATH.read_text(
            encoding="utf-8"
        )
    )


def save_report(results: list) -> Path:
    REPORT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = REPORT_DIR / f"rag_evaluation_{timestamp}.json"

    report_path.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return report_path


def run_pipeline() -> list:
    test_cases = load_test_cases()

    final_results = []

    logging.info("RAG 챗봇 품질 평가를 시작합니다.")

    for test_case in test_cases:
        case_id = test_case["case_id"]
        question = test_case["user_question"]

        logging.info(f"[{case_id}] 평가 중")

        try:
            rag_result = answer_question(question)

            ai_answer = rag_result.get(
                "answer",
                "답변을 생성하지 못했습니다."
            )

            retrieved_sources = rag_result.get(
                "sources",
                []
            )

            evaluation = get_evaluation_from_openai(
                user_question=question,
                ai_answer=ai_answer,
                retrieved_sources=retrieved_sources
            )

            record = {
                "case_id": case_id,
                "category": test_case["category"],
                "user_question": question,
                "ai_answer": ai_answer,
                "retrieved_sources": retrieved_sources,
                "evaluation": evaluation
            }

            final_results.append(record)

        except Exception as error:
            logging.exception(
                f"[{case_id}] 실행 중 오류가 발생했습니다."
            )

            final_results.append(
                {
                    "case_id": case_id,
                    "user_question": question,
                    "error": str(error)
                }
            )

    report_path = save_report(final_results)

    logging.info("모든 평가가 완료되었습니다.")
    logging.info(f"보고서 저장 위치: {report_path}")

    return final_results


if __name__ == "__main__":
    run_pipeline()
