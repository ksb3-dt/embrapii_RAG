# Milestone 03c: Local Storage And SQLite

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-03c-local-storage-and-sqlite"
title: "Local File Storage And SQLite Metadata"
created_at_utc: "2026-07-01T14:40:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-03-overview.md"
depends_on:
  - "docs/specs/milestone-03a-pymupdf-parser.md"
  - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 3. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window. Follow the pattern of spec division I was using in this project.
```

## 3. System Interpretation

```yaml
system_translation: |
  Implement the local infrastructure needed by the ingestion prototype: storing
  uploaded PDFs under the configured documents directory and persisting document
  and chunk metadata in SQLite at data/app.db. This spec should provide concrete
  FileStorage, DocumentRepository, and ChunkRepository adapters without changing
  document API behavior yet.

  Expected user-visible result:
    - No route behavior changes yet unless a previous accepted spec already
      started replacing placeholders.

  Expected engineering result:
    - Local storage and SQLite adapters are tested and ready for
      DocumentIngestionService to orchestrate in the next child spec.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Implement LocalFileStorage for saving, resolving, and deleting PDF files under the configured documents directory."
    - "Implement SQLiteDocumentRepository and SQLiteChunkRepository for document and chunk metadata."
    - "Create SQLite schema initialization for documents and chunks."
    - "Add settings for SQLite database path if missing, preserving data/app.db as the default."
    - "Add tests using temporary directories and temporary SQLite databases."
  out_of_scope:
    - "Do not implement answer, job, evidence, or evaluation repositories unless existing tests require placeholders to remain importable."
    - "Do not implement parser, chunking, service orchestration, API upload behavior, embeddings, Qdrant indexing, retrieval, or background jobs."
    - "Do not add Alembic or migration tooling unless the repository already uses it; keep MVP SQLite initialization simple."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/core/config.py"
      - "backend/app/infrastructure/storage/local_file_storage.py"
      - "backend/app/infrastructure/persistence/sqlite_repositories.py"
      - "backend/tests/test_local_file_storage.py"
      - "backend/tests/test_sqlite_repositories.py"
  tests:
    unit:
      - "backend/tests/test_local_file_storage.py"
      - "backend/tests/test_sqlite_repositories.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Concrete filesystem behavior belongs in backend/app/infrastructure/storage/local_file_storage.py."
  - "Concrete SQLite behavior belongs in backend/app/infrastructure/persistence/sqlite_repositories.py."
  - "Application services and routes must not open SQLite connections directly."
  - "Repositories implement existing ports from backend/app/ports/repositories.py."
  - "File storage implements the existing FileStorage port from backend/app/ports/file_storage.py."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious intent."
  - "Use parameterized SQL for all variable values."
  - "Keep SQLite schema small and explicit."
  - "Use pathlib for path safety."
```

## 7. Storage And Persistence Contract Requirements

```yaml
contracts:
  file_storage_contracts:
    - name: "LocalFileStorage.save_pdf"
      requirements:
        - "Accepts filename and bytes."
        - "Rejects empty content and non-PDF filenames or content if a lightweight validation is practical."
        - "Sanitizes filenames to avoid path traversal."
        - "Stores under the configured documents directory."
        - "Returns a storage-relative path suitable for Document.source_path."
    - name: "LocalFileStorage.resolve_document_path"
      requirements:
        - "Resolves only paths under the configured documents directory."
        - "Rejects traversal outside the storage root."
    - name: "LocalFileStorage.delete_document_file"
      requirements:
        - "Deletes the stored file if it exists."
        - "Does not delete paths outside the storage root."

  repository_contracts:
    - name: "SQLiteDocumentRepository"
      methods:
        - "save_document(document) -> Document"
        - "get_document(document_id) -> Document | None"
        - "list_documents() -> list[Document]"
        - "delete_document(document_id) -> None"
      compatibility: "must implement existing DocumentRepository port"
    - name: "SQLiteChunkRepository"
      methods:
        - "save_chunks(chunks) -> None"
        - "get_chunks_by_document(document_id) -> list[DocumentChunk]"
      compatibility: "must implement existing ChunkRepository port"

  schema_contracts:
    - name: "documents table"
      fields:
        - "id"
        - "filename"
        - "source_path"
        - "status"
        - "title"
        - "created_at"
        - "updated_at"
    - name: "chunks table"
      fields:
        - "chunk_id"
        - "document_id"
        - "page_number"
        - "text"
        - "chunk_type"
        - "section_title"
        - "source_file_path"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect ports and settings"
    action: "Read FileStorage, repositories ports, domain models, and backend/app/core/config.py."
    expected_output: "Adapter constructors and settings names align with existing contracts."
  - step: 2
    name: "Implement local file storage"
    action: "Add LocalFileStorage with safe save, resolve, and delete behavior."
    expected_output: "PDF files can be stored under a temp documents root in tests."
  - step: 3
    name: "Implement SQLite schema and repositories"
    action: "Create schema initialization and document/chunk repository classes."
    expected_output: "Document and chunk metadata round-trips through SQLite."
  - step: 4
    name: "Add tests"
    action: "Use tmp_path for storage and SQLite database tests."
    expected_output: "Tests cover persistence round trip, list ordering, delete behavior, and path safety."
  - step: 5
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "LocalFileStorage saves PDF bytes under a configured documents directory."
    - "LocalFileStorage rejects or safely handles path traversal filenames."
    - "SQLiteDocumentRepository saves, loads, lists, and deletes Document records."
    - "SQLiteChunkRepository saves chunks and loads chunks by document id."
    - "Deleting a document record also removes related chunks, either through repository behavior or documented service-level orchestration in the next spec."
  architectural:
    - "Routes and application services do not open SQLite connections directly."
    - "Domain modules do not import sqlite3 or pathlib storage adapters."
    - "Concrete storage and persistence classes live under backend/app/infrastructure/."
  quality:
    - "Storage and SQLite repository tests pass."
    - "uv run pytest -q passes."
    - "uv run ruff check --no-cache . passes."
    - "uv run ruff format --check --no-cache . passes."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate storage, repositories, and existing backend behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check --no-cache ."
      cwd: "backend"
      purpose: "Validate lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check --no-cache ."
      cwd: "backend"
      purpose: "Validate formatting."
      success_condition: "Ruff exits with code 0."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "SQLite schema may need migration support later."
    severity: "medium"
    mitigation: "Keep schema minimal and initialization idempotent; defer migration tooling until schema churn warrants it."
  - risk: "Document deletion semantics are not fully decided for future answer/evidence records."
    severity: "medium"
    mitigation: "For Milestone 3, delete only document, chunks, and file; document future cleanup for later records."
  - risk: "Filename sanitization can accidentally make duplicate names collide."
    severity: "medium"
    mitigation: "Use generated document IDs or unique prefixes in stored filenames."

unknowns:
  - question: "Should data/app.db be created automatically on backend startup or lazily when repositories are first used?"
    resolution_strategy: "Prefer idempotent lazy initialization in repository construction for this MVP unless existing startup patterns favor explicit app startup hooks."
```

## 12. Minimal Output Contract

```yaml
agent_result:
  status: "<completed | failed | blocked>"
  summary: "<short factual summary>"
  files_read:
    - "PROJECT_DECISIONS.md"
    - "AGENTS.md"
    - "docs/specs/milestone-03-overview.md"
    - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
    - "backend/app/ports/file_storage.py"
    - "backend/app/ports/repositories.py"
    - "backend/app/core/config.py"
    - "backend/app/domain/models/document.py"
    - "backend/app/domain/models/chunk.py"
  files_changed:
    - "backend/app/core/config.py"
    - "backend/app/infrastructure/storage/local_file_storage.py"
    - "backend/app/infrastructure/persistence/sqlite_repositories.py"
    - "backend/tests/test_local_file_storage.py"
    - "backend/tests/test_sqlite_repositories.py"
  commands_run:
    - command: "uv run pytest -q"
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "uv run ruff check --no-cache ."
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "uv run ruff format --check --no-cache ."
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
  validation:
    passed: []
    failed: []
  remaining_risks:
    - "SQLite schema may need migration tooling after more record types are implemented."
  next_recommended_action: "Implement docs/specs/milestone-03d-ingestion-service-and-documents-api.md"
```
