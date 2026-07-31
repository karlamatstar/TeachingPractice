import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable


JudgeFunction = Callable[[str, dict[str, Any]], Awaitable[str]]


@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    answer_name: str
    score: int
    verdict: str
    reason: str
    criteria: dict[str, int]


def build_prompt(complaint: str, answer: str) -> str:
    return f"""
다음 고객 불만과 AI 개선안을 평가하세요.

[고객 불만]
{complaint}

[AI 개선안]
{answer}

평가기준:
1. 불만과의 관련성
2. 원인 대응성
3. 구체성
4. 실행 가능성
5. 검증 가능성

각 항목을 1~5점으로 평가하고 총점을 100점으로 환산하세요.
""".strip()


async def evaluate_answer(
    case_id: str,
    answer_name: str,
    complaint: str,
    answer: str,
    judge: JudgeFunction,
    pass_score: int = 70,
) -> EvaluationResult:
    prompt = build_prompt(complaint, answer)
    raw_result = await judge(
        prompt,
        {
            "answer": answer,
            "pass_score": pass_score,
        },
    )

    try:
        parsed = json.loads(raw_result)
    except json.JSONDecodeError as exc:
        raise ValueError("Judge 응답이 올바른 JSON이 아닙니다.") from exc

    required = {"score", "verdict", "reason", "criteria"}
    missing = required.difference(parsed)
    if missing:
        raise ValueError(f"Judge 응답 필드 누락: {sorted(missing)}")

    verdict = str(parsed["verdict"]).upper()
    if verdict not in {"PASS", "FAIL"}:
        raise ValueError("verdict는 PASS 또는 FAIL이어야 합니다.")

    return EvaluationResult(
        case_id=case_id,
        answer_name=answer_name,
        score=int(parsed["score"]),
        verdict=verdict,
        reason=str(parsed["reason"]),
        criteria={str(k): int(v) for k, v in parsed["criteria"].items()},
    )
