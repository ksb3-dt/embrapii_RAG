# Milestone 03 Overview: PDF Ingestion Prototype

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-03-overview"
title: "PDF Ingestion Prototype Overview"
created_at_utc: "2026-07-01T14:40:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
depends_on:
  - "docs/specs/milestone-02-overview.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 3. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window. Follow the pattern of spec division I was using in this project.

source_project_decision: |
  3. PDF Ingestion Prototype
     - Use PyMuPDF to parse a few real EMBRAPII PDFs.
     - Store extracted page/chunk metadata locally.
```

## 3. System Interpretation

```yaml
system_translation: |
  Milestone 3 replaces the document upload placeholder with a local ingestion
  prototype. It should accept PDF bytes, store the original PDF in
  data/documents/, parse page-level text with PyMuPDF, create deterministic text
  chunks, and persist document/page/chunk metadata locally so Milestone 4 can
  embed and index the chunks.

  This overview is a coordination spec only. Do not implement the whole
  milestone from this file in one Composer session. Execute the child specs in
  dependency order and validate each session before starting the next.

  Expected user-visible result:
    - Uploading a selectable-text PDF through POST /documents returns a real
      document record instead of a 501 placeholder.
    - GET /documents lists locally stored document metadata.
    - DELETE /documents/{document_id} removes local document metadata and the
      stored PDF for this prototype.

  Expected engineering result:
    - PyMuPDF parsing, file storage, chunking, SQLite persistence, and service
      orchestration are implemented behind ports and dependency wiring.
    - No embedding, Qdrant indexing, retrieval, LLM, OCR, or background job
      behavior is introduced yet.
```

## 4. Composer Execution Strategy

```yaml
composer_strategy:
  use_this_file_for:
    - "Overall milestone context."
    - "Dependency order."
    - "Cross-spec guardrails."
    - "Final milestone acceptance criteria."
  do_not_use_this_file_for:
    - "One-shot implementation of all Milestone 3 code."
  execute_child_specs_in_order:
    - "docs/specs/milestone-03a-pymupdf-parser.md"
    - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
    - "docs/specs/milestone-03c-local-storage-and-sqlite.md"
    - "docs/specs/milestone-03d-ingestion-service-and-documents-api.md"
  review_after_each_spec:
    - "Inspect every diff before accepting."
    - "Run the spec's validation commands."
    - "Do not start the next spec until the current spec is accepted or revised."
```

## 5. Business / Product Context

```yaml
business_context:
  user_problem: "The MVP needs reliable report text extraction and local metadata before retrieval, Q&A, citations, and evidence auditing can be useful."
  target_user: "Developers and coding agents implementing the EMBRAPII Reports RAG ingestion path."
  expected_outcome: "A few real selectable-text EMBRAPII PDFs can be uploaded, parsed into pages and chunks, and inspected through persisted metadata."
  product_surface:
    - "Document upload/list/delete API."
    - "PyMuPDF parser adapter."
    - "Local PDF file storage."
    - "SQLite metadata storage."
    - "Document ingestion application service."
```

## 6. Global Scope

```yaml
scope:
  in_scope:
    - "Add PyMuPDF as the backend PDF parsing dependency."
    - "Implement the DocumentParser port with a PyMuPDF adapter."
    - "Create deterministic page-to-chunk behavior for extracted text."
    - "Persist documents and chunks in SQLite at data/app.db."
    - "Store uploaded PDFs under data/documents/ through the FileStorage port."
    - "Wire parser, storage, and repositories through backend/app/core/dependencies.py."
    - "Replace document route placeholders with real upload/list/delete behavior."
    - "Add focused tests for parsing, chunking, SQLite repositories, storage, service orchestration, and document API behavior."
  out_of_scope:
    - "Do not implement embeddings, BAAI/bge-m3, Qdrant collections, or vector indexing."
    - "Do not implement dense retrieval, keyword retrieval, RRF, Q&A, summaries, comparisons, evidence audit, evaluation, or LLM calls."
    - "Do not add OCR or scanned-PDF processing."
    - "Do not add advanced table extraction beyond PyMuPDF text extraction."
    - "Do not move ingestion to Redis/RQ jobs yet; Milestone 8 owns background jobs."
    - "Do not create frontend upload UI unless a later spec explicitly requests it."
```

## 7. Global Architecture Rules

```yaml
architecture_rules:
  project_specific_rules:
    - "PROJECT_DECISIONS.md is the source of truth for MVP architecture and constraints."
    - "Use pragmatic Hexagonal Architecture."
    - "Keep FastAPI routes thin and delegate workflow coordination to application services."
    - "Keep domain models and policies independent of FastAPI, Qdrant, PyMuPDF, LangChain, Redis, RQ, SQLite clients, and LLM SDKs."
    - "Concrete PyMuPDF, filesystem, and SQLite behavior belongs in infrastructure adapters."
    - "Wire mostly static dependencies in backend/app/core/dependencies.py."
    - "Use data/documents/ for uploaded PDFs and data/app.db for metadata."
    - "Use English for code identifiers, filenames, modules, API fields, database fields, and technical documentation."
    - "Use Portuguese for code comments only."
```

## 8. Cross-Spec Contracts

```yaml
contracts:
  parser_contract:
    invariant: "DocumentParser.parse(file_path) returns 1-based DocumentPage objects for selectable-text PDFs and fails with an actionable application/infrastructure error for unreadable or invalid PDFs."

  chunking_contract:
    invariant: "Chunking preserves document_id, page_number, chunk text, chunk_type, section_title when known, and source_file_path when available."

  persistence_contract:
    invariant: "SQLite repositories can save, list, load, and delete document metadata and save/load chunks by document id."

  upload_contract:
    response_shape: "DocumentUploadResponse with document metadata and job_id null until background jobs exist."
    compatibility: "can extend when Milestone 8 adds background jobs"

  deletion_contract:
    invariant: "For this local prototype, deleting a document removes its document row, related chunk rows, and stored PDF file. Later answer/evidence cleanup can be added when those records exist."
```

## 9. Milestone Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "POST /documents accepts a PDF upload and returns HTTP 200 or 201 with a real DocumentUploadResponse."
    - "GET /documents returns stored documents from SQLite."
    - "DELETE /documents/{document_id} removes the document metadata, related chunk metadata, and local file for this prototype."
    - "A selectable-text PDF produces one or more DocumentPage records and one or more DocumentChunk records."
    - "Invalid or non-PDF uploads fail with a stable application error response, not an unhandled traceback."
    - "GET /health still returns HTTP 200 with status ok."

  architectural:
    - "Routes do not import or instantiate PyMuPDF, SQLite connections, file storage adapters, or parser adapters."
    - "Application services depend on ports/domain models, not concrete infrastructure classes."
    - "Domain modules remain free of FastAPI, PyMuPDF, SQLite, Qdrant, LangChain, Redis, RQ, and LLM SDK imports."
    - "Concrete adapters live under backend/app/infrastructure/."

  quality:
    - "Backend pytest suite passes."
    - "Ruff check passes."
    - "Ruff format --check passes."
    - "Tests cover parser adapter behavior, chunking boundaries, repository persistence, storage safety, and document API behavior."
```

## 10. Milestone Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv sync --locked --dev"
      cwd: "backend"
      purpose: "Install locked backend dependencies after adding PyMuPDF."
      success_condition: "Dependencies sync successfully."
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate ingestion prototype and existing backend behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check --no-cache ."
      cwd: "backend"
      purpose: "Validate backend lint rules while avoiding known local ruff cache permission issues."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check --no-cache ."
      cwd: "backend"
      purpose: "Validate backend formatting while avoiding known local ruff cache permission issues."
      success_condition: "Ruff exits with code 0."
  runtime_checks:
    - name: "Document upload smoke check"
      method: "curl or FastAPI TestClient"
      expected: "Uploading a small selectable-text PDF returns document metadata and creates stored document/chunk records."
    - name: "Document list/delete smoke check"
      method: "curl or FastAPI TestClient"
      expected: "Uploaded document appears in list and is removed by delete."
```

## 11. Risks And Guardrails

```yaml
risks:
  - risk: "A prototype ingestion milestone can drift into embedding and Qdrant indexing."
    severity: "medium"
    mitigation: "Stop at persisted chunks; Milestone 4 owns embeddings and indexing."
  - risk: "PyMuPDF extraction quality may be poor for tables, infographics, or scanned PDFs."
    severity: "medium"
    mitigation: "Support selectable text only, persist available text, and document OCR/table limitations."
  - risk: "SQLite schema choices may need changes when answers, jobs, and evidence records are implemented."
    severity: "medium"
    mitigation: "Keep schema minimal and focused on document/chunk metadata needed by Milestone 4."
  - risk: "Synchronous upload ingestion may be slow for large reports."
    severity: "medium"
    mitigation: "Accept synchronous behavior for the prototype and keep service boundaries ready for Milestone 8 job migration."

guardrails:
  - "Do not implement multiple child specs in one Composer prompt."
  - "Do not introduce Qdrant, embeddings, retrieval, or LLM behavior in Milestone 3."
  - "Do not store API keys or add provider configuration."
  - "If a child spec changes a shared contract, update dependent specs or stop and ask."
```

## 12. Deliverables

```yaml
deliverables:
  specs:
    - "docs/specs/milestone-03-overview.md"
    - "docs/specs/milestone-03a-pymupdf-parser.md"
    - "docs/specs/milestone-03b-chunking-and-domain-refinement.md"
    - "docs/specs/milestone-03c-local-storage-and-sqlite.md"
    - "docs/specs/milestone-03d-ingestion-service-and-documents-api.md"
```
