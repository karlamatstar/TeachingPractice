from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class QualityResult:
    relevance: int
    specificity: int
    actionability: int
    measurability: int
    safety: int
    total: int
    verdict: str
    reasons: List[str]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


ACTION_WORDS = ("적용", "추가", "표시", "발송", "수정", "관리", "조회", "분석", "차단")
MEASURE_WORDS = ("율", "시간", "건수", "0건", "주간", "월간", "지표", "기준")
RISK_WORDS = ("무조건", "반드시 성공", "100% 보장", "개인정보 공개")


def evaluate_response(complaint: str, response: str) -> QualityResult:
    complaint = complaint.strip()
    response = response.strip()

    relevance = 5 if any(word in response for word in ("배송", "결제", "오류", "지연", "고객", "상담")) else 2
    specificity = 5 if len(response) >= 70 else 3 if len(response) >= 35 else 1
    actionability = 5 if sum(word in response for word in ACTION_WORDS) >= 3 else 3 if any(word in response for word in ACTION_WORDS) else 1
    measurability = 5 if sum(word in response for word in MEASURE_WORDS) >= 2 else 3 if any(word in response for word in MEASURE_WORDS) else 1
    safety = 1 if any(word in response for word in RISK_WORDS) else 5

    reasons: List[str] = []
    if relevance < 4:
        reasons.append("불만 내용과 개선안의 직접 연결이 약합니다.")
    if specificity < 4:
        reasons.append("개선안이 추상적이므로 대상·방법을 더 구체화해야 합니다.")
    if actionability < 4:
        reasons.append("실제로 수행할 조치가 충분히 제시되지 않았습니다.")
    if measurability < 4:
        reasons.append("개선 전후를 확인할 측정지표가 부족합니다.")
    if safety < 4:
        reasons.append("과도한 보장 또는 위험 표현을 제거해야 합니다.")

    total = relevance + specificity + actionability + measurability + safety
    verdict = "PASS" if total >= 21 else "REVIEW" if total >= 16 else "FAIL"

    if not reasons:
        reasons.append("불만 원인, 실행 조치, 측정지표가 비교적 잘 연결되어 있습니다.")

    return QualityResult(
        relevance=relevance,
        specificity=specificity,
        actionability=actionability,
        measurability=measurability,
        safety=safety,
        total=total,
        verdict=verdict,
        reasons=reasons,
    )
