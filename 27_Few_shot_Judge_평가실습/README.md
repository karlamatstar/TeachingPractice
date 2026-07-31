# Few shot Judge 평가실습

루브릭과 Few-shot 예시를 적용해 테스트 실행·실패 재실행·보고를 연결하는 실습입니다.

## 학습 위치

- 강의 제목: 루브릭 기반 Judge Prompt 설계 / Few-shot Judge
- 강의 순서: 2026-06-18 \~ 2026-06-22 · 16\~18일차
- 난이도: 중급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/test_runner.py`
- `src/what_time_is_it_terminal.py`
- `src/what_time_is_it_streamlit.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)을 구성하고 `requirements.txt`의 OpenAI·Streamlit·웹 조회 모듈을 설치해야 합니다.
- Judge와 챗봇 호출에는 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`

## 산출물

테스트 실행기가 생성하는 Markdown 결과서는 `_OUTPUT/test_report.md`에 저장됩니다. 기본본과 ALT 변형을 포함한 실행 코드는 `src`에서 확인할 수 있습니다.
