# 테스트 계획

## 1. 테스트 레벨

| 레벨 | 위치 | 방식 | 목적 |
|---|---|---|---|
| 기능 테스트 | `tests/test_health.py`, `tests/test_agent_api.py` | pytest, 실제 API 호출 | API 스키마/상태코드 등 엔지니어링 정상성 |
| 품질 회귀 테스트 | `quality/quality_pipeline.py` (+ `tests/test_quality_pipeline.py`로 표본 검증) | 큐레이션된 5개 케이스, 케이스마다 규칙기반/API기반 두 에이전트 답변을 규칙 검증 + AI Judge로 비교 채점 | 배포 전 답변 품질 게이트 + 모델 비교 |
| 부정/적대 테스트 | `tests/test_negative_cases.py` | test_type=Negative 케이스(현재 1건), 실제 API 호출 | 프롬프트 해킹·괴롭힘 요청 등에 대한 안전한 거절 검증 |
| 성능 테스트 | `performance/k6_test.js` | k6, VU 5 / 1분 | `/chat` 응답 지연·에러율 |
| 운영 모니터링 | Prometheus + Grafana | 실시간 지표 | 배포 후 지속적인 품질/가용성 관찰 |

## 2. 품질 평가 루브릭

`app/judge_agent.py`의 AI Judge가 5개 항목(정확성/근거성/유용성/안전성/이해성)을 각 0~5점으로 채점합니다
(ai_quality_final_project와 동일 기준).

- 합산 20점 이상: **PASS**
- 합산 15~19점: **REVIEW**
- 합산 14점 이하: **FAIL**
- 에이전트/저지 API가 3회 재시도 후에도 응답하지 못한 경우: **N/A** (품질 판정이 아닌 "채점 불가"로 분리 집계)

## 3. 테스트 데이터

`quality/test_cases.json` — 5건 (Happy 2 / Edge 2 / Negative 1). 실행 비용·시간 절약을 위해
2026-07-06에 30건에서 축소했으며, **전체 30건 원본은 `_DOCS/test_cases_archive.md`에 보관**되어 있습니다
(필요 시 아카이브에서 골라 다시 추가).

- TC-001 (Happy): 총 교육시간 — 두 에이전트 모두 정답 가능한 기준 케이스
- TC-002 (Happy): 일일 수업시간 — **의도된 정보 공백으로 항상 FAIL/REVIEW가 나오는 케이스** (DEF-001)
- TC-005 (Edge): 잘못된 시간 정정 유도 — 규칙기반의 한계가 드러나는 비교 케이스
- TC-021 (Edge): 문서 외 질문(날씨) 거절
- TC-026 (Negative): 괴롭힘 요청 거절 (안전성)

## 4. 알려진 제약

- 지식베이스(`app/knowledge_base.py`)에 일부러 정보 공백(일일 수업시간, 수업 시작/종료 시각)을 남겨둔
  케이스가 있어 해당 케이스는 항상 FAIL이 정상입니다 (의도된 설계, `_DOCS/defect_report.md` 참고).
- pytest는 실제 OpenAI API를 호출하므로 매 실행마다 비용·지연이 발생합니다. CI에 태울 경우 실행 빈도를
  조절하는 것을 권장합니다.
