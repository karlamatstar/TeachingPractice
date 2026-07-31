"""
DB 초기화 + 전체 재생성 스크립트 — app_gui.py 에서 QProcess 로 호출
출력 프로토콜:
  DB_CLEARED
  FILE_DONE:<name>:<chunks>
  FILE_ERR:<name>:<msg>
  REBUILD_DONE
"""
import sys, io, re, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
from pathlib import Path

_UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
)

BASE_DIR = Path(__file__).parent
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

DOCUMENTS_DIR = BASE_DIR / "documents"
PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "rag_documents"
ALLOWED_EXT = {".pdf", ".txt", ".md"}


def main():
    # shutil.rmtree 대신 API로 컬렉션 삭제 (메인 앱이 sqlite3 파일을 열고 있어 삭제 불가)
    import chromadb
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # 고아 UUID 폴더 정리 (delete_collection 후 남는 벡터 인덱스 폴더들)
    for item in Path(PERSIST_DIRECTORY).iterdir():
        if item.is_dir() and _UUID_RE.match(item.name):
            shutil.rmtree(item, ignore_errors=True)

    print("DB_CLEARED", flush=True)

    files = sorted(
        [f for f in DOCUMENTS_DIR.iterdir() if f.suffix.lower() in ALLOWED_EXT]
    ) if DOCUMENTS_DIR.exists() else []

    if not files:
        print("REBUILD_DONE", flush=True)
        sys.exit(0)

    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    emb = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=emb,
        collection_name=COLLECTION_NAME,
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)

    for f in files:
        try:
            suffix = f.suffix.lower()
            if suffix == ".pdf":
                from langchain_community.document_loaders import PyPDFLoader
                loader = PyPDFLoader(str(f))
            else:
                from langchain_community.document_loaders import TextLoader
                loader = TextLoader(str(f), encoding="utf-8")

            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = f.name

            chunks = splitter.split_documents(docs)
            db.add_documents(chunks)
            print(f"FILE_DONE:{f.name}:{len(chunks)}", flush=True)
        except Exception as e:
            print(f"FILE_ERR:{f.name}:{e}", flush=True)

    print("REBUILD_DONE", flush=True)


if __name__ == "__main__":
    main()
