# AI 챗봇 품질관리 최종프로젝트

참고본·실습본·최종본을 나란히 보존해 챗봇 품질평가와 대시보드 발전 과정을 확인하는 프로젝트입니다.

## 프로젝트별 학습 요약

- 해결하려던 문제: 규칙 기반 챗봇과 API 기반 챗봇의 답변을 같은 테스트 케이스와 평가 기준으로 비교할 수 있어야 합니다.
- 구현한 QA 흐름: 테스트 케이스를 두 챗봇에 적용하고, 규칙 검증과 LLM Judge 결과를 모아 CSV·JSON·Markdown으로 저장한 뒤 대시보드에서 확인합니다.
- 사용 기술: Python, OpenAI API, pandas, Streamlit, Plotly
- 확인한 결과: 참고본·실습본·최종본의 코드 단계와 최종 실행의 평가 데이터, 로그 및 품질 보고서가 함께 보존되어 있습니다.
- 한계와 개선 방향: 단계별 모델·루브릭·테스트 데이터 조건을 동일하게 비교할 수 있도록 실행 설정과 테스트 ID를 하나의 매니페스트로 관리할 수 있습니다.

## 학습 위치

- 강의 제목: IT 운영·모니터링 실무 프로젝트
- 강의 순서: 2026-07-01 \~ 2026-07-03 · 25\~27일차
- 난이도: 고급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/stage_00_reference/main.py`
- `src/stage_01_practice/main.py`
- `src/stage_02_final/main.py`
- `src/stage_02_final/dashboard/run_dashboard.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)을 구성하고 참고본·실습본·최종본의 각 `requirements.txt`를 목적에 맞게 설치해야 합니다.
- 실제 챗봇과 Judge 호출에는 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`
- Python: `python -m pip install -r "src/stage_00_reference/requirements.txt"`
- Python: `python -m pip install -r "src/stage_01_practice/requirements.txt"`
- Python: `python -m pip install -r "src/stage_02_final/requirements.txt"`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
