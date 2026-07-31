import time

# 도구(Tools) 정의
def turn_on_do_not_disturb(): return "💡 [Action] 메신저를 '방해 금지 모드'로 전환했습니다."
def prepare_meeting_room(): return "💡 [Action] 화상회의 툴(Zoom)을 미리 실행하고 대기합니다."
def order_coffee(): return "💡 [Action] 사용자가 선호하는 아이스 아메리카노 주문을 완료했습니다."
def send_daily_report(): return "💡 [Action] 금일 업무 요약 보고서를 작성하여 공유했습니다."

# 가짜 에이전트 판단 로직 (규칙 기반 시뮬레이션)
def mock_agent_reasoning(context_data):
    current_time = context_data["current_time"]
    calendar = context_data["calendar"]
    user_status = context_data["user_status"]
    
    # 상황(Context)을 분석하여 스스로 행동을 결정하는 로직
    if "회의" in calendar and "08:45" in current_time:
        return {
            "reasoning": "15분 뒤에 중요한 회의가 예정되어 있으므로 화상회의 환경을 미리 준비합니다.",
            "action": prepare_meeting_room
        }
    elif "집중 근무" in user_status:
        return {
            "reasoning": "사용자가 집중 근무 중이며 스트레스 지수가 높으므로 리프레시용 커피를 주문합니다.",
            "action": order_coffee
        }
    elif "17:50" in current_time:
        return {
            "reasoning": "퇴근 시간이 임박했고 소스코드 커밋이 완료되었으므로 일일 보고서를 제출합니다.",
            "action": send_daily_report
        }
    return {"reasoning": "현재는 스스로 개입할 필요가 없습니다.", "action": None}

# 실행부
scenarios = [
    {"current_time": "오전 08:45", "calendar": "09:00 - 주간 기획 회의", "user_status": "출근 완료", "device_log": ""},
    {"current_time": "오전 11:30", "calendar": "일정 없음", "user_status": "30분째 집중 근무 모드", "device_log": ""},
    {"current_time": "오후 17:50", "calendar": "일정 없음", "user_status": "업무 마무리 중", "device_log": ""}
]

for i, context in enumerate(scenarios, 1):
    print(f"\n=== 시나리오 {i} ===")
    print(f"[🔄 에이전트 센싱 중...] 현재 시간: {context['current_time']}")
    
    decision = mock_agent_reasoning(context)
    print(f"🤖 [에이전트 생각]: {decision['reasoning']}")
    
    if decision["action"]:
        print(decision["action"]())
    time.sleep(1)