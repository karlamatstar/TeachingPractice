"""JupyterLab 셀에서 불러와 테스트할 수 있는 보조 예제"""

from agent_app import build_agent
from main import extract_answer

agent = build_agent()

# JupyterLab 셀에서 아래 두 줄을 실행하세요.
# result = agent.invoke({"messages": [{"role": "user", "content": "서울 날씨 알려주고 25*4도 계산해줘"}]})
# extract_answer(result)
