import asyncio
import json
from typing import Any


async def fake_judge(prompt: str, config: dict[str, Any]) -> str:
    """실제 LLM API 대신 고정 규칙으로 JSON 문자열을 반환합니다."""
    await asyncio.sleep(0.05)

    answer = str(config.get("answer", "")).strip()
    pass_score = int(config.get("pass_score", 70))

    criteria = {
        "불만과의 관련성": 0,
        "원인 대응성": 0,
        "구체성": 0,
        "실행 가능성": 0,
        "검증 가능성": 0,
    }

    keywords = {
        "불만과의 관련성": ["배송", "지연", "고객", "상담"],
        "원인 대응성": ["알림", "지연 사유", "실시간", "상태"],
        "구체성": ["자동", "화면", "매주", "표시", "발송"],
        "실행 가능성": ["발송한다", "표시한다", "점검", "관리한다"],
        "검증 가능성": ["지연률", "재문의율", "건수", "지표", "목표", "측정"],
    }

    for criterion, words in keywords.items():
        matched = sum(1 for word in words if word in answer)
        criteria[criterion] = min(5, 1 + matched)

    total_25 = sum(criteria.values())
    score = round(total_25 / 25 * 100)
    verdict = "PASS" if score >= pass_score else "FAIL"

    if verdict == "PASS":
        reason = "불만 원인과 개선안이 연결되고 실행 및 검증이 가능함"
    else:
        reason = "개선안이 추상적이거나 원인 대응 및 측정지표가 부족함"

    result = {
        "score": score,
        "verdict": verdict,
        "reason": reason,
        "criteria": criteria,
        "prompt_received": bool(prompt.strip()),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
