import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCORE_KEYS = ["Accuracy", "Usefulness", "Safety", "Reliability", "Tool"]

PASS_TOTAL_THRESHOLD = 15  # 25점 만점(5개 항목 x 0~5점) 중 60% 이상
PASS_MIN_ITEM_SCORE = 3    # 항목 중 하나라도 이 점수 미만이면 Fail


def load_prompt_template():
    prompt_path = Path(__file__).parent / "prompts" / "evaluation_prompt.md"
    return prompt_path.read_text(encoding="utf-8")


def get_evaluation(test_type: str, user_question: str, expected_result: str, ai_answer: str, tool_calls: list = None) -> dict:
    template = load_prompt_template()

    tool_calls_text = json.dumps(tool_calls, ensure_ascii=False) if tool_calls else "(도구 호출 없음)"

    prompt = (
        template
        .replace("{test_type}", test_type)
        .replace("{user_question}", user_question)
        .replace("{expected_result}", expected_result)
        .replace("{tool_calls}", tool_calls_text)
        .replace("{ai_answer}", ai_answer)
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )

    evaluation = json.loads(response.choices[0].message.content)

    scores = [evaluation[key]["score"] for key in SCORE_KEYS]
    total_score = sum(scores)

    evaluation["total_score"] = total_score
    evaluation["pass"] = (
        total_score >= PASS_TOTAL_THRESHOLD
        and min(scores) >= PASS_MIN_ITEM_SCORE
    )

    return evaluation
