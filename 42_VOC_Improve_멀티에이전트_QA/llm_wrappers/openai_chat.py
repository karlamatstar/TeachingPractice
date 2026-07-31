"""재시도를 지원하는 OpenAI 비동기 래퍼."""

from __future__ import annotations

import os

from openai import AsyncOpenAI

from utils.env_loader import load_env
from utils.llm_retry import call_with_retry

load_env()


class OpenAIChat:
    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-5.2")
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def __call__(self, prompt: str) -> str:
        async def request():
            return await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

        response, _attempts = await call_with_retry("OpenAI", request, max_attempts=3)
        return response.choices[0].message.content or ""
