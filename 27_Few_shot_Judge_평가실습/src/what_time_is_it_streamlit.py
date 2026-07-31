from gpt_functions import (
    get_current_time,
    get_weather,
    search_news,
    search_web,
    tools,
)

from openai import OpenAI
from dotenv import load_dotenv

import os
import json
import streamlit as st


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    return response


def execute_tool(tool_name, arguments):
    """GPT가 요청한 도구 이름에 따라 실제 함수를 실행합니다."""

    if tool_name == "get_current_time":
        return get_current_time(
            timezone=arguments.get("timezone", "Asia/Seoul")
        )

    if tool_name == "get_weather":
        return get_weather(
            location=arguments.get("location", "서울")
        )

    if tool_name == "search_news":
        return search_news(
            query=arguments.get("query", "")
        )

    if tool_name == "search_web":
        return search_web(
            query=arguments.get("query", "")
        )

    return f"지원하지 않는 도구입니다: {tool_name}"


st.title("💬 AI Agent Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
너는 사용자를 도와주는 AI 상담사야.

사용자가 현재 시간, 날씨, 뉴스, 인터넷 검색을 요청하면
반드시 적절한 도구를 사용해서 답변해.

도구 결과가 제공되면 그 내용을 자연스럽고 이해하기 쉽게 정리해.
""",
        }
    ]


for msg in st.session_state.messages:
    if msg["role"] in ["assistant", "user"]:
        st.chat_message(msg["role"]).write(msg["content"])


if user_input := st.chat_input("궁금한 내용을 입력하세요."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    st.chat_message("user").write(user_input)

    # 1단계: GPT가 도구 사용 여부 판단
    ai_response = get_ai_response(
        st.session_state.messages,
        tools=tools,
    )

    ai_message = ai_response.choices[0].message

    # GPT의 assistant 메시지 자체를 대화 내역에 추가
    st.session_state.messages.append(ai_message.model_dump())

    # 2단계: Tool Calling 요청이 있으면 실행
    if ai_message.tool_calls:

        for tool_call in ai_message.tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_result = execute_tool(
                tool_name=tool_name,
                arguments=arguments,
            )

            # 최신 Tool Calling 방식
            st.session_state.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result,
                }
            )

        # 3단계: 도구 결과를 바탕으로 최종 답변 생성
        ai_response = get_ai_response(
            st.session_state.messages,
            tools=tools,
        )

        ai_message = ai_response.choices[0].message

    # 4단계: 최종 답변 저장 및 화면 출력
    final_answer = ai_message.content or "응답을 생성하지 못했습니다."

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer,
        }
    )

    st.chat_message("assistant").write(final_answer)