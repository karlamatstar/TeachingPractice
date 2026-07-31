import pytest
import os
from loguru import logger

@pytest.fixture(scope="session", autouse=True)
def setup_testing_env():
    """RaiT 테스트 프로세스를 위한 로그 파일 정의 및 초기화"""
    os.makedirs("outputs", exist_ok=True)
    logger.add(
        "outputs/rait_quality.log", 
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
        level="INFO",
        rotation="10 MB"
    )
    logger.info("=== RaiT (Reliable AI Testing) 프로세스 시작 ===")
    os.environ["TARGET_SERVER_URL"] = "http://127.0.0.1:8000"
    yield
    logger.info("=== RaiT (Reliable AI Testing) 프로세스 종료 ===")
