
from pathlib import Path
from datetime import datetime

from question_loader import load_testcases
from chatbot_agent import ChatbotAgent
from result_writer import save_json, save_excel


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "Input" / "testcases_questions.jsonl"
PROJECT_DIR = BASE_DIR.parents[1]
OUTPUT_DIR = PROJECT_DIR / "_OUTPUT" / "stage_01"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("=" * 60)
    print("Game Gacha TC Chatbot Test Start")
    print("=" * 60)

    # 1. 테스트케이스 로드
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"입력 파일을 찾을 수 없습니다.\n{INPUT_FILE}"
        )

    testcases = load_testcases(INPUT_FILE)

    if not testcases:
        print("[WARNING] 유효한 테스트케이스가 없어서 실행을 종료합니다.")
        return

    print(f"총 {len(testcases)}건 로드 완료")

    # 2. 챗봇 초기화
    agent = ChatbotAgent()

    results = []

    # 3. 질문 수행
    for idx, tc in enumerate(testcases, start=1):

        tc_id = tc.get("TC_ID", "")

        question = tc.get("질문", "")

        print(
            f"[{idx}/{len(testcases)}] "
            f"{tc_id} 실행중..."
        )

        try:

            answer = agent.ask(question)

        except Exception as e:

            answer = f"ERROR: {str(e)}"

        result = {
            "TC_ID": tc.get("TC_ID"),
            "품질지표": tc.get("품질지표"),
            "검색형태": tc.get("검색형태", ""),
            "유형": tc.get("유형"),
            "난이도": tc.get("난이도"),
            "질문": question,
            "답변": answer,
            "기대결과": tc.get("기대결과"),
            "검증주요요소": tc.get("검증주요요소", "")
        }

        results.append(result)

    # 4. 결과 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_file = (
        OUTPUT_DIR
        / f"result_{timestamp}.json"
    )

    excel_file = (
        OUTPUT_DIR
        / f"result_{timestamp}.xlsx"
    )

    save_json(
        results=results,
        file_path=json_file
    )

    save_excel(
        results=results,
        file_path=excel_file
    )

    print()
    print("=" * 60)
    print("테스트 완료")
    print(f"JSON : {json_file}")
    print(f"EXCEL: {excel_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
