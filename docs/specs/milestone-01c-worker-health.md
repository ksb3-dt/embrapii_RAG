# Milestone 01c: Worker Health

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01c-worker-health"
title: "Worker Container And Health Signal"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "low"
parent_spec: "docs/specs/milestone-01-overview.md"
depends_on:
  - "docs/specs/milestone-01a-root-docker-compose.md"
  - "docs/specs/milestone-01b-backend-health.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  ok, so go ahead and split it as you described
```

## 3. System Interpretation

```yaml
system_translation: |
  Create a distinct worker process/container for the local MVP stack. The worker
  should prove that background-processing infrastructure can start, but it must
  not implement real ingestion, summaries, comparisons, evaluation, or RQ job
  behavior yet unless that is needed only as a harmless startup placeholder.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create backend/app/worker/main.py."
    - "Ensure Docker Compose can run a separate worker service."
    - "Provide clear worker startup logs or a simple health/status signal."
    - "Use Redis URL and Qdrant URL environment variables for future compatibility."
    - "Document that the worker is a placeholder until the Background Jobs milestone."
  out_of_scope:
    - "Do not implement RQ queues or real background tasks unless limited to an inert startup check."
    - "Do not implement ingestion, summaries, comparisons, or evaluation jobs."
    - "Do not connect to external LLM providers."
    - "Do not add persistent job metadata."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/worker/__init__.py"
      - "backend/app/worker/main.py"
      - "backend/pyproject.toml"
  root:
    files:
      - "docker-compose.yml"
  tests:
    unit:
      - "backend/tests/test_worker.py"
    integration:
      - "docker compose ps worker"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Worker must be a separate Docker Compose service from backend."
  - "Worker may share the backend Docker image."
  - "Worker startup must not pretend to process real jobs."
  - "Future RQ integration should be possible without changing service names."

coding_rules:
  - "Use English for identifiers and documentation."
  - "Use Portuguese for comments only if needed."
  - "Keep worker code minimal and explicit."
  - "Avoid busy loops that consume unnecessary CPU."
```

## 7. Contract Requirements

```yaml
contracts:
  worker_contracts:
    - name: "Worker service identity"
      invariant: "The worker service must be distinguishable from backend in docker compose ps and logs."
    - name: "Worker startup"
      invariant: "Worker starts without requiring PDFs, embeddings, Qdrant collections, or LLM keys."
    - name: "Worker status"
      invariant: "Health script can determine that the worker container is running or healthy."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect backend scaffold"
    action: "Read backend app/config files created by spec 01b."
    expected_output: "Worker can reuse project config safely."
  - step: 2
    name: "Create worker entrypoint"
    action: "Implement a minimal process that logs startup and remains alive safely."
    expected_output: "python -m app.worker.main starts locally."
  - step: 3
    name: "Wire worker service"
    action: "Update docker-compose.yml worker command if needed."
    expected_output: "docker compose starts worker as a separate service."
  - step: 4
    name: "Add worker test if practical"
    action: "Test importability or startup helper behavior without starting an infinite loop."
    expected_output: "Worker code has a safe unit test."
  - step: 5
    name: "Validate"
    action: "Run backend tests and inspect worker service status under Docker when possible."
    expected_output: "Worker startup is verified."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "The worker service is defined separately from backend in Docker Compose."
    - "The worker process starts without needing real jobs."
    - "Worker logs clearly state it is a Milestone 1 placeholder."
    - "The worker can be checked by scripts/check-health.sh in spec 01e."
  architectural:
    - "No background job workflow is implemented yet."
    - "Service name remains worker."
    - "Future RQ startup can replace the placeholder command."
  quality:
    - "Worker module imports without side effects that block tests."
    - "Backend tests still pass."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate worker import test and backend health tests."
      success_condition: "All backend tests pass."
    - command: "docker compose config"
      cwd: "."
      purpose: "Validate worker service in Compose."
      success_condition: "Compose config renders successfully."
  runtime_checks:
    - name: "Worker container status"
      method: "docker compose ps worker"
      expected: "Worker container is running or healthy after docker compose up --build."
    - name: "Worker logs"
      method: "docker compose logs worker"
      expected: "Logs identify placeholder worker startup."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "An infinite placeholder process could make tests hang."
    severity: "medium"
    mitigation: "Keep infinite wait behavior inside main(), not at import time."
  - risk: "Adding RQ too early may create dependency churn."
    severity: "low"
    mitigation: "Prefer a simple placeholder until the Background Jobs milestone."

unknowns:
  - question: "Should worker health use Docker healthcheck or running container status?"
    resolution_strategy: "Use container status for Milestone 1 unless a simple healthcheck is already available."
```

## 12. Minimal Output Contract

```yaml
agent_result:
  status: "<completed | failed | blocked>"
  summary: "<short factual summary>"
  files_read:
    - "docs/specs/milestone-01-overview.md"
    - "docs/specs/milestone-01a-root-docker-compose.md"
    - "docs/specs/milestone-01b-backend-health.md"
  files_changed:
    - "backend/app/worker/main.py"
    - "backend/app/worker/__init__.py"
    - "backend/tests/test_worker.py"
    - "docker-compose.yml"
  commands_run:
    - command: "uv run pytest -q"
      cwd: "backend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "docker compose config"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
  validation:
    passed: []
    failed: []
  remaining_risks: []
  next_recommended_action: "Implement docs/specs/milestone-01d-frontend-shell.md"
```
