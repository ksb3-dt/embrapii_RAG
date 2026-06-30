# Milestone 02 Overview: Backend Architecture Skeleton

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02-overview"
title: "Backend Architecture Skeleton Overview"
created_at_utc: "2026-06-30T23:10:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
depends_on:
  - "docs/specs/milestone-01-overview.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 2. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window.

source_project_decision: |
  2. Backend Architecture Skeleton
     - Implement the pragmatic hexagonal folder structure.
     - Add basic FastAPI routes, config, dependency wiring, and placeholder ports/services.
```

## 3. System Interpretation

```yaml
system_translation: |
  Milestone 2 turns the Milestone 1 backend scaffold into a pragmatic
  hexagonal backend skeleton. It should create the stable folders, typed
  contracts, route placeholders, service placeholders, ports, and dependency
  wiring that later ingestion, retrieval, Q&A, audit, summary, comparison, jobs,
  and evaluation milestones can extend.

  This overview is a coordination spec only. Do not implement the whole
  milestone from this file in one Composer session. Execute the child specs in
  dependency order and validate each session before starting the next.

  Expected user-visible result:
    - The backend still starts and /health still works.
    - Placeholder API routes expose predictable "not implemented yet" behavior
      instead of fake RAG responses.

  Expected engineering result:
    - Backend package boundaries are ready for the next milestones without
      coupling FastAPI routes directly to concrete infrastructure.
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
    - "One-shot implementation of all Milestone 2 code."
  execute_child_specs_in_order:
    - "docs/specs/milestone-02a-backend-package-layout.md"
    - "docs/specs/milestone-02b-domain-models-and-policies.md"
    - "docs/specs/milestone-02c-ports-contracts.md"
    - "docs/specs/milestone-02d-api-route-placeholders.md"
    - "docs/specs/milestone-02e-services-and-dependency-wiring.md"
  review_after_each_spec:
    - "Inspect every diff before accepting."
    - "Run the spec's validation commands."
    - "Do not start the next spec until the current spec is accepted or revised."
```

## 5. Business / Product Context

```yaml
business_context:
  user_problem: "The MVP needs a backend structure that can grow into accurate, grounded RAG workflows without route-level coupling or fake behavior."
  target_user: "Developers and coding agents implementing later EMBRAPII Reports RAG milestones."
  expected_outcome: "Later milestones can add ingestion, retrieval, Q&A, evidence audit, jobs, summaries, comparisons, and evaluation in bounded modules."
  product_surface:
    - "FastAPI backend package."
    - "Application services and use cases."
    - "Domain models and policies."
    - "Port/interface modules."
    - "Dependency wiring."
    - "Placeholder API routes."
```

## 6. Global Scope

```yaml
scope:
  in_scope:
    - "Create the backend folders described in PROJECT_DECISIONS.md where they are needed for Milestone 2."
    - "Add importable domain models and policy placeholders."
    - "Add typed ports/interfaces for realistic replacement points."
    - "Add typed API schemas and route placeholders for MVP surfaces."
    - "Add application service placeholders that define later workflow boundaries."
    - "Wire static dependencies through backend/app/core/dependencies.py."
    - "Add tests proving imports, route registration, placeholder behavior, and health compatibility."
  out_of_scope:
    - "Do not implement PDF parsing, chunking, embedding, Qdrant, Redis/RQ jobs, retrieval, LLM calls, citations, evidence persistence, SQLite repositories, or frontend UI."
    - "Do not add real infrastructure adapters except lightweight placeholders needed for type wiring."
    - "Do not return fake answers, fake documents, fake evidence, or fake job results."
    - "Do not persist API keys."
    - "Do not add OCR, reranking, auth, user permissions, or production cloud configuration."
```

## 7. Global Architecture Rules

```yaml
architecture_rules:
  project_specific_rules:
    - "PROJECT_DECISIONS.md is the source of truth for MVP architecture and constraints."
    - "Use pragmatic Hexagonal Architecture."
    - "Keep FastAPI routes thin and delegate workflow coordination to application services/use cases."
    - "Keep domain models and policies independent of FastAPI, Qdrant, PyMuPDF, LangChain, and LLM SDKs."
    - "Define ports only where replacement is realistic."
    - "Wire mostly static dependencies in backend/app/core/dependencies.py."
    - "Use a request/session-specific LLM provider factory interface; do not construct concrete LLM clients in routes."
    - "Use English for code identifiers, filenames, modules, API fields, database fields, commits, and technical documentation."
    - "Use Portuguese for code comments only."
```

## 8. Cross-Spec Contracts

```yaml
contracts:
  api_error_contract:
    response_shape: |
      {
        "code": "NOT_IMPLEMENTED",
        "message": "<human-readable message>",
        "details": {}
      }
    compatibility: "must preserve until real behavior replaces placeholders"

  placeholder_behavior:
    invariant: "Placeholder routes must fail explicitly with HTTP 501 or another documented not-implemented response; they must not simulate completed RAG behavior."

  dependency_wiring:
    invariant: "Routes consume services through dependency functions or typed aliases from backend/app/core/dependencies.py."
```

## 9. Milestone Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "GET /health still returns HTTP 200 with status ok."
    - "Documents, Q&A, summaries, comparisons, jobs, evidence, and evaluation route modules are registered or intentionally documented as pending by child specs."
    - "Placeholder routes return a consistent not-implemented error shape."
    - "Application services and ports are importable."

  architectural:
    - "Route handlers are thin and do not contain workflow logic."
    - "Domain modules import no FastAPI, Qdrant, PyMuPDF, LangChain, Redis, RQ, or LLM SDK modules."
    - "Ports define contracts but do not implement concrete infrastructure behavior."
    - "Dependency wiring is centralized in backend/app/core/dependencies.py."

  quality:
    - "Backend pytest suite passes."
    - "Ruff check passes."
    - "Ruff format --check passes."
    - "No unrelated frontend or Docker behavior is changed."
```

## 10. Milestone Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate backend import, route, and placeholder behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check ."
      cwd: "backend"
      purpose: "Validate backend lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check ."
      cwd: "backend"
      purpose: "Validate backend formatting."
      success_condition: "Ruff exits with code 0."
  runtime_checks:
    - name: "Backend health compatibility"
      method: "curl"
      expected: "GET http://localhost:8000/health returns status ok after backend startup."
    - name: "Placeholder route behavior"
      method: "curl or pytest TestClient"
      expected: "Representative placeholder routes return the documented not-implemented response."
```

## 11. Risks And Guardrails

```yaml
risks:
  - risk: "A broad architecture skeleton can drift into implementing real ingestion or RAG behavior."
    severity: "medium"
    mitigation: "Keep each child spec focused on contracts, placeholders, and tests only."
  - risk: "Too many interfaces can over-engineer the MVP."
    severity: "medium"
    mitigation: "Create only the ports named in PROJECT_DECISIONS.md or directly needed by near-term milestones."
  - risk: "Route placeholders may accidentally become public contracts that conflict with later implementation."
    severity: "low"
    mitigation: "Keep request/response schemas close to planned MVP contracts and document compatibility."

guardrails:
  - "Do not implement multiple child specs in one Composer prompt."
  - "Do not introduce infrastructure dependencies in domain modules."
  - "Do not bypass backend/app/core/dependencies.py for service wiring."
  - "If a child spec changes a shared contract, update dependent specs or stop and ask."
```

## 12. Deliverables

```yaml
deliverables:
  specs:
    - "docs/specs/milestone-02-overview.md"
    - "docs/specs/milestone-02a-backend-package-layout.md"
    - "docs/specs/milestone-02b-domain-models-and-policies.md"
    - "docs/specs/milestone-02c-ports-contracts.md"
    - "docs/specs/milestone-02d-api-route-placeholders.md"
    - "docs/specs/milestone-02e-services-and-dependency-wiring.md"
```
