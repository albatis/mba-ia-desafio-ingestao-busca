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

3. Copie o arquivo `.env.example` para `.env` e preencha as variáveis necessárias conforme seu ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com seus dados (chaves de API, caminhos, etc).

Observacoes:
- O script espera um arquivo `document.pdf` dentro de `PDF_PATH`.
- Atualmente o `src/ingest.py` usa `DATABASE_URL` e `PG_VECTOR_COLLECTION_NAME`.

4. Execute a ingestao:

```bash
python src/ingest.py
```

Tempo de execução observado: 8m51,575s

Informações do hardware utilizado para este teste:
- CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz (12 threads)
- Memória RAM: 15 GiB
- Armazenamento: SSD NVMe, 234 GB total, 42 GB livres
- Sistema operacional: Linux x86_64

5. Execute o chat para perguntar e obter respostas referentes aos dados do document.pdf:

```bash
python src/chat.py
```