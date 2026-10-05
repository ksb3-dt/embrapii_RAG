# EMBRAPII Reports RAG

Local Docker-based MVP for analyzing public EMBRAPII PDF reports. The application is an internal tool for managers and should prioritize grounded answers, page-level citations, and evidence auditing in later milestones.


## Stack

| Service  | Technology              | Default port |
| -------- | ----------------------- | ------------ |
| Frontend | React + TypeScript + Vite | `5173`     |
| Backend  | Python + FastAPI + uv   | `8000`       |
| Worker   | Python (placeholder)    | n/a          |
| Redis    | Redis 7                 | `6379`       |
| Qdrant   | Qdrant                  | `6333`       |

Persistent local data:

- `data/documents/` — PDF storage (used in later milestones)
- `data/qdrant/` — Qdrant vector store data
- `data/app.db` — SQLite metadata (planned for later milestones)

## Prerequisites

- Docker and Docker Compose
- `curl` (for the health script)
- Optional: `redis-cli` on the host if Redis is checked outside Docker

No API keys or other secrets are required for Milestone 1.

## Quick start

From the repository root:

```bash
cp .env.example .env
docker compose up --build
```

After the stack starts:

- Frontend shell: [http://localhost:5173](http://localhost:5173)
- Backend health: [http://localhost:8000/health](http://localhost:8000/health)

To run services in the background:

```bash
docker compose up --build -d
```

To stop the stack:

```bash
docker compose down
```

## Verify the stack

Run the health script from the repository root:

```bash
bash scripts/check-health.sh
```

The script checks:

- Backend `GET /health` (required)
- Qdrant health on port `6333` (required)
- Redis `PING` via `docker compose exec` when possible (required)
- Worker container running status (required)
- Frontend availability on port `5173` (optional; failure does not fail the script)

The script exits `0` when all required checks pass and `1` when any required check fails.

## Environment variables

Copy `.env.example` to `.env` and adjust if needed. Defaults match the Docker Compose setup:

| Variable       | Default                     | Purpose                          |
| -------------- | --------------------------- | -------------------------------- |
| `BACKEND_HOST` | `0.0.0.0`                   | Backend bind host                |
| `BACKEND_PORT` | `8000`                      | Backend host port                |
| `FRONTEND_PORT`| `5173`                      | Frontend host port               |
| `REDIS_URL`    | `redis://redis:6379/0`      | Redis URL inside Compose network |
| `QDRANT_URL`   | `http://qdrant:6333`        | Qdrant URL inside Compose network|
| `DOCUMENTS_DIR`| `/app/data/documents`       | PDF directory inside containers  |


## Development notes

Backend (outside Docker, optional):

```bash
cd backend
uv sync
uv run pytest -q
uv run ruff check .
```

Frontend (outside Docker, optional):

```bash
cd frontend
npm install
npm run build
```

## Project documentation

- `PROJECT_DECISIONS.md` — product and architecture source of truth
- `AGENTS.md` — conventions for coding agents
- `docs/specs/` — implementation specs by milestone
