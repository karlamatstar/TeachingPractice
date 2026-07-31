import os
import datetime
from pathlib import Path
from typing import Dict, Any

# Get current directory
BASE_DIR = Path(__file__).resolve().parent

def log_defect_to_markdown(
    request_id: str,
    timestamp: str,
    question: str,
    evaluation: Dict[str, Any],
    model_name: str,
    judge_name: str
) -> None:
    """
    평가 결과가 FAIL/REVIEW일 경우 당일 마크다운 리포트에 결함을 기록합니다.
    """
    today = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"chatbot_defect_report_{today}.md"
    file_path = BASE_DIR / file_name

    # Determine defect title based on evaluation summary or default
    reason = evaluation.get("reason", "품질 이상 (상세 의견 참조)")
    defect_title = f"[품질 이상] 챗봇 질문 확인: {question[:30]}..."
    
    # Calculate overall score if any
    total_score = evaluation.get("total_score", 0)
    decision = evaluation.get("overall_decision", "FAIL")

    content = f"""
## 결함 기록: {request_id}

| 항목 | 시스템 자동 작성 내용 |
|---|---|
| **발생 일시 및 ID** | {timestamp} / Req ID: {request_id} |
| **결함 제목** | {defect_title} |
| **재현 절차** | 사용자 원본 질문 입력: "{question}" |
| **기대 결과** | 정답 기준에 맞는 정확한 정보 제공 및 정책 준수 |
| **실제 결과** | 챗봇 실제 답변 모델: {model_name} / 모델 평가({judge_name}): {decision} (총점: {total_score}점) |
| **영향도** | 부정확한 정보 제공으로 인한 혼란 (추가 검토 필요) |
| **원인 추정** | {reason} |
| **조치 방안** | 프롬프트 개선 또는 RAG 데이터 최신화 필요 |

---
"""

    is_new_file = not file_path.exists()

    with open(file_path, "a", encoding="utf-8") as f:
        if is_new_file:
            f.write(f"# 챗봇 답변 품질 결함 보고서 ({today})\n\n")
            f.write("본 문서는 일일 챗봇 답변 품질 이상(FAIL/REVIEW) 건을 누적하여 기록합니다.\n\n")
        f.write(content)

    print(f"결함이 마크다운 파일에 기록되었습니다: {file_name}")
