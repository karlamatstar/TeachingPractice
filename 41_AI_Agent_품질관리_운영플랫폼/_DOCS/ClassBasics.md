# 2차 과제명: "AI Agent 품질관리·운영 모니터링 플랫폼" 구축

- 최초 구조는 **"AI 답변을 만들고, 평가하고, 보고서를 만드는 프로그램"**입니다.
- 확장 구조는 최초 프로젝트에 다음 요소를 추가한 것입니다.

```text
기능 개발
 + 자동 테스트
 + API 서비스
 + 성능 테스트
 + 모니터링
 + Docker 배포
 + 문서화 
```

핵심은 단순 챗봇이 아니라 **전체 흐름을 보여주는 것**입니다.

## 폴더별 차이

| 최초 구조 | 확장 구조 | 차이 |
| :--- | :--- | :--- |
| 루트에 모든 Python 파일 | `app/`, `quality/`, `tests/`로 분리 | 역할별 구조화 |
| `service_agent.py` | `app/service_agent.py` | 실제 서비스 기능 분리 |
| `judge_agent.py` | `app/judge_agent.py` | Judge 기능을 서비스 계층에 배치 |
| `knowledge_base.py` | `app/knowledge_base.py` | 지식 데이터 처리 분리 |
| `rule_validator.py` | `quality/rule_validator.py` | 품질검증 모듈로 이동 |
| `report_generator.py` | `quality/report_generator.py` | 품질보고서 생성 영역 분리 |
| `data/test_cases.json` | `quality/test_cases.json` | 품질 테스트 데이터로 명확화 |
| 없음 | `tests/` | pytest 자동 테스트 추가 |
| 없음 | `performance/` | k6 성능·부하 테스트 추가 |
| 없음 | `monitoring/` | Prometheus·Grafana 추가 |
| 없음 | `Dockerfile`, `docker-compose.yml` | 컨테이너 실행·배포 추가 |
| 없음 | `_DOCS/` | 테스트 계획서·결함보고서·성능보고서 추가 |
| 없음 | `metrics.py` | Prometheus 측정 지표 추가 |
| 없음 | `logger_config.py` | 로그 관리 추가 |
| 없음 | `schemas.py` | 요청·응답 데이터 형식 관리 |

## 최종 포트폴리오 구조

기존 `ai_quality_final_project`를 아래처럼 확장합니다.
**기존 프로젝트를 그대로 복사한 것이 아니라, 기존 기능을 폴더별 책임에 맞게 재배치하고 확장한 형태**입니다.

| 기존 `ai_quality_final_project` | 확장 프로젝트 위치 (`ai_agent_quality_portfolio`) | 연결 내용 |
| :--- | :--- | :--- |
| `main.py` | `app/main.py` | FastAPI 서버, `/health`, `/ask`, `/metrics` API 역할 |
| `service_agent.py` | `app/service_agent.py` | 사용자 질문을 받아 규칙 기반 또는 API 기반 답변 생성 |
| `judge_agent.py` | `app/judge_agent.py` | 답변 정확성·안전성·유용성 평가 |
| `knowledge_base.py` | `app/knowledge_base.py` | 교육과정, QA, Docker 등 지식 검색 |
| `rule_validator.py` | `quality/rule_validator.py` | 키워드·안전성 기준으로 PASS/FAIL 판정 |
| `report_generator.py` | `quality/report_generator.py` | CSV·Markdown 품질 보고서 생성 |
| `data/test_cases.json` | `quality/test_cases.json` | 테스트 질문, 기대 키워드, 기대 안전성 상태 |
| `reports/` | `_OUTPUT/quality/` | 평가 결과 저장 위치 |
| `dashboard/streamlit_app.py` | `dashboard/streamlit_app.py` | 기존 대시보드 기능을 유지·확장 |
| `config.py` | `.env`, `app/schemas.py`, 향후 `app/config.py` | 환경변수·입력 검증·설정 역할로 분리 |

### 확장 구조도

```text
ai_agent_quality_portfolio/
│
├─ app/
│  ├─ main.py
│  ├─ service_agent.py
│  ├─ judge_agent.py
│  ├─ knowledge_base.py
│  ├─ metrics.py
│  ├─ logger_config.py
│  └─ schemas.py
│
├─ tests/
│  ├─ test_health.py
│  ├─ test_agent_api.py
│  ├─ test_quality_pipeline.py
│  └─ test_negative_cases.py
│
├─ quality/
│  ├─ test_cases.json
│  ├─ rule_validator.py
│  ├─ quality_pipeline.py
│  ├─ report_generator.py
│  └─ reports/
│
├─ performance/
│  ├─ k6_test.js
│  └─ results/
│
├─ dashboard/
│  └─ streamlit_app.py
│
├─ monitoring/
│  ├─ prometheus.yml
│  └─ grafana_dashboard.json
│
├─ _DOCS/
│  ├─ README.md
│  ├─ test_plan.md
│  ├─ defect_report.md
│  ├─ performance_report.md
│  └─ final_quality_report.md
│
├─ .env
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ .gitignore
```

## 가장 큰 차이: 테스트 수준

최초 구조:
```text
테스트 케이스 입력
 → 답변 생성
 → Judge 평가
 → 보고서 생성
```

확장 구조에서는 여러 층으로 테스트합니다.
```text
1. Health Test
   서버가 정상 실행되는가?

2. API Test
   요청과 응답 형식이 정상인가?

3. Quality Pipeline Test
   답변 → Judge → 규칙 검증 → 보고서가 정상인가?

4. Negative Test
   빈 질문, 위험 질문, 잘못된 입력에도 안전한가?

5. Performance Test
   여러 사용자가 동시에 접속해도 정상인가?

6. Monitoring Test
   오류율·응답시간·성공률을 관찰할 수 있는가?
```

## 사례로 보면

- **최초 구조**: 자동차 엔진이 잘 작동하는지 확인하는 실습용 모델
- **확장 구조**: 엔진 + 브레이크 검사 + 계기판 + 정비 기록 + 도로 주행시험 + 운행 모니터링까지 갖춘 실제 차량 운영 구조

## 🎖️ 단계별 연결 순서

처음부터 모든 기능을 한 번에 연결하면 오류가 많아집니다. 아래 순서가 가장 안정적입니다.

| 단계 | 구현 내용 | 산출물 |
| :---: | :--- | :--- |
| 1단계 | Service Agent + FastAPI | `/ask`, `/health` API |
| 2단계 | pytest 기능 테스트 | 자동 테스트 결과 |
| 3단계 | AI Judge 품질평가 | 정확성·안전성 점수 |
| 4단계 | JSON·CSV·Markdown 리포트 | 품질 보고서 |
| 5단계 | Streamlit 대시보드 | 품질 현황 화면 |
| 6단계 | k6 성능 테스트 | 응답시간·오류율 결과 |
| 7단계 | Prometheus 지표 수집 | `/metrics` |
| 8단계 | Grafana 운영 대시보드 | 실시간 모니터링 |
| 9단계 | Jira 결함관리 | FAIL 사례 등록 |
| 10단계 | Docker 통합 실행 | 전체 환경 재현 |

## 작성 우선순위

| 우선순위 | 목적 | 파일 |
| :---: | :--- | :--- |
| 1 | API 기본 실행 | `app/schemas.py`, `knowledge_base.py`, `service_agent.py`, `logger_config.py`, `metrics.py`, `main.py` |
| 2 | 품질 평가 엔진 | `quality/test_cases.json`, `rule_validator.py`, `quality_pipeline.py`, `report_generator.py` |
| 3 | 자동 테스트 | `tests/*.py` |
| 4 | 성능·모니터링 | `performance/k6_test.js`, `monitoring/prometheus.yml` |
| 5 | 대시보드 | `dashboard/streamlit_app.py` |
| 6 | 배포·문서화 | `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `_DOCS/*.md` |

즉, 기존 프로젝트의 핵심 흐름은 그대로 유지됩니다.

```text
사용자 질문
   ↓
service_agent.py
   ↓
knowledge_base.py 또는 API 기반 답변
   ↓
judge_agent.py
   ↓
rule_validator.py
   ↓
quality_pipeline.py
   ↓
report_generator.py
   ↓
CSV / Markdown / Streamlit Dashboard
```

차이는 기존에는 파일이 루트에 모여 있었다면, 확장 구조에서는 역할별로 나눈 것입니다.

```text
[기존]
main.py
service_agent.py
judge_agent.py
rule_validator.py
report_generator.py
data/
reports/

[확장]
app/         → 실제 AI Agent API 서비스
quality/     → 테스트·평가·보고서 생성
tests/       → pytest 자동화 테스트
performance/ → k6 부하 테스트
monitoring/  → Prometheus·Grafana 설정
dashboard/   → Streamlit 시각화
_DOCS/        → 포트폴리오 문서
```

특히 새로 추가되는 부분은 아래입니다.
- `tests/`: 기존에는 사람이 직접 확인하던 기능을 pytest로 자동 검증
- `performance/`: k6로 동시 사용자와 응답시간 검증
- `monitoring/`: Prometheus와 Grafana로 운영 지표 확인
- `Dockerfile`, `docker-compose.yml`: 다른 PC나 서버에서도 동일하게 실행
- `_DOCS/`: 테스트 계획서, 결함 보고서, 성능 보고서, 최종 품질 보고서

따라서 이 확장 프로젝트는 완전히 새로운 프로그램이라기보다,

> **기존 `ai_quality_final_project`를 기반으로 "개발 → 테스트 → 품질평가 → 성능검증 → 모니터링 → 배포"까지 포함하도록 포트폴리오 수준으로 확장한 구조**

라고 이해하시면 됩니다.

가장 중요한 연결 파일은 다음 6개입니다.

```text
app/service_agent.py
app/judge_agent.py
app/knowledge_base.py
quality/rule_validator.py
quality/quality_pipeline.py
quality/report_generator.py
```

기존 프로젝트 코드가 이미 있다면, 우선 이 6개 파일부터 기존 코드를 옮기고 수정하는 방식이 가장 안전합니다.

---

## 🚀 접속 정보 (Streamlit 정상 실행 시)

옆자리 동료가 접속할 주소는 아래와 같습니다.

| 서비스 | 동료가 접속할 주소 |
| :--- | :--- |
| 챗봇 API (Swagger) | `http://192.168.0.22:8000/docs` |
| Streamlit 대시보드 | `http://192.168.0.22:8501` |
| Prometheus | `http://192.168.0.22:9090` |
| Grafana | `http://192.168.0.22:3000` |

> 💡 **참고사항**
> Streamlit 로그에 `External URL: 121.161.204.172`도 뜨는데, 이건 공인 IP라 같은 강의실 내부망에서는 못 씁니다. 무시하고 **Network URL (`192.168.0.22`)**만 동료에게 공유하시면 됩니다.

같은 Wi-Fi/공유기에 연결돼 있으면 동료 쪽에서 바로 접속될 겁니다. 접속이 안 되면 알려주세요.