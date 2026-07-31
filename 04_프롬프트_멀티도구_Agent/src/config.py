"""환경변수 설정 파일"""

from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """프로그램 실행에 필요한 환경 설정"""

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    serper_api_key: str | None = os.getenv("SERPER_API_KEY")


settings = Settings()


def validate_required_env() -> None:
    """필수 환경변수가 없으면 실행 전에 명확한 오류를 발생시킵니다."""

    missing = []
    if not settings.openai_api_key:
        missing.append("OPENAI_API_KEY")

    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"필수 환경변수가 없습니다: {joined}")
