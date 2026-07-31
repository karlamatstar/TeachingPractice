from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "_OUTPUT" / "models"
REPORT_DIR = BASE_DIR / "_OUTPUT" / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# 1. 엣지 케이스 테스트 데이터 불러오기
edge_df = pd.read_csv(
    DATA_DIR / "edge_test_data.csv",
    encoding="utf-8-sig"
)


# 2. 학습된 라우팅 분류 모델 불러오기
routing_classifier = joblib.load(
    MODEL_DIR / "routing_classifier.joblib"
)


# 3. 엣지 케이스 예측 수행
edge_df["predicted_label"] = routing_classifier.predict(
    edge_df["text"]
)


# 4. 실제 기대값과 예측값 비교
edge_df["is_correct"] = (
    edge_df["expected_label"]
    == edge_df["predicted_label"]
)


# 5. 결과 파일 저장
result_path = REPORT_DIR / "edge_test_result.csv"

edge_df.to_csv(
    result_path,
    index=False,
    encoding="utf-8-sig"
)


# 6. 통계 계산
total_count = len(edge_df)
correct_count = edge_df["is_correct"].sum()
wrong_count = total_count - correct_count
accuracy = correct_count / total_count if total_count > 0 else 0


# 7. 오분류 사례 추출
wrong_df = edge_df[
    edge_df["is_correct"] == False
]


# 8. Markdown 보고서 생성
report_path = REPORT_DIR / "edge_case_report.md"

if wrong_df.empty:
    wrong_case_text = "오분류된 엣지 케이스가 없습니다."
else:
    wrong_case_text = wrong_df.to_markdown(index=False)


markdown_text = f"""# 라우팅 분류 모델 엣지 케이스 테스트 보고서

## 1. 테스트 요약

| 항목 | 결과 |
|---|---:|
| 전체 테스트 건수 | {total_count}건 |
| 정답 건수 | {correct_count}건 |
| 오답 건수 | {wrong_count}건 |
| 정확도 | {accuracy:.2%} |

## 2. 테스트 목적

엣지 케이스 테스트는 일반적인 입력뿐 아니라 다음과 같은 예외 상황에서
라우팅 분류 모델이 적절히 동작하는지 확인하기 위한 테스트입니다.

- 오타가 포함된 문장
- 짧은 문장
- 복합 의도 문장
- 스포츠와 시간처럼 여러 의미가 섞인 문장
- 지원하지 않는 기능 요청
- 의미 없는 입력

## 3. 전체 테스트 결과

{edge_df.to_markdown(index=False)}

## 4. 오분류 사례

{wrong_case_text}

## 5. 평가 의견

엣지 케이스는 일반 테스트보다 분류 난도가 높습니다.

오분류된 문장이 있다면 해당 문장과 유사한 표현을
학습 데이터에 추가한 후 모델을 다시 학습해야 합니다.

특히 복합 의도 문장은 하나의 에이전트만 선택하도록 설계할지,
여러 에이전트로 분기하도록 설계할지 정책을 먼저 정해야 합니다.

## 6. 최종 판정

| 기준 | 판정 |
|---|---|
| 정확도 90% 이상 | 엣지 케이스 대응이 비교적 안정적 |
| 정확도 70~89% | 일부 예외 입력 보강 필요 |
| 정확도 70% 미만 | 학습 데이터와 라우팅 정책 재설계 필요 |

현재 엣지 케이스 정확도는 **{accuracy:.2%}** 입니다.
"""

report_path.write_text(
    markdown_text,
    encoding="utf-8"
)
