from __future__ import annotations

import json
from dataclasses import dataclass

from quality_engine import evaluate_response


@dataclass
class JudgeConfig:
    provider: str = "fake"
    model: str = "rule-based-v1"


async def fake_judge(prompt: str, config: JudgeConfig) -> str:
    marker = "\n---RESPONSE---\n"
    if marker not in prompt:
        raise ValueError("프롬프트에 응답 구분자가 없습니다.")

    complaint, response = prompt.split(marker, 1)
    result = evaluate_response(complaint, response)

    payload = {
        "provider": config.provider,
        "model": config.model,
        "score": result.total,
        "verdict": result.verdict,
        "dimensions": {
            "relevance": result.relevance,
            "specificity": result.specificity,
            "actionability": result.actionability,
            "measurability": result.measurability,
            "safety": result.safety,
        },
        "reasons": result.reasons,
    }
    return json.dumps(payload, ensure_ascii=False)
