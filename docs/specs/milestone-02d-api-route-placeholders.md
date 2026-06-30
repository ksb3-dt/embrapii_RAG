# Milestone 02d: API Route Placeholders

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02d-api-route-placeholders"
title: "FastAPI Route And Schema Placeholders"
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
  Add thin FastAPI route modules and Pydantic schemas for the planned MVP API
  surfaces, but return explicit not-implemented responses until later milestones
  add real behavior. This creates stable API boundaries without fake ingestion,
  retrieval, LLM, evidence, job, summary, comparison, or evaluation logic.

  Expected user-visible result:
    - Existing /health still works.
    - Planned API endpoints exist only as honest placeholders.

  Expected engineering result:
    - Later feature specs can replace placeholder behavior behind already named
      route and schema modules.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create API schema modules for documents, QA, summaries, comparisons, jobs, evidence, and evaluation."
    - "Create route modules for documents, QA, summaries, comparisons, jobs, evidence, and evaluation."
    - "Register route modules in backend/app/main.py or a routes package aggregator."
    - "Add a shared application error response helper or schema if needed."
    - "Add tests for route registration and placeholder error behavior."
  out_of_scope:
    - "Do not implement upload storage, PDF ingestion, retrieval, LLM calls, background jobs, evidence lookup, summaries, comparisons, or evaluation execution."
    - "Do not call application services yet unless Milestone 02e has already been implemented and this spec is intentionally revised."
    - "Do not add frontend API clients."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/api/schemas/errors.py"
      - "backend/app/api/schemas/documents.py"
      - "backend/app/api/schemas/qa.py"
      - "backend/app/api/schemas/summaries.py"
      - "backend/app/api/schemas/comparisons.py"
      - "backend/app/api/schemas/jobs.py"
      - "backend/app/api/schemas/evidence.py"
      - "backend/app/api/schemas/evaluation.py"
      - "backend/app/api/routes/documents.py"
      - "backend/app/api/routes/qa.py"
      - "backend/app/api/routes/summaries.py"
      - "backend/app/api/routes/comparisons.py"
      - "backend/app/api/routes/jobs.py"
      - "backend/app/api/routes/evidence.py"
      - "backend/app/api/routes/evaluation.py"
      - "backend/app/api/routes/__init__.py"
      - "backend/app/main.py"
      - "backend/tests/test_api_placeholders.py"
  tests:
    unit:
      - "backend/tests/test_api_placeholders.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Routes must stay thin."
  - "Routes may use Pydantic API schemas and FastAPI only."
  - "Routes must not import infrastructure adapters."
  - "Routes must not construct LLM providers, Qdrant clients, Redis clients, parsers, embeddings, or repositories."
  - "Placeholder routes must return explicit not-implemented errors instead of fake successful responses."

coding_rules:
  - "Use English API field names."
  - "Use Portuguese comments only for non-obvious intent."
  - "Keep schemas minimal and aligned with PROJECT_DECISIONS.md."
  - "Use stable error codes such as NOT_IMPLEMENTED."
```

## 7. API Contract Requirements

```yaml
contracts:
  api_contracts:
    - name: "Application error response"
      response_shape: |
        {
          "code": "NOT_IMPLEMENTED",
          "message": "<human-readable message>",
          "details": {}
        }
      compatibility: "must preserve for application-level errors"
    - name: "Documents placeholders"
      endpoints:
        - "POST /documents"
        - "GET /documents"
        - "DELETE /documents/{document_id}"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Question answering placeholder"
      endpoints:
        - "POST /qa"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Summary placeholder"
      endpoints:
        - "POST /summaries"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Comparison placeholder"
      endpoints:
        - "POST /comparisons"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Jobs placeholders"
      endpoints:
        - "GET /jobs/{job_id}"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Evidence placeholder"
      endpoints:
        - "GET /evidence/{answer_id}"
      placeholder_status: "501"
      compatibility: "can extend"
    - name: "Evaluation placeholders"
      endpoints:
        - "GET /evaluation/questions"
        - "POST /evaluation/runs"
      placeholder_status: "501"
      compatibility: "can extend"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect current FastAPI app"
    action: "Read backend/app/main.py, health route, schemas, and tests."
    expected_output: "Current route registration style is known."
  - step: 2
    name: "Create error schema/helper"
    action: "Add shared application error schema or helper for not-implemented responses."
    expected_output: "Placeholder routes can return a consistent shape."
  - step: 3
    name: "Create API schemas"
    action: "Add minimal request/response schemas for each planned API surface."
    expected_output: "Schemas are importable and typed."
  - step: 4
    name: "Create route placeholders"
    action: "Add route modules returning HTTP 501 with the application error shape."
    expected_output: "Routes are registered and honest about missing behavior."
  - step: 5
    name: "Add tests"
    action: "Use FastAPI TestClient to verify representative placeholder routes and health compatibility."
    expected_output: "Tests lock down status code and error shape."
  - step: 6
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "GET /health still returns HTTP 200."
    - "Representative placeholder routes return HTTP 501."
    - "Placeholder error bodies include code, message, and details."
    - "Route modules and schema modules import successfully."
  architectural:
    - "Routes do not implement workflow logic."
    - "Routes do not import infrastructure adapters or concrete provider clients."
    - "No fake successful RAG responses are returned."
  quality:
    - "API placeholder tests pass."
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
      purpose: "Validate route placeholders, schemas, and existing backend behavior."
      success_condition: "All tests pass."
    - command: "uv run ruff check ."
      cwd: "backend"
      purpose: "Validate lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check ."
      cwd: "backend"
      purpose: "Validate formatting."
      success_condition: "Ruff exits with code 0."
  runtime_checks:
    - name: "Placeholder API smoke check"
      method: "curl"
      expected: "Calling a representative placeholder endpoint returns HTTP 501 and code NOT_IMPLEMENTED."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Endpoint names may conflict with later frontend expectations."
    severity: "medium"
    mitigation: "Use route names from PROJECT_DECISIONS.md and keep contracts extensible."
  - risk: "File upload placeholder may be awkward to test without real storage."
    severity: "low"
    mitigation: "Test with TestClient using a small in-memory file only to verify placeholder behavior, not storage."

unknowns:
  - question: "Should final route paths be singular or plural?"
    resolution_strategy: "Prefer plural resource paths for documents, summaries, comparisons, jobs, evidence, and evaluation as specified here unless existing routes dictate otherwise."
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
    - "backend/app/main.py"
    - "backend/app/api/routes/health.py"
    - "backend/app/api/schemas/health.py"
  files_changed:
    - "backend/app/api/schemas/errors.py"
    - "backend/app/api/schemas/documents.py"
    - "backend/app/api/schemas/qa.py"
    - "backend/app/api/schemas/summaries.py"
    - "backend/app/api/schemas/comparisons.py"
    - "backend/app/api/schemas/jobs.py"
    - "backend/app/api/schemas/evidence.py"
    - "backend/app/api/schemas/evaluation.py"
    - "backend/app/api/routes/documents.py"
    - "backend/app/api/routes/qa.py"
    - "backend/app/api/routes/summaries.py"
    - "backend/app/api/routes/comparisons.py"
    - "backend/app/api/routes/jobs.py"
    - "backend/app/api/routes/evidence.py"
    - "backend/app/api/routes/evaluation.py"
    - "backend/app/api/routes/__init__.py"
    - "backend/app/main.py"
    - "backend/tests/test_api_placeholders.py"
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
    - "Route contracts may need refinement when real workflows are implemented."
  next_recommended_action: "Implement docs/specs/milestone-02e-services-and-dependency-wiring.md"
```
