# Milestone 03a: PyMuPDF Parser

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-03a-pymupdf-parser"
title: "PyMuPDF Parser Adapter"
created_at_utc: "2026-07-01T14:40:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-03-overview.md"
depends_on:
  - "docs/specs/milestone-02-overview.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 3. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window. Follow the pattern of spec division I was using in this project.
```

## 3. System Interpretation

```yaml
system_translation: |
  Add the concrete PDF parser adapter for the existing DocumentParser port using
  PyMuPDF. This spec proves that selectable-text PDFs can be parsed into
  1-based DocumentPage domain objects without adding storage, chunking,
  indexing, API behavior, or persistence.

  Expected user-visible result:
    - No route behavior changes yet; document endpoints may still return
      placeholders until later Milestone 3 specs.

  Expected engineering result:
    - backend/app/infrastructure/parsers/pymupdf_parser.py implements the parser
      port and is covered by focused tests with a generated small PDF fixture.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Add PyMuPDF to backend dependencies using uv."
    - "Implement backend/app/infrastructure/parsers/pymupdf_parser.py."
    - "Return DocumentPage objects with stable document_id, 1-based page_number, and extracted text."
    - "Handle invalid, missing, encrypted, or unreadable PDFs with explicit exceptions."
    - "Add focused parser tests that generate or use a tiny selectable-text PDF fixture."
  out_of_scope:
    - "Do not implement chunking, local file storage, SQLite repositories, upload route behavior, embeddings, Qdrant indexing, retrieval, OCR, or table-specific extraction."
    - "Do not change DocumentIngestionService orchestration yet except if a narrow parser import smoke test requires no behavior change."
    - "Do not add frontend behavior."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/pyproject.toml"
      - "backend/uv.lock"
      - "backend/app/infrastructure/parsers/pymupdf_parser.py"
      - "backend/tests/test_pymupdf_parser.py"
  tests:
    unit:
      - "backend/tests/test_pymupdf_parser.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "The PyMuPDF import must stay inside infrastructure parser code or parser tests."
  - "Domain models and ports must not import PyMuPDF."
  - "The adapter must implement the existing DocumentParser port rather than inventing a separate parser contract."
  - "Parser errors should be actionable and should not expose long internal tracebacks through application code."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious intent."
  - "Keep generated test PDFs small and deterministic."
  - "Prefer pathlib.Path internally where it improves filesystem clarity, while preserving the current port contract unless there is a strong reason to extend it."
```

## 7. Parser Contract Requirements

```yaml
contracts:
  port_contracts:
    - name: "DocumentParser"
      method: "parse(file_path: str) -> list[DocumentPage]"
      compatibility: "must preserve or only extend in a backwards-compatible way"

  adapter_contracts:
    - name: "PyMuPDFDocumentParser"
      requirements:
        - "Accepts a PDF path and a document_id, or another explicit mechanism to set document_id without guessing from global state."
        - "Returns pages in original PDF order."
        - "Uses 1-based page numbers."
        - "Preserves extracted text without aggressive normalization beyond trimming obviously empty page text."
        - "Returns empty text for pages PyMuPDF can open but cannot extract, unless a clear parser policy says to skip blank pages."
        - "Raises a clear parser exception for missing files and invalid PDFs."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect current contracts"
    action: "Read PROJECT_DECISIONS.md, AGENTS.md, milestone-03-overview.md, backend/app/ports/document_parser.py, backend/app/domain/models/document.py, and current parser package."
    expected_output: "Parser adapter can align with existing domain and port names."
  - step: 2
    name: "Add PyMuPDF dependency"
    action: "Use uv to add the latest PyMuPDF dependency and update uv.lock."
    expected_output: "backend/pyproject.toml and backend/uv.lock include PyMuPDF."
  - step: 3
    name: "Implement parser adapter"
    action: "Create PyMuPDFDocumentParser with explicit document_id handling and clear parser errors."
    expected_output: "Adapter returns DocumentPage objects from selectable-text PDFs."
  - step: 4
    name: "Add parser tests"
    action: "Generate a tiny PDF in a temp directory with PyMuPDF and assert extracted page text and page numbers."
    expected_output: "Tests cover successful parsing and invalid/missing file behavior."
  - step: 5
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "PyMuPDFDocumentParser parses a generated selectable-text PDF into DocumentPage objects."
    - "Parsed pages use 1-based page numbers."
    - "Parsed pages include the caller-provided document_id."
    - "Invalid or missing PDFs raise clear parser errors."
    - "GET /health still returns HTTP 200."
  architectural:
    - "Only infrastructure parser code and parser tests import PyMuPDF."
    - "Domain models remain infrastructure-free."
    - "No route or application service starts doing real ingestion in this spec."
  quality:
    - "Parser tests pass."
    - "uv run pytest -q passes."
    - "uv run ruff check --no-cache . passes."
    - "uv run ruff format --check --no-cache . passes."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv add PyMuPDF"
      cwd: "backend"
      purpose: "Add the accepted PDF parsing dependency."
      success_condition: "Dependency is added to pyproject.toml and uv.lock."
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate parser adapter and existing backend behavior."
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
  - risk: "The existing DocumentParser port lacks an explicit document_id parameter."
    severity: "medium"
    mitigation: "Extend the port minimally if needed and update contract tests; do not hide document_id derivation inside the adapter."
  - risk: "Generated PDF tests may pass while real EMBRAPII PDFs expose extraction quirks."
    severity: "medium"
    mitigation: "Add a manual verification note for a real selectable-text EMBRAPII PDF in later ingestion service testing."
  - risk: "Parser exceptions may leak infrastructure details."
    severity: "low"
    mitigation: "Wrap low-level PyMuPDF exceptions in a small infrastructure/application parser error."

unknowns:
  - question: "Should blank pages be persisted as empty pages or skipped?"
    resolution_strategy: "Prefer preserving page numbers by returning DocumentPage records with empty text; chunking can skip empty text later."
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
    - "backend/app/ports/document_parser.py"
    - "backend/app/domain/models/document.py"
    - "backend/pyproject.toml"
  files_changed:
    - "backend/pyproject.toml"
    - "backend/uv.lock"
    - "backend/app/infrastructure/parsers/pymupdf_parser.py"
    - "backend/tests/test_pymupdf_parser.py"
  commands_run:
    - command: "uv add PyMuPDF"
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
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
    - "Real EMBRAPII PDF extraction quality still needs manual inspection in a later child spec."
  next_recommended_action: "Implement docs/specs/milestone-03b-chunking-and-domain-refinement.md"
```
