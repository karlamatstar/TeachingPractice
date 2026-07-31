# AI 평가 전에 기본적인 규칙 검증을 하는 파일입니다.
# 이 단계는 AI 평가 결과가 이상하더라도 최소한의 오류를 먼저 찾아내기 위해 필요합니다.

def validate_by_rules(
    user_question: str,
    ai_answer: str,
    expected_keyword: str
) -> dict:
    keyword_found = expected_keyword.lower() in ai_answer.lower()

    result = {
        "keyword_found": keyword_found,
        "rule_status": "PASS" if keyword_found else "FAIL",
        "rule_reason": ""
    }

    if keyword_found:
        result["rule_reason"] = (
            f"예상 핵심 키워드 '{expected_keyword}'가 답변에 포함되어 있습니다."
        )
    else:
        result["rule_reason"] = (
            f"예상 핵심 키워드 '{expected_keyword}'가 답변에 포함되지 않았습니다."
        )

    return result