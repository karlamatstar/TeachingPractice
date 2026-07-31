import os
import streamlit as st
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

PERSIST_DIRECTORY = "chroma_db"

st.set_page_config(
    page_title="RAG 문서 챗봇",
    page_icon="📚"
)

st.title("📚 RAG 기반 문서 챗봇")
st.caption("등록된 문서 내용에 근거하여 답변합니다.")


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