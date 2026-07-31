from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# 최대 응답 길이 (문자 수)
MAX_RESPONSE_LENGTH = 100

# 기본 시스템 지침: 도메인/언어/길이 제약을 1차 응답부터 유도
DEFAULT_SYSTEM_PROMPT = (
    "당신은 게임 및 확률형 아이템(가챠) 정보를 안내하는 한국어 도우미입니다. "
    f"항상 {MAX_RESPONSE_LENGTH}자 이내로 핵심만 간결하게 답하세요. "
    "이전 대화의 맥락을 이어서 답변하세요."
)


class ChatbotAgent:
    """
    OpenAI 기반 챗봇 에이전트 (멀티턴 컨텍스트 유지)
    """

    def __init__(self, model: str | None = None):
        repo_root = Path(__file__).resolve().parent.parent
        env_path = repo_root / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY가 없습니다. .env 또는 환경변수에 설정하세요.")

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.client = OpenAI(api_key=api_key)
        # 대화 히스토리: [{"role": "user"/"assistant", "content": str}, ...]
        self.history: list[dict] = []
        logger.info("ChatbotAgent 초기화: 모델=%s", self.model)

    def reset_history(self) -> None:
        """대화 컨텍스트를 초기화 (클리어 버튼에서 호출)."""
        self.history.clear()
        logger.info("대화 히스토리 초기화됨")

    def ask(self, question: str, system_prompt: str | None = None) -> str:
        if not question or not question.strip():
            raise ValueError("질문 내용을 입력해야 합니다.")

        logger.info("질문 전송: %s", question)
        # 누적된 히스토리 + 이번 질문을 함께 전달하여 맥락을 유지
        messages = self.history + [{"role": "user", "content": question}]
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt or DEFAULT_SYSTEM_PROMPT,
            input=messages,
        )

        answer = response.output_text.strip()
        logger.info("응답 수신 (길이=%d)", len(answer))
        if len(answer) > MAX_RESPONSE_LENGTH:
            logger.info("응답이 %d자를 초과하여 요약 요청합니다.", MAX_RESPONSE_LENGTH)
            # 모델에게 요약을 요청하여 100자 이내로 간결히 반환받음
            summary_prompt = f"다음 내용을 {MAX_RESPONSE_LENGTH}자 이내로 간결히 요약해줘:\n\n{answer}"
            summary_resp = self.client.responses.create(
                model=self.model,
                input=summary_prompt,
            )
            answer = summary_resp.output_text.strip()
            # 안전장치: 그래도 길면 자름
            if len(answer) > MAX_RESPONSE_LENGTH:
                answer = answer[:MAX_RESPONSE_LENGTH]

        # 최종 답변(요약본)을 히스토리에 기록하여 다음 턴의 맥락으로 사용
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def health_check(self) -> str:
        response = self.client.responses.create(model=self.model, input="안녕하세요")
        return response.output_text
