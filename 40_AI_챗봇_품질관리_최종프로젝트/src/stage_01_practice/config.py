import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = PROJECT_DIR / "_OUTPUT" / "stage_01_practice" / "reports"

load_dotenv(PROJECT_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVICE_MODEL = "gpt-4o-mini"
JUDGE_MODEL = "gpt-4o-mini"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
