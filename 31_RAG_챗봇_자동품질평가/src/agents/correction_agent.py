import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
from prompts.correction_prompt import CORRECTION_PROMPT_TEMPLATE

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY를 찾을 수 없습니다. .env 파일을 확인하십시오."
    )

client = OpenAI(api_key=api_key)


def create_corrected_answer(
    user_question: str,
    ai_answer: str,
    retrieved_sources: list[str],
    evaluation_result: dict
) -> dict:
    """평가 결과를 반영하여 수정 모범답안을 생성합니다."""

    sources_text = "\n".join(
        f"- {source}"
        for source in retrieved_sources
    )

    evaluation_text = json.dumps(
        evaluation_result,
        ensure_ascii=False,
        indent=2
    )

    prompt = CORRECTION_PROMPT_TEMPLATE.format(
        user_question=user_question,
        ai_answer=ai_answer,
        retrieved_sources=sources_text,
        evaluation_result=evaluation_text
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

        return json.loads(
            response.choices[0].message.content
        )

    except Exception as error:
        logging.exception("수정 모범답안 생성 중 오류가 발생했습니다.")

        return {
            "corrected_answer": "",
            "reason_for_correction": "",
            "applied_improvements": [],
            "error": str(error)
        }