# AI Agent Quality Portfolio

FastAPI 기반 AI 교육과정 안내 챗봇을 자동 테스트(pytest) + AI Judge 품질평가 + 성능테스트(k6) +
실시간 관측성(Prometheus/Grafana)까지 갖춰 운영하는 포트폴리오 프로젝트입니다.

## 파이프라인

```
사용자 질문 → FastAPI 기반 AI Agent → 자동 테스트(pytest) → AI Judge 평가
→ CSV·JSON·Markdown 리포트 → Streamlit 품질 대시보드
→ Prometheus 지표 수집 → Grafana 운영 모니터링 → (결함은 _DOCS/defect_report.md로 관리)
```

## 폴더 구조

- `app/` — FastAPI 챗봇 서비스 (에이전트, AI Judge, 지표, 로깅)
- `quality/` — 큐레이션된 테스트케이스 기반 배치 품질 회귀 테스트
- `tests/` — pytest 기능/통합 테스트 (실제 OpenAI API 호출)
- `dashboard/` — Streamlit 품질 대시보드 (배치 리포트 + 실시간 대화 로그)
- `monitoring/` — Prometheus/Grafana 설정
- `performance/` — k6 부하 테스트
- `_DOCS/` — 문서 (테스트 계획, 결함 리포트, 성능 리포트, 종합 품질 리포트)

## 로컬 실행 (venv)

```bash
pip install -r requirements.txt

# 챗봇 서버
uvicorn app.main:app --reload

# 배치 품질 회귀 테스트 (quality/test_cases.json 전체, 실제 API 호출)
python -m quality.quality_pipeline

# pytest (실제 API 호출 - 비용/지연 발생)
pytest

# 대시보드
streamlit run dashboard/streamlit_app.py
```

## Docker로 실행 (앱 + Prometheus + Grafana)

```bash
docker compose up --build
```

| 서비스 | 주소 |
|---|---|
| 챗봇 API | http://localhost:8000 (문서: /docs) |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (익명 뷰어 접속 허용, admin/admin으로 로그인 시 편집 가능) |

Streamlit 대시보드는 compose에 포함되어 있지 않으므로 `streamlit run dashboard/streamlit_app.py`로 별도 실행합니다
(배치/실시간 리포트, 챗봇 로그 모두 `_OUTPUT/quality/` 아래에 있으므로 로컬 venv 프로세스로 돌리는 쪽이 파일 경로가 간단합니다).

## 같은 네트워크의 다른 팀원이 접속하려면

1. 이 컴퓨터의 사설 IP 확인 (`ipconfig`에서 IPv4 주소)
2. Windows 방화벽에서 8000/9090/3000 포트 인바운드 허용
3. 팀원은 `http://<이 컴퓨터의 IP>:3000` 등으로 접속

이 컴퓨터가 꺼지거나 `docker compose down`을 하면 팀원도 접속할 수 없습니다. 상시 접근이 필요해지면
같은 `docker-compose.yml`을 클라우드 VM에 그대로 올리는 것을 권장합니다.

## 규칙기반 vs API기반 비교 평가

기존 `ai_quality_final_project`의 비교 평가 방식을 유지합니다.

- **배치**: `quality/quality_pipeline.py`가 케이스마다 규칙 기반(`app/rule_based_agent.py`)과
  API 기반(`app/service_agent.py`) 답변을 모두 받아 동일한 규칙 검증 + AI Judge 루브릭으로 채점하고,
  CSV/JSON/MD 리포트와 Streamlit 테스트케이스 탭 4개에서 두 모델을 나란히 비교합니다.
- **실시간**: `/chat` 응답에 `answer`(API 기반, 주 답변)와 `rule_answer`(규칙 기반, 비교용)가 함께
  반환되고, 두 답변 모두 백그라운드에서 채점되어 Prometheus 지표에 `model="api"/"rule"` 라벨로
  분리 기록됩니다 (Grafana에서 모델별 비교 가능). 대화와 채점은 `request_id`(UUID)로 1:1 연결됩니다.

## 리포트 2종 (완전 별개) + 로그 폴더 구조

| 리포트 | 데이터 원천 | 생성 방법 | 최신본 | 이력본·원본 로그 |
|---|---|---|---|---|
| 배치 테스트케이스 리포트 | `quality/test_cases.json` (실제 API 호출) | 대시보드 "➕ 케이스 관리·실행" 탭 버튼 또는 `python -m quality.quality_pipeline` | `_OUTPUT/quality/evaluation_result.*` + `_DOCS/final_quality_report.md` | `_OUTPUT/quality/testcase_log/*_evaluation_result.*`, 대시보드 실행 시 `pipeline_*.log`도 여기에 |
| 실시간 대화 리포트 | 챗봇 대화/채점 로그 (이미 쌓인 로그 집계, API 호출 없음) | 대시보드 "🗒️ 대화 로그" 탭 버튼 또는 `python -m quality.live_report_generator` | `_OUTPUT/quality/live_report.*` + `_DOCS/live_quality_report.md` | `_OUTPUT/quality/live_log/conversations.jsonl`, `live_evaluations.jsonl` (원본 로그) + `*_live_report.*`(이력본) |

두 리포트 모두 대시보드 "📄 종합 리포트" 탭에서 선택해서 볼 수 있습니다.

```
_OUTPUT/quality/
├─ evaluation_result.json/csv, final_quality_report.md   ← 배치 최신본
├─ live_report.json/csv, live_report.md                  ← 실시간 최신본
├─ testcase_log/   ← 배치 실행 이력(타임스탬프본) + pipeline_*.log
└─ live_log/       ← 챗봇 원본 로그(conversations.jsonl, live_evaluations.jsonl) + 실시간 리포트 이력
```

## 설계 메모

- **API 재시도/N/A 처리**: 에이전트·저지 API 모두 20초 타임아웃 · 최대 3회 재시도. 재시도 소진 시
  "품질이 나쁨(FAIL)"이 아니라 "채점 불가(N/A)"로 구분해 통과율 계산에서 제외합니다.
- **실시간 채점은 비동기**: `/chat` 응답은 에이전트 답변만 기다리고 즉시 반환하며, AI Judge 채점은
  `BackgroundTasks`로 백그라운드 실행되어 사용자 응답 속도에 영향을 주지 않습니다.
- **배치 vs 실시간 평가 역할 분리**: `quality/test_cases.json` 기반 배치 평가는 배포 전 회귀 테스트
  (CSV/JSON/MD 리포트), 실시간 평가는 배포 후 운영 모니터링(Prometheus/Grafana)을 담당합니다.
- **Jira 연동 없음**: 결함은 `_DOCS/defect_report.md`에 문서로만 관리합니다.
