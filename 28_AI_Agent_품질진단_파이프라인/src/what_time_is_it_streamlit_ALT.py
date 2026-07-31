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
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

# tool_name -> 실제 실행할 함수 매핑
available_functions = {
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "search_news": search_news,
    "search_web": search_web,
}


def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환


st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},  # 초기 시스템 메시지
    ]

for msg in st.session_state.messages:
    # 화면에는 사용자/AI 메시지 중 실제 내용이 있는 것만 출력
    if msg["role"] in ("assistant", "user") and msg.get("content"):
        st.chat_message(msg["role"]).write(msg["content"])


if user_input := st.chat_input():    # ① 사용자 입력 받기
    st.session_state.messages.append({"role": "user", "content": user_input})  # ① 사용자 메시지를 대화 기록에 추가
    st.chat_message("user").write(user_input)  # ① 사용자 메시지를 브라우저에서도 출력

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = ai_response.choices[0].message

    tool_calls = ai_message.tool_calls  # AI 응답에 포함된 tool_calls를 가져옵니다.
    if tool_calls:  # tool_calls가 있는 경우
        # tools API 규칙: tool 결과를 넣기 전에 tool_calls를 담은 assistant 메시지를 먼저 추가해야 함
        st.session_state.messages.append(ai_message.model_dump(exclude_none=True))

        for tool_call in tool_calls:
            tool_name = tool_call.function.name  # 실행해야 한다고 판단한 함수명 받기
            tool_call_id = tool_call.id          # tool_call 아이디 받기
            arguments = json.loads(tool_call.function.arguments)  # (1) 문자열을 딕셔너리로 변환

            func = available_functions.get(tool_name)
            if func is None:
                tool_result = f"알 수 없는 도구입니다: {tool_name}"
            else:
                tool_result = func(**arguments)  # 인자를 그대로 전달해 실행

            st.session_state.messages.append({
                "role": "tool",  # tools API에서는 결과 role을 "tool"로 설정
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": tool_result,
            })

        # 도구 실행 결과를 바탕으로 최종 답변 받기
        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

    content = ai_message.content or ""
    st.session_state.messages.append({
        "role": "assistant",
        "content": content,
    })  # ③ AI 응답을 대화 기록에 추가합니다.

    st.chat_message("assistant").write(content)  # 브라우저에 메시지 출력
