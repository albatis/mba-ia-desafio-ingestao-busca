import os
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()
for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_PATH = os.getenv("PDF_PATH")

pdf_path = os.path.join(PDF_PATH, "document.pdf")

docs = PyPDFLoader(str(pdf_path)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150, add_start_index=False
).split_documents(docs)
if not splits:
    raise SystemExit(0)

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
    )
    for d in splits
]

ids = [f"doc-{i}" for i in range(len(enriched))]

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
)

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

batch_size = int(os.getenv("INGEST_BATCH_SIZE", "2"))
pause_seconds = float(os.getenv("INGEST_BATCH_PAUSE_SECONDS", "15"))

for i in range(0, len(enriched), batch_size):
    batch_docs = enriched[i : i + batch_size]
    batch_ids = ids[i : i + batch_size]

    try:
        store.add_documents(documents=batch_docs, ids=batch_ids)
    except Exception as e:
        print(e)
        raise

    if pause_seconds > 0:
        time.sleep(pause_seconds)

def ingest_pdf():
    pass

if __name__ == "__main__":
    ingest_pdf()
