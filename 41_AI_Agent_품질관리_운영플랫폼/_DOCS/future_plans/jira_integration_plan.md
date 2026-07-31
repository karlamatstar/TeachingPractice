# 지라(Jira) 티켓 자동 생성 기능 구현 계획

대시보드의 챗봇에서 사용자가 질문했을 때, 채점 결과(API 기반 또는 규칙 기반 중 1개 이상)가 `FAIL` 이나 `REVIEW`로 판정되면 해당 질문 내용을 지라(Jira)에 자동으로 등록하는 기능에 대한 구현 설계 문서입니다.

## 1. 사전 준비 사항 (환경 변수)

Jira 연동을 위해 프로젝트 최상단 `.env` 파일에 다음 4가지 정보가 필요합니다.

```env
JIRA_URL=https://(사용자스페이스).atlassian.net
JIRA_USER=(Jira에 로그인하는 이메일 주소)
JIRA_API_TOKEN=(Atlassian 계정 설정에서 발급받은 API 토큰)
JIRA_PROJECT_KEY=BUG
JIRA_EPIC_KEY=BUG-1
JIRA_SPRINT_ID=36
```

## 2. 컴포넌트별 변경 설계

### 2.1. `app/jira_client.py` 신규 생성
Jira REST API를 호출하여 이슈를 생성하는 전용 클라이언트 모듈을 생성합니다.
- `httpx` 라이브러리를 사용하여 추가 패키지 설치 없이 통신합니다.
- `create_jira_issue_for_question(request_id, timestamp, question, api_eval, rule_eval, answer_model, judge_model)` 함수를 구현합니다.
- 본문(Description)에는 사용자의 **질문**과 각 모델의 **채점 결과(결과, 총점, 세부 항목별 점수, 채점 의견)**, 그리고 **요청 ID**, **질문 시간**, **답변 및 채점 모델 정보**를 상세하게 포함하며, 이슈 타입은 `Bug`(버그)로 지정합니다.
- **우선순위(Priority)**: 채점 결과 중 하나라도 `FAIL`이 있으면 `High` (높음), `FAIL` 없이 `REVIEW`만 있으면 `Medium` (보통)으로 동적 설정합니다.
- (추가) `JIRA_EPIC_KEY`가 환경변수에 설정되어 있다면, 생성 시 payload의 `parent` 필드에 해당 에픽 키를 지정하여 특정 에픽 하위로 티켓이 들어가도록 구현합니다.
- (추가) **스프린트 할당**: 지라에서 스프린트는 '이름'이 아닌 '고유 숫자 ID'로 관리되므로, `JIRA_SPRINT_ID`가 환경변수에 설정되어 있다면 티켓 생성 직후 Jira Agile API(`POST /rest/agile/1.0/sprint/{sprintId}/issue`)를 추가로 호출하여 해당 티켓을 지정된 스프린트에 자동으로 배정합니다.
- 환경변수가 누락된 경우 서버 에러 없이 "경고 로그"만 출력하고 안전하게 넘어가도록 처리합니다.

**지라 API 전송 데이터(Payload) 예시:**
```json
{
  "fields": {
    "project": {"key": "BUG"},
    "parent": {"key": "BUG-1"}, 
    "issuetype": {"name": "Bug"},
    "priority": {"name": "High"},
    "summary": "[품질 이상] 챗봇 질문 확인: 회원가입은 어떻게 하나요?",
    "description": "다음 질문에 대한 챗봇 답변 채점 결과 품질 이상(FAIL/REVIEW)이 발견되었습니다.\n\n*요청 ID*: req-12345\n*질문 시간*: 2026-07-08 10:15:00\n*질문*: 회원가입은 어떻게 하나요?\n\n[API 기반 챗봇 답변 (답변 모델: gpt-4.1-mini, 채점 모델: gpt-4o)]\n* 결과: FAIL (총점: 45점)\n  - 상세 점수: 정확성 15점, 관련성 10점, 유창성 10점, 완전성 10점\n* 의견: 답변이 부정확하며 핵심 정보가 누락되었습니다.\n\n[규칙 기반 챗봇 답변 (답변 모델: Rule-based, 채점 모델: gpt-4o)]\n* 결과: PASS (총점: 85점)\n  - 상세 점수: 정확성 25점, 관련성 20점, 유창성 20점, 완전성 20점\n* 의견: 정해진 매뉴얼에 따라 적절히 답변했습니다."
  }
}
```

**스프린트 자동 할당 API(`POST /rest/agile/1.0/sprint/36/issue`) Payload 예시:**
- 티켓 생성 후, 앞서 찾아낸 스프린트 ID(`36`)를 활용해 해당 스프린트로 티켓을 즉시 편입시킵니다.
```json
{
  "issues": ["BUG-123"]
}
```

### 2.2. `app/config.py` 수정
Jira 접속에 필요한 환경변수들을 읽어오는 로직을 추가합니다.
- `JIRA_URL`, `JIRA_USER`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`, `JIRA_EPIC_KEY`, `JIRA_SPRINT_ID` 변수 매핑 추가.

### 2.3. `app/main.py` 수정
기존에는 API 답변과 규칙 답변에 대한 채점이 각각 개별 백그라운드 태스크로 분리되어 실행되었습니다. 이를 하나의 백그라운드 태스크로 묶어 채점 결과를 종합하도록 변경합니다.
- 신규 태스크 함수 `_score_both_and_check_jira_background`를 정의합니다.
- 내부적으로 기존 채점 함수를 순차 실행하여 `api_decision`과 `rule_decision`을 획득합니다.
- 획득한 결과 중 하나라도 `FAIL` 이나 `REVIEW`에 해당할 경우 `jira_client.py`의 함수를 호출해 지라에 등록합니다.
- `/chat` 엔드포인트에서 기존의 두 개 Task 호출 대신, 병합된 신규 Task를 호출하도록 수정합니다.

## 3. 검증 방법

1. `.env` 파일에 유효한(또는 더미) Jira 인증 정보를 입력합니다.
2. 애플리케이션을 실행하고(`uvicorn app.main:app`) 대시보드 챗봇에서 `FAIL` 또는 `REVIEW`를 받을 만한 질문을 테스트로 전송합니다.
3. 애플리케이션 로그에 `✅ Jira 이슈 생성 성공` 이 출력되는지 확인합니다.
4. 실제 Jira 프로젝트 보드에 들어가 해당 질문 내용이 티켓(Task)으로 잘 등록되었는지 확인합니다.