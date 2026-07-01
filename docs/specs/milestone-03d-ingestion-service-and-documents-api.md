# Milestone 03d: Ingestion Service And Documents API

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-03d-ingestion-service-and-documents-api"
title: "Ingestion Service And Documents API"
created_at_utc: "2026-07-01T14:40:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-03-overview.md"
depends_on:
  - "docs/specs/milestone-03a-pymupdf-parser.md"
  - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
  - "docs/specs/milestone-03c-local-storage-and-sqlite.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 3. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window. Follow the pattern of spec division I was using in this project.
```

## 3. System Interpretation

```yaml
system_translation: |
  Wire the Milestone 3 parser, chunker, local file storage, and SQLite
  repositories into DocumentIngestionService and replace document route
  placeholders with real synchronous prototype behavior. This completes the PDF
  ingestion prototype while deliberately stopping before embeddings, Qdrant
  indexing, retrieval, evidence audit, and background jobs.

  Expected user-visible result:
    - POST /documents accepts PDF uploads and returns stored document metadata.
    - GET /documents lists stored documents.
    - DELETE /documents/{document_id} deletes the local prototype document,
      chunks, and file.

  Expected engineering result:
    - Routes stay thin and call a dependency-provided service.
    - Service orchestration uses ports and domain models.
    - Concrete adapter construction remains centralized in dependencies.py.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Update DocumentIngestionService constructor to accept FileStorage, DocumentParser, chunking service, DocumentRepository, and ChunkRepository dependencies."
    - "Implement ingest_document(filename, content) synchronously for the prototype."
    - "Implement list_documents() and delete_document(document_id) through the service boundary."
    - "Wire concrete LocalFileStorage, PyMuPDFDocumentParser, chunker, and SQLite repositories in backend/app/core/dependencies.py."
    - "Replace POST /documents, GET /documents, and DELETE /documents/{document_id} placeholders with real route behavior."
    - "Map domain Document objects to existing DocumentResponse and DocumentUploadResponse schemas."
    - "Add tests for service orchestration, dependency wiring, document API success cases, and error cases."
    - "Update README status if user-facing API behavior changes materially."
  out_of_scope:
    - "Do not implement embeddings, Qdrant indexing, dense retrieval, keyword retrieval, RRF, Q&A, evidence audit, summaries, comparisons, evaluation, LLM calls, or Redis/RQ background jobs."
    - "Do not add frontend upload/list/delete UI in this spec."
    - "Do not persist API keys."
    - "Do not add OCR or scanned-PDF fallback behavior."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/application/services/document_ingestion_service.py"
      - "backend/app/core/dependencies.py"
      - "backend/app/api/routes/documents.py"
      - "backend/app/api/schemas/documents.py"
      - "backend/app/api/schemas/errors.py"
      - "backend/tests/test_document_ingestion_service.py"
      - "backend/tests/test_dependency_wiring.py"
      - "backend/tests/test_documents_api.py"
      - "README.md"
  tests:
    unit:
      - "backend/tests/test_document_ingestion_service.py"
      - "backend/tests/test_dependency_wiring.py"
    integration:
      - "backend/tests/test_documents_api.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "FastAPI routes must remain thin: validate/request file bytes, call DocumentIngestionService, and map domain results to response schemas."
  - "Routes must not import PyMuPDF, sqlite3, LocalFileStorage, or repository classes."
  - "DocumentIngestionService coordinates workflow and depends on ports/domain/application chunking, not concrete infrastructure classes."
  - "Concrete adapter construction belongs in backend/app/core/dependencies.py."
  - "Background job status should remain absent or job_id null until Milestone 8."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious intent."
  - "Return stable application-level error responses for invalid uploads and ingestion failures."
  - "Avoid broad exception swallowing; translate expected parser/storage/persistence errors into actionable API errors."
```

## 7. API And Service Contract Requirements

```yaml
contracts:
  service_contracts:
    - name: "DocumentIngestionService.ingest_document"
      request_shape: "filename: str, content: bytes"
      response_shape: "Document domain model"
      behavior:
        - "Generate a stable unique document id."
        - "Save original PDF through FileStorage."
        - "Create a Document record with processing/indexed/failed status transitions appropriate for synchronous prototype behavior."
        - "Parse pages with DocumentParser."
        - "Create chunks with the chunking service."
        - "Persist document metadata and chunk metadata in SQLite repositories."
        - "Return the final Document metadata."
    - name: "DocumentIngestionService.list_documents"
      response_shape: "list[Document]"
      behavior:
        - "Delegate to DocumentRepository."
    - name: "DocumentIngestionService.delete_document"
      request_shape: "document_id: str"
      behavior:
        - "Load document metadata."
        - "Delete chunk metadata and document metadata."
        - "Delete the stored PDF file."
        - "Return a clear not-found error if document_id is unknown."

  api_contracts:
    - name: "POST /documents"
      request_shape: "multipart/form-data with file UploadFile"
      response_shape: "DocumentUploadResponse"
      compatibility: "can extend with job_id when Milestone 8 adds background jobs"
    - name: "GET /documents"
      response_shape: "DocumentListResponse"
      compatibility: "must preserve documents list shape"
    - name: "DELETE /documents/{document_id}"
      response_shape: "HTTP 204 or a small success response, documented in tests"
      compatibility: "can extend later if frontend requires deleted document metadata"
    - name: "Application errors"
      response_shape: |
        {
          "code": "<STABLE_ERROR_CODE>",
          "message": "<human-readable message>",
          "details": {}
        }
      compatibility: "must preserve application-level error shape"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect prior child specs and current implementation"
    action: "Read milestone-03a through 03c outputs, document service, dependencies, document schemas, and document routes."
    expected_output: "Existing method names and adapter constructors are known."
  - step: 2
    name: "Implement service orchestration"
    action: "Update DocumentIngestionService with constructor injection and methods for ingest/list/delete."
    expected_output: "Service coordinates ports and domain objects without infrastructure imports."
  - step: 3
    name: "Wire dependencies"
    action: "Update backend/app/core/dependencies.py to construct local storage, parser, chunker, and SQLite repositories from settings."
    expected_output: "Routes receive a fully wired DocumentIngestionService."
  - step: 4
    name: "Replace document route placeholders"
    action: "Update POST/GET/DELETE document routes to call the service and return real schemas."
    expected_output: "Document API no longer returns 501 for Milestone 3 document endpoints."
  - step: 5
    name: "Add tests"
    action: "Test service with fakes and API with temporary dependency overrides or temporary settings."
    expected_output: "Tests cover upload, list, delete, invalid file, not found, and dependency wiring."
  - step: 6
    name: "Update README"
    action: "Adjust status and implemented/not-implemented sections to mention Milestone 3 document ingestion prototype."
    expected_output: "README matches actual document API behavior."
  - step: 7
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "POST /documents with a valid selectable-text PDF returns DocumentUploadResponse with job_id null."
    - "GET /documents returns the uploaded document metadata from SQLite."
    - "DELETE /documents/{document_id} deletes the document, its chunks, and its stored PDF file for the local prototype."
    - "Invalid or non-PDF uploads return a stable application error response."
    - "Unknown document deletion returns a stable not-found error response."
    - "Generated chunks are persisted and can be loaded by document id through ChunkRepository."
    - "GET /health still returns HTTP 200."
  architectural:
    - "Document routes do not instantiate parser, storage, or repository adapters."
    - "DocumentIngestionService imports ports/domain/application chunking only, not concrete infrastructure classes."
    - "Dependency wiring for concrete adapters is centralized in backend/app/core/dependencies.py."
    - "No embeddings, Qdrant, retrieval, LLM, OCR, or Redis/RQ behavior is introduced."
  quality:
    - "Document service tests pass."
    - "Document API tests pass."
    - "Dependency wiring tests pass."
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
      purpose: "Validate ingestion service, document API behavior, persistence, and existing backend behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check --no-cache ."
      cwd: "backend"
      purpose: "Validate lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check --no-cache ."
      cwd: "backend"
      purpose: "Validate formatting."
      success_condition: "Ruff exits with code 0."
  runtime_checks:
    - name: "Upload/list/delete smoke check"
      method: "curl or FastAPI TestClient"
      expected: "Upload a small selectable-text PDF, confirm it appears in GET /documents, then delete it and confirm it is removed."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Synchronous ingestion may block for larger reports."
    severity: "medium"
    mitigation: "Keep job_id null and service boundaries ready for Milestone 8 background job migration."
  - risk: "A failure after file save but before metadata persistence can leave an orphan file."
    severity: "medium"
    mitigation: "Use clear try/except cleanup in the service and add a test for parser failure cleanup when practical."
  - risk: "Deleting local files and metadata may conflict with future answer/evidence history."
    severity: "medium"
    mitigation: "Limit current cleanup to documents/chunks/files and revisit once answer/evidence records exist."
  - risk: "Route-level error handling may become inconsistent with other placeholder routes."
    severity: "low"
    mitigation: "Use existing application error response shape and helpers where possible."

unknowns:
  - question: "Should upload response status be HTTP 200 or 201?"
    resolution_strategy: "Prefer HTTP 201 for created documents if existing tests/contracts allow it; otherwise preserve the current route style and document the choice in tests."
  - question: "Should document status be indexed before Qdrant indexing exists?"
    resolution_strategy: "Use a status that honestly reflects local ingestion completion, such as indexed only if the project defines indexed as chunk metadata ready; otherwise prefer a clearer existing status and document the limitation."
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
    - "docs/specs/milestone-03a-pymupdf-parser.md"
    - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
    - "docs/specs/milestone-03c-local-storage-and-sqlite.md"
    - "backend/app/application/services/document_ingestion_service.py"
    - "backend/app/core/dependencies.py"
    - "backend/app/api/routes/documents.py"
    - "backend/app/api/schemas/documents.py"
  files_changed:
    - "backend/app/application/services/document_ingestion_service.py"
    - "backend/app/core/dependencies.py"
    - "backend/app/api/routes/documents.py"
    - "backend/app/api/schemas/documents.py"
    - "backend/app/api/schemas/errors.py"
    - "backend/tests/test_document_ingestion_service.py"
    - "backend/tests/test_dependency_wiring.py"
    - "backend/tests/test_documents_api.py"
    - "README.md"
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
    - "Ingestion remains synchronous until Milestone 8 background jobs."
    - "Chunks are persisted locally but not embedded or indexed until Milestone 4."
  next_recommended_action: "Start Milestone 4 specs for BAAI/bge-m3 embeddings and Qdrant indexing after reviewing Milestone 3 results."
```
