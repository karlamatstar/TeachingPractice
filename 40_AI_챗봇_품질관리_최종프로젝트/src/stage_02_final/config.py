import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = PROJECT_DIR / "_OUTPUT" / "stage_02_final" / "reports"
LOG_DIR = PROJECT_DIR / "_OUTPUT" / "stage_02_final" / "log"

load_dotenv(PROJECT_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def validate_config() -> None:
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY가 없습니다. "
            "프로젝트 최상위 .env 파일에 OPENAI_API_KEY=발급받은키 형식으로 입력하세요."
        )
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
