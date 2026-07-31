import pytest

from evaluator import evaluate_answer


async def always_pass_judge(prompt, config):
    return """
    {
      "score": 88,
      "verdict": "PASS",
      "reason": "불만 원인과 개선안이 연결되고 실행 가능함",
      "criteria": {
        "불만과의 관련성": 5,
        "원인 대응성": 4,
        "구체성": 4,
        "실행 가능성": 5,
        "검증 가능성": 4
      }
    }
    """


async def always_fail_judge(prompt, config):
    return """
    {
      "score": 40,
      "verdict": "FAIL",
      "reason": "구체적인 조치와 측정지표가 부족함",
      "criteria": {
        "불만과의 관련성": 2,
        "원인 대응성": 2,
        "구체성": 2,
        "실행 가능성": 2,
        "검증 가능성": 2
      }
    }
    """


async def broken_judge(prompt, config):
    return """
    {
      "score": 88,
      "verdict": "PASS"
    }
    """


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("judge", "expected"),
    [
        (always_pass_judge, "PASS"),
        (always_fail_judge, "FAIL"),
    ],
)
async def test_pass_fail_branch(judge, expected) -> None:
    result = await evaluate_answer(
        case_id="BRANCH-001",
        answer_name="분기 테스트",
        complaint="배송 지연 불만",
        answer="개선안",
        judge=judge,
        pass_score=70,
    )

    assert result.verdict == expected


@pytest.mark.asyncio
async def test_broken_judge_missing_fields() -> None:
    with pytest.raises(ValueError, match="Judge 응답 필드 누락"):
        await evaluate_answer(
            case_id="BROKEN-001",
            answer_name="불완전 응답 테스트",
            complaint="배송 지연 불만",
            answer="배송 개선안",
            judge=broken_judge,
            pass_score=90,
        )
