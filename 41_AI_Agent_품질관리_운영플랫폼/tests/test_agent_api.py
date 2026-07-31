"""실제 OpenAI API를 호출하는 통합 테스트입니다 (비용/지연 발생, 소수 케이스만 유지)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_returns_answer_for_valid_question():
    response = client.post("/chat", json={"question": "이 교육과정은 총 몇 시간인가요?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"].strip() != ""
    assert "320시간" in body["answer"]
    # 비교용 규칙 기반 답변도 함께 반환된다
    assert body["rule_answer"].strip() != ""
    assert "320시간" in body["rule_answer"]


def test_chat_rejects_empty_question():
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422
