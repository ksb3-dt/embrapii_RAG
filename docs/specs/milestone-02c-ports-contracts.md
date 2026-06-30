# Milestone 02c: Ports Contracts

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02c-ports-contracts"
title: "Backend Ports And Interface Contracts"
created_at_utc: "2026-06-30T23:10:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-02-overview.md"
depends_on:
  - "docs/specs/milestone-02a-backend-package-layout.md"
  - "docs/specs/milestone-02b-domain-models-and-policies.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 2. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window.
```

## 3. System Interpretation

```yaml
system_translation: |
  Add typed port/interface modules for the replaceable backend boundaries named
  in PROJECT_DECISIONS.md. These ports let later infrastructure adapters
  implement PDF parsing, embeddings, retrieval, LLM providers, repositories,
  and file storage without coupling application services to concrete tools.

  Expected user-visible result:
    - No user-facing behavior changes.

  Expected engineering result:
    - Later milestones can implement adapters against stable Protocol contracts.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create port modules for document parser, embedding provider, dense retriever, keyword retriever, fusion retriever, LLM provider, LLM provider factory, repositories, and file storage."
    - "Use typing.Protocol and domain models where useful."
    - "Add short docstrings for public ports."
    - "Add tests that import ports and verify simple fake implementations satisfy the expected method names."
  out_of_scope:
    - "Do not implement PyMuPDF, BAAI/bge-m3, Qdrant, keyword search, RRF, LLM SDKs, SQLite, or filesystem storage behavior."
    - "Do not add route handlers or application services in this spec."
    - "Do not introduce LangChain dependencies."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/ports/document_parser.py"
      - "backend/app/ports/embedding_provider.py"
      - "backend/app/ports/dense_retriever.py"
      - "backend/app/ports/keyword_retriever.py"
      - "backend/app/ports/fusion_retriever.py"
      - "backend/app/ports/llm_provider.py"
      - "backend/app/ports/llm_provider_factory.py"
      - "backend/app/ports/repositories.py"
      - "backend/app/ports/file_storage.py"
      - "backend/tests/test_ports_contracts.py"
  tests:
    unit:
      - "backend/tests/test_ports_contracts.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Ports may depend on domain models and standard-library typing."
  - "Ports must not depend on FastAPI schemas, infrastructure adapters, Qdrant clients, PyMuPDF, LangChain, Redis, RQ, SQLite drivers, or LLM SDKs."
  - "Keep ports coarse enough for MVP workflows; avoid one-method abstractions that are not realistic replacement points."
  - "Repository ports can live in one repositories.py module unless they become too large."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious implementation intent."
  - "Use Protocol and dataclasses/typing aliases where they clarify contracts."
  - "Prefer explicit method names tied to use cases, such as parse, embed_texts, retrieve, fuse, generate, save_document, get_job."
```

## 7. Port Contract Requirements

```yaml
contracts:
  api_contracts: []
  port_contracts:
    - name: "DocumentParser"
      methods:
        - "parse(file_path) -> parsed pages/document content"
      compatibility: "can extend"
    - name: "EmbeddingProvider"
      methods:
        - "embed_texts(texts) -> list of 1024-dimensional vectors for BAAI/bge-m3 adapters"
      compatibility: "must preserve vector-size expectation for default adapter"
    - name: "DenseRetriever"
      methods:
        - "retrieve(query, filters, limit) -> ranked evidence candidates"
      compatibility: "can extend"
    - name: "KeywordRetriever"
      methods:
        - "retrieve(query, filters, limit) -> ranked evidence candidates"
      compatibility: "can extend"
    - name: "FusionRetriever"
      methods:
        - "retrieve(query, filters, limit) -> fused evidence candidates"
      compatibility: "can extend"
    - name: "LLMProvider"
      methods:
        - "generate(prompt, context) -> generated text or structured result"
      compatibility: "can extend"
    - name: "LLMProviderFactory"
      methods:
        - "create(provider, model, api_key) -> LLMProvider"
      compatibility: "must not persist api_key"
    - name: "Repositories"
      methods:
        - "document, chunk, answer, job, and evaluation persistence contracts needed by later services"
      compatibility: "can extend"
    - name: "FileStorage"
      methods:
        - "save_pdf, delete_document_file, resolve_document_path"
      compatibility: "can extend"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect domain models"
    action: "Read the domain models produced by Milestone 02b."
    expected_output: "Ports can reference existing domain objects without inventing duplicates."
  - step: 2
    name: "Create port modules"
    action: "Add Protocol classes and lightweight request/result types only if needed."
    expected_output: "Ports are importable and infrastructure-free."
  - step: 3
    name: "Add contract tests"
    action: "Use small fake classes in tests to exercise key method signatures."
    expected_output: "Tests catch accidental missing method names or imports."
  - step: 4
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "All port modules import successfully."
    - "Tests can define fake implementations of important ports."
    - "Existing health and domain tests still pass."
  architectural:
    - "Ports depend only on domain modules and Python standard-library typing."
    - "No concrete infrastructure behavior is implemented."
    - "LLM provider factory contract accepts provider, model, and api_key without persisting the key."
  quality:
    - "Port contract tests pass."
    - "uv run pytest -q passes."
    - "uv run ruff check . passes."
    - "uv run ruff format --check . passes."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate port contracts and existing backend behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check ."
      cwd: "backend"
      purpose: "Validate lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check ."
      cwd: "backend"
      purpose: "Validate formatting."
      success_condition: "Ruff exits with code 0."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Ports may lock in signatures before real adapters are implemented."
    severity: "medium"
    mitigation: "Keep signatures minimal and allow extension in later milestones."
  - risk: "Repository contracts may become too broad."
    severity: "medium"
    mitigation: "Define only methods needed by planned services and keep implementation out of this spec."

unknowns:
  - question: "Exact metadata fields for chunks and evidence may change after PDF parsing."
    resolution_strategy: "Reference domain models and use optional metadata where future refinement is likely."
```

## 12. Minimal Output Contract

```yaml
agent_result:
  status: "<completed | failed | blocked>"
  summary: "<short factual summary>"
  files_read:
    - "PROJECT_DECISIONS.md"
    - "AGENTS.md"
    - "docs/specs/milestone-02-overview.md"
    - "docs/specs/milestone-02b-domain-models-and-policies.md"
    - "backend/app/domain/models/*.py"
  files_changed:
    - "backend/app/ports/document_parser.py"
    - "backend/app/ports/embedding_provider.py"
    - "backend/app/ports/dense_retriever.py"
    - "backend/app/ports/keyword_retriever.py"
    - "backend/app/ports/fusion_retriever.py"
    - "backend/app/ports/llm_provider.py"
    - "backend/app/ports/llm_provider_factory.py"
    - "backend/app/ports/repositories.py"
    - "backend/app/ports/file_storage.py"
    - "backend/tests/test_ports_contracts.py"
  commands_run:
    - command: "uv run pytest -q"
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "uv run ruff check ."
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "uv run ruff format --check ."
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
  validation:
    passed: []
    failed: []
  remaining_risks:
    - "Port signatures may need refinement after real adapters are implemented."
  next_recommended_action: "Implement docs/specs/milestone-02d-api-route-placeholders.md"
```
