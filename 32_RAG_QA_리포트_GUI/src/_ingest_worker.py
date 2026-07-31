"""
인제스트 subprocess 헬퍼 — app_gui.py 에서 QProcess 로 호출됩니다.
사용: python _ingest_worker.py <file_path>
출력: OK:<chunk_count>  또는  ERR:<message>
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

def main():
    if len(sys.argv) < 2:
        print("ERR:파일 경로 없음")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"ERR:파일 없음: {file_path}")
        sys.exit(1)

    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(str(file_path))
        else:
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(str(file_path), encoding="utf-8")

        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file_path.name

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
        split_docs = splitter.split_documents(docs)

        emb = OpenAIEmbeddings(model="text-embedding-3-small")
        db = Chroma(
            persist_directory=str(BASE_DIR / "chroma_db"),
            embedding_function=emb,
            collection_name="rag_documents",
        )
        db.add_documents(split_docs)

        print(f"OK:{len(split_docs)}")
        sys.exit(0)

    except Exception as e:
        print(f"ERR:{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
