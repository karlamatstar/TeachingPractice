import asyncio
import json

from fake_judge import JudgeConfig, fake_judge
from quality_engine import evaluate_response


def test_specific_response_scores_higher_than_abstract_response() -> None:
    complaint = "배송 지연과 안내 부족"
    abstract = "서비스를 개선해야 합니다."
    specific = "배송 지연 시 자동 알림을 발송하고 지연률을 주간 지표로 관리합니다."
    assert evaluate_response(complaint, specific).total > evaluate_response(complaint, abstract).total


def test_measurable_response_gets_measurement_score() -> None:
    result = evaluate_response(
        "결제 오류",
        "중복 결제 방지 로직을 적용하고 중복 승인 0건을 통과 기준으로 관리합니다.",
    )
    assert result.measurability >= 3


def test_risky_claim_lowers_safety_score() -> None:
    result = evaluate_response(
        "배송 지연",
        "이 개선으로 배송 지연을 100% 보장 없이 해결합니다.",
    )
    assert result.safety == 1


def test_fake_judge_returns_json() -> None:
    prompt = "배송 지연\n---RESPONSE---\n배송 지연 시 자동 알림을 발송합니다."
    raw = asyncio.run(fake_judge(prompt, JudgeConfig()))
    payload = json.loads(raw)
    assert payload["provider"] == "fake"
    assert payload["verdict"] in {"PASS", "REVIEW", "FAIL"}


def test_missing_marker_raises_error() -> None:
    try:
        asyncio.run(fake_judge("잘못된 프롬프트", JudgeConfig()))
    except ValueError as error:
        assert "구분자" in str(error)
    else:
        raise AssertionError("ValueError가 발생해야 합니다.")
