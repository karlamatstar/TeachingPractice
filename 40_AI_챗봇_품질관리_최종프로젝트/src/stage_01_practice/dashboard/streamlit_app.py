import json
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent.parent
REPORTS_DIR = PROJECT_DIR / "_OUTPUT" / "stage_01_practice" / "reports"

st.set_page_config(page_title="AI 챗봇 품질 대시보드", layout="wide")
st.title("AI 교육과정 안내 챗봇 — 품질 평가 대시보드")

json_path = REPORTS_DIR / "evaluation_result.json"
if not json_path.exists():
    st.warning("평가 결과 파일이 없습니다. main.py를 먼저 실행하세요.")
    st.stop()

with open(json_path, encoding="utf-8") as f:
    results = json.load(f)

# ── 요약 지표 ────────────────────────────────────────────
total  = len(results)
passed = sum(1 for r in results if r.get("evaluation_result", {}).get("overall_decision") == "PASS")
review = sum(1 for r in results if r.get("evaluation_result", {}).get("overall_decision") == "REVIEW")
failed = total - passed - review

col1, col2, col3, col4 = st.columns(4)
col1.metric("총 케이스",   total)
col2.metric("PASS",        passed, delta=f"{passed/total*100:.0f}%")
col3.metric("REVIEW",      review)
col4.metric("FAIL",        failed)

st.divider()

# ── 점수 표 ──────────────────────────────────────────────
st.subheader("케이스별 평가 결과")
rows = []
for r in results:
    ev = r.get("evaluation_result", {})
    rv = r.get("rule_validation", {})
    rows.append({
        "case_id":    r["case_id"],
        "category":   r["category"],
        "test_type":  r["test_type"],
        "rule":       rv.get("rule_status", ""),
        "accuracy":   ev.get("accuracy",     {}).get("score", ""),
        "groundedness": ev.get("groundedness", {}).get("score", ""),
        "helpfulness":  ev.get("helpfulness",  {}).get("score", ""),
        "safety":       ev.get("safety",       {}).get("score", ""),
        "판정":         ev.get("overall_decision", ""),
    })

df = pd.DataFrame(rows)

def highlight_decision(val):
    if val == "PASS":
        return "background-color:#d4edda; color:#155724; font-weight:bold"
    if val == "REVIEW":
        return "background-color:#fff3cd; color:#856404; font-weight:bold"
    if val == "FAIL":
        return "background-color:#f8d7da; color:#721c24; font-weight:bold"
    return ""

styled = df.style.map(highlight_decision, subset=["판정", "rule"])
st.dataframe(styled, use_container_width=True)

st.divider()

# ── 항목별 평균 점수 차트 ─────────────────────────────────
st.subheader("항목별 평균 점수")
score_cols = ["accuracy", "groundedness", "helpfulness", "safety"]
avg = df[score_cols].apply(pd.to_numeric, errors="coerce").mean()
st.bar_chart(avg)

st.divider()

# ── 케이스별 상세 보기 ───────────────────────────────────
st.subheader("케이스 상세 보기")
selected = st.selectbox("케이스 선택", [r["case_id"] for r in results])
detail   = next(r for r in results if r["case_id"] == selected)
ev       = detail.get("evaluation_result", {})

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"**질문:** {detail['user_question']}")
    st.markdown(f"**챗봇 답변:** {detail.get('ai_answer', '')}")
    st.markdown(f"**총평:** {ev.get('summary', '')}")

with col_b:
    for item in ["accuracy", "groundedness", "helpfulness", "safety"]:
        info = ev.get(item, {})
        st.markdown(f"**{item}** ({info.get('score','?')}점): {info.get('reason','')}")
