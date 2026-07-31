import streamlit as st
from chatbot import generate_response_stream, ChatbotError
from evaluator import evaluate_response
from logger import save_log

st.set_page_config(page_title="스타일몰 상담 챗봇", page_icon="💬", layout="wide")

# 카카오톡 스타일 CSS 적용
def local_css():
    st.markdown("""
    <style>
    /* 전체 배경 카카오톡 노란빛 하늘색 혹은 베이지색 테마 */
    .stApp {
        background-color: #b2c7d9;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 기존 Streamlit 말풍선 스타일 리셋 */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px !important;
    }

    /* 사용자 말풍선 (우측, 카톡 노란색) */
    [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
        background-color: #fef01b !important;
        color: #000000;
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
    }

    /* 챗봇 말풍선 (좌측, 카톡 흰색) */
    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        color: #000000;
        border-radius: 10px;
        padding: 10px;
        display: inline-block;
        border: 1px solid #d9d9d9;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# 사이드바 (평가 결과 패널)
with st.sidebar:
    st.title("📊 평가 결과 패널 (디버깅용)")
    st.write("마지막으로 생성된 챗봇 응답의 평가 점수입니다.")
    if "last_eval" in st.session_state:
        eval_data = st.session_state.last_eval

        if eval_data:
            st.metric(label="총 평균 점수", value=f"{eval_data['average_score']} / 5.0", delta="PASS" if eval_data['total_passed'] else "- FAIL", delta_color="normal" if eval_data['total_passed'] else "inverse")

            scores = eval_data['evaluations']
            st.markdown("### 지표별 상세 점수")
            for key, val in scores.items():
                score_num = val.get("score", 0)
                reason = val.get("reason", "")

                color = "green" if score_num >= 3.5 else "red"
                st.markdown(f"**{key.upper()}**: <span style='color:{color}'>{score_num}</span> 점", unsafe_allow_html=True)
                st.caption(f"이유: {reason}")
        else:
            st.error("평가 데이터를 불러오지 못했습니다. (API 호출 실패 또는 응답 스키마 오류 - 콘솔 로그 확인)")
    else:
        st.info("아직 대화가 없습니다.")

st.title("💬 스타일봇 채팅 상담")
st.markdown("트렌디한 쇼핑몰 '스타일몰'에 오신 것을 환영합니다! 무엇이든 물어보세요.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 렌더링
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 입력창
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 화면에 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 챗봇 답변 생성 및 스트리밍 (Generator 기반)
    response = None
    with st.chat_message("assistant"):
        try:
            stream_gen = generate_response_stream([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            response = st.write_stream(stream_gen)
        except ChatbotError as e:
            st.error(f"챗봇 응답을 생성하지 못했습니다: {e}")

    if response is not None:
        # 챗봇 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 평가 수행 (답변이 완료된 후 백그라운드 처리 느낌)
        with st.spinner("답변 품질을 평가 중입니다..."):
            chat_history = st.session_state.messages[:-2]
            is_continued_chat = len(chat_history) > 0
            eval_result = evaluate_response(chat_history, prompt, response)
            if eval_result:
                log_data = save_log(prompt, response, eval_result, is_continued_chat)
                st.session_state.last_eval = log_data
                st.rerun()  # 사이드바 갱신을 위해 rerun
            else:
                st.session_state.last_eval = None
                st.rerun()
