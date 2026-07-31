# 성능 테스트 리포트

`performance/k6_test.js` 실행 결과를 기록합니다.

## 실행 방법

```bash
k6 run performance/k6_test.js
# 결과를 JSON summary로 저장하려면:
k6 run --summary-export=_OUTPUT/performance/summary.json performance/k6_test.js
```

## 테스트 조건

- 시나리오: VU(가상 사용자) 5명, 1분간 지속 요청 (`constant-vus`)
- 대상: `POST /chat`
- 통과 기준(thresholds): 에러율 5% 미만, p95 지연 20초 미만
  (에이전트/저지 API가 재시도 최대 3회 · 각 20초 타임아웃까지 갈 수 있음을 감안한 값)

## 결과 (최근 실행)

> `k6 run`을 실행한 뒤 아래 표를 채워주세요.

| 지표 | 값 |
|---|---|
| 총 요청 수 | - |
| 에러율 | - |
| p50 지연 | - |
| p95 지연 | - |
| p99 지연 | - |

## 관찰 사항

-
