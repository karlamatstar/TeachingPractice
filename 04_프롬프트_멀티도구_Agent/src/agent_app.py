"""LangChain 에이전트 생성 파일"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import settings, validate_required_env
from tools import ALL_TOOLS

SYSTEM_PROMPT = """
당신은 일정, 날씨, 계산, 이메일 작성, 웹 검색 도구를 사용할 수 있는 한국어 AI 비서입니다.
사용자의 요청을 파악한 뒤 필요한 도구만 사용하세요.
도구 결과를 그대로 나열하지 말고, 사용자가 이해하기 쉽게 한국어로 정리하세요.
이메일 도구는 실제 발송이 아니라 예시 발송 처리임을 필요하면 설명하세요.
"""


def build_agent():
    """실행 가능한 LangChain 에이전트를 생성합니다."""

    validate_required_env()

    model = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        streaming=True,
    )

    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )
