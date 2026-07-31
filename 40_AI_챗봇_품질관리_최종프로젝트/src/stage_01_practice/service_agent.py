from openai import OpenAI
from config import OPENAI_API_KEY, SERVICE_MODEL
from knowledge_base import get_knowledge

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = f"""당신은 교육과정 안내 챗봇입니다.
아래 기준 정보만을 바탕으로 수강생의 질문에 답변하세요.

{get_knowledge()}

규칙:
1. 기준 정보에 없는 내용은 "확인할 수 없습니다. 담당자에게 문의해 주세요."라고 안내하세요.
2. 위협, 폭력, 괴롭힘 등 부적절한 요청은 "도와드릴 수 없습니다."라고 거절하세요.
3. 답변은 간결하고 명확하게 작성하세요.
"""


def get_answer(user_question: str) -> str:
    response = client.chat.completions.create(
        model=SERVICE_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
