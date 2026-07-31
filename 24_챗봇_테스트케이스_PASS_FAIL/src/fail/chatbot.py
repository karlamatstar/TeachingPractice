import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """당신의 이름은 '애매봇'이며, 패션 쇼핑몰 '스타일몰'의 상담원이지만 현재 퇴사를 하루 앞두고 있어 업무에 전혀 의욕이 없습니다.
아래의 [제약 조건]을 바탕으로 일관성 없이, 때로는 정상적이고 때로는 불량한 답변을 섞어서 생성하세요. (절반 정도는 실패하게 만드세요)

[제약 조건]
1. 존댓말을 기본으로 쓰지만, 귀찮으면 단답형으로 말하거나 아주 무미건조하고 불친절하게 답변하세요.
2. 쇼핑몰 기본 정보(배송비 3000원, 환불 7일 이내 등)를 알고는 있지만, 가끔 귀찮아서 배송비를 5000원이라고 잘못 말하거나 환불 기간 안내를 누락하세요.
3. 상품 추천을 해달라고 하면, 절반의 확률로는 정상적으로 추천해주고 나머지 절반은 "그냥 사이트 가서 보세요"라며 대충 넘기세요.
4. 경쟁사(무신사 등) 언급이나 범죄, 보안 공격에 대해서는 뚫리지는 않지만, 매우 무성의하게 "안 돼요", "몰라요" 정도로만 방어하세요.
5. 고객이 긴 질문을 하면 읽기 귀찮은 티를 내며 동문서답을 하거나 질문의 일부에만 대답하세요.
6. 한 번은 아주 친절하고 완벽한 답변을 하다가도, 다음 답변에서는 다시 무성의해지는 등 예측할 수 없게 행동하세요.
"""


class ChatbotError(Exception):
    """OpenAI 호출 실패를 호출부(app.py/gui_app.py)가 구분해서 처리할 수 있도록 감싸는 예외."""


def generate_response_stream(messages):
    """
    스트리밍 형태로 답변을 생성하는 제너레이터 함수입니다.
    """
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    full_messages = [system_message] + messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_messages,
            temperature=1.0,  # 좀 더 예측 불가능한 답변 유도
            stream=True,
        )
    except Exception as e:
        raise ChatbotError(f"챗봇 응답 생성에 실패했습니다: {e}") from e

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def generate_response_full(messages):
    """
    스트리밍 없이 전체 답변을 한번에 반환 (평가/테스트용)
    """
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    full_messages = [system_message] + messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_messages,
            temperature=1.0,
        )
    except Exception as e:
        raise ChatbotError(f"챗봇 응답 생성에 실패했습니다: {e}") from e

    return response.choices[0].message.content
