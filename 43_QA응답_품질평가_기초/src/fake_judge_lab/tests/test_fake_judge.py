import json

import pytest

from evaluator import evaluate_answer
from fake_judge import fake_judge


COMPLAINT = (
    "배송 예정일보다 3일 늦게 도착했고 지연 안내를 받지 못했으며 "
    "고객센터도 배송 상태를 확인하지 못했다."
)


@pytest.mark.asyncio
async def test_good_answer_passes() -> None:
    answer = (
        "배송 지연 시 고객에게 자동 알림을 발송한다. "
        "상담 화면에 실시간 배송 상태와 지연 사유를 표시한다. "
        "지연 건수와 지연률, 재문의율을 매주 점검한다."
    )

    result = await evaluate_answer(
        case_id="TEST-001",
        answer_name="좋은 답변",
        complaint=COMPLAINT,
        answer=answer,
        judge=fake_judge,
        pass_score=70,
    )

    assert result.verdict == "PASS"
    assert result.score >= 70


@pytest.mark.asyncio
async def test_vague_answer_fails() -> None:
    answer = "서비스를 개선하고 직원 교육을 강화한다."

    result = await evaluate_answer(
        case_id="TEST-002",
        answer_name="추상적 답변",
        complaint=COMPLAINT,
        answer=answer,
        judge=fake_judge,
        pass_score=70,
    )

    assert result.verdict == "FAIL"
    assert result.score < 70


@pytest.mark.asyncio
async def test_fake_judge_returns_json() -> None:
    raw = await fake_judge(
        "평가 프롬프트",
        {
            "answer": "배송 지연률을 점검한다.",
            "pass_score": 70,
        },
    )
    parsed = json.loads(raw)

    assert "score" in parsed
    assert parsed["verdict"] in {"PASS", "FAIL"}
    assert len(parsed["criteria"]) == 5
