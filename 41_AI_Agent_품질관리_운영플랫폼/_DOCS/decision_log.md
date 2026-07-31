# 프로젝트 의사결정/변경 로그

이 문서는 `ai_agent_quality_platform` 프로젝트를 만들면서 나눴던 대화에서 나온
**결정 사항, 변경 이력, 아직 안 끝난 일**을 정리한 기록입니다. 집에서 여기까지 진행하고
강의실에서 이어서 작업할 예정이라, 다음에 다시 볼 때 맥락을 빠르게 복구하는 용도입니다.

## 1. 프로젝트의 시작 — 어디서 왔나

원래 `ai_quality_final_project`(구 `test` 폴더)라는 별도 프로젝트가 있었고, 거기서:
- 규칙 기반 챗봇 vs API 기반 챗봇을 비교 평가하는 배치 스크립트(`main.py`)
- AI Judge(LLM 심사관)로 5개 항목(정확성/근거성/유용성/안전성/이해성) 채점
- Streamlit 대시보드로 결과 시각화

를 만들어뒀었고, 거기서 2가지를 먼저 개선했습니다:
- **API 호출 실패 시 재시도(3회) + N/A 처리** — 재시도 끝에도 실패하면 "품질이 나쁨(FAIL)"이 아니라
  "채점 자체를 못 함(N/A)"으로 구분해서 통과율 계산이 왜곡되지 않게 함
- **judge_agent의 JSON 파싱 견고화** — 모델이 코드펜스(` ```json `)를 붙여도 파싱되도록

이후 "실시간 챗봇 + Prometheus/Grafana 모니터링"으로 프로젝트를 확장하기로 하면서, 별도 폴더
`ai_agent_quality_platform`을 새로 만들어 지금 이 프로젝트로 넘어왔습니다.

## 2. 확정된 설계 결정 사항

프로젝트를 새로 짤 때 사용자가 명시적으로 확정한 것들입니다.

| 항목 | 결정 | 이유 |
|---|---|---|
| API 키 | `ai_quality_final_project`와 동일한 키 재사용 | 새로 발급받을 필요 없음 |
| 테스트 방식 | 실제 OpenAI API 호출 (목(mock) 안 씀) | 진짜 동작을 검증하고 싶음 |
| 결함 관리 | ~~Jira 연동 없음, `_DOCS/defect_report.md`로 문서 관리~~ → **Jira 연동으로 번복** (10장 참고) | 별도 연동 불필요 → 결함 추적 자동화 필요로 재검토 |
| 판정 기준/대시보드 톤 | 기존 프로젝트와 동일 (PASS≥20, REVIEW 15~19, FAIL≤14) | 일관성 유지 |
| 에이전트 구성 | 규칙기반 vs API기반 비교 없이 **단일 API 기반 에이전트**만 서빙 | 실제 배포 가능한 프로덕션 에이전트 하나를 가정 |
| AI Judge 채점 범위 | 큐레이션된 배치 테스트(`quality/test_cases.json`) **+ 실제 사용자 대화도 실시간 채점** | 배포 전 게이트 + 배포 후 운영 모니터링을 모두 원함 |
| 모니터링 스택 | docker-compose로 Prometheus/Grafana를 **실제 컨테이너로 구동** | 로컬에 각각 개별 설치하는 대신 한 번에 재현 가능하게 |

## 3. 아키텍처 핵심 설계 포인트 (질의응답으로 정리된 것들)

- **배치 vs 실시간 평가는 역할이 다르다.**
  - 배치(`quality/quality_pipeline.py` + `test_cases.json`) → 배포 전 회귀 테스트, CSV/JSON/MD 리포트로 남음
  - 실시간(`/chat` 호출마다 백그라운드로 채점) → 배포 후 운영 모니터링, Prometheus/Grafana로 시각화
  - 이 둘은 완전히 별개의 데이터 흐름이며, 대시보드 탭도 이 기준으로 "🔴 실시간"(챗봇과 대화/대화 로그) vs
    "🧪 테스트케이스 사용"(배치 품질 현황/유형별 비교/케이스 상세/종합 리포트)로 시각적으로 분리해뒀다.
- **Prometheus/Grafana는 숫자만, 대화 원문은 로그 파일에.** Prometheus는 시계열 지표 전용 도구라
  개별 대화 내용을 담을 수 없음. 대화 원문·개별 채점 결과는 `logs/conversations.jsonl`,
  `logs/live_evaluations.jsonl`에 남기고, 이건 Streamlit "대화 로그" 탭에서 확인.
- **실시간 채점은 비동기(백그라운드).** `/chat` 응답은 에이전트 답변만 기다리고 바로 반환하며, AI Judge
  채점은 `BackgroundTasks`로 뒤에서 처리 → 사용자 응답 속도에 영향 없음.
- **재시도는 병렬 유지 + 세마포어 상한(5) + 백오프.** "느린 요청 하나가 뒤의 모든 채점을 막는" 순차 큐
  방식은 채택하지 않음 (실시간성을 해치므로). 대신:
  - 동시에 OpenAI로 나가는 호출을 최대 5개로 제한 (`app/concurrency.py`, `threading.Semaphore(5)`)
  - 재시도 사이에 1초→2초 백오프를 둬서 순간적인 rate limit이 풀릴 시간을 확보
  - 완전한 순서 보장이 필요하면(지금은 불필요 판단) 요청마다 고유 ID를 발급해 로그 간 상관관계를
    맞추는 방법이 대안으로 논의됐음 (미구현, 필요시 추가)
- **로그/지표는 전부 "서버를 실행 중인 컴퓨터"에 저장된다.** 여러 명이 각자 다른 컴퓨터로 접속해도,
  실제 FastAPI 프로세스가 도는 컴퓨터 하나에 모든 로그가 쌓인다. Docker로 띄워도 마찬가지 (같은
  컴퓨터 안의 컨테이너일 뿐). `docker-compose.yml`에서 `./logs:/srv/app/logs`로 호스트 폴더에
  바인드 마운트해뒀기 때문에, Docker로 실행해도 로그 파일은 호스트(`ai_agent_quality_platform/logs/`)
  에서 그대로 보인다.
- **"내 IP로 공유"와 "실제 배포"는 다른 개념.** LAN IP 공유는 같은 네트워크 안에서만 되고, 컴퓨터를
  끄면 끊기는 임시 방편. 실제 배포는 클라우드 서버(AWS/GCP 등)를 별도로 빌려 그 서버의 IP/도메인을
  쓰는 것. 다만 **이번 경우는 강의실 환경 + 고정 IP**라서, 클라우드 서버 없이 강의실 컴퓨터를 사실상의
  서버로 써도 실용적으로 충분하다고 판단함.

## 4. 이번 세션에서 구현/변경한 것 (시간순)

1. `ai_agent_quality_platform` 폴더 스켈레톤 생성 (app/, tests/, quality/, performance/, dashboard/,
   monitoring/, _DOCS/, Docker 관련 파일)
2. `ai_quality_final_project`에서 `.env`, `knowledge_base.py`, `test_cases.json` 이관
3. `app/` 전체 구현: FastAPI 앱(`main.py`), 에이전트(`service_agent.py`), 저지(`judge_agent.py`),
   지표(`metrics.py`), 로깅(`logger_config.py`), 스키마(`schemas.py`), 설정(`config.py`, 스켈레톤에
   없었으나 필요해서 추가)
4. `quality/` 배치 파이프라인 + 리포트 생성기 (단일 에이전트 버전으로 재작성, N/A 집계 로직 포함)
5. `tests/` pytest 4종 (헬스체크/메트릭, 실제 API 호출 채팅 테스트, 배치 파이프라인 표본 테스트,
   부정 케이스 테스트) — `pytest.ini`(스켈레톤에 없었으나 임포트 경로 문제로 추가)
6. `dashboard/streamlit_app.py`: 배치 리포트 대시보드 + **실시간 채팅 탭(메신저 스타일 UI)** + 대화 로그 탭
7. `monitoring/`: Prometheus 스크레이핑 설정, Grafana 대시보드 JSON + 자동 프로비저닝 설정
   (7개 패널: 요청 처리량, 지연시간 p50/p90/p99, 재시도/N/A, 판정 분포, 판정 추이, 세부 항목별 평균 점수,
   종합 평균 점수)
8. `performance/k6_test.js`, `Dockerfile`, `docker-compose.yml`(app+prometheus+grafana 3개 서비스),
   `requirements.txt`, `.gitignore`
9. `_DOCS/`: README, test_plan, defect_report, performance_report, demo_script 작성
10. Python 3.12 신규 설치(이 컴퓨터에 Python이 아예 없었음), venv 생성 및 패키지 설치
11. Docker Desktop 설치 → (한 번 중지 요청으로 제거) → 사용자가 직접 재설치 → 정상 동작 확인
12. 로컬 실행 검증: `/health`, `/metrics` 정상 확인. `/chat` 호출 시 **OpenAI 키 할당량 초과(429
    insufficient_quota)**로 실패 → 재시도 3회 → N/A 처리가 의도대로 작동하는 것까지 확인 (코드 문제 아님,
    계정 결제/크레딧 문제)
13. `docker compose up`으로 3개 컨테이너 실제 구동 확인, Grafana 대시보드 프로비저닝 확인
14. Grafana 대시보드를 5개 항목 점수 등 세분화 (`app/metrics.py`에 `judge_axis_score` 히스토그램 추가)
15. 동시성 이슈 논의 후 `app/concurrency.py` 추가 (백오프 + 동시 호출 5개 제한)를 `service_agent.py`,
    `judge_agent.py`에 적용
16. Streamlit 채팅 UI를 기본 `st.chat_message`에서 **커스텀 메신저 스타일**(헤더/아바타/말풍선/시간)로 교체,
    입력창-대화창 순서 수정(placeholder 트릭), 라이트/다크 모드 대응, 채팅창·입력창 배경 대비 강화
17. 탭 이름 변경("실시간 대화"→"대화 로그") 및 순서 재배치, "🔴 실시간" / "🧪 테스트케이스 사용" 그룹
    시각적 분리 (CSS `margin-left:auto` 트릭)

## 5. 미해결/보류 사항 (강의실에서 이어서 할 것)

- **OpenAI API 키 할당량 문제** — 실제 채팅 응답, 배치 파이프라인 전체 실행, 부정 케이스 테스트가 아직
  실제 데이터로 검증되지 못함. 크레딧/결제 확인 필요.
- **방화벽 인바운드 규칙 미완료** — `New-NetFirewallRule`은 관리자 권한이 필요해서 이 세션에서 직접
  실행하지 못함. 포트 8000(API)/8501(대시보드)/9090(Prometheus)/3000(Grafana)에 대해 관리자 권한
  PowerShell에서 직접 실행 필요 (본 문서 4장 이전 대화 또는 README 참고). 강의실 고정 IP가 내부용인지
  외부에서도 접속 가능한 공인 IP인지도 아직 미확인.
- **로그 파일 무한 증가(rotation 없음)** — `_OUTPUT/quality/live_log/*.jsonl`에 용량 제한이나 자동 정리가
  없음. 장기 운영 시 추가 필요. (2026-07-07: 위치가 `logs/`에서 `_OUTPUT/quality/live_log/`로 이동됨, 9장 참고)
- ~~**대화-채점 상관관계 ID 없음**~~ — **2026-07-06 해결됨**: 요청마다 UUID(`request_id`)를 발급해
  두 로그에 공통 기록 (7장 참고).
- **실제 배포(클라우드)는 범위 밖** — 지금은 로컬/강의실 컴퓨터 기준. 리버스 프록시, 도메인, HTTPS,
  클라우드 VM은 별도 작업.

## 6. 다음에 다시 시작할 때 체크리스트

1. OpenAI API 키 크레딧 확인 (`https://platform.openai.com/settings/organization/billing`)
2. 관리자 권한으로 방화벽 규칙 4개 추가
3. 강의실 고정 IP가 내부용/외부용인지 확인
4. `docker compose up --build -d`로 스택 재기동
5. Swagger(`/docs`) 또는 Streamlit 채팅 탭에서 실제 대화 테스트 → Grafana에 지표 반영되는지 확인
6. 필요하면 `python -m quality.quality_pipeline`으로 배치 30개 케이스 전체 실행 → 대시보드 확인

## 7. 규칙기반 vs API기반 비교 평가 복원 (2026-07-06 확정)

원래 2장에서 "규칙기반 vs API기반 비교 없이 단일 API 기반 에이전트만 서빙"으로 확정했었으나,
2026-07-06 강의실 세션에서 **기존 프로젝트의 비교 평가를 유지하기로 번복·확정**했다.

- 배치 파이프라인: 케이스마다 두 에이전트 답변을 받아 각각 채점하는 비교 방식으로 전환
  (`app/rule_based_agent.py` 이식, 리포트가 케이스 × 모델 2행 구조로 변경)
- 실시간 /chat: 응답에 `rule_answer` 필드 추가, 두 답변 모두 백그라운드 채점,
  Prometheus judge 지표에 `model` 라벨(api/rule) 추가, Grafana 쿼리도 모델별 분리
- 대시보드: 채팅 탭에 두 답변 말풍선 표시, 테스트케이스 탭 4개 전부 비교형으로 개편
- ClassBasics.md의 `/ask` 명명은 채택하지 않고 `/chat` 유지 (기능 동일, 이름 차이일 뿐)
- 테스트 케이스를 30건 → 5건으로 축소 (비용/시간 절약, 원본 30건은 `_DOCS/test_cases_archive.md`에 보관)
- 대시보드에 "➕ 케이스 관리·실행" 탭 추가: 케이스 추가/삭제(JSON 즉시 반영) + 확인 팝업을 거친
  배치 테스트 실행 버튼 (실행 중 전체 화면 잠금, 완료 시 리포트·로그 저장 후 자동 새로고침)
- **대화-채점 상관관계 ID 구현 완료**: `/chat` 요청마다 UUID(`request_id`)를 발급해
  `conversations.jsonl`과 `live_evaluations.jsonl` 양쪽에 기록 (5장의 미해결 사항 해소)
- **실시간 대화 리포트 추가** (배치 리포트와 완전 별개): `quality/live_report_generator.py`가
  대화+채점 로그만 집계해 `*_live_report.md/csv` 생성 (API 호출 없음). 대화 로그 탭에 생성 버튼,
  종합 리포트 탭에서 배치/실시간 선택 조회.

## 8. 모델 선택 메모 (결정 보류, 참고용)

`OPENAI_MODEL` 값을 무엇으로 할지에 대한 논의 내용. 아직 최종 결정은 안 됨 — 참고용 메모.

- **gpt-4.1-mini**: 토큰 가격이 저렴하고, 이 프로젝트(정해진 지식베이스 기반 FAQ + 구조화된 채점)
  수준의 작업엔 적당히 쓰기 좋음. 지금 기본값.
- **gpt-5.4-mini**: gpt-4.1-mini보다 토큰 가격이 약 2배. 더 똑똑하지만 그만큼 비쌈.
- **답변 모델과 채점(Judge) 모델을 분리하는 것도 고려 중** — LLM-as-judge 관행상 채점자가 답변자보다
  같거나 더 똑똑한 모델인 게 좋다는 논리. 예: 답변은 gpt-4.1-mini(저렴), 채점은 gpt-5.4-mini(정확도
  우선)로 나누는 방향.
- **추론 수준(reasoning effort)은 낮게 유지하는 방향** — 속도를 우선하기 위함. 재시도 타임아웃(20초)
  예산과 실시간 채팅 응답성을 감안하면, 추론을 깊게 하는 모델/설정은 지금 구조와 안 맞음.

미확정 상태이므로, 실제로 모델을 바꾸거나 역할별로 분리하기로 결정되면 `app/config.py`의
`OPENAI_MODEL` 및 `service_agent.py`/`judge_agent.py`의 모델 참조 방식을 수정해야 함
(현재는 두 파일이 같은 `OPENAI_MODEL` 값을 공유).

## 9. 로그·리포트 폴더 재구성 (2026-07-07 확정)

`_OUTPUT/quality/`와 프로젝트 루트 `logs/`로 나뉘어 있던 것을 `_OUTPUT/quality/` 하나 아래로 통합했다.

- **챗봇 로그 이동**: `logs/conversations.jsonl`, `logs/live_evaluations.jsonl` →
  `_OUTPUT/quality/live_log/` (프로젝트 루트 `logs/` 폴더는 삭제됨, `app/config.py`의 `LOG_DIR`이
  이 경로를 가리키도록 변경)
- **배치 이력 폴더 이름 변경**: `_OUTPUT/quality/log/` → `_OUTPUT/quality/testcase_log/`
  (배치 실행 이력본 + 대시보드에서 실행 시 남는 `pipeline_*.log`)
- **실시간 리포트 이력도 `live_log/`로**: `quality/live_report_generator.py`가 만드는
  `{timestamp}_live_report.*` 이력본도 원본 대화 로그와 같은 `live_log/` 폴더에 저장 (분리했던
  `log/` 공용 폴더 대신, "배치=testcase_log / 실시간=live_log"로 완전히 대칭 구조)
- **Docker**: `docker-compose.yml`의 `./logs:/srv/app/logs` 마운트 제거 — 챗봇 로그가 이제
  `_OUTPUT/quality/` 아래에 있어서 기존 `./_OUTPUT/quality:/srv/app/_OUTPUT/quality` 마운트 하나로 충분
- 최종 구조:
  ```
  _OUTPUT/quality/
  ├─ evaluation_result.*, final_quality_report.md   ← 배치 최신본
  ├─ live_report.*                                   ← 실시간 최신본
  ├─ testcase_log/  ← 배치 실행 이력 + pipeline_*.log
  └─ live_log/      ← 챗봇 원본 로그(conversations.jsonl, live_evaluations.jsonl) + 실시간 리포트 이력
  ```

## 10. Jira 자동 티켓 연동 (2장 "Jira 연동 없음" 결정 번복)

실시간 `/chat` 채점 결과(API 기반/규칙 기반) 중 하나라도 FAIL 또는 REVIEW가 나오면, **답변이 아니라
질문 기준으로** Jira에 Bug 티켓을 자동 생성하도록 변경했다. 2장에서 확정했던 "Jira 연동 없음" 결정을
번복한 것이다.

- `app/jira_client.py`: `create_jira_issue_for_question()` — Jira REST API(`/rest/api/2/issue`)로
  티켓 생성. 설명(description)에 질문 원문 + API/규칙 두 모델의 채점 결과를 모두 근거로 첨부.
  FAIL이 하나라도 있으면 우선순위 High, REVIEW만 있으면 Medium으로 동적 결정. `JIRA_EPIC_KEY`가
  있으면 에픽 하위로, `JIRA_SPRINT_ID`가 있으면 생성 직후 Jira Agile API로 스프린트에도 자동 배정.
- `app/main.py`: 기존에 API/규칙 채점이 개별 백그라운드 태스크였던 것을 `_score_both_and_check_jira_background`
  하나로 합쳐, 두 채점이 모두 끝난 뒤 Jira 등록 여부를 판단하도록 변경.
- `app/config.py`에 `JIRA_URL`/`JIRA_USER`/`JIRA_API_TOKEN`/`JIRA_PROJECT_KEY`/`JIRA_EPIC_KEY`/`JIRA_SPRINT_ID`
  환경변수 매핑 추가 (`.env`, `.gitignore`에 이미 포함되어 있어 안전).
- Jira/결함 리포트에 표시되는 답변·채점 모델명은 하드코딩하지 않고 `app/config.py`의 `OPENAI_MODEL`을
  그대로 참조하도록 함 (답변 에이전트와 저지 에이전트가 같은 모델을 공유하므로 8장 메모와 별개로
  실제 설정값을 항상 정확히 반영).
- 의도적으로 유발하는 장애 모의훈련(Chaos Test, `/fault-lab`)은 이 흐름과 무관하며, Jira 자동 등록은
  명시적으로 비활성화되어 있음 (`scripts/run_validation_tests.py`).
- 동일 질문이 반복돼도 매번 새 티켓이 생성됨 — 중복 방지(dedup) 로직은 아직 미구현 (필요시 추가).
