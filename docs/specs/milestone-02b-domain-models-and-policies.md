# Milestone 02b: Domain Models And Policies

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02b-domain-models-and-policies"
title: "Domain Models And Policy Skeleton"
created_at_utc: "2026-06-30T23:10:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-02-overview.md"
depends_on:
  - "docs/specs/milestone-02a-backend-package-layout.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 2. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window.
```

## 3. System Interpretation

```yaml
system_translation: |
  Add lightweight, infrastructure-free domain models and policy placeholders for
  the RAG MVP. These models define vocabulary for documents, chunks, evidence,
  citations, answers, jobs, and evaluation without implementing ingestion,
  retrieval, LLM generation, persistence, or provider integrations.

  Expected user-visible result:
    - No user-facing behavior changes.

  Expected engineering result:
    - Later services and ports can share typed domain objects rather than
      passing unstructured dictionaries.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create domain models for documents, pages, chunks, citations, evidence, answers, jobs, and evaluation records."
    - "Create minimal confidence and citation policy modules with explicit TODO-safe behavior."
    - "Add unit tests for domain invariants that are clear at this milestone."
  out_of_scope:
    - "Do not parse PDFs, create chunks, embed text, retrieve from Qdrant, call LLMs, or persist records."
    - "Do not import FastAPI, Pydantic API schemas, Qdrant, PyMuPDF, LangChain, Redis, RQ, SQLite clients, or LLM SDKs in domain modules."
    - "Do not over-model fields that are still unknown; prefer extensible minimal models."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/domain/models/document.py"
      - "backend/app/domain/models/chunk.py"
      - "backend/app/domain/models/answer.py"
      - "backend/app/domain/models/job.py"
      - "backend/app/domain/models/evaluation.py"
      - "backend/app/domain/policies/confidence_policy.py"
      - "backend/app/domain/policies/citation_policy.py"
      - "backend/tests/test_domain_models.py"
      - "backend/tests/test_domain_policies.py"
  tests:
    unit:
      - "backend/tests/test_domain_models.py"
      - "backend/tests/test_domain_policies.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Domain code must be independent of framework and infrastructure libraries."
  - "Use dataclasses, enums, typing.Protocol-free plain Python, or other standard-library structures unless the repository already has a preferred domain modeling pattern."
  - "Do not use API schemas as domain models."
  - "Keep policies small and deterministic."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only when explaining non-obvious intent."
  - "Use short docstrings for public, non-obvious models and policies."
  - "Prefer explicit enums for bounded values such as job status, confidence level, chunk type, and retrieval source."
```

## 7. Domain Contract Requirements

```yaml
contracts:
  domain_contracts:
    - name: "Document"
      invariant: "Represents an uploaded report with stable id, title or filename, source path, status, and timestamps when available."
    - name: "DocumentPage"
      invariant: "Represents extracted text for one 1-based PDF page."
    - name: "DocumentChunk"
      invariant: "Carries document id, chunk id, page number, text, chunk type, and citation metadata needed by later audit views."
    - name: "Citation"
      invariant: "Page-level citation must include document id/title and page number."
    - name: "EvidenceChunk"
      invariant: "Stores chunk text plus retrieval metadata such as source, rank, score, and citation."
    - name: "Answer"
      invariant: "Carries answer text, citations, evidence, confidence level, and not-found/low-confidence indicators."
    - name: "Job"
      invariant: "Represents background work status without depending on Redis or RQ."
    - name: "Evaluation"
      invariant: "Represents golden-set question/result concepts without implementing scoring."
    - name: "ConfidencePolicy"
      invariant: "Can classify empty or weak evidence as low confidence/not found using deterministic inputs."
    - name: "CitationPolicy"
      invariant: "Can identify claim types that should require citations, especially numbers, dates, named programs, and comparisons."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect current backend packages"
    action: "Read domain package created by the previous spec and existing tests."
    expected_output: "Existing modules and naming patterns are known."
  - step: 2
    name: "Create model modules"
    action: "Add minimal domain models and enums using standard-library typing."
    expected_output: "Models import without infrastructure dependencies."
  - step: 3
    name: "Create policy modules"
    action: "Add deterministic confidence and citation policy placeholders."
    expected_output: "Policies expose stable methods for later services."
  - step: 4
    name: "Add tests"
    action: "Test model construction, enum values, citation metadata, and simple policy behavior."
    expected_output: "Tests describe core invariants."
  - step: 5
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "Domain model modules are importable."
    - "Policy modules are importable and deterministic."
    - "Existing /health behavior still passes."
  architectural:
    - "Domain modules have no FastAPI, Qdrant, PyMuPDF, LangChain, Redis, RQ, SQLite, or LLM SDK imports."
    - "No API routes or services depend on unfinished domain behavior yet unless explicitly needed by tests."
  quality:
    - "Domain tests pass."
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
      purpose: "Validate domain model, policy, and existing backend behavior."
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
  - risk: "Models may become too detailed before ingestion and retrieval reveal actual metadata needs."
    severity: "medium"
    mitigation: "Use minimal required fields and allow optional metadata dictionaries only at boundaries where future evidence needs are expected."
  - risk: "Policy placeholders may appear to solve confidence or citation quality."
    severity: "medium"
    mitigation: "Keep policy behavior conservative and document that later milestones must tune it with the golden set."

unknowns:
  - question: "Which metadata can be reliably extracted from EMBRAPII reports?"
    resolution_strategy: "Do not require uncertain fields yet; ingestion milestone will refine metadata."
  - question: "What exact confidence thresholds are acceptable for manager demos?"
    resolution_strategy: "Use conservative placeholders now; golden-set milestone tunes thresholds later."
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
    - "docs/specs/milestone-02a-backend-package-layout.md"
  files_changed:
    - "backend/app/domain/models/document.py"
    - "backend/app/domain/models/chunk.py"
    - "backend/app/domain/models/answer.py"
    - "backend/app/domain/models/job.py"
    - "backend/app/domain/models/evaluation.py"
    - "backend/app/domain/policies/confidence_policy.py"
    - "backend/app/domain/policies/citation_policy.py"
    - "backend/tests/test_domain_models.py"
    - "backend/tests/test_domain_policies.py"
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
    - "Domain models may need refinement after real ingestion metadata is known."
  next_recommended_action: "Implement docs/specs/milestone-02c-ports-contracts.md"
```
