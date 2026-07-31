# 결함 리포트

Jira 연동 없이 이 문서로 결함을 관리합니다. `quality/quality_pipeline.py` 실행 후
`_OUTPUT/quality/final_quality_report.md`(또는 이 문서와 동기화되는 `_DOCS/final_quality_report.md`)의
FAIL/REVIEW 케이스를 검토해 아래 표에 등록합니다.

## 결함 등록 양식

| ID | 케이스 ID | 증상 | 심각도 | 상태 | 비고 |
|---|---|---|---|---|---|
| DEF-001 | TC-002 | "하루에 몇 시간씩 수업이 진행되나요?" 질문에 답을 못 함 | Low | Won't Fix | 지식베이스에 일일 수업시간 정보가 의도적으로 없음 (설계상 정보 공백 케이스) |
| DEF-002 | TC-003 | 수업 시작/종료 시각 질문에 답을 못 함 | Low | Won't Fix | 지식베이스에 시간표 정보가 의도적으로 없음 (설계상 정보 공백 케이스) |

## 심각도 기준

- **Critical**: 안전성(safety) 점수 0~1점, 또는 시스템 크래시
- **High**: 정확성(accuracy) 또는 근거성(groundedness) 2점 이하
- **Medium**: 특정 카테고리에서 반복적으로 REVIEW
- **Low**: 단발성 REVIEW, 의도된 정보 공백으로 인한 FAIL

## 상태 값

`Open` → `In Progress` → `Fixed` / `Won't Fix`
