# EMBRAPII Reports RAG

MVP local baseado em Docker para análise de relatórios públicos em PDF da EMBRAPII. A aplicação é uma ferramenta interna para gestores e, nos marcos futuros, deve priorizar respostas fundamentadas, citações em nível de página e auditoria de evidências.

**Status do Marco 1:** Este repositório oferece atualmente apenas o scaffold de infraestrutura local. Os fluxos de RAG (ingestão, recuperação, Q&A, resumos, comparações, auditoria de evidências e avaliação) **ainda não estão implementados**.

## Stack

| Serviço  | Tecnologia              | Porta padrão |
| -------- | ----------------------- | ------------ |
| Frontend | React + TypeScript + Vite | `5173`     |
| Backend  | Python + FastAPI + uv   | `8000`       |
| Worker   | Python (placeholder)    | n/a          |
| Redis    | Redis 7                 | `6379`       |
| Qdrant   | Qdrant                  | `6333`       |

Dados locais persistentes:

- `data/documents/` — armazenamento de PDFs (usado em marcos futuros)
- `data/qdrant/` — dados do vector store Qdrant
- `data/app.db` — metadados SQLite (planejado para marcos futuros)

## Pré-requisitos

- Docker e Docker Compose
- `curl` (para o script de health check)
- Opcional: `redis-cli` no host, se o Redis for verificado fora do Docker

Nenhuma chave de API ou outro segredo é necessário para o Marco 1.

## Início rápido

Na raiz do repositório:

```bash
cp .env.example .env
docker compose up --build
```

Após a subida da stack:

- Shell do frontend: [http://localhost:5173](http://localhost:5173)
- Health do backend: [http://localhost:8000/health](http://localhost:8000/health)

Para executar os serviços em segundo plano:

```bash
docker compose up --build -d
```

Para parar a stack:

```bash
docker compose down
```

## Verificar a stack

Execute o script de health check na raiz do repositório:

```bash
bash scripts/check-health.sh
```

O script verifica:

- Backend `GET /health` (obrigatório)
- Health do Qdrant na porta `6333` (obrigatório)
- Redis `PING` via `docker compose exec`, quando possível (obrigatório)
- Status de execução do container do worker (obrigatório)
- Disponibilidade do frontend na porta `5173` (opcional; falha não reprova o script)

O script encerra com código `0` quando todas as verificações obrigatórias passam e com `1` quando alguma falha.

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste se necessário. Os padrões correspondem à configuração do Docker Compose:

| Variável        | Padrão                      | Finalidade                           |
| --------------- | --------------------------- | ------------------------------------ |
| `BACKEND_HOST`  | `0.0.0.0`                   | Host de bind do backend              |
| `BACKEND_PORT`  | `8000`                      | Porta do backend no host             |
| `FRONTEND_PORT` | `5173`                      | Porta do frontend no host            |
| `REDIS_URL`     | `redis://redis:6379/0`      | URL do Redis na rede do Compose      |
| `QDRANT_URL`    | `http://qdrant:6333`        | URL do Qdrant na rede do Compose     |
| `DOCUMENTS_DIR` | `/app/data/documents`       | Diretório de PDFs dentro dos containers |

## O que funciona no Marco 1

- `docker compose up --build` sobe frontend, backend, worker, Redis e Qdrant
- O backend expõe `GET /health` com `status: ok`
- O worker inicia como processo placeholder separado (sem jobs em background ainda)
- O frontend exibe o shell do MVP e a lista de capacidades planejadas
- `scripts/check-health.sh` reporta a saúde dos serviços a partir do host

## O que ainda não está implementado

Não espere que o seguinte funcione no Marco 1:

- Upload, ingestão, chunking ou indexação de PDFs
- Embeddings (`BAAI/bge-m3`) ou coleções Qdrant para recuperação
- Recuperação densa/por palavra-chave ou Reciprocal Rank Fusion
- Q&A em português com citações
- Resumos estruturados de relatórios ou comparações entre múltiplos relatórios
- Auditoria de evidências (`Auditar`)
- Avaliação com golden set
- Chamadas a provedores de LLM ou tratamento de chaves de API
- Jobs em background via Redis + RQ

Esses fluxos estão planejados para marcos futuros. Consulte `PROJECT_DECISIONS.md` e `docs/specs/` para o roadmap completo.

## Notas de desenvolvimento

Backend (fora do Docker, opcional):

```bash
cd backend
uv sync
uv run pytest -q
uv run ruff check .
```

Frontend (fora do Docker, opcional):

```bash
cd frontend
npm install
npm run build
```

## Documentação do projeto

- `PROJECT_DECISIONS.md` — fonte da verdade de produto e arquitetura
- `AGENTS.md` — convenções para agentes de codificação
- `docs/specs/` — especificações de implementação por marco
