
# 게임 가챠 테스트용 챗봇 Agent

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os


class ChatbotAgent:

    def __init__(
        self,
        model: str = None
    ):
        """
        OpenAI 챗봇 에이전트
        """

        repository_root = Path(__file__).resolve().parents[1]
        env_path = repository_root / ".env"

        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY가 없습니다. 환경변수 또는 .env에 설정하세요."
            )

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.client = OpenAI(api_key=api_key)

    def ask(
        self,
        question: str,
        system_prompt: str | None = None
    ) -> str:
        """
        질문 전달 후 답변 반환
        """

        if not question or not question.strip():
            raise ValueError("질문 내용을 입력해야 합니다.")

        if system_prompt:
            response = self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=question
            )
        else:
            response = self.client.responses.create(
                model=self.model,
                input=question
            )

        return response.output_text.strip()

    def health_check(self):

        response = self.client.responses.create(
            model=self.model,
            input="안녕하세요"
        )

        return response.output_text


if __name__ == "__main__":

    agent = ChatbotAgent()

    result = agent.ask(
        "가챠 천장 시스템이 무엇인가요?"
    )

    print(result)
