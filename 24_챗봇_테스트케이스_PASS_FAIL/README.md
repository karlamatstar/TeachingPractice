# 챗봇 테스트케이스 PASS FAIL

동일 챗봇의 실패·통과 변형을 같은 테스트로 실행하고 결과 차이를 확인하는 실습입니다.

## 학습 위치

- 강의 제목: 테스트 케이스 도출 / 테스트 실행 프로세스
- 강의 순서: 2026-06-12 \~ 2026-06-15 · 12\~13일차
- 난이도: 초급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/fail/app.py`
- `src/pass/app.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)을 구성하고 `src/fail`, `src/pass`의 각 `requirements.txt`를 설치해야 합니다.
- 챗봇 응답과 평가를 재실행하려면 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "src/fail/requirements.txt"`
- Python: `python -m pip install -r "src/pass/requirements.txt"`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
