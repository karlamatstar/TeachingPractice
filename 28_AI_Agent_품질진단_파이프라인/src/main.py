import json
import logging
from pathlib import Path
from dotenv import load_dotenv

from service_agent import get_answer_from_my_service
from evaluator_agent import get_evaluation_from_openai
# from report import save_report
from report import save_report, save_markdown_report


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_CASE_PATH = PROJECT_ROOT / "data" / "test_cases.json"


def load_test_cases(path: str | Path = TEST_CASE_PATH) -> list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_pipeline() -> list:
    test_cases = load_test_cases()
    final_results = []

    logging.info("LLM 평가 자동화 파이프라인을 시작합니다.")

    for test_case in test_cases:
        case_id = test_case["case_id"]
        user_question = test_case["user_question"]

        logging.info(f"\n[{case_id}] 평가 실행")

        try:
            ai_answer = get_answer_from_my_service(user_question)

            evaluation_result = get_evaluation_from_openai(
                user_question=user_question,
                ai_answer=ai_answer
            )

            result_record = {
                "case_id": case_id,
                "user_question": user_question,
                "ai_answer": ai_answer,
                "evaluation_result": evaluation_result
            }

            final_results.append(result_record)
            logging.info("평가 완료")

        except Exception as error:
            logging.error(f"[오류 발생] {case_id}: {error}")

    # save_report(final_results)

    json_report_path = save_report(final_results)
    markdown_report_path = save_markdown_report(final_results)

    logging.info("\n모든 평가가 완료되었습니다.")
    logging.info(f"JSON 보고서 생성 완료: {json_report_path}")
    logging.info(f"Markdown 보고서 생성 완료: {markdown_report_path}")


    return final_results


if __name__ == "__main__":
    run_pipeline()
