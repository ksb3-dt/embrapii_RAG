# Milestone 03b: Chunking And Domain Refinement

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-03b-chunking-and-domain-refinement"
title: "Chunking And Domain Refinement"
created_at_utc: "2026-07-01T14:40:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-03-overview.md"
depends_on:
  - "docs/specs/milestone-03a-pymupdf-parser.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 3. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window. Follow the pattern of spec division I was using in this project.
```

## 3. System Interpretation

```yaml
system_translation: |
  Add deterministic chunk creation for extracted PDF pages and refine domain
  metadata only where ingestion needs it. This spec turns DocumentPage objects
  into DocumentChunk objects that can be persisted locally now and embedded in
  Milestone 4.

  Expected user-visible result:
    - No document API behavior changes yet unless existing placeholders are
      already wired by a prior accepted spec.

  Expected engineering result:
    - A tested chunking component exists in the application layer or another
      repository-consistent non-infrastructure location and produces chunks with
      stable IDs, page metadata, chunk type, and source path metadata.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create a deterministic page text chunker for DocumentPage inputs."
    - "Define chunk size and overlap constants suitable for later BAAI/bge-m3 embedding."
    - "Skip or handle empty page text according to an explicit policy."
    - "Create stable chunk IDs derived from document id, page number, and chunk sequence."
    - "Refine DocumentChunk fields only if needed for persistence and future citation/evidence metadata."
    - "Add focused tests for chunk boundaries, overlap, empty pages, stable IDs, and page metadata preservation."
  out_of_scope:
    - "Do not embed chunks, index chunks in Qdrant, implement retrieval, call LLMs, parse PDFs, persist to SQLite, or change document API behavior."
    - "Do not introduce LangChain text splitters unless the repository has already accepted LangChain for this layer and the dependency is present."
    - "Do not add OCR or table-specific chunk types beyond existing domain concepts."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/domain/models/chunk.py"
      - "backend/app/application/services/document_chunking_service.py"
      - "backend/tests/test_document_chunking_service.py"
      - "backend/tests/test_domain_models.py"
  tests:
    unit:
      - "backend/tests/test_document_chunking_service.py"
      - "backend/tests/test_domain_models.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Chunking is application/domain logic and must not depend on FastAPI, PyMuPDF, SQLite, Qdrant, Redis, RQ, LangChain, or LLM SDKs."
  - "Chunking should consume DocumentPage domain objects from the parser port result."
  - "Chunking should emit DocumentChunk domain objects for repository persistence and future embeddings."
  - "Do not duplicate citation metadata rules outside the existing domain models unless a narrow helper is justified."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious intent."
  - "Prefer deterministic pure functions or a small service class."
  - "Avoid broad text normalization that could harm citation fidelity."
```

## 7. Chunking Contract Requirements

```yaml
contracts:
  domain_contracts:
    - name: "DocumentChunk"
      invariant: "Every chunk carries document_id, chunk_id, page_number, text, chunk_type, optional section_title, and optional source_file_path."
    - name: "Chunk IDs"
      invariant: "Chunk IDs are stable for the same document id, page number, chunk sequence, and text splitting parameters."

  chunking_contracts:
    - name: "Page text chunking"
      requirements:
        - "Input: list[DocumentPage], source_file_path optional."
        - "Output: list[DocumentChunk]."
        - "Use page-local chunking so page-level citation metadata remains correct."
        - "Use a conservative default chunk size and overlap documented in code and tests."
        - "Skip empty/whitespace-only page text unless preserving blank chunks is explicitly needed."
        - "Set chunk_type to ChunkType.TEXT for PyMuPDF extracted page text."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect current domain models"
    action: "Read DocumentPage and DocumentChunk definitions plus existing domain tests."
    expected_output: "Required model fields and validation rules are known."
  - step: 2
    name: "Choose chunking location"
    action: "Place chunking in an application service module unless existing code shows a clearer domain policy pattern."
    expected_output: "Chunking stays independent of infrastructure."
  - step: 3
    name: "Implement deterministic chunking"
    action: "Add chunk size, overlap, whitespace handling, and stable chunk id generation."
    expected_output: "DocumentPage inputs produce predictable DocumentChunk outputs."
  - step: 4
    name: "Refine domain only if necessary"
    action: "Add minimal DocumentChunk metadata fields required for local persistence and future citation audit."
    expected_output: "Existing domain tests still pass and new invariants are covered."
  - step: 5
    name: "Add chunking tests"
    action: "Test short text, long text, overlap, blank pages, multi-page input, and stable IDs."
    expected_output: "Tests lock down chunking behavior without external services."
  - step: 6
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "Chunker returns one chunk for short non-empty page text."
    - "Chunker returns multiple ordered chunks for text above the configured chunk size."
    - "Chunker preserves original document_id and page_number on every chunk."
    - "Chunker creates stable and unique chunk IDs within a document."
    - "Chunker handles empty or whitespace-only pages according to the documented policy."
  architectural:
    - "Chunking code imports no FastAPI, PyMuPDF, SQLite, Qdrant, Redis, RQ, LangChain, or LLM SDK modules."
    - "Domain models remain infrastructure-free."
    - "No upload route, parser adapter, repository, embedding, or indexing behavior is added in this spec."
  quality:
    - "Chunking tests pass."
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
      purpose: "Validate chunking and existing backend behavior."
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
  - risk: "Chunk size and overlap are chosen before golden-set retrieval data exists."
    severity: "medium"
    mitigation: "Use conservative constants, document them clearly, and expect Milestone 9 tuning."
  - risk: "Naive text splitting may split tables or numeric context poorly."
    severity: "medium"
    mitigation: "Preserve page-level metadata and avoid table-specific claims until retrieval/evaluation reveals needs."
  - risk: "Stable IDs based on sequence can change if chunking constants change later."
    severity: "low"
    mitigation: "Treat re-chunking as a re-ingestion operation and document that Milestone 4 embeddings must be rebuilt after chunking changes."

unknowns:
  - question: "What chunk size is best for EMBRAPII reports and BAAI/bge-m3?"
    resolution_strategy: "Start with a documented default and tune with retrieval inspection and the golden set."
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
    - "backend/app/domain/models/document.py"
    - "backend/app/domain/models/chunk.py"
  files_changed:
    - "backend/app/domain/models/chunk.py"
    - "backend/app/application/services/document_chunking_service.py"
    - "backend/tests/test_document_chunking_service.py"
    - "backend/tests/test_domain_models.py"
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
    - "Chunking defaults must be tuned after retrieval and golden-set results exist."
  next_recommended_action: "Implement docs/specs/milestone-03c-local-storage-and-sqlite.md"
```
