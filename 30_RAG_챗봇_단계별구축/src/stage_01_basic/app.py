import os
import sys
import shutil
import subprocess
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

PERSIST_DIRECTORY = "chroma_db"
DOCUMENTS_DIR = Path("documents")

st.set_page_config(
    page_title="RAG 문서 챗봇",
    page_icon="📚"
)

st.title("📚 RAG 기반 문서 챗봇")
st.caption("등록된 문서 내용에 근거하여 답변합니다.")


def save_uploaded_pdfs(uploaded_files):
    DOCUMENTS_DIR.mkdir(exist_ok=True)

    saved = []
    for uploaded_file in uploaded_files:
        target_path = DOCUMENTS_DIR / uploaded_file.name

        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved.append(uploaded_file.name)

    return saved


with st.sidebar:
    st.header("📄 PDF 문서 추가")
    st.caption("PDF 파일을 드래그해서 올리면 documents 폴더에 저장됩니다.")

    uploaded_files = st.file_uploader(
        "PDF 파일을 여기에 드롭하세요.",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("documents 폴더에 저장"):
        saved = save_uploaded_pdfs(uploaded_files)
        st.success(f"{len(saved)}개 파일을 저장했습니다: {', '.join(saved)}")
        st.info("새 문서를 검색에 반영하려면 아래 'DB 생성' 버튼을 누르세요.")

    st.divider()
    st.subheader("🔄 DB 생성")
    st.caption("기존 벡터 DB를 초기화하고 documents 폴더 기준으로 다시 생성합니다.")

    if st.button("DB 초기화 및 재생성"):
        # 캐시된 Chroma 연결이 chroma_db 파일을 잡고 있으면
        # Windows에서 폴더 삭제가 실패하므로 먼저 캐시를 비운다.
        st.cache_resource.clear()

        with st.spinner("기존 DB 삭제 후 다시 생성 중입니다..."):
            shutil.rmtree(PERSIST_DIRECTORY, ignore_errors=True)

            result = subprocess.run(
                [sys.executable, "ingest.py"],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:
            st.success("DB를 다시 생성했습니다.")
            if result.stdout:
                st.code(result.stdout)
        else:
            st.error("DB 생성 중 오류가 발생했습니다.")
            st.code(result.stderr or result.stdout)


@st.cache_resource
def get_vector_db():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="rag_documents"
    )


@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )


def answer_question(question: str):
    vector_db = get_vector_db()
    llm = get_llm()

    retrieved_docs = vector_db.similarity_search(
        question,
        k=3
    )

    if not retrieved_docs:
        return "관련 문서를 찾지 못했습니다.", []

    context = "\n\n".join(
        [
            f"[출처: {doc.metadata.get('source', '알 수 없음')}]\n{doc.page_content}"
            for doc in retrieved_docs
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

    return response.content, sources


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("문서에 대해 질문해 보세요.")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("관련 문서를 찾고 있습니다..."):
            answer, sources = answer_question(question)

        st.markdown(answer)

        if sources:
            st.caption(f"참고 문서: {', '.join(sources)}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )