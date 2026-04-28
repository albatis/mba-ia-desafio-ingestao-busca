import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector


load_dotenv()
for k in ("GOOGLE_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_PATH = os.getenv("PDF_PATH")

pdf_path = os.path.join(PDF_PATH, "document.pdf")

docs = PyPDFLoader(str(pdf_path)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, add_start_index=False).split_documents(docs)
if not splits:
    raise SystemExit(0)

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
]    

ids = [f"doc-{i}" for i in range(len(enriched))]

google_embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
if google_embedding_model in ("models/embedding-001", "text-embedding-004", "models/text-embedding-004"):
    google_embedding_model = "models/gemini-embedding-001"

embeddings = GoogleGenerativeAIEmbeddings(model=google_embedding_model)

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

store.add_documents(documents=enriched, ids=ids)



def ingest_pdf():
    pass


if __name__ == "__main__":
    ingest_pdf()