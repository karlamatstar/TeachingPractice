# 단계 자료 설명

`src/runner/agent_caller.py`와 `src/utils/logger.py`는 후속 확장을 위해 자리만 잡은 기초 골격입니다. 이 단계의 실제 평가 흐름은 `src/main.py`, `src/runner/llm_judge.py`, `src/engine`과 `config`에서 확인할 수 있습니다. Agent 호출기와 공통 로거의 구현은 품질평가 엔진을 외부 서비스와 연결할 때 이어서 확장하면 됩니다.
