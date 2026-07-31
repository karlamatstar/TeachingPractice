from pathlib import Path
import textwrap

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent.parent
CSV_FILE = PROJECT_DIR / "_OUTPUT" / "stage_00_reference" / "reports" / "evaluation_result.csv"


st.set_page_config(
    page_title="AI 챗봇 품질관리 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("AI 교육과정 안내 챗봇 품질관리 대시보드")

if not CSV_FILE.exists():
    st.warning("아직 평가 결과 파일이 없습니다. 먼저 main.py를 실행하세요.")
    st.stop()

df = pd.read_csv(CSV_FILE)

model_label_map = {
    "전체": "전체",
    "규칙 기반 챗봇": "rule_based",
    "API 기반 챗봇": "api_based"
}

selected_model_label = st.selectbox(
    "비교할 챗봇 선택",
    list(model_label_map.keys())
)

selected_model = model_label_map[selected_model_label]

if selected_model != "전체":
    df = df[df["model_type"] == selected_model]



def show_status_card(title: str, value: int, background_color: str) -> None:
    card_html = f"""
    <div style="
        background-color: {background_color};
        color: white;
        padding: 22px 10px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        min-height: 110px;
        box-shadow: 1px 2px 5px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 16px;">{title}</div>
        <div style="font-size: 34px; margin-top: 8px;">{value}</div>
    </div>
    """

    st.markdown(
        textwrap.dedent(card_html),
        unsafe_allow_html=True
    )


def get_score_color(score_100: float) -> str:
    """100점 환산 점수에 따른 빨주노초 색상 반환"""
    if score_100 < 60:
        return "#E53935"  # 빨강
    if score_100 < 75:
        return "#FB8C00"  # 주황
    if score_100 < 90:
        return "#FBC02D"  # 노랑
    return "#43A047"      # 초록


total_count = len(df)
pass_count = len(df[df["overall_decision"] == "PASS"])
review_count = len(df[df["overall_decision"] == "REVIEW"])
fail_count = len(df[df["overall_decision"] == "FAIL"])


st.subheader("테스트 판정 현황")

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_status_card("FAIL", fail_count, "#E53935")

with col2:
    show_status_card("REVIEW", review_count, "#FB8C00")

with col3:
    show_status_card("전체 테스트", total_count, "#FBC02D")

with col4:
    show_status_card("PASS", pass_count, "#43A047")


st.divider()

st.subheader("평균 점수")

score_columns = [
    "accuracy_score",
    "groundedness_score",
    "helpfulness_score",
    "safety_score"
]

missing_columns = [
    column for column in score_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV 파일에 다음 점수 컬럼이 없습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()

score_name_map = {
    "accuracy_score": "정확성",
    "groundedness_score": "근거성",
    "helpfulness_score": "유용성",
    "safety_score": "안전성"
}

score_df = df[score_columns].mean().reset_index()
score_df.columns = ["평가항목", "평균점수_5점"]

# CSV의 5점 만점 점수를 100점 만점으로 환산
score_df["평균점수_100점"] = score_df["평균점수_5점"] * 20

score_df["평가항목"] = score_df["평가항목"].map(score_name_map)
score_df["색상"] = score_df["평균점수_100점"].apply(get_score_color)

st.markdown(
    """
    <div style="font-size:14px; margin-bottom:12px;">
        <span style="color:#E53935; font-weight:bold;">■ 빨강: 60점 미만</span>
        &nbsp;&nbsp;&nbsp;
        <span style="color:#FB8C00; font-weight:bold;">■ 주황: 60~74점</span>
        &nbsp;&nbsp;&nbsp;
        <span style="color:#C9A000; font-weight:bold;">■ 노랑: 75~89점</span>
        &nbsp;&nbsp;&nbsp;
        <span style="color:#43A047; font-weight:bold;">■ 초록: 90점 이상</span>
    </div>
    """,
    unsafe_allow_html=True
)

bars_html = ""

for _, row in score_df.iterrows():
    score_5 = float(row["평균점수_5점"])
    score_100 = float(row["평균점수_100점"])
    color = row["색상"]
    label = row["평가항목"]

    bar_height = max(score_100 * 2.2, 12)

    bars_html += f"""
    <div style="
        flex: 1;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        text-align: center;
    ">
        <div style="
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        ">
            {score_5:.1f}점
        </div>

        <div style="
            height: {bar_height}px;
            background-color: {color};
            border-radius: 10px 10px 0 0;
        ">
        </div>

        <div style="
            margin-top: 10px;
            font-weight: bold;
            font-size: 16px;
        ">
            {label}
        </div>
    </div>
    """

chart_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="margin: 0; background-color: white;">
    <div style="
        display: flex;
        gap: 20px;
        align-items: flex-end;
        height: 310px;
        padding: 20px;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        background-color: #FAFAFA;
        box-sizing: border-box;
    ">
        {bars_html}
    </div>
</body>
</html>
"""

components.html(
    textwrap.dedent(chart_html),
    height=335,
    scrolling=False
)

st.divider()

st.subheader("케이스별 상세 결과")

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("FAIL 또는 REVIEW 사례")

issue_df = df[
    df["overall_decision"].isin(["FAIL", "REVIEW"])
]

if issue_df.empty:
    st.success("현재 FAIL 또는 REVIEW 사례가 없습니다.")
else:
    st.dataframe(
        issue_df,
        use_container_width=True
    )
