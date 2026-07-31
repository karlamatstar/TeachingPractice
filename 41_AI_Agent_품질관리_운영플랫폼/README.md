# AI Agent 품질관리 운영플랫폼

API·Judge·품질 파이프라인·성능시험·Prometheus·Grafana·대시보드를 통합한 운영 플랫폼입니다.

## 프로젝트별 학습 요약

- 해결하려던 문제: 기능, AI 답변 품질, 성능, 장애 대응과 운영 메트릭이 분리되어 있으면 같은 실행의 상태를 종합적으로 추적하기 어렵습니다.
- 구현한 QA 흐름: FastAPI 서비스와 규칙 검증·LLM Judge를 품질 파이프라인으로 묶고, pytest와 k6 시나리오 및 Prometheus·Grafana·Streamlit 관측 화면을 연결합니다.
- 사용 기술: FastAPI, pytest, OpenAI API, k6, Prometheus, Grafana, Streamlit, Docker Compose
- 확인한 결과: 품질평가 CSV·JSON·Markdown, Smoke·Load·Stress·Spike·장애 시험 결과와 관측 설정이 용도별로 정리되어 있습니다.
- 한계와 개선 방향: 외부 모델과 Docker 서비스 상태에 따라 일부 검증을 수행할 수 없으므로, 실행 ID·N/A 조건·중단 기준을 공통 운영 규칙으로 관리할 수 있습니다.

## 학습 위치

- 강의 제목: IT 운영·모니터링 실무(5~8)
- 강의 순서: 2026-07-03 \~ 2026-07-09 · 27\~31일차
- 난이도: 고급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `app/main.py`
- `scripts/run_api_disconnect_test.py`
- `scripts/run_performance_tests.py`
- `scripts/run_validation_tests.py`
- `src/stage_01_foundation/app/main.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python API·대시보드는 가상환경(`.venv`)과 루트 또는 단계별 `requirements.txt` 설치가 필요합니다.
- API·Prometheus·Grafana 통합 구성을 사용하려면 Docker Desktop 또는 Docker Engine과 Docker Compose가 필요하며, 실제 모델 평가에는 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`
- Python: `python -m pip install -r "src/stage_01_foundation/requirements.txt"`
- 컨테이너: `docker compose -f "docker-compose.yml" up --build`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
