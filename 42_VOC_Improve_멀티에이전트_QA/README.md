# VOC Improve 멀티에이전트 QA

VOC 분석·개선 Agent와 독립 LLM Judge, 교차검증, GUI·보고서를 통합한 프로젝트입니다.

## 프로젝트별 학습 요약

- 해결하려던 문제: 여러 Agent가 만든 VOC 분석과 개선안을 내부 평가만으로 판단하지 않고, 원문 근거와 독립된 기준으로 검증해야 합니다.
- 구현한 QA 흐름: Interpreter·Retriever·Summarizer·Evaluator·Critic·Improver가 VOC를 처리하고, pytest·독립 LLM Judge·교차검증이 결과와 장애 대응을 점검합니다.
- 사용 기술: Python, gRPC, Protocol Buffers, OpenAI API, Anthropic API, pytest
- 확인한 결과: 테스트 설정과 루브릭, Judge CSV, 품질 점수 Markdown 및 두 종류의 DOCX 결과 문서가 역할별 폴더에 보존되어 있습니다.
- 한계와 개선 방향: 모델 조합과 외부 API 상태가 평가 결과 및 응답 시간에 영향을 주므로, 미평가 N/A와 기능 결함을 분리하고 같은 VOC 세트로 모델 조합을 비교할 수 있습니다.

## 학습 위치

- 강의 제목: VOC Improve 및 QA 프로젝트
- 강의 순서: 2026-07-13 \~ 2026-07-16 · 33\~36일차
- 난이도: 고급

## 폴더 구성

- `src`: 실행 코드와 실습 단계
- `_DOCS`: 설명서, 계획서, 의존성 안내
- `_OUTPUT`: 실행 결과, 로그, 리포트와 과거 산출물
- `.env` 또는 `.env.example`: 필요한 경우 사용하는 환경변수 파일
- 설치 목록 파일: 프로젝트 루트 또는 `src` 하위의 `requirements.txt`, `package.json`, `pyproject.toml` 등

## 주요 실행 진입점

- `main.py`
- `RUN/run_gui.py`

세부 실행법이 원래 문서에 있었던 프로젝트는 `_DOCS/기존_상세안내.md`에 보존했습니다. 교재형 실습은 프로젝트 루트에서 `Set-Location src` 후 각 챕터의 코드를 실행하면 상대 경로를 유지할 수 있습니다.

## 실행 환경 안내

- Python 가상환경(`.venv`)에서 `pyproject.toml` 기반 패키지를 설치해야 하며, 에이전트 간 통신에는 gRPC·Protocol Buffers 도구가 사용됩니다.
- 실제 Agent와 독립 Judge 실행에는 `OPENAI_API_KEY`와 `ANTHROPIC_API_KEY`가 필요합니다.

## 의존성 설치

- Python 패키지: ``python -m pip install -e .``

## 산출물

새로 생성되는 로그·평가표·리포트는 `_OUTPUT`에 저장하도록 정리했습니다. 단계별 원본 코드는 `src/stage_*`에서 확인할 수 있습니다.
