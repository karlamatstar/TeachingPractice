import os
import pytest
from loguru import logger
from playwright.sync_api import sync_playwright

def test_web_ui_e2e_capture():
    logger.info("[시작] 시나리오: UI 이벤트 추적 및 화면 캡처 자동화")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_page()
        
        try:
            server_url = os.environ.get("TARGET_SERVER_URL", "http://127.0.0.1:8000")
            context.goto(f"{server_url}/docs")
            context.wait_for_load_state("networkidle")
            logger.info(f"접속 성공 웹 타이틀: {context.title()}")
            
            output_img_path = "outputs/evidence_screen.png"
            context.screenshot(path=output_img_path)
            logger.info(f"[E2E 증적 저장] 파일 경로: {output_img_path}")
            
            assert "API" in context.title() or "Swagger" in context.title()
            
        except Exception as e:
            logger.error(f"[E2E 결함] 웹 UI 제어 중 에러 발생: {e}")
            raise e
        finally:
            browser.close()
