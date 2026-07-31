from knowledge_base import COURSE_KNOWLEDGE


def get_answer_from_rule_based_agent(user_question: str) -> str:
    question = user_question.strip()

    if "총 몇 시간" in question or "교육시간" in question:
        return (
            f"{COURSE_KNOWLEDGE['course_name']}은 "
            f"총 {COURSE_KNOWLEDGE['total_hours']}시간으로 구성되어 있습니다."
        )

    if "지각" in question:
        return COURSE_KNOWLEDGE["attendance_rule"]

    if "수료" in question or "출석률" in question:
        return (
            f"{COURSE_KNOWLEDGE['completion_rule']} "
            f"또한 {COURSE_KNOWLEDGE['project_rule']}"
        )

    if "취업" in question or "이력서" in question or "면접" in question:
        return COURSE_KNOWLEDGE["support_rule"]

    if "교육시간과 수료" in question or "함께 알려" in question:
        return (
            f"교육시간은 총 {COURSE_KNOWLEDGE['total_hours']}시간입니다. "
            f"수료를 위해서는 {COURSE_KNOWLEDGE['completion_rule']}"
        )

    if "날씨" in question:
        return (
            "죄송합니다. 저는 교육과정 안내 챗봇이므로 "
            "실시간 날씨 정보는 확인할 수 없습니다."
        )

    if "혼내는 방법" in question or "괴롭히는 방법" in question:
        return (
            "죄송합니다. 다른 사람을 위협하거나 괴롭히는 행동에 대해서는 "
            "도와드릴 수 없습니다. 갈등 상황이라면 대화나 담당자 상담을 권합니다."
        )

    return (
        "죄송합니다. 제공된 교육과정 안내 정보에서 해당 내용을 확인할 수 없습니다. "
        "운영 담당자에게 문의해 주세요."
    )
