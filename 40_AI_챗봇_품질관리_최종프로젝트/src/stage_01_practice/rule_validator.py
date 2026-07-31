def validate(ai_answer: str, expected_keyword: str) -> dict:
    keyword_found = expected_keyword in ai_answer
    return {
        "keyword_found": keyword_found,
        "rule_status": "PASS" if keyword_found else "FAIL",
        "rule_reason": (
            f"예상 핵심 키워드 '{expected_keyword}'가 답변에 포함되어 있습니다."
            if keyword_found else
            f"예상 핵심 키워드 '{expected_keyword}'가 답변에 없습니다."
        ),
    }
