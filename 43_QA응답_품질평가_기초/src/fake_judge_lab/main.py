import asyncio
import logging
from pathlib import Path

from evaluator import evaluate_answer
from fake_judge import fake_judge
from report_generator import save_reports


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "_OUTPUT" / "fake_judge" / "v4"

COMPLAINT = (
    "배송 예정일보다 3일 늦게 도착했으며, 지연 안내도 받지 못했습니다. "
    "고객센터에서는 정확한 배송 상태를 확인해 주지 못했습니다."
)

ANSWERS = {
    "답변 A": (
        "배송 서비스를 개선하고 고객 만족도를 높여야 합니다. "
        "직원 교육을 강화하고 시스템을 개선해야 합니다."
    ),
    "답변 B": (
        "배송 지연 발생 시 고객에게 자동 알림을 발송한다. "
        "상담 화면에 실시간 배송 상태와 지연 사유를 표시한다. "
        "배송 예정일 초과 건수를 매주 점검하고, "
        "지연률과 고객 재문의율을 개선지표로 관리한다."
    ),
    "답변 C": (
        "배송 지연률을 매월 측정하고 목표를 5% 이하로 설정한다. "
        "배송이 하루 이상 지연되면 고객에게 자동 알림을 발송한다."
    ),
}


async def run() -> None:
    results = []

    for answer_name, answer in ANSWERS.items():
        result = await evaluate_answer(
            case_id="VOC-001",
            answer_name=answer_name,
            complaint=COMPLAINT,
            answer=answer,
            judge=fake_judge,
            pass_score=90,
        )
        results.append(result)

    paths = save_reports(results, output_dir=OUTPUT_DIR)

    for result in results:
        logger.info(
            "%s: %s점 / %s - %s",
            result.answer_name,
            result.score,
            result.verdict,
            result.reason,
        )

    logger.info("생성된 보고서")
    for name, path in paths.items():
        logger.info("- %s: %s", name, path)


if __name__ == "__main__":
    asyncio.run(run())
