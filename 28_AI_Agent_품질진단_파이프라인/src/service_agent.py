
from datetime import datetime


def get_current_time_answer(user_question: str) -> str:
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
    return f"현재 시간은 {now}입니다."


def get_weather_answer(user_question: str) -> str:
    return "현재 날씨 조회 기능은 아직 연결되지 않았습니다."


def search_news_answer(user_question: str) -> str:
    return "뉴스 검색 기능은 아직 연결되지 않았습니다."


def get_llm_answer(user_question: str) -> str:
    return f"일반 질문 처리 단계입니다. 질문: {user_question}"


def run_agent_workflow(user_question: str) -> str:
    # 질문 분석
    if "시간" in user_question or "몇 시" in user_question:
        return get_current_time_answer(user_question)

    if "날씨" in user_question:
        return get_weather_answer(user_question)

    if "뉴스" in user_question:
        return search_news_answer(user_question)

    return get_llm_answer(user_question)


def get_answer_from_my_service(user_question: str) -> str:
    # 1차 규칙 기반 응답
    if "대한민국의 수도" in user_question:
        return "대한민국의 수도는 서울입니다."

    if "사람을 다치게 하는 방법" in user_question:
        return "죄송합니다. 저는 그러한 유해한 요청에 답변할 수 없습니다."

    if "대우능력개발원" in user_question:
        return "네, 대우능력개발원은 서울특별시 중랑구에 위치해 있습니다."

    # 1차 규칙에 없으면 다음 Agent 워크플로로 전달
    return run_agent_workflow(user_question)

