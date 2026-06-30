# AGENTS.md

## First Step

Read `PROJECT_DECISIONS.md` before making project changes. It is the source of truth for the MVP scope, architecture, constraints, conventions, and milestones.

## Project Goal

Build a local Docker-based MVP RAG application for analyzing public EMBRAPII PDF reports. The app is an internal tool for managers and should prioritize high accuracy, grounded answers, page-level citations, and evidence auditing.

## Core Product Scope

The MVP supports:

- Portuguese-only user questions.
- Question answering across reports with citations.
- Structured summary of one report.
- Structured comparison of multiple reports.
- User-uploaded PDFs stored in `data/documents/`.
- Evidence auditing through an `Auditar` button on answer cards.
- Golden-set evaluation under `docs/evaluation/`.

The MVP does not include:

- OCR for scanned PDFs.
- Advanced table extraction beyond PyMuPDF.
- User permissions or role-based access.
- Document version history.
- Persistent API key storage.
- Fine-tuning.
- In-app PDF viewer.

## Architecture Rules

Use pragmatic Hexagonal Architecture.

- Keep FastAPI routes thin.
- Put workflow coordination in application services/use cases.
- Keep domain models and policies independent of FastAPI, Qdrant, PyMuPDF, LangChain, and LLM SDKs.
- Define ports/interfaces only where replacement is realistic.
- Put concrete integrations in infrastructure adapters.
- Wire mostly static dependencies in `backend/app/core/dependencies.py`.
- Use a request/session-specific LLM provider factory for provider, model, and API key selection.

## Stack

- Frontend: React + TypeScript + Vite + npm.
- Backend: Python + FastAPI + LangChain + uv.
- Vector store: Qdrant.
- Metadata storage: SQLite at `data/app.db`.
- Embeddings: local `BAAI/bge-m3`, 1024 dimensions.
- PDF parsing: PyMuPDF.
- Job queue: Redis + RQ.
- Containers: frontend, backend, worker, Redis, and Qdrant.

Default local ports:

- Frontend: `5173`
- Backend: `8000`
- Qdrant: `6333`
- Redis: `6379`

`docker compose up --build` should start the full local MVP stack.

## Retrieval Rules

Use:

- Dense retrieval with `BAAI/bge-m3`.
- Exact keyword retrieval.
- Reciprocal Rank Fusion to combine dense and keyword results.

Do not add reranking in the MVP unless a later decision or ADR explicitly changes this.

Answers must be grounded in retrieved report content. Do not use general model knowledge for factual claims unless explicitly requested by a future decision.

## Citation And Evidence Rules

- Important factual claims should cite report pages.
- Numbers, dates, named programs, and comparisons should be cited when possible.
- If evidence is insufficient, clearly say the information was not found in the indexed reports.
- If confidence is low, show a small warning at the beginning of the answer and mention the uncertainty in the answer text.
- Store enough evidence metadata to power the `Auditar` view.

Evidence chunks should include useful metadata such as:

- Document/report title.
- Page number.
- Chunk text.
- Retrieval source.
- Rank/score.
- Citation information.

## LLM Provider Rules

The app should support predefined dropdown options for:

- Claude.
- Gemini.
- OpenAI.
- DeepSeek.

Users paste their API key each session. Do not hardcode keys. Do not persist API keys unless a future decision explicitly adds encrypted persistence.

## Prompt Rules

Do not scatter prompts through API routes.

Store prompts in:

- `backend/app/application/prompts/qa_prompt.py`
- `backend/app/application/prompts/summary_prompt.py`
- `backend/app/application/prompts/comparison_prompt.py`

Prompts must support grounded answers, citation behavior, insufficient-evidence behavior, low-confidence wording, structured summaries, and structured comparisons.

## Output Structures

Report summaries should use:

1. Executive Summary
2. Main Findings
3. Relevant Numbers/KPIs
4. Risks, Gaps, Or Limitations
5. Notable Evidence
6. What Was Not Clear

Multi-report comparisons should use:

1. High-Level Conclusion
2. Similarities
3. Differences
4. Trends Over Time
5. Evidence By Report
6. Uncertainties Or Missing Data

Separate what reports explicitly say from interpretation or implications.

## Frontend Rules

The MVP frontend should be centered around a chat screen.

- Include a sidebar with chat history.
- Let users ask normal questions by typing in chat.
- Expose actions such as `Compare Documents` and `Summarize Document` as buttons/actions.
- Show `Auditar` on answer fields and open a popup or side panel with evidence chunks.
- Include document upload, document list, and document deletion.
- Do not include an in-app PDF viewer.
- Evaluation should be accessible from another part of the app through a menu.

## Coding Conventions

- Code identifiers, filenames, modules, API fields, database fields, commit messages, and technical documentation must be written in English.
- Code comments must be written in Portuguese.
- Comments should explain intent, trade-offs, or non-obvious behavior; avoid comments that merely restate the code.
- Public ports/interfaces and non-obvious services should have short docstrings.

Backend:

- Use `uv` for dependency management.
- Use `pytest` for tests.
- Use `ruff` for linting and formatting.

Frontend:

- Use `npm`.
- Use `eslint` and `prettier`.

## API Conventions

Successful FastAPI responses may return response objects directly.

Application-level errors should use:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error message.",
  "details": {}
}
```

FastAPI validation errors may keep the default FastAPI validation response unless a future decision changes this.

## Testing Expectations

Each implementation spec must include acceptance criteria and verification steps.

Add automated tests where practical, especially for:

- Chunking behavior.
- Reciprocal Rank Fusion.
- Confidence and not-found behavior.
- API schemas and key routes.
- Job status behavior.

Manual verification is acceptable for early MVP milestones, especially Docker startup, PDF extraction quality, retrieval quality, and LLM output behavior.

## Documentation Rules

- Update `README.md` when setup, Docker usage, or user-facing workflows change.
- Use `docs/specs/` for implementation specs.
- Use `docs/adr/` only for future architecture decisions made after coding starts.
- If implementation diverges from `PROJECT_DECISIONS.md`, update the relevant decision document or add an ADR.

## Safety Rules

- Do not modify an older project folder related to the first version of this RAG.
- Do not commit unless explicitly asked.
- Do not add secrets, API keys, or credentials to the repository.
- Keep edits scoped to the current spec or user request.
