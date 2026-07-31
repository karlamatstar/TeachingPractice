# RAIT Pytest E2E 자동화

API Judge와 UI E2E를 pytest로 검증하고 결함 보고서 증거를 생성하는 실습입니다.

## 프로젝트별 학습 요약

- 해결하려던 문제: API의 상태 코드와 응답 시간만으로는 AI 답변 품질과 웹 화면 동작을 함께 확인하기 어렵습니다.
- 구현한 QA 흐름: FastAPI `/chat` 응답을 매개변수화된 pytest와 LLM Judge로 평가하고, Playwright로 Swagger UI 접속과 화면 증거 생성을 확인합니다.
- 사용 기술: FastAPI, pytest, httpx, OpenAI API, Playwright, Loguru
- 확인한 결과: API Judge 로그, UI 화면 증거와 HTML 결함 보고서가 `_OUTPUT`에 구분되어 있습니다.
- 한계와 개선 방향: 외부 Judge와 브라우저 바이너리가 필요하므로, Judge를 사용할 수 없을 때의 N/A 처리와 증거 파일 경로 규칙을 더 명확히 정할 수 있습니다.

## 학습 위치

- 강의 제목: AI Agent 품질 프레임워크 테스트 자동화
- 강의 순서: 2026-06-09 \~ 2026-06-10 · 9\~10일차
- 난이도: 중급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/app/main.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)을 구성하고 `requirements.txt`의 pytest·Playwright 모듈을 설치해야 합니다.
- UI E2E 테스트에는 `python -m playwright install chromium`으로 별도 브라우저 바이너리를 준비해야 하며, API Judge에는 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
