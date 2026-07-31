from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


train_data = [
    {"text": "손흥민 경기 결과 알려줘", "label": "sports_agent"},
    {"text": "어제 축구 경기 누가 이겼어?", "label": "sports_agent"},
    {"text": "야구 점수 알려줘", "label": "sports_agent"},
    {"text": "한국 대표팀 경기 일정 알려줘", "label": "sports_agent"},
    {"text": "농구 경기 결과 궁금해", "label": "sports_agent"},
    {"text": "오늘 축구 몇 시에 해?", "label": "sports_agent"},
    {"text": "김민재 선수 소속팀 알려줘", "label": "sports_agent"},
    {"text": "월드컵 경기 일정 보여줘", "label": "sports_agent"},
    {"text": "야구 순위 알려줘", "label": "sports_agent"},
    {"text": "손흥민 골 넣었어?", "label": "sports_agent"},

    {"text": "지금 몇 시야?", "label": "timer_agent"},
    {"text": "현재 시간 알려줘", "label": "timer_agent"},
    {"text": "5분 타이머 맞춰줘", "label": "timer_agent"},
    {"text": "10분 후에 알려줘", "label": "timer_agent"},
    {"text": "30분 알람 설정해줘", "label": "timer_agent"},
    {"text": "서울 시간 알려줘", "label": "timer_agent"},
    {"text": "뉴욕은 지금 몇 시야?", "label": "timer_agent"},
    {"text": "1시간 타이머 해줘", "label": "timer_agent"},
    {"text": "내일 아침 7시에 깨워줘", "label": "timer_agent"},
    {"text": "회의 시작까지 몇 분 남았어?", "label": "timer_agent"},

    {"text": "피자 주문하고 싶어", "label": "order_agent"},
    {"text": "치킨 배달 가능한가요?", "label": "order_agent"},
    {"text": "햄버거 주문해줘", "label": "order_agent"},
    {"text": "짜장면 한 그릇 시켜줘", "label": "order_agent"},
    {"text": "커피 주문하고 싶어요", "label": "order_agent"},
    {"text": "배달 언제 와요?", "label": "order_agent"},
    {"text": "주문 취소하고 싶어", "label": "order_agent"},
    {"text": "결제가 안 돼요", "label": "order_agent"},
    {"text": "내 주문 내역 보여줘", "label": "order_agent"},
    {"text": "피자 두 판 주문해줘", "label": "order_agent"},

    {"text": "안녕하세요", "label": "general_chat"},
    {"text": "오늘 기분이 안 좋아", "label": "general_chat"},
    {"text": "재미있는 이야기 해줘", "label": "general_chat"},
    {"text": "인공지능이 뭐야?", "label": "general_chat"},
    {"text": "고마워", "label": "general_chat"},
    {"text": "오늘 날씨 좋네", "label": "general_chat"},
    {"text": "점심 뭐 먹을까?", "label": "general_chat"},
    {"text": "심심해", "label": "general_chat"},
    {"text": "너는 누구야?", "label": "general_chat"},
    {"text": "ㅎㅎㅎㅎ", "label": "general_chat"},
    

]

test_data = [
    {"text": "손흥민 어제 경기 어땠어?", "label": "sports_agent"},
    {"text": "프로야구 순위 알려줘", "label": "sports_agent"},
    {"text": "축구 경기 몇 시에 시작해?", "label": "sports_agent"},
    {"text": "농구 결과 보여줘", "label": "sports_agent"},

    {"text": "15분 타이머 설정해줘", "label": "timer_agent"},
    {"text": "한국 시간 지금 몇 시야?", "label": "timer_agent"},
    {"text": "20분 뒤에 알려줘", "label": "timer_agent"},
    {"text": "알람 맞춰줘", "label": "timer_agent"},

    {"text": "치킨 한 마리 주문해줘", "label": "order_agent"},
    {"text": "피자 배달 시켜줘", "label": "order_agent"},
    {"text": "결제 방법 알려줘", "label": "order_agent"},
    {"text": "주문을 취소하고 싶어요", "label": "order_agent"},

    {"text": "오늘 너무 피곤해", "label": "general_chat"},
    {"text": "좋은 말 해줘", "label": "general_chat"},
    {"text": "반가워", "label": "general_chat"},
    {"text": "ㅋㅋㅋㅋ", "label": "general_chat"},
]

edge_test_data = [
    {
        "text": "손흥민 경기 결과",
        "expected_label": "sports_agent",
        "test_type": "오타 및 짧은 표현"
    },
    {
        "text": "손흥민 경긱 결과 알려줘",
        "expected_label": "sports_agent",
        "test_type": "오타"
    },
    {
        "text": "피자 주문하고 5분 타이머 맞춰줘",
        "expected_label": "order_agent",
        "test_type": "복합 의도"
    },
    {
        "text": "오늘 축구 몇 시에 해?",
        "expected_label": "sports_agent",
        "test_type": "스포츠와 시간 혼합"
    },
    {
        "text": "방탄소년단 신곡 틀어줘",
        "expected_label": "general_chat",
        "test_type": "미지원 기능"
    },
    {
        "text": "ㅋㅋㅋㅋㅋㅋ",
        "expected_label": "general_chat",
        "test_type": "의미 없는 입력"
    },
    {
        "text": "피자 주문 언제 도착해?",
        "expected_label": "order_agent",
        "test_type": "주문 상태 확인"
    },
    {
        "text": "뉴욕 시간 알려주고 축구 결과도 알려줘",
        "expected_label": "timer_agent",
        "test_type": "복합 의도"
    },
]

pd.DataFrame(train_data).to_csv(
    DATA_DIR / "train_data.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame(test_data).to_csv(
    DATA_DIR / "test_data.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame(edge_test_data).to_csv(
    DATA_DIR / "edge_test_data.csv",
    index=False,
    encoding="utf-8-sig"
)
