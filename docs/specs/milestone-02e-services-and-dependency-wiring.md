# Milestone 02e: Services And Dependency Wiring

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02e-services-and-dependency-wiring"
title: "Application Services And Dependency Wiring"
created_at_utc: "2026-06-30T23:10:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-02-overview.md"
depends_on:
  - "docs/specs/milestone-02a-backend-package-layout.md"
  - "docs/specs/milestone-02b-domain-models-and-policies.md"
  - "docs/specs/milestone-02c-ports-contracts.md"
  - "docs/specs/milestone-02d-api-route-placeholders.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 2. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window.
```

## 3. System Interpretation

```yaml
system_translation: |
  Add application service placeholder classes and dependency wiring functions for
  the planned MVP workflows. Services should define coordination boundaries for
  document ingestion, question answering, report summaries, report comparisons,
  evidence audit, jobs, and evaluation, but must not implement real
  infrastructure behavior yet.

  Expected user-visible result:
    - Placeholder API routes can be wired to service dependencies while still
      returning explicit not-implemented errors.
    - Existing /health remains healthy.

  Expected engineering result:
    - Later milestones have clear service classes to fill in without moving
      orchestration logic into routes.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create application service placeholder modules for document ingestion, question answering, report summary, report comparison, evidence audit, evaluation, and jobs."
    - "Optionally create thin use-case wrapper modules only if they clarify dependency boundaries without duplicating service behavior."
    - "Add dependency provider functions and typed aliases in backend/app/core/dependencies.py."
    - "Wire placeholder routes to dependency functions where useful while preserving not-implemented responses."
    - "Add tests for dependency functions, service imports, and representative route behavior."
  out_of_scope:
    - "Do not implement real ingestion, parsing, chunking, embedding, indexing, retrieval, LLM calls, evidence persistence, job queue execution, summary generation, comparison generation, or golden-set evaluation."
    - "Do not add concrete SQLite, Qdrant, Redis, PyMuPDF, BAAI/bge-m3, LangChain, or LLM provider adapters."
    - "Do not change frontend behavior."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/application/services/document_ingestion_service.py"
      - "backend/app/application/services/question_answering_service.py"
      - "backend/app/application/services/report_summary_service.py"
      - "backend/app/application/services/report_comparison_service.py"
      - "backend/app/application/services/evidence_audit_service.py"
      - "backend/app/application/services/evaluation_service.py"
      - "backend/app/application/services/job_service.py"
      - "backend/app/application/use_cases/ingest_document.py"
      - "backend/app/application/use_cases/ask_question.py"
      - "backend/app/application/use_cases/summarize_report.py"
      - "backend/app/application/use_cases/compare_reports.py"
      - "backend/app/core/dependencies.py"
      - "backend/app/api/routes/documents.py"
      - "backend/app/api/routes/qa.py"
      - "backend/app/api/routes/summaries.py"
      - "backend/app/api/routes/comparisons.py"
      - "backend/app/api/routes/jobs.py"
      - "backend/app/api/routes/evidence.py"
      - "backend/app/api/routes/evaluation.py"
      - "backend/tests/test_service_placeholders.py"
      - "backend/tests/test_dependency_wiring.py"
  tests:
    unit:
      - "backend/tests/test_service_placeholders.py"
      - "backend/tests/test_dependency_wiring.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Application services coordinate workflows and depend on ports/domain models, not concrete infrastructure adapters."
  - "FastAPI routes stay thin and call dependency-provided services when they need workflow behavior."
  - "Dependency wiring for mostly static dependencies lives in backend/app/core/dependencies.py."
  - "Request-specific LLM provider selection must remain a factory contract; services must not store API keys."
  - "Placeholder service methods must fail explicitly instead of returning fake results."

coding_rules:
  - "Use English identifiers and docstrings."
  - "Use Portuguese comments only for non-obvious intent."
  - "Use explicit NotImplementedError or a domain/application-level not-implemented exception consistently."
  - "Keep service constructors narrow; do not require infrastructure dependencies that are not implemented yet."
```

## 7. Service And Wiring Contract Requirements

```yaml
contracts:
  service_contracts:
    - name: "DocumentIngestionService"
      methods:
        - "ingest_document(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "QuestionAnsweringService"
      methods:
        - "answer_question(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "ReportSummaryService"
      methods:
        - "summarize_report(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "ReportComparisonService"
      methods:
        - "compare_reports(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "EvidenceAuditService"
      methods:
        - "get_answer_evidence(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "JobService"
      methods:
        - "get_job_status(...)"
        - "create_job(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."
    - name: "EvaluationService"
      methods:
        - "list_questions(...)"
        - "run_evaluation(...)"
      placeholder_behavior: "Raises explicit not-implemented application error."

  dependency_contracts:
    - name: "Dependency providers"
      invariant: "backend/app/core/dependencies.py exposes typed dependency functions or aliases for each application service."
    - name: "API key safety"
      invariant: "No dependency function stores, logs, or hardcodes provider API keys."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect existing routes, ports, and domain"
    action: "Read Milestone 02b, 02c, and 02d outputs."
    expected_output: "Service method names align with existing schemas, domain models, and ports."
  - step: 2
    name: "Create application exception if needed"
    action: "Add a small application-level not-implemented exception only if route error handling needs it."
    expected_output: "Placeholder services fail consistently."
  - step: 3
    name: "Create service placeholders"
    action: "Add service classes with narrow constructors and explicit placeholder methods."
    expected_output: "Services define workflow boundaries without real behavior."
  - step: 4
    name: "Add dependency wiring"
    action: "Update backend/app/core/dependencies.py with provider functions and typed aliases."
    expected_output: "Routes and tests can request services consistently."
  - step: 5
    name: "Wire representative routes"
    action: "Inject services in placeholder routes where useful and keep HTTP 501/application error shape."
    expected_output: "Route thinness and placeholder behavior are both preserved."
  - step: 6
    name: "Add tests"
    action: "Test service imports, dependency providers, and representative route placeholder behavior."
    expected_output: "Tests lock down wiring and prevent routes from constructing concrete adapters."
  - step: 7
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "Application service modules import successfully."
    - "Dependency functions return service instances or placeholders without requiring external services."
    - "Representative API routes still return documented not-implemented responses."
    - "GET /health still returns HTTP 200."
  architectural:
    - "Routes do not instantiate infrastructure adapters or LLM clients."
    - "Services do not import FastAPI route modules or API schemas."
    - "Services depend only on domain models, policies, and ports."
    - "Dependency wiring is centralized in backend/app/core/dependencies.py."
  quality:
    - "Service and dependency tests pass."
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
      purpose: "Validate service placeholders, dependency wiring, route behavior, and existing tests."
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
    - name: "Backend starts after wiring"
      method: "curl"
      expected: "GET http://localhost:8000/health returns status ok after backend startup."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Service placeholders may duplicate future use-case wrappers."
    severity: "medium"
    mitigation: "Create use-case wrappers only if they add clarity; otherwise let services be the workflow boundary for now."
  - risk: "Dependency functions may need real adapter construction in later milestones."
    severity: "low"
    mitigation: "Keep dependency function names stable and replace internals later."
  - risk: "Not-implemented exception handling may be split across routes."
    severity: "medium"
    mitigation: "Prefer a shared helper or exception handler if multiple routes need identical behavior."

unknowns:
  - question: "Should ingestion be synchronous in API routes or queued immediately?"
    resolution_strategy: "Do not decide here; Milestone 8 owns Redis/RQ job behavior. Keep service contract extensible."
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
    - "docs/specs/milestone-02c-ports-contracts.md"
    - "docs/specs/milestone-02d-api-route-placeholders.md"
    - "backend/app/core/dependencies.py"
    - "backend/app/api/routes/*.py"
  files_changed:
    - "backend/app/application/services/document_ingestion_service.py"
    - "backend/app/application/services/question_answering_service.py"
    - "backend/app/application/services/report_summary_service.py"
    - "backend/app/application/services/report_comparison_service.py"
    - "backend/app/application/services/evidence_audit_service.py"
    - "backend/app/application/services/evaluation_service.py"
    - "backend/app/application/services/job_service.py"
    - "backend/app/application/use_cases/ingest_document.py"
    - "backend/app/application/use_cases/ask_question.py"
    - "backend/app/application/use_cases/summarize_report.py"
    - "backend/app/application/use_cases/compare_reports.py"
    - "backend/app/core/dependencies.py"
    - "backend/app/api/routes/*.py"
    - "backend/tests/test_service_placeholders.py"
    - "backend/tests/test_dependency_wiring.py"
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
    - "Service internals are intentionally unimplemented until later feature milestones."
  next_recommended_action: "Start Milestone 3 specs or implement PDF ingestion prototype after reviewing Milestone 2 results."
```
