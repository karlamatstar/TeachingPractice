import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from gpt_functions import get_current_time, tools

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

SYSTEM_PROMPT = "너는 사용자를 도와주는 상담사야."


def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환


def converse(messages, tool_trace=None):
    """messages 기록을 받아 한 턴을 진행하고, 최종 AI 메시지를 messages에 추가한 뒤 반환한다.
    tool_trace 리스트가 주어지면 실제로 호출된 도구명/인자/결과를 기록한다. (Tool Calling 품질 채점용)
    """
    ai_response = get_ai_response(messages, tools=tools)
    ai_message = ai_response.choices[0].message

    tool_calls = ai_message.tool_calls  # AI 응답에 포함된 tool_calls를 가져옵니다.
    if tool_calls:  # tool_calls가 있는 경우
        for tool_call in tool_calls:
            tool_name = tool_call.function.name  # 실행해야한다고 판단한 함수명 받기
            tool_call_id = tool_call.id  # tool_call 아이디 받기
            arguments = json.loads(tool_call.function.arguments)  # 문자열을 딕셔너리로 변환

            if tool_name == "get_current_time":  # 만약 tool_name이 "get_current_time"이라면
                timezone = arguments.get("timezone", "Asia/Seoul")
                try:
                    result = get_current_time(timezone=timezone)
                    error_text = None
                except Exception as error:
                    # 자동 테스트(엣지/네거티브 케이스)에서 잘못된 타임존이 들어와도
                    # 파이프라인 전체가 죽지 않도록 방어한다.
                    result = f"[오류] 알 수 없는 타임존입니다: {timezone} ({error})"
                    error_text = str(error)

                if tool_trace is not None:
                    tool_trace.append({
                        "name": tool_name,
                        "arguments": arguments,
                        "result": result,
                        "error": error_text,
                    })

                messages.append({
                    "role": "function",  # role을 "function"으로 설정
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": result,
                })

        messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
        # 도구 결과 반영 후에는 tools를 넘기지 않아, 모델이 또 도구를 호출하는 대신
        # 반드시 텍스트로 최종 답변을 생성하도록 강제한다. (빈 응답 방지)
        ai_response = get_ai_response(messages)  # 다시 GPT 응답 받기
        ai_message = ai_response.choices[0].message

    messages.append(ai_message)  # AI 응답을 대화 기록에 추가하기

    if not ai_message.content:
        # 그래도 빈 응답이 나오는 극히 드문 경우를 위한 안전장치
        ai_message.content = "죄송합니다, 답변을 생성하는 데 문제가 있었습니다. 다시 한 번 질문해 주시겠어요?"

    return ai_message


def get_chatbot_answer(user_question: str) -> dict:
    """단발성 질문 하나를 새 대화로 보내고 최종 답변과 도구 호출 내역을 반환한다. (자동 테스트용)"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]
    tool_trace = []
    ai_message = converse(messages, tool_trace)
    return {
        "answer": ai_message.content or "",
        "tool_calls": tool_trace,
    }


def run_interactive():
    """터미널에서 직접 대화하는 챗봇 실행 모드."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    while True:
        user_input = input("사용자\t: ")  # 사용자 입력 받기

        if user_input == "exit":  # 사용자가 대화를 종료하려는지 확인
            break

        messages.append({"role": "user", "content": user_input})
        ai_message = converse(messages)

        print("AI\t: " + (ai_message.content or ""))  # AI 응답 출력


if __name__ == "__main__":
    run_interactive()
