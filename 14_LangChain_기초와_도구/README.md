# LangChain 기초와 도구

메시지 기록, LCEL, Pydantic 도구, 스트리밍과 Streamlit 연동을 다루는 실습입니다.

## 학습 위치

- 강의 제목: LangChain 구성 요소 확장 실습
- 학습 흐름: LangChain 구성 요소와 도구 활용
- 난이도: 초급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `src/chap08/sec01/langchain_chatbot.ipynb`
- `src/chap08/sec01/langchain_message_history.ipynb`
- `src/chap08/sec02/lcel.ipynb`
- `src/chap08/sec03/langchain_tool.ipynb`
- `src/chap08/sec03/pydantic.ipynb`
- `src/chap08/sec04/langchain_tool_stream.ipynb`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)과 Jupyter Notebook 환경을 구성하고 `requirements.txt`의 LangChain 모듈을 설치해야 합니다.
- 외부 모델을 호출하는 단계에는 `OPENAI_API_KEY`가 필요합니다.

## 의존성 설치

- Python: `python -m pip install -r "requirements.txt"`

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
