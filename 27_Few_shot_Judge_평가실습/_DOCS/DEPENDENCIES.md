# 의존성 복구 안내

가상환경과 설치된 모듈 폴더는 포함하지 않습니다. 아래 명령으로 필요한 모듈을 다시 설치할 수 있습니다.

- Python: `python -m pip install -r "requirements.txt"`
- 실행 환경: 프로젝트별 Python 가상환경(`.venv`)
- 외부 서비스: Judge와 챗봇 호출 시 `OPENAI_API_KEY`
- 선택 인터페이스: Streamlit

## 권장 순서

1. 프로젝트 최상위에서 `python -m venv .venv`로 가상환경을 만듭니다.
2. `.venv\Scripts\Activate.ps1`로 활성화합니다.
3. 위 설치 명령 중 해당하는 항목을 실행합니다.
4. API가 필요하면 `.env.example`을 참고해 최상위 `.env`를 준비합니다.

`.venv`, `venv`, `node_modules`는 저장하지 않으며 설치 목록 파일만 보존합니다.
