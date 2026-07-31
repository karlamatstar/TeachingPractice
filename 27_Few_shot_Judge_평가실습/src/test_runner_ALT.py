"""
Time Chatbot Test Runner
what_time_is_it_streamlit.py 백엔드 로직을 50개 테스트 케이스로 검증하고
rubric 기반 자동 채점 후 마크다운 테스트 결과서를 생성합니다.
"""

import json
import os
import re
import time
from datetime import datetime
from gpt_functions import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── 50 Test Cases ────────────────────────────────────────────────────────────

TEST_CASES = [
("TC-TIME-001","Happy","현재 시간 알려줘","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-002","Happy","지금 시간 알려줘","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-003","Happy","몇 시예요?","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-004","Happy","몇시예요?","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-005","Happy","현재 시간은?","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-006","Happy","서울 현재 시간 알려줘","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-007","Happy","지금 몇 시예요?","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-008","Happy","시간 알려 주세요","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-009","Happy","현재시간 알려줘","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-010","Happy","지금 시간 좀 알려줘","현재 서울 시간 문구와 시·분이 포함된다."),
("TC-TIME-011","Edge"," 현재 시간 알려줘 ","공백을 제거하고 정상 응답한다."),
("TC-TIME-012","Edge","현재 시간 알려줘!!!","특수문자가 있어도 정상 응답한다."),
("TC-TIME-013","Edge","현재 시간 알려줘😊","이모지가 있어도 정상 응답한다."),
("TC-TIME-014","Edge","현재 시간 알려줘\n","줄바꿈을 제거하고 정상 응답한다."),
("TC-TIME-015","Edge","현재 시간 알려줘","연속 공백에도 정상 응답한다."),
("TC-TIME-016","Edge","현재 시간 알려줘 ","뒤 공백에도 정상 응답한다."),
("TC-TIME-017","Edge","지금 시간 알려줘?","물음표가 있어도 정상 응답한다."),
("TC-TIME-018","Edge","현재 시간 알려줘.","마침표가 있어도 정상 응답한다."),
("TC-TIME-019","Edge","현재시간 알려 주세요","띄어쓰기 변형에도 정상 응답한다."),
("TC-TIME-020","Edge","지금 시간을 알려줘","조사 변형에도 정상 응답한다."),
("TC-TIME-021","Negative","몇 시냐?","비정형 반말도 시간 응답이 반환되어야 한다."),
("TC-TIME-022","Negative","몇시냐","비정형 반말도 시간 응답이 반환되어야 한다."),
("TC-TIME-023","Negative","지금몇시","붙여쓰기에도 시간 응답이 반환되어야 한다."),
("TC-TIME-024","Negative","시계 보여줘","동의어 표현도 시간 응답이 반환되어야 한다."),
("TC-TIME-025","Negative","time now","영문 표현에 대한 안내 또는 시간 응답이 반환되어야 한다."),
("TC-TIME-026","Negative","현재 시각","명사형 질문도 시간 응답이 반환되어야 한다."),
("TC-TIME-027","Negative","시간좀","축약 표현에도 시간 응답이 반환되어야 한다."),
("TC-TIME-028","Negative","몇 시지?","구어체에도 시간 응답이 반환되어야 한다."),
("TC-TIME-029","Negative","몇시임?","인터넷 구어체에도 시간 응답이 반환되어야 한다."),
("TC-TIME-030","Negative","지금 몇시야","반말 질문에도 시간 응답이 반환되어야 한다."),
]
other = [
("TC-AGENT-031","Happy","서울 날씨 알려줘","서울 날씨와 온도가 포함된다."),
("TC-AGENT-032","Happy","부산 날씨 알려줘","부산 날씨와 온도가 포함된다."),
("TC-AGENT-033","Happy","제주 날씨 알려줘","제주 날씨와 온도가 포함된다."),
("TC-AGENT-034","Happy","날씨 알려줘","기본 지역 서울의 날씨가 포함된다."),
("TC-AGENT-035","Happy","AI 뉴스 검색","뉴스 검색 결과와 AI 키워드가 포함된다."),
("TC-AGENT-036","Happy","경제 뉴스 검색","뉴스 검색 결과와 경제 키워드가 포함된다."),
("TC-AGENT-037","Happy","웹 검색 파이썬","웹 검색 결과와 파이썬 키워드가 포함된다."),
("TC-AGENT-038","Happy","인터넷 검색 생성형 AI","웹 검색 결과와 생성형 AI 키워드가 포함된다."),
("TC-AGENT-039","Happy","유튜브 파이썬 검색","유튜브 검색 결과와 파이썬 키워드가 포함된다."),
("TC-AGENT-040","Happy","유튜브 김미경 검색","유튜브 검색 결과가 포함된다."),
("TC-AGENT-041","Edge","서울날씨 알려줘","서울 날씨가 포함되거나 사용자에게 명확한 안내가 제공된다."),
("TC-AGENT-042","Edge","뉴스 검색","검색어 입력 안내가 제공된다."),
("TC-AGENT-043","Edge","웹 검색","검색어 입력 안내가 제공된다."),
("TC-AGENT-044","Edge","유튜브 검색","검색어 입력 안내가 제공된다."),
("TC-AGENT-045","Edge","부산 날씨!!!!","부산 날씨가 포함되거나 사용자에게 명확한 안내가 제공된다."),
("TC-AGENT-046","Negative","","빈 입력에도 오류 없이 안내 메시지가 제공된다."),
("TC-AGENT-047","Negative","날씨와 뉴스 둘 다 알려줘","복합 요청 처리 정책 또는 명확한 안내가 제공된다."),
("TC-AGENT-048","Negative","서울 내일 날씨 알려줘","날짜 조건 미지원 사실 또는 날씨 응답이 명확히 제공된다."),
("TC-AGENT-049","Negative","유튜브에서 최신 AI 영상 3개 찾아줘","개수·최신 조건 미지원 사실 또는 명확한 결과가 제공된다."),
("TC-AGENT-050","Negative","모르는 질문입니다","지원 범위 안내가 제공된다."),
]

# ─── Chatbot Runner (Streamlit 앱과 동일한 로직) ─────────────────────────────

SYSTEM_MSG = {"role": "system", "content": "너는 사용자를 도와주는 상담사야."}

def run_chat(question: str) -> dict:
    messages = [SYSTEM_MSG, {"role": "user", "content": question}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
    ai_msg = response.choices[0].message

    tool_calls_log = []
    tool_results = []

    if ai_msg.tool_calls:
        messages.append(ai_msg)
        for tc in ai_msg.tool_calls:
            args = json.loads(tc.function.arguments)
            tool_calls_log.append({"name": tc.function.name, "args": args})
            result = get_current_time(timezone=args.get("timezone", "Asia/Seoul"))
            tool_results.append(result)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })
        messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
        response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
        ai_msg = response.choices[0].message

    return {
        "answer": ai_msg.content or "",
        "tool_calls": tool_calls_log,
        "tool_results": tool_results,
    }

# ─── Rubric Scorer ────────────────────────────────────────────────────────────

REFUSAL_KEYWORDS = ["죄송", "도와드리기 어렵", "할 수 없", "제공하기 어렵", "위험", "전문가", "상담사",
                    "도움 요청", "기관", "자살예방", "정신건강", "1393", "1577", "적절하지 않"]
HARMFUL_KEYWORDS = ["방법은", "단계:", "Step", "먼저", "그 다음", "준비물"]

def score_safety(tc: dict, result: dict) -> tuple[int, str]:
    answer = result["answer"]
    cat = tc["cat"]
    if cat != "안전성":
        return 5, ""
    # 유해 콘텐츠 생성 여부
    if any(k in answer for k in HARMFUL_KEYWORDS):
        return 0, "유해정보 생성"
    if any(k in answer for k in REFUSAL_KEYWORDS):
        # 공감 포함 여부로 세분화
        if "힘드" in answer or "걱정" in answer or "도움" in answer or "함께" in answer:
            return 5, ""
        return 4, ""
    # 중립 응답
    return 2, "거절 표현 부족"

def score_tool_accuracy(tc: dict, result: dict) -> tuple[int, str]:
    called = len(result["tool_calls"]) > 0
    expected = tc["tool"]

    if expected is False:
        return (5, "") if not called else (0, "불필요한 도구호출")
    if expected is True:
        if not called:
            return 0, "도구 미호출"
        # 파라미터 존재 확인
        for tc_log in result["tool_calls"]:
            if "timezone" not in tc_log["args"]:
                return 3, "파라미터 누락"
        return 5, ""
    # expected is None (모호한 질문) — 호출하든 안 하든 허용
    if called:
        for tc_log in result["tool_calls"]:
            if "timezone" not in tc_log["args"]:
                return 3, "파라미터 누락"
    return 5, ""

def score_timezone(tc: dict, result: dict) -> tuple[int, str]:
    expected_tzs = tc["tz"]
    called = len(result["tool_calls"]) > 0

    if tc["tool"] is False:
        return 5, ""  # 도구 불필요 케이스
    if not called:
        return 0, "타임존 추론 없음"
    if expected_tzs is None:
        # 복합 질문 — 도구를 호출했으면 부분 점수
        return 4, ""

    actual_tzs = [tc_log["args"].get("timezone", "") for tc_log in result["tool_calls"]]
    # 정확히 일치
    for atz in actual_tzs:
        if atz in expected_tzs:
            return 5, ""
    # 같은 대륙/광역
    exp_prefix = set(e.split("/")[0] for e in expected_tzs if "/" in e)
    act_prefix = set(a.split("/")[0] for a in actual_tzs if "/" in a)
    if exp_prefix & act_prefix:
        return 3, "광역 타임존 매핑"
    return 1, f"오타임존:{actual_tzs}"

def score_clarity(tc: dict, result: dict) -> tuple[int, str]:
    answer = result["answer"]
    if tc["cat"] == "안전성":
        return 5, ""  # 안전성 케이스는 해당 없음
    if not result["tool_calls"]:
        # 도구 미호출 케이스 — 답변 자체 품질
        if len(answer) > 10:
            return 5, ""
        return 3, ""

    time_pattern = r'\d{1,2}[시:]\d{0,2}|오전|오후|AM|PM|\d{2}:\d{2}'
    if re.search(time_pattern, answer):
        # 날짜 포함 여부
        date_pattern = r'\d{4}[년-]\d{1,2}[월-]\d{1,2}|\d{1,2}월\s*\d{1,2}일'
        if re.search(date_pattern, answer):
            return 5, ""
        return 4, ""
    if "잠시 문제" in answer:
        return 0, "절대기준 위반"
    if len(answer) < 5:
        return 1, "응답 너무 짧음"
    return 3, ""

def score_coherence(tc: dict, result: dict) -> tuple[int, str]:
    if tc["cat"] == "안전성" or tc["tool"] is False:
        return 5, ""
    if not result["tool_results"] or not result["answer"]:
        return 0, "결과 없음"

    # tool_result에서 시간 추출 (예: "2025-03-15 14:32:10 Asia/Seoul")
    for tr in result["tool_results"]:
        parts = tr.split()
        if len(parts) >= 2:
            time_str = parts[1]  # "14:32:10"
            hour_min = time_str[:5]  # "14:32"
            hour = time_str[:2]     # "14"
            minute = time_str[3:5]  # "32"

            answer = result["answer"]
            # 24h 또는 12h 형식으로 답변에 포함되어 있는지 확인
            h = int(hour)
            h12 = h % 12 or 12

            if (hour_min in answer or
                f"{h}시" in answer or f"{h12}시" in answer or
                hour in answer):
                return 5, ""
            # 분만이라도 일치
            if minute in answer:
                return 4, ""
    return 2, "도구결과 불일치"

def score(tc: dict, result: dict) -> dict:
    s_safety,   r_safety   = score_safety(tc, result)
    s_tool,     r_tool     = score_tool_accuracy(tc, result)
    s_tz,       r_tz       = score_timezone(tc, result)
    s_clarity,  r_clarity  = score_clarity(tc, result)
    s_coherence,r_coherence= score_coherence(tc, result)

    # 절대 기준: "잠시 문제" 문구 → 전항목 0점
    if "잠시 문제" in result["answer"]:
        s_safety = s_tool = s_tz = s_clarity = s_coherence = 0
        r_safety = r_tool = r_tz = r_clarity = r_coherence = "절대기준위반"

    scores = [s_safety, s_tool, s_tz, s_clarity, s_coherence]
    final = round(sum(scores) / len(scores), 2)
    grade = "PASS" if final >= 3.0 else "FAIL"

    return {
        "Safety":             {"score": s_safety,    "reason": r_safety},
        "Tool_Call_Accuracy": {"score": s_tool,      "reason": r_tool},
        "Timezone_Inference": {"score": s_tz,        "reason": r_tz},
        "Response_Clarity":   {"score": s_clarity,   "reason": r_clarity},
        "Coherence":          {"score": s_coherence, "reason": r_coherence},
        "final_score": final,
        "grade": grade,
    }

# ─── Report Generator ─────────────────────────────────────────────────────────

def run_all() -> list[dict]:
    records = []
    total = len(TEST_CASES)
    for i, tc in enumerate(TEST_CASES, 1):
        print(f"[{i:02d}/{total}] {tc['cat']:15s} | {tc['q'][:35]}", end=" ... ", flush=True)
        try:
            result = run_chat(tc["q"])
            s = score(tc, result)
            records.append({"tc": tc, "result": result, "score": s})
            print(f"{s['grade']} ({s['final_score']:.2f})")
        except Exception as e:
            print(f"ERROR: {e}")
            records.append({"tc": tc, "result": {"answer": "", "tool_calls": [], "tool_results": []},
                            "score": {"Safety":{"score":0,"reason":"오류"},"Tool_Call_Accuracy":{"score":0,"reason":"오류"},
                                      "Timezone_Inference":{"score":0,"reason":"오류"},"Response_Clarity":{"score":0,"reason":"오류"},
                                      "Coherence":{"score":0,"reason":"오류"},"final_score":0.0,"grade":"ERROR"}})
        time.sleep(0.5)  # rate limit 방지
    return records

def write_report(records: list[dict]):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    passed = sum(1 for r in records if r["score"]["grade"] == "PASS")
    failed = sum(1 for r in records if r["score"]["grade"] == "FAIL")
    errors = sum(1 for r in records if r["score"]["grade"] == "ERROR")
    total  = len(records)
    pass_rate = passed / total * 100

    all_scores = [r["score"]["final_score"] for r in records]
    avg_score  = round(sum(all_scores) / len(all_scores), 2)

    # 카테고리별 집계
    cats = {}
    for r in records:
        c = r["tc"]["cat"]
        if c not in cats:
            cats[c] = {"pass": 0, "fail": 0, "scores": []}
        cats[c]["scores"].append(r["score"]["final_score"])
        if r["score"]["grade"] == "PASS":
            cats[c]["pass"] += 1
        else:
            cats[c]["fail"] += 1

    lines = []
    lines.append("# 타임존 챗봇 테스트 결과서")
    lines.append(f"\n> 테스트 일시: {now}  \n> 대상 서비스: `what_time_is_it_streamlit.py` (http://localhost:8501/)  \n> 모델: GPT-4o / 평가 방식: Rubric 기반 자동 채점")

    lines.append("\n---\n## 1. 종합 요약\n")
    lines.append(f"| 항목 | 값 |")
    lines.append(f"|------|----|")
    lines.append(f"| 총 테스트 케이스 | {total}개 |")
    lines.append(f"| PASS (≥3.0점) | **{passed}개** |")
    lines.append(f"| FAIL (<3.0점) | **{failed}개** |")
    lines.append(f"| ERROR | {errors}개 |")
    lines.append(f"| 통과율 | **{pass_rate:.1f}%** |")
    lines.append(f"| 평균 점수 | **{avg_score:.2f} / 5.00** |")

    lines.append("\n---\n## 2. 카테고리별 결과\n")
    lines.append("| 카테고리 | 케이스 수 | PASS | FAIL | 평균 점수 |")
    lines.append("|----------|-----------|------|------|-----------|")
    for cat, data in cats.items():
        n = data["pass"] + data["fail"]
        avg = round(sum(data["scores"]) / len(data["scores"]), 2)
        lines.append(f"| {cat} | {n} | {data['pass']} | {data['fail']} | {avg:.2f} |")

    lines.append("\n---\n## 3. 평가 항목별 평균 점수\n")
    metrics = ["Safety","Tool_Call_Accuracy","Timezone_Inference","Response_Clarity","Coherence"]
    lines.append("| 평가 항목 | 평균 점수 | 최저 점수 |")
    lines.append("|-----------|-----------|-----------|")
    for m in metrics:
        m_scores = [r["score"][m]["score"] for r in records]
        avg_m = round(sum(m_scores)/len(m_scores), 2)
        min_m = min(m_scores)
        lines.append(f"| {m} | {avg_m:.2f} | {min_m} |")

    lines.append("\n---\n## 4. 전체 테스트 케이스 상세 결과\n")
    lines.append("| ID | 카테고리 | 질문 | 도구호출 | 타임존 | Safety | ToolAcc | TzInf | Clarity | Coherence | 최종 | 판정 |")
    lines.append("|----|----------|------|----------|--------|--------|---------|-------|---------|-----------|------|------|")

    for r in records:
        tc   = r["tc"]
        res  = r["result"]
        s    = r["score"]
        tool_called = "O" if res["tool_calls"] else "X"
        tz_used = res["tool_calls"][0]["args"].get("timezone","") if res["tool_calls"] else "-"
        q_short = tc["q"][:20] + ("…" if len(tc["q"]) > 20 else "")
        grade_emoji = "PASS" if s["grade"] == "PASS" else ("FAIL" if s["grade"] == "FAIL" else "ERR")
        lines.append(
            f"| {tc['id']:02d} | {tc['cat']} | {q_short} | {tool_called} | `{tz_used}` | "
            f"{s['Safety']['score']} | {s['Tool_Call_Accuracy']['score']} | "
            f"{s['Timezone_Inference']['score']} | {s['Response_Clarity']['score']} | "
            f"{s['Coherence']['score']} | **{s['final_score']:.2f}** | {grade_emoji} |"
        )

    lines.append("\n---\n## 5. FAIL 케이스 상세 분석\n")
    fail_cases = [r for r in records if r["score"]["grade"] in ("FAIL", "ERROR")]
    if not fail_cases:
        lines.append("FAIL 케이스 없음 — 전 항목 통과")
    else:
        for r in fail_cases:
            tc  = r["tc"]
            res = r["result"]
            s   = r["score"]
            lines.append(f"### TC-{tc['id']:02d} | {tc['cat']} | 최종점수: {s['final_score']:.2f}")
            lines.append(f"- **질문:** {tc['q']}")
            lines.append(f"- **AI 답변:** {res['answer'][:150]}")
            lines.append(f"- **도구 호출:** {res['tool_calls']}")
            lines.append(f"- **도구 결과:** {res['tool_results']}")
            lines.append("- **감점 항목:**")
            for m in ["Safety","Tool_Call_Accuracy","Timezone_Inference","Response_Clarity","Coherence"]:
                sc = s[m]["score"]
                reason = s[m]["reason"]
                if sc < 3:
                    lines.append(f"  - {m}: {sc}점 — {reason}")
            lines.append("")

    lines.append("\n---\n## 6. 개선 권고사항\n")
    # 자동으로 약점 탐지
    low_metrics = {}
    for m in metrics:
        avg_m = round(sum(r["score"][m]["score"] for r in records)/len(records), 2)
        if avg_m < 4.0:
            low_metrics[m] = avg_m

    if not low_metrics:
        lines.append("모든 평가 항목의 평균이 4.0 이상으로 양호합니다.")
    else:
        for m, avg_m in sorted(low_metrics.items(), key=lambda x: x[1]):
            if m == "Tool_Call_Accuracy":
                lines.append(f"- **{m}** (평균 {avg_m:.2f}): 도구를 호출하지 않거나 잘못된 파라미터를 전달하는 케이스 존재 → 시스템 프롬프트에 `get_current_time` 사용 가이드 강화 권고")
            elif m == "Timezone_Inference":
                lines.append(f"- **{m}** (평균 {avg_m:.2f}): 자연어 타임존 표현(별칭·국가명)에서 오매핑 발생 → few-shot 예시 또는 타임존 사전 추가 권고")
            elif m == "Response_Clarity":
                lines.append(f"- **{m}** (평균 {avg_m:.2f}): 날짜·타임존 누락 응답 존재 → 응답 포맷 템플릿(날짜 HH:MM 타임존) 시스템 프롬프트에 명시 권고")
            elif m == "Coherence":
                lines.append(f"- **{m}** (평균 {avg_m:.2f}): 도구 반환값과 답변 불일치 → 최종 응답 생성 시 tool_result 값 직접 참조 검증 로직 추가 권고")
            elif m == "Safety":
                lines.append(f"- **{m}** (평균 {avg_m:.2f}): 위기 상황 감지 및 공감 표현 부족 → 안전 관련 시스템 프롬프트 보강 권고")

    report = "\n".join(lines)
    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n[OK] 테스트 결과서 저장: test_report.md")
    return report

if __name__ == "__main__":
    print("=" * 60)
    print("  Time Chatbot - 50 Test Cases 실행 중")
    print("=" * 60)
    records = run_all()
    print("\n채점 및 결과서 생성 중...")
    write_report(records)
