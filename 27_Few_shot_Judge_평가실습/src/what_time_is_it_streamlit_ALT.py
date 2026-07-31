from gpt_functions import get_current_time, tools 
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
import streamlit.components.v1 as components

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환

# ───────────────────────── 페이지 설정 ─────────────────────────
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide",  # 넓은 레이아웃으로 좌우 공간 확보
)

# ───────────────────────── 스타일 ─────────────────────────
st.markdown(
    """
    <style>
    /* 전체 여백을 줄여 채팅창을 왼쪽으로 붙입니다 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* 채팅 메시지 영역 */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.4rem 0.6rem;
        margin-bottom: 0.3rem;
    }
    /* 게임 채팅창처럼: 메시지를 아래쪽부터 채웁니다.
       내용이 적으면 빈 공간이 위로 가고, 최근 메시지는 항상 맨 아래에 위치 */
    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatMessage"]) {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatMessage"]) > div:first-child {
        margin-top: auto;  /* 빈 공간이 있을 때만 작동 -> 메시지를 아래로 밀어줌 */
    }
    /* 오른쪽 정보 패널 카드 */
    .info-panel {
        background: linear-gradient(160deg, #f8f9ff 0%, #eef1fb 100%);
        border: 1px solid #e3e6f3;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        min-height: 420px;
    }
    .info-panel h3 {
        margin-top: 0;
        color: #4a4ae0;
    }
    .info-placeholder {
        color: #9aa0b5;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────────────────── 세션 상태 ─────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},  # 초기 시스템 메시지
    ]

# ───────────────────────── 레이아웃: 좌(채팅) / 우(정보) ─────────────────────────
chat_col, info_col = st.columns([2, 1], gap="large")  # 왼쪽이 더 넓게

with chat_col:
    st.title("💬 Chatbot")
    st.caption("무엇이든 물어보세요. 현재 시각도 알려드려요 🕒")

    # 채팅 메시지를 일정 높이의 컨테이너 안에 표시
    chat_container = st.container(height=480)
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] in ("assistant", "user"):  # assistant 혹은 user 메시지인 경우만
                st.chat_message(msg["role"]).write(msg["content"])


def scroll_chat_to_bottom():
    """게임 채팅창처럼 최근 메시지가 보이도록 채팅 영역을 맨 아래로 스크롤"""
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const scrollToBottom = () => {
            const wrappers = doc.querySelectorAll(
                '[data-testid="stVerticalBlockBorderWrapper"]'
            );
            wrappers.forEach((el) => {
                if (el.scrollHeight > el.clientHeight) {
                    el.scrollTop = el.scrollHeight;
                }
            });
        };
        // 렌더링이 끝난 뒤 실행
        setTimeout(scrollToBottom, 50);
        setTimeout(scrollToBottom, 200);
        </script>
        """,
        height=0,
    )

with info_col:
    # 오른쪽 정보 패널 (현재는 비워둠)
    st.markdown(
        """
        <div class="info-panel">
            <h3>ℹ️ 정보 패널</h3>
            <div class="info-placeholder">
                여기에 정보가 표시됩니다.<br>(준비 중)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ───────────────────────── 입력 처리 ─────────────────────────
if user_input := st.chat_input("메시지를 입력하세요..."):    # ① 사용자 입력 받기
    st.session_state.messages.append({"role": "user", "content": user_input})  # ① 사용자 메시지를 대화 기록에 추가
    with chat_container:
        st.chat_message("user").write(user_input)  # ① 사용자 메시지를 브라우저에서도 출력

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = ai_response.choices[0].message
    print(ai_message)  # ③ gpt에서 반환되는 값을 파악하기 위해 임시로 추가

    tool_calls = ai_message.tool_calls  # AI 응답에 포함된 tool_calls를 가져옵니다.
    if tool_calls:  # tool_calls가 있는 경우
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 실행해야한다고 판단한 함수명 받기
            tool_call_id = tool_call.id         # tool_call 아이디 받기
            arguments = json.loads(tool_call.function.arguments) # (1) 문자열을 딕셔너리로 변환

            if tool_name == "get_current_time":  # ⑤ 만약 tool_name이 "get_current_time"이라면
                st.session_state.messages.append({
                    "role": "function",  # role을 "function"으로 설정
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": get_current_time(timezone=arguments['timezone']),  # 타임존 추가
                })
        st.session_state.messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
        ai_response = get_ai_response(st.session_state.messages, tools=tools) # 다시 GPT 응답 받기
        ai_message = ai_response.choices[0].message

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message.content
    })  # ③ AI 응답을 대화 기록에 추가합니다.

    print("AI\t: " + ai_message.content)  # AI 응답 출력
    with chat_container:
        st.chat_message("assistant").write(ai_message.content)  # 브라우저에 메시지 출력

# 최근 메시지가 항상 맨 아래에 보이도록 스크롤 (게임 채팅창 효과)
scroll_chat_to_bottom()
