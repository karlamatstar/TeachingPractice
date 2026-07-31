# 역할은 다음과 같습니다.

# 프로젝트 경로 관리
# .env 파일 읽기
# API Key 읽기
# 결과 저장 폴더 자동 생성

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = PROJECT_DIR / "_OUTPUT" / "stage_00_reference" / "reports"

# 프로젝트 최상위 .env 파일 읽기
load_dotenv(PROJECT_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def validate_config() -> None:
    """실행 전 API 키와 필수 폴더를 점검합니다."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY가 없습니다. "
            ".env 파일에 OPENAI_API_KEY=발급받은키 형식으로 입력하세요."
        )

    DATA_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
