import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
from prompts.evaluation_prompt import EVALUATION_PROMPT_TEMPLATE

# .env 파일의 OPENAI_API_KEY 값을 읽어옵니다.
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY를 찾지 못했습니다. "
        "C:\\rag_chatbot\\.env 파일을 확인하십시오."
    )

client = OpenAI(
    api_key=api_key
)


def get_evaluation_from_openai(
    user_question: str,
    ai_answer: str,
    retrieved_sources: list[str]
) -> dict:

    sources_text = "\n".join(
        f"- {source}"
        for source in retrieved_sources
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

    except Exception as error:
        logging.exception("Judge Agent 평가 중 오류가 발생했습니다.")

        return {
            "error": str(error)
        }