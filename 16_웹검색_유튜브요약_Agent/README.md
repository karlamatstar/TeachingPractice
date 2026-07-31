# 웹검색 유튜브요약 Agent

DuckDuckGo·Tavily 웹 검색과 YouTube 요약을 Agent 화면에 연결하는 실습입니다.

## 학습 위치

- 강의 제목: 검색 도구 Agent 확장 실습
- 학습 흐름: 검색·요약 Agent 활용
- 난이도: 초급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/chap10/sec01/duckduckgo_search.ipynb`
- `src/chap10/sec02/tavily_search.ipynb`
- `src/chap10/sec03/youtbe_summary.ipynb`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)과 Jupyter Notebook 환경을 구성하고 `requirements.txt`의 검색·영상 처리 모듈을 설치해야 합니다.
- 웹 검색·YouTube 자료 조회와 외부 모델 호출에는 인터넷 연결 및 예제에서 사용하는 서비스 인증정보가 필요할 수 있습니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
