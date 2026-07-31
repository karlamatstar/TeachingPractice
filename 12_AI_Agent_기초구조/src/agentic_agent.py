import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from openai import OpenAI

# 프로젝트 최상위 .env 파일로부터 환경 변수 로드
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ==========================================
# 1. 가상의 외부 도구(Tool) 정의
# ==========================================

def get_weather_forecast(location):
    """날씨 정보를 가져오는 모의(Mock) 함수"""
    print(f"\n[Tool Action] 'get_weather_forecast' 호출됨 (위치: {location})")
    # 실제 환경에서는 날씨 API를 호출하나, 여기서는 테스트용 고정 데이터 반환
    return {"location": location, "forecast": "맑음", "temperature": "24°C"}

def search_place(query):
    """장소/맛집을 검색하는 함수 (Serper API 활용 및 Fallback)"""
    print(f"\n[Tool Action] 'search_place' 호출됨 (검색어: {query})")
    
    # Serper API 키가 있으면 실제 검색을 수행하고, 없으면 Mock 데이터 반환
    if SERPER_API_KEY and SERPER_API_KEY != "your_serper_api_key_here":
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "gl": "kr", "hl": "ko"})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            results = response.json()
            # 간단하게 유기적인 텍스트로 요약하기 위해 top 3 유기적 검색 결과 추출
            organic = results.get("organic", [])[:3]
            return [{"title": item.get("title"), "snippet": item.get("snippet")} for item in organic]
        except Exception as e:
            return f"검색 중 오류 발생: {str(e)}"
    else:
        # Mock 데이터 (이미지 79페이지의 최종 답변 예시 기준)
        return [
            {"title": "황리단길 도그카페", "snippet": "반려견 입장 가능, 가족 단위 손님에게 인기입니다."},
            {"title": "교촌마을 한우명가", "snippet": "넓은 실내와 가족 테이블을 보유하고 있습니다."},
            {"title": "월정교 근처 라이스워드", "snippet": "반려견 동반 테라스를 운영 중입니다."}
        ]

# OpenAI API에 전달할 함수 목록 스펙 (Function Calling)
functions = [
    {
        "name": "get_weather_forecast",
        "description": "특정 지역의 날씨 예보 정보를 가져옵니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "날씨를 조회할 지역 (예: 경주, 서울)"}
            },
            "required": ["location"]
        }
    },
    {
        "name": "search_place",
        "description": "특정 조건이나 목적에 맞는 장소나 맛집을 검색합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 키워드 (예: 경주 맛집, 반려견 동반 식당)"}
            },
            "required": ["query"]
        }
    }
]

# ==========================================
# 2.Memory 세팅 (이미지 기준(기 제시된)이력 주입)
# ==========================================
chat_history = [
    {"role": "system", "content": "복합 요청은 subgoal로 나누고 tool을 호출하세요. 사용자의 이전 맥락(가족 구성원, 반려동물 여부, 여행 계획 등)을 항상 기억하고 답변에 반영하세요."},
    {"role": "user", "content": "가족은 엄마, 아빠, 반려견 뭉치야"},
    {"role": "assistant", "content": "가족 구성원은 엄마, 아빠, 그리고 뭉치(반려견)이시군요."},
    {"role": "user", "content": "이번 주말에 엄마랑 경주 여행 가기로 했어"},
    {"role": "assistant", "content": "경주에서의 주말 여행을 계획하고 계시군요!"}
]

# 새로운 사용자 입력 (Input)
user_input = "경주 가족여행 맛집 추천해줘"
chat_history.append({"role": "user", "content": user_input})

print(f"사용자 입력: '{user_input}'")
print("-" * 50)

# ==========================================
# 3. Subgoal Decomposition & Tool Selection
# ==========================================
print("[Step 1] Subgoal Decomposition 진행 중...")

# openai>=1.0.0 버전 문법에 맞게 수정된 호출부
response = client.chat.completions.create(
    model="gpt-4o",  # 이미지의 gpt-4o 반영
    messages=chat_history,
    functions=functions,
    function_call="auto"
)

msg = response.choices[0].message
# 대화 이력에 에이전트의 중간 판단 결과 추가
chat_history.append(msg)

# ==========================================
# 4. Tool Orchestration & Fallback 처리
# ==========================================
print("[Step 2] Tool Orchestration 및 실행...")

if msg.function_call:
    name = msg.function_call.name
    args = json.loads(msg.function_call.arguments)
    
    if name == "get_weather_forecast":
        result = get_weather_forecast(**args)
        chat_history.append({
            "role": "function",
            "name": name,
            "content": json.dumps(result, ensure_ascii=False)
        })
        
    elif name == "search_place":
        result = search_place(**args)
        chat_history.append({
            "role": "function",
            "name": name,
            "content": json.dumps(result, ensure_ascii=False)
        })
        
    else:
        # Fallback 처리: 정의되지 않은 함수 호출 시 또는 매칭 실패 시 serper 검색 활용 유도
        print(f"\n[Fallback] 정의되지 않은 함수 '{name}' 가 호출되어 대안 검색을 실행합니다.")
        result = search_place(query=user_input)
        chat_history.append({
            "role": "function",
            "name": "search_place",
            "content": f"관련 정보를 검색해드릴게요:\n{json.dumps(result, ensure_ascii=False)}"
        })
else:
    # Function Call이 일어나지 않고 바로 텍스트 답변이 나온 경우
    result = msg.content
    print("\n[Direct Response] 모델이 도구를 호출하지 않고 바로 답변했습니다.")

# ==========================================
# 5. Output 생성 (최종 답변 도출)
# ==========================================
print("-" * 50)
print("[Step 3] 최종 답변(Output) 생성 중...")

final_response = client.chat.completions.create(
    model="gpt-4o",
    messages=chat_history
)

print("\n## 최종 답변 예시 ##")
print(final_response.choices[0].message.content)
