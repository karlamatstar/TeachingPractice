# test_cases.json 의 질문을 RAG 챗봇 로직으로 일괄 질의하고 로그로 저장하는 코드
# app.py 와 동일한 검색/프롬프트/LLM 구성을 사용한다.
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parents[1]
load_dotenv(PROJECT_DIR / ".env")

PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
TEST_CASES_FILE = BASE_DIR / "test_cases.json"
LOG_DIR = PROJECT_DIR / "_OUTPUT" / "stage_01"


def get_vector_db():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="rag_documents"
    )


def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )


def answer_question(vector_db, llm, question):
    retrieved_docs = vector_db.similarity_search(
        question,
        k=3
    )

    if not retrieved_docs:
        return "관련 문서를 찾지 못했습니다.", [], []

    context_items = [
        {
            "source": doc.metadata.get("source", "알 수 없음"),
            "content": doc.page_content
        }
        for doc in retrieved_docs
    ]

    context = "\n\n".join(
        [
            f"[출처: {item['source']}]\n{item['content']}"
            for item in context_items
        ]
    )

    prompt = f"""
당신은 교육과정 안내 문서 챗봇입니다.

반드시 아래 제공된 문서 내용만 근거로 답변하십시오.
문서에 없는 내용은 추측하지 말고,
"제공된 문서에서는 확인할 수 없습니다."라고 답하십시오.

[문서 내용]
{context}

[사용자 질문]
{question}

[답변 작성 원칙]
1. 한국어로 답변한다.
2. 핵심 답변을 먼저 제시한다.
3. 문서 근거가 있으면 자연스럽게 설명한다.
4. 답변 끝에 참고한 파일명을 표시한다.
"""

    response = llm.invoke(prompt)

    sources = list(
        {
            doc.metadata.get("source", "알 수 없음")
            for doc in retrieved_docs
        }
    )

    return response.content, sources, context_items


def load_test_cases():
    with open(TEST_CASES_FILE, encoding="utf-8") as f:
        return json.load(f)


def main():
    test_cases = load_test_cases()

    vector_db = get_vector_db()
    llm = get_llm()

    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"test_log_{timestamp}.txt"

    results = []

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("RAG 챗봇 테스트 케이스 실행 로그\n")
        log_file.write(f"실행 시각: {timestamp}\n")
        log_file.write(f"총 테스트 케이스: {len(test_cases)}건\n")
        log_file.write("=" * 70 + "\n\n")

        for index, case in enumerate(test_cases, start=1):
            case_id = case.get("case_id", f"CASE_{index}")
            question = case.get("user_question", "")

            print(f"[{index}/{len(test_cases)}] {case_id} 질의 중...")

            try:
                answer, sources, context_items = answer_question(vector_db, llm, question)
            except Exception as error:  # 개별 케이스 실패가 전체를 멈추지 않도록
                answer = f"[오류] {error}"
                sources = []
                context_items = []

            log_file.write(f"[{index}] {case_id}\n")
            log_file.write(f"질문: {question}\n")
            log_file.write(f"답변: {answer}\n")
            log_file.write(f"참고 문서: {', '.join(sources) if sources else '없음'}\n")
            log_file.write("-" * 70 + "\n\n")
            log_file.flush()

            results.append(
                {
                    "case_id": case_id,
                    "user_question": question,
                    "answer": answer,
                    "sources": sources,
                    "context": context_items
                }
            )

    # 구조화된 결과도 함께 저장(후속 Judge 평가 등에 활용)
    json_path = LOG_DIR / f"test_log_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print()
    print(f"완료: {len(test_cases)}건 질의")
    print(f"로그 파일: {log_path}")
    print(f"JSON 결과: {json_path}")


if __name__ == "__main__":
    main()
