# Milestone 1 Overview And Direction Check

Project: EMBRAPII Reports RAG  
Milestone: 1 - Project Scaffold And Docker  
Review date: 2026-06-30  
Reviewer: Cursor agent

## Executive Summary

Milestone 1 is complete for its intended scope. The project has a runnable local Docker scaffold with frontend, backend, worker, Redis, and Qdrant services, plus a host health script and README instructions.

The project is moving in the right direction. The implementation keeps RAG behavior out of Milestone 1, does not fake ingestion or question answering, and leaves the codebase ready for the backend architecture skeleton and later ingestion/retrieval work.

No blocker or high-severity issue was found. The most important risk is Docker readiness: immediately after `docker compose up --build -d`, the first health script run failed because the backend was not reachable yet; a retry moments later passed. This confirms that Compose healthchecks and readiness-aware startup should be added before ingestion, indexing, or background jobs depend on Redis and Qdrant.

## Scope Check

Milestone 1 expected:

- Docker Compose stack with `frontend`, `backend`, `worker`, `redis`, and `qdrant`.
- Backend `GET /health`.
- Placeholder worker process.
- React + TypeScript + Vite frontend shell.
- Local persistence paths under `data/documents/` and `data/qdrant/`.
- `scripts/check-health.sh`.
- README and non-secret environment template.

All of those are present.

Milestone 1 explicitly did not include PDF ingestion, embeddings, Qdrant indexing, retrieval, Q&A, citations, summaries, comparisons, evidence audit, evaluation, LLM calls, API key handling, or Redis + RQ jobs. The current implementation respects that boundary.

The repository now also contains Milestone 2 backend skeleton work: placeholder API routes, application services, ports, domain models, and dependency wiring. That is not a Milestone 1 problem, but future reviews should separate M1 acceptance from M2 progress.

## Current Validation Results

Static validation passed:

- `uv --directory backend sync --frozen`
- `uv --directory backend run pytest -q`: `56 passed, 1 warning`
- `uv --directory backend run ruff check .`: passed
- `uv --directory backend run ruff format --check .`: `82 files already formatted`
- `npm --prefix frontend run build`: passed
- `npm --prefix frontend run lint`: passed
- `docker compose config`: passed
- `bash -n scripts/check-health.sh`: passed

Runtime validation:

- `docker compose ps` showed all five services running.
- `docker compose up --build -d` rebuilt and started backend, frontend, and worker successfully.
- The immediate `bash scripts/check-health.sh` run failed on backend reachability while Qdrant, Redis, worker, and frontend passed.
- A retry shortly after startup passed all checks:
  - Backend `/health`
  - Qdrant `/healthz`
  - Redis `PING`
  - Worker container running
  - Frontend optional check

Known non-blocking warnings:

- Backend tests emit a Starlette/TestClient deprecation warning.
- npm emits an environment warning for unknown config `devdir`; this appears local and does not fail build or lint.

## Architecture And Direction Assessment

Positive signs:

- Service names, ports, and local data paths match `PROJECT_DECISIONS.md`.
- Docker Compose includes the expected five-service local MVP stack.
- The frontend shell clearly says upload, Q&A, summary, comparison, and evidence audit are not functional yet.
- Backend placeholder routes return explicit `501` responses with `NOT_IMPLEMENTED`.
- Application services raise not-implemented errors instead of returning fake answers or fake evidence.
- Tests cover placeholder API behavior, service placeholders, package layout, ports, dependency wiring, domain models, and policies.
- Domain and application modules currently have no imports from FastAPI, Qdrant, PyMuPDF, LangChain, Redis, RQ, or LLM SDKs.
- Dependency wiring is centralized in `backend/app/core/dependencies.py`.
- No hardcoded LLM secrets or provider API keys were found.

Direction risk to watch:

- `README.md` and `frontend/src/App.tsx` still describe the project as Milestone 1 only, while the backend has already moved into Milestone 2 skeleton work. This is acceptable during active development, but documentation/status copy should be updated when Milestone 2 is accepted.

## Findings

### Blockers

None.

### High Severity

None.

### Medium Severity

1. Docker startup is not readiness-aware.
   - Evidence: the immediate health script run after `docker compose up --build -d` failed because backend `/health` was not reachable yet; a retry passed.
   - Impact: later ingestion or background jobs may race Redis, Qdrant, or backend startup.
   - Recommendation: add Compose `healthcheck:` blocks and use readiness-aware `depends_on` where appropriate.

2. Qdrant uses `qdrant/qdrant:latest`.
   - Impact: reproducibility risk across machines and future runs.
   - Recommendation: pin Qdrant to a tested version before retrieval/indexing work.

3. Backend `/health` does not live-probe Redis or Qdrant.
   - Impact: backend can report `status: ok` while dependencies are not actually validated.
   - Recommendation: keep this acceptable for M1/M2 placeholders, but add live probes once real Redis/Qdrant clients are introduced.

### Low Severity

1. Worker health is only container-running status.
   - Recommendation: add worker heartbeat or queue connectivity checks when Redis + RQ jobs are implemented.

2. Prettier is not configured for the frontend.
   - Recommendation: add Prettier when frontend work becomes more active.

3. No CI pipeline exists.
   - Recommendation: add CI after the early milestone workflow stabilizes on `develop`.

4. README and frontend status copy may drift as Milestone 2 progresses.
   - Recommendation: update user-facing status after M2 is accepted.

## Go / No-Go Recommendation

Go for the next milestone.

Milestone 1 achieved its purpose: the local scaffold exists, validates, and starts. The immediate health-check timing failure is not an acceptance blocker, but it is strong evidence that Docker readiness hardening should happen before Milestone 3 or before any workflow depends on Redis, Qdrant, or background jobs at startup.

Recommended next order:

1. Finish or accept Milestone 2 backend architecture skeleton.
2. Add a small Docker hardening pass: Compose healthchecks, pinned Qdrant version, and clearer backend dependency health semantics.
3. Then proceed to the PDF ingestion prototype.
