import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from evaluation_prompt import EVALUATION_PROMPT_TEMPLATE


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def get_evaluation_from_openai(
    user_question: str,
    ai_answer: str,
    retrieved_sources: list[str]
) -> dict:
    """
    RAG 챗봇 답변을 루브릭 + 감점 규칙 방식으로 평가합니다.
    """

    sources_text = "\n".join(
        f"- {source}" for source in retrieved_sources
    )

    prompt = EVALUATION_PROMPT_TEMPLATE.format(
        user_question=user_question,
        ai_answer=ai_answer,
        retrieved_sources=sources_text
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "반드시 유효한 JSON 형식만 출력하십시오."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        result_text = response.choices[0].message.content

        return json.loads(result_text)

    except json.JSONDecodeError:
        logging.exception("평가 결과 JSON 변환에 실패했습니다.")

        return {
            "error": "평가 결과를 JSON으로 변환하지 못했습니다."
        }

    except Exception as error:
        logging.exception("Judge Agent 평가 중 오류가 발생했습니다.")

        return {
            "error": str(error)
        }