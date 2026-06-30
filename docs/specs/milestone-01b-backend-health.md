# Milestone 01b: Backend Health

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01b-backend-health"
title: "Backend FastAPI Scaffold And Health Endpoint"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-01-overview.md"
depends_on:
  - "docs/specs/milestone-01a-root-docker-compose.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  ok, so go ahead and split it as you described
```

## 3. System Interpretation

```yaml
system_translation: |
  Create a minimal FastAPI backend scaffold with a typed /health endpoint,
  uv-managed dependencies, Docker startup, and focused tests. This spec proves
  that the backend service can start and report its own status before any RAG
  workflows are implemented.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create backend Python project managed by uv."
    - "Create FastAPI app entrypoint."
    - "Create a thin health route under backend/app/api/routes/health.py."
    - "Create health response schema under backend/app/api/schemas/health.py."
    - "Create config loading under backend/app/core/config.py."
    - "Create dependency placeholder under backend/app/core/dependencies.py."
    - "Create backend Dockerfile."
    - "Create pytest coverage for /health."
    - "Configure ruff for lint and format checks."
  out_of_scope:
    - "Do not implement document, Q&A, summary, comparison, job, evidence, or evaluation routes."
    - "Do not connect to SQLite, Qdrant, Redis, LangChain, PyMuPDF, or LLM providers except optional dependency status placeholders."
    - "Do not persist API keys."
    - "Do not add real ingestion or retrieval behavior."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/Dockerfile"
      - "backend/pyproject.toml"
      - "backend/app/__init__.py"
      - "backend/app/main.py"
      - "backend/app/api/__init__.py"
      - "backend/app/api/routes/__init__.py"
      - "backend/app/api/routes/health.py"
      - "backend/app/api/schemas/__init__.py"
      - "backend/app/api/schemas/health.py"
      - "backend/app/core/__init__.py"
      - "backend/app/core/config.py"
      - "backend/app/core/dependencies.py"
      - "backend/tests/test_health.py"
  tests:
    unit:
      - "backend/tests/test_health.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Keep FastAPI routes thin."
  - "Keep app creation separate from route modules."
  - "Use backend/app/core/config.py for environment-derived settings."
  - "Use backend/app/core/dependencies.py for dependency wiring placeholders."
  - "Do not import infrastructure adapters into domain or schema modules."

coding_rules:
  - "Use English for identifiers and documentation."
  - "Use Portuguese for code comments only; avoid comments unless intent is non-obvious."
  - "Use typed Pydantic schemas for API responses."
  - "Keep health behavior deterministic and lightweight."
  - "Use pytest and ruff."
```

## 7. API Contract

```yaml
contracts:
  api_contracts:
    - name: "Backend health endpoint"
      request_shape: "GET /health"
      response_shape: |
        {
          "status": "ok",
          "service": "backend",
          "version": "<string>",
          "dependencies": {
            "redis": "<ok | unavailable | not_configured>",
            "qdrant": "<ok | unavailable | not_configured>"
          }
        }
      compatibility: "can extend"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Create backend package"
    action: "Create pyproject.toml, package directories, and __init__.py files."
    expected_output: "Backend package imports cleanly."
  - step: 2
    name: "Create config"
    action: "Implement Settings with app version, Redis URL, Qdrant URL, and host/port defaults."
    expected_output: "Settings are importable and test-friendly."
  - step: 3
    name: "Create health schema and route"
    action: "Implement response model and GET /health route."
    expected_output: "/health returns status ok."
  - step: 4
    name: "Create app entrypoint"
    action: "Create FastAPI app and register health router."
    expected_output: "uvicorn app.main:app can serve the API."
  - step: 5
    name: "Create backend Dockerfile"
    action: "Build backend image with uv and run uvicorn on port 8000."
    expected_output: "Backend container can start under Compose."
  - step: 6
    name: "Add tests"
    action: "Test /health response shape and status."
    expected_output: "pytest validates health contract."
  - step: 7
    name: "Validate"
    action: "Run pytest and ruff commands."
    expected_output: "Backend validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "uvicorn app.main:app starts the backend."
    - "GET /health returns HTTP 200."
    - "GET /health returns service backend and status ok."
    - "The Dockerfile starts the backend on port 8000."
  architectural:
    - "Route code stays thin."
    - "Config lives under backend/app/core/config.py."
    - "No future RAG routes are implemented."
  quality:
    - "backend/tests/test_health.py passes."
    - "ruff check passes."
    - "ruff format --check passes."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate backend tests."
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
    - name: "Backend health via Docker"
      method: "curl"
      expected: "GET http://localhost:8000/health returns status ok after Compose startup."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Dependency health checks may require network clients not needed yet."
    severity: "low"
    mitigation: "Return not_configured or simple status placeholders until integration milestones wire real clients."
  - risk: "Backend dependencies may be over-specified."
    severity: "medium"
    mitigation: "Install only FastAPI, uvicorn, pydantic-settings if needed, pytest, httpx, and ruff."

unknowns:
  - question: "Should /health check Redis and Qdrant live in Milestone 1?"
    resolution_strategy: "Prefer lightweight explicit dependency fields; full dependency clients can be added later if needed."
```

## 12. Minimal Output Contract

```yaml
agent_result:
  status: "<completed | failed | blocked>"
  summary: "<short factual summary>"
  files_read:
    - "PROJECT_DECISIONS.md"
    - "AGENTS.md"
    - "docs/specs/milestone-01-overview.md"
    - "docs/specs/milestone-01a-root-docker-compose.md"
  files_changed:
    - "backend/pyproject.toml"
    - "backend/Dockerfile"
    - "backend/app/main.py"
    - "backend/app/api/routes/health.py"
    - "backend/app/api/schemas/health.py"
    - "backend/app/core/config.py"
    - "backend/app/core/dependencies.py"
    - "backend/tests/test_health.py"
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
  remaining_risks: []
  next_recommended_action: "Implement docs/specs/milestone-01c-worker-health.md"
```
