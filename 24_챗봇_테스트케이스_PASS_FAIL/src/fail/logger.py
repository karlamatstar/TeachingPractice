import os
import json
import csv
from datetime import datetime

from evaluator import METRIC_NAMES_KO, compute_summary

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(PROJECT_ROOT, "_OUTPUT", "fail", "logs")
JSONL_FILE = os.path.join(LOGS_DIR, "evaluation_logs.jsonl")
CSV_FILE = os.path.join(LOGS_DIR, "QA_Result_Log.csv")
GROUP_STATE_FILE = os.path.join(LOGS_DIR, ".group_state.json")


def _next_group_id(is_continued_chat):
    """
    직전 대화그룹 번호를 사이드카 상태 파일에서 O(1)로 읽어온다.
    (이전 구현은 매 호출마다 CSV 전체를 끝까지 스캔해서 마지막 줄을 찾았다.)
    """
    last_group_id = 0
    if os.path.isfile(GROUP_STATE_FILE):
        try:
            with open(GROUP_STATE_FILE, "r", encoding="utf-8") as f:
                last_group_id = json.load(f).get("last_group_id", 0)
        except (json.JSONDecodeError, OSError):
            last_group_id = 0

    group_id = last_group_id if (is_continued_chat and last_group_id > 0) else last_group_id + 1

    with open(GROUP_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_group_id": group_id}, f)

    return group_id


def save_log(question, answer, eval_result, is_continued_chat=False):
    if not eval_result:
        return None

    os.makedirs(LOGS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scores, average_score, total_passed = compute_summary(eval_result)

    # 평가 이유 추출 (점수가 낮아 reason이 채워진 항목만 결합)
    reasons = []
    for key, name in METRIC_NAMES_KO.items():
        reason_text = eval_result.get(key, {}).get("reason", "")
        if reason_text:
            reasons.append(f"[{name}] {reason_text}")
    combined_reasons = " | ".join(reasons)

    group_id = _next_group_id(is_continued_chat)

    log_data = {
        "timestamp": timestamp,
        "is_continued_chat": is_continued_chat,
        "question": question,
        "answer": answer,
        "evaluations": eval_result,
        "scores": scores,
        "average_score": average_score,
        "total_passed": total_passed,
    }

    with open(JSONL_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        headers = ["타임스탬프", "대화그룹", "연속대화_여부", "질문", "답변", "평균점수", "최종_Pass여부"] \
            + list(METRIC_NAMES_KO.values()) + ["평가사유"]
        writer = csv.DictWriter(f, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        clean_question = question.replace("\n", " ").replace("\r", " ")
        clean_answer = answer.replace("\n", " ").replace("\r", " ")
        row = {
            "타임스탬프": timestamp,
            "대화그룹": group_id,
            "연속대화_여부": "O" if is_continued_chat else "X",
            "질문": clean_question,
            "답변": clean_answer,
            "평균점수": average_score,
            "최종_Pass여부": "Pass" if total_passed else "Fail",
            "평가사유": combined_reasons,
        }
        for key, name in METRIC_NAMES_KO.items():
            row[name] = scores[key]
        writer.writerow(row)

    return log_data
