# 문서를 벡터 DB에 저장하는 코드
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCUMENTS_DIR = Path("documents")
PERSIST_DIRECTORY = "chroma_db"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*"):
        suffix = file_path.suffix.lower()

        if suffix in [".txt", ".md"]:
            loader = TextLoader(str(file_path), encoding="utf-8")
        elif suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        else:
            continue

        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source"] = file_path.name

        documents.extend(loaded_docs)

    return documents


def create_vector_db():
    documents = load_documents()

    if not documents:
        raise ValueError("documents 폴더에 .txt 또는 .md 문서가 없습니다.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    split_documents = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    Chroma.from_documents(
        documents=split_documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="rag_documents"
    )

    return len(documents), len(split_documents)


if __name__ == "__main__":
    document_count, chunk_count = create_vector_db()

    print(f"원본 문서 수: {document_count}")
    print(f"저장된 문서 조각 수: {chunk_count}")
    print("벡터 DB 생성이 완료되었습니다.")