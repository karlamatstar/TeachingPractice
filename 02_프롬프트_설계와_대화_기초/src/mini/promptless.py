import os
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 1. API 키 설정 (.env 파일에서 OPENAI_API_KEY를 가져옵니다)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY가 .env에서 설정되지 않았습니다.")
os.environ["OPENAI_API_KEY"] = openai_api_key


# 2. 에이전트가 사용할 도구(Tools) 정의
def turn_on_do_not_disturb():
    return "💡 [Action] 메신저를 '방해 금지 모드'로 전환하고, 알림을 차단했습니다."

def prepare_meeting_room():
    return "💡 [Action] 캘린더의 회의 링크를 분석하여 화상회의 툴(Zoom)을 미리 실행하고 대기합니다."

def order_coffee():
    return "💡 [Action] 사용자가 선호하는 아이스 아메리카노 주문을 완료했습니다. (픽업 예정)"

def send_daily_report():
    return "💡 [Action] 금일 업무 요약 보고서를 작성하여 팀 채널에 공유했습니다."

# 도구 매핑 딕셔너리
TOOLS = {
    "TURN_ON_DND": turn_on_do_not_disturb,
    "PREPARE_MEETING": prepare_meeting_room,
    "ORDER_COFFEE": order_coffee,
    "SEND_REPORT": send_daily_report
}

# 3. 프롬프트리스 자율 판단 LLM 정의
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 핵심: 사용자의 프롬프트가 아니라 '상황(Context)'을 주입받아 스스로 판단하도록 유도
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    당신은 사용자의 명령 없이 상황을 인지해 작동하는 '프롬프트리스 에이전트'입니다.
    현재 제공된 '사용자의 맥락 데이터(Context)'를 분석하여, 지금 사용자에게 가장 필요한 조치가 무엇인지 판단하세요.
    
    실행 가능한 작업 목록:
    - TURN_ON_DND: 집중이 필요하거나 회의 중일 때 방해금지 모드 켜기
    - PREPARE_MEETING: 곧 중요한 회의가 시작될 때 회의 환경 준비하기
    - ORDER_COFFEE: 피로도가 높은 시간대이거나 리프레시가 필요할 때 커피 주문하기
    - SEND_REPORT: 퇴근 시간이 임박했을 때 하루 보고서 전송하기
    
    반드시 아래 JSON 형식으로만 응답하세요:
    {{
        "reasoning": "현재 상황을 분석한 이유",
        "action": "실행할 작업 코드 (TURN_ON_DND, PREPARE_MEETING, ORDER_COFFEE, SEND_REPORT 중 하나, 필요 없으면 NONE)"
    }}
    """),
    ("human", "현재 맥락 데이터:\n{context}")
])

chain = prompt | llm | JsonOutputParser()

# 4. 프롬프트리스 에이전트 실행 함수
def run_promptless_agent(context_data):
    print(f"\n[🔄 에이전트가 주변 맥락 센싱 중...] 현재 시간: {context_data['current_time']}")
    
    # LLM이 상황을 분석하여 스스로 '의도'를 파악
    decision = chain.invoke({"context": str(context_data)})
    
    print(f"🤖 [에이전트 생각]: {decision['reasoning']}")
    
    # 판단에 따른 자율 행동 실행
    action_code = decision.get("action")
    if action_code in TOOLS:
        result = TOOLS[action_code]()
        print(result)
    else:
        print("💡 [Action] 현재는 스스로 개입할 필요가 없다고 판단했습니다.")


## 🏃‍♂️ 실행 가능한 시나리오 테스트
prompt = """
에이전트에게 사용자의 직접적인 명령을 전혀 주지 않고,
사용자의 요청을 분석하여 적절한 도구를 선택하게 하세요.
"""
"에이전트에게 **사용자의 직접적인 명령을 전혀 주지 않고**, 오직 '상황 데이터(Context)'만 바뀐 채로 루프를 돌려보겠습니다."

# 시나리오 시뮬레이션 데이터
scenarios = [
    {
        "current_time": "오전 08:45",
        "calendar": "09:00 - 주간 기획 회의 (임원 참여)",
        "user_status": "출근 완료, PC 구동됨",
        "device_log": "최근 3시간 동안 카페인 섭취 기록 없음"
    },
    {
        "current_time": "오전 11:30",
        "calendar": "일정 없음",
        "user_status": "30분째 집중 근무 모드 (IDE 및 개발 툴 활성화)",
        "device_log": "키보드 타수 급증, 생체 인식상 스트레스 지수 다소 높음"
    },
    {
        "current_time": "오후 17:50",
        "calendar": "일정 없음",
        "user_status": "업무 마무리 중",
        "device_log": "오늘 작성한 소스코드 커밋 완료"
    }
]

# 사용자의 명령 없이 상황 변화만으로 에이전트가 판단하는 과정 출력
for i, context in enumerate(scenarios, 1):
    print(f"\n=== 시나리오 {i} ===")
    run_promptless_agent(context)
    time.sleep(1) # 시뮬레이션 간격