# Milestone 2 Overview And Direction Check

Project: EMBRAPII Reports RAG  
Milestone: 2 - Backend Architecture Skeleton  
Review date: 2026-06-30  
Reviewer: Cursor agent

## Executive Summary

Milestone 2 is complete for its intended scope. The backend now has a pragmatic hexagonal architecture skeleton with domain models, policies, ports, API route placeholders, application service placeholders, use-case wrappers, and centralized dependency wiring.

The project is moving in the right direction. The implementation keeps real RAG behavior out of this milestone, avoids fake answers or fake evidence, preserves thin FastAPI routes, and keeps domain/application code independent from concrete infrastructure such as Qdrant, PyMuPDF, Redis, LangChain, and LLM SDKs.

No blocker or high-severity issue was found. The most important follow-up before Milestone 3 is to tighten the service and dependency story for document operations: upload is already routed through `DocumentIngestionService`, but document list/delete still return placeholder responses directly from the route layer.

## Scope Check

Milestone 2 expected:

- Pragmatic hexagonal backend folder structure.
- Importable domain models and policy placeholders.
- Typed ports/interfaces for realistic replacement points.
- Typed API schemas and route placeholders for MVP surfaces.
- Application service placeholders for planned workflows.
- Dependency wiring in `backend/app/core/dependencies.py`.
- Tests for imports, route registration, placeholder behavior, and boundary rules.

All of those are present.

Milestone 2 explicitly did not include PDF parsing, chunking, embedding, Qdrant indexing, retrieval, LLM calls, citations, evidence persistence, SQLite repositories, Redis/RQ jobs, summary generation, comparison generation, or golden-set evaluation. The current implementation respects that boundary.

## Current Validation Results

Backend validation:

- `uv sync --locked --dev`: passed
- `uv run pytest -q`: `56 passed, 1 warning`
- `uv run ruff check --no-cache .`: passed
- `uv run ruff format --check --no-cache .`: `82 files already formatted`

Known non-blocking warnings and environment notes:

- Backend tests emit a Starlette/TestClient deprecation warning about `httpx`.
- `uv run ruff check .` without `--no-cache` failed because `backend/.ruff_cache` has a local filesystem permission issue. Ruff itself passes when cache is disabled.
- The working tree contains an unrelated untracked report file: `docs/reports/milestone-01-overview-direction-check.md`.

## Architecture And Direction Assessment

Positive signs:

- `backend/app/main.py` registers routes through a centralized router list.
- API routes are thin and use dependency aliases from `backend/app/core/dependencies.py`.
- Placeholder routes return explicit HTTP `501` responses using the shared `NOT_IMPLEMENTED` error shape.
- Application services raise `NotImplementedApplicationError` instead of returning fake RAG results.
- Domain models and policies do not import FastAPI, Qdrant, PyMuPDF, LangChain, Redis, RQ, or LLM SDKs.
- Ports use `typing.Protocol` and define replacement points that match the MVP plan.
- LLM provider, model, and API key are represented as request/session fields only; no API keys are hardcoded or persisted.
- Tests cover package layout, domain models, policies, port contracts, API placeholders, service placeholders, and dependency wiring.

Direction risks to watch:

- Document list/delete are route-level placeholders today. They should move behind `DocumentIngestionService` or a dedicated document service before real document management logic is added.
- Use-case wrappers exist but are not wired. Decide early whether routes should depend on services directly or on use cases, so the project does not maintain two workflow boundaries without a reason.
- Service constructors are currently parameterless. Milestone 3 should introduce constructor injection for realistic ports such as `DocumentParser`, `FileStorage`, and document/chunk repositories.
- Prompt files are not present yet. That is acceptable for Milestone 2 and Milestone 3, but `qa_prompt.py`, `summary_prompt.py`, and `comparison_prompt.py` should be added before Q&A, summary, or comparison work.

## Findings

### Blockers

None.

### High Severity

None.

### Medium Severity

1. Document list/delete bypass the service layer.
   - Evidence: `backend/app/api/routes/documents.py` routes upload through `DocumentIngestionService.ingest_document()`, while list and delete return `not_implemented_response()` directly.
   - Impact: real document management logic could drift into routes when Milestone 3 adds storage and metadata.
   - Recommendation: extend the application service boundary with list/delete methods, or introduce a dedicated document management service before implementing real behavior.

2. Use-case wrappers are unwired and may duplicate services.
   - Evidence: `backend/app/application/use_cases/` contains pass-through wrappers, but routes and `dependencies.py` currently inject services directly.
   - Impact: future agents may be unsure whether orchestration belongs in services or use cases.
   - Recommendation: choose one primary workflow boundary before Milestone 3 grows the ingestion path.

3. Dependency injection needs to evolve before real ingestion.
   - Evidence: service providers in `backend/app/core/dependencies.py` currently instantiate parameterless placeholders.
   - Impact: Milestone 3 will need parser, storage, and repository dependencies. If this is delayed, concrete infrastructure may leak into routes or services ad hoc.
   - Recommendation: wire Milestone 3 adapters through ports in `dependencies.py` as soon as they are introduced.

### Low Severity

1. README still describes the project as Milestone 1 only.
   - Recommendation: update `README.md` after accepting Milestone 2 so project status stays accurate.

2. Ruff cache has a local permission issue.
   - Recommendation: recreate or clean `backend/.ruff_cache`; keep `--no-cache` as a temporary workaround.

3. `ConfidencePolicy` is an early placeholder and should be revisited.
   - Recommendation: tune thresholds and confidence categories with retrieval results and the golden set.

4. Prompt modules are still missing.
   - Recommendation: add prompt stubs before Milestone 6, and avoid placing prompts in API routes.

5. Evidence/service return types are placeholders.
   - Recommendation: define mapping from domain models to response schemas when real evidence and answer persistence are implemented.

## Go / No-Go Recommendation

Go for the next milestone.

Milestone 2 achieved its purpose: the backend architecture skeleton is present, tested, and aligned with the project decisions. The project is ready for Milestone 3, provided the ingestion prototype stays focused on PDF parsing, local file storage, page/chunk metadata, and clean port-based wiring.

Recommended next order:

1. Update README/status copy to acknowledge Milestone 2 completion.
2. Decide whether routes depend on services directly or use cases.
3. Move document list/delete behind an application service boundary.
4. Start Milestone 3 with `PyMuPDF` parsing and local storage adapters wired through ports.
5. Add SQLite metadata persistence alongside or immediately after the ingestion prototype, before embedding and Qdrant indexing.
