from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="RaiT 실습용 AI 에이전트 서버")

class ChatRequest(BaseModel):
    message: str
    role: str = "CS 안내 에이전트"

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    msg = request.message
    
    # [결함 시뮬레이션] 특정 키워드 조건에 따라 일부러 불친절한 답변 출력
    if "환불" in msg and "영수증" not in msg:
        reply = "환불 안 됩니다. 규정 보시든가요."
    elif "배송" in msg:
        reply = f"안녕하세요! {request.role}입니다. 주문하신 상품의 배송 지연으로 불편을 드려 죄송합니다. 택배사 확인 후 빠르게 안내해 드리겠습니다."
    else:
        reply = f"안녕하세요. {request.role}입니다. 무엇을 도와드릴까요?"
        
    latency_ms = int((time.time() - start_time) * 1000)
    
    return {
        "status": "success",
        "reply": reply,
        "latency_ms": latency_ms
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
