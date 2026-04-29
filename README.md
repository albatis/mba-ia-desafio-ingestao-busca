# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.

## Como executar o ingest.py

1. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Suba o PostgreSQL com pgvector:

```bash
docker compose up -d
```

3. Configure o arquivo `.env` com os valores necessarios para ingestao:

```env
GOOGLE_API_KEY=...
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=document_collection
PDF_PATH=.
INGEST_BATCH_SIZE=2
INGEST_BATCH_PAUSE_SECONDS=15
```

Observacoes:
- O script espera um arquivo `document.pdf` dentro de `PDF_PATH`.
- Atualmente o `src/ingest.py` usa `PGVECTOR_URL` e `PGVECTOR_COLLECTION`.

4. Execute a ingestao:

```bash
python src/ingest.py
```