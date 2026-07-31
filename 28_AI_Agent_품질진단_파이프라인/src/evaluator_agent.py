import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_prompt_template():
    prompt_path = PROJECT_ROOT / "config" / "prompts" / "evaluation_prompt.md"
    return prompt_path.read_text(encoding="utf-8")

def get_evaluation_from_openai(user_question, ai_answer):
    template = load_prompt_template()

    prompt = template.replace(
        "{user_question}",
        user_question
    ).replace(
        "{ai_answer}",
        ai_answer
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result_text = response.choices[0].message.content
    return json.loads(result_text)  
