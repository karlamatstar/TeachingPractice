from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from fake_judge import JudgeConfig, fake_judge


DATA_PATH = Path(__file__).parent / "data" / "cases.json"


def load_cases() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def judge_response(complaint: str, response: str) -> dict:
    prompt = f"{complaint}\n---RESPONSE---\n{response}"
    raw = asyncio.run(fake_judge(prompt, JudgeConfig()))
    return json.loads(raw)


st.set_page_config(page_title="AI 서비스 품질평가 실습", layout="wide")
st.title("AI 서비스 품질평가 실습")
st.caption("관련성·구체성·실행가능성·측정가능성·안전성 관점에서 응답을 평가합니다.")

cases = load_cases()
selected_id = st.selectbox("VOC 사례 선택", [case["case_id"] for case in cases])
case = next(item for item in cases if item["case_id"] == selected_id)

st.subheader("고객 불만")
st.info(case["complaint"])

left, right = st.columns(2)

with left:
    st.subheader("응답 A")
    st.write(case["answer_a"])
    if st.button("응답 A 평가", use_container_width=True):
        result_a = judge_response(case["complaint"], case["answer_a"])
        st.metric("총점", f'{result_a["score"]}/25')
        st.metric("판정", result_a["verdict"])
        st.dataframe(pd.DataFrame([result_a["dimensions"]]), use_container_width=True, hide_index=True)
        for reason in result_a["reasons"]:
            st.write(f"- {reason}")

with right:
    st.subheader("응답 B")
    st.write(case["answer_b"])
    if st.button("응답 B 평가", use_container_width=True):
        result_b = judge_response(case["complaint"], case["answer_b"])
        st.metric("총점", f'{result_b["score"]}/25')
        st.metric("판정", result_b["verdict"])
        st.dataframe(pd.DataFrame([result_b["dimensions"]]), use_container_width=True, hide_index=True)
        for reason in result_b["reasons"]:
            st.write(f"- {reason}")

st.divider()
st.subheader("직접 작성한 개선안 평가")
custom_response = st.text_area("개선안을 작성하세요", height=160)
if st.button("내 개선안 평가", type="primary"):
    if not custom_response.strip():
        st.warning("개선안을 입력하세요.")
    else:
        result = judge_response(case["complaint"], custom_response)
        st.metric("총점", f'{result["score"]}/25')
        st.metric("판정", result["verdict"])
        st.dataframe(pd.DataFrame([result["dimensions"]]), use_container_width=True, hide_index=True)
        for reason in result["reasons"]:
            st.write(f"- {reason}")
