# AI Agent 운영모니터링

FastAPI 로그·메트릭·테스트·Prometheus·부하 측정을 연결하는 실습입니다.

## 프로젝트별 학습 요약

- 해결하려던 문제: AI Agent API의 정상 응답 여부뿐 아니라 오류율, 응답 시간과 부하 상황을 같은 기준으로 관찰해야 합니다.
- 구현한 QA 흐름: FastAPI 요청을 로그와 Prometheus 메트릭으로 기록하고, 기능 테스트와 k6 부하 측정 결과를 별도 산출물로 남겨 운영 상태를 확인합니다.
- 사용 기술: FastAPI, pytest, Prometheus, Grafana, k6, Streamlit, Docker Compose
- 확인한 결과: Agent 로그, 기능 테스트 JSON, k6 요약 JSON과 성능 판정 문서가 `_OUTPUT`에 구분되어 있습니다.
- 한계와 개선 방향: 모니터링 전체 구성을 확인하려면 Docker 환경이 필요하며, 오류율·지연시간·처리량 임계값을 테스트와 대시보드에서 동일하게 관리할 필요가 있습니다.

## 학습 위치

- 강의 제목: IT 운영·모니터링 실무(1~4)
- 강의 순서: 2026-06-29 \~ 2026-07-02 · 23\~26일차
- 난이도: 중급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/app.py`
- `tests/run_tests.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python API·테스트는 가상환경(`.venv`)과 `requirements.txt` 설치가 필요합니다.
- Prometheus·Grafana 모니터링 구성을 사용하려면 Docker Desktop 또는 Docker Engine과 Docker Compose가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`
- 컨테이너: `docker compose -f "docker-compose.yml" up --build`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
