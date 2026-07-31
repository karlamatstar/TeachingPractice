# k6는 **Grafana Labs에서 개발한 오픈소스 성능 및 부하 테스트 도구**

- 개발자와 QA 엔지니어가 API, 마이크로서비스, 웹사이트의 성능을 쉽게 검증할 수 있도록 돕습니다
- K6의 주요 컴포넌트:

🎯 테스트 엔진 (Test Engine):  낮은 메모리 사용량과 높은 처리량
📝 스크립트 레이어 (Script Layer):  Node.js와 유사한 API 제공
📊 메트릭 수집기 (Metrics Collector):  테스트 진행 중 실시간 데이터 수집
🔌 출력 시스템 (Output System):   
      • 다양한 백엔드 지원—> InfluxDB, Prometheus, Grafana, CSV 등
      • 결과 분석—> 상세한 성능 분석 리포트


- k6가 성능 테스트를 실행할 때의 **기본 라이프사이클(4단계)

초기 준비 → setup() 1회 실행 → default() 여러 VU가 반복 실행 → teardown() 1회 실행**


```jsx
**// 1. 초기화 단계 (Init Phase) -- 테스트 코드/설정 준비**
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

// 2. 설정 단계 (Setup Phase) --  테스트 시작 전 1회 실행 
export function setup() {
  // 테스트 준비 작업
  return { token: 'auth-token' };
}

// 3. VU 실행 단계 (VU Phase) --  실제 부하 테스트
export default function(data) {
  // 실제 테스트 로직
  let response = http.get('https://api.example.com', {
    headers: { Authorization: `Bearer ${data.token}` }
  });
  
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
}

**// 4. 정리 단계 (Teardown Phase) --  테스트 종료 후 1회 실행**
export function teardown(data) {
  // 테스트 후 정리 작업
}
```

- 실행하면 개념적으로 다음 순서가 됩니다.
1. setup() 실행
└─ 테스트 환경 준비
2. VU 1, VU 2, VU 3 ... 실행
└─ **default(data)를 반복 실행**
└─ API 호출
└─ 응답시간, 오류율 측정
3. 모든 VU 종료
4. teardown(data) 실행
└─ 테스트 종료 처리

[실 습]

performance/lifecycle_test.js

```jsx
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 3,
  duration: "10s",
};

export function setup() {
  console.log("1. setup() 실행: 테스트 시작 전 서버 상태 확인");

  const response = http.get("http://127.0.0.1:8000/health");

  check(response, {
    "health API 상태코드가 200인가": (res) => res.status === 200,
  });

  return {
    baseUrl: "http://127.0.0.1:8000",
    testName: "k6 라이프사이클 실습",
  };
}

export default function (data) {
  const response = http.get(`${data.baseUrl}/health`);

  check(response, {
    "VU 요청 성공": (res) => res.status === 200,
  });

  sleep(1);
}

export function teardown(data) {
  console.log(`4. teardown() 실행: ${data.testName} 종료`);
}
```

- 기타 다양한 환경(하이브리드 환경)에서도 지원 가능함
*프론트엔드, 백엔드 모두 테스트 가능함

- 다양한 테스트 유형 지원

**Smoke Testing (연기 테스트)**
- 가장 빠르고 가볍게 핵심 기능만 검증하는 테스트
- 목표: 시스템이 최소한의 정상 상태인지 빠르게 확인
- 주요 지표: 성공률, 응답시간

**Load Testing (부하 테스트)**
- 예상되는 실제 사용자 부하를 시뮬레이션
- 목표: 최대 사용자 수에서도 시스템이 안정적인지 확인
- 주요 지표: TPS, 응답시간, 에러율, CPU/메모리 사용량

**Stress Testing (스트레스 테스트)**
- 시스템의 한계점이나 불안정 구간을 찾기 위해 설계
- 목표: 시스템이 비정상 상황에서 어떻게 동작하는지 확인
- 주요 지표: 에러율 급증, 응답시간 저하 구간

**Spike Testing (스파이크 테스트)**
- 갑작스러운 사용자 급증(피크타임)에 대비한 테스트
- 목표: 예상치 못한 트래픽 증가에 시스템이 적절히 대응하는지 확인
- 주요 지표: 에러율 급증, 응답시간 저하 구간

**장점**
- CLI 사용이 직관적이고 편리합니다.
- 다양한 테스트 유형 지원
- 다양한 출력 시스템 지원
- Grafana 연동으로 시각화 용이

**단점**
- JavaScript/TypeScript만 지원 (Go 등 다른 언어 지원 X)

-Grafana는 시각화 대시보드에 강점이 있으며, Prometheus는 시계열 데이터베이스로서 메트릭 수집 및 저장에 강점이 있습니다. -> 통합이 더 편합니다.

**k6의 공식 테스트 유형은 다음과 같습니다.**

**1. Load Test (부하 테스트)**
**2. Spike Test (스파이크 테스트)**
**3. Stress Test (스트레스 테스트)**
**4. Soak Test (지속 부하 테스트)**
**5. Breakpoint Test (임계점 테스트)**
**6. Penetration Test (침투 테스트)**
**7. Smoke Test (연기 테스트)**
**8. Integration Test (통합 테스트)**
**9. End-to-End Test (E2E 테스트)**
