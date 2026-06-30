# Milestone 01e: Health Script And README

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01e-health-script-readme"
title: "Health Script And README Setup Documentation"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-01-overview.md"
depends_on:
  - "docs/specs/milestone-01a-root-docker-compose.md"
  - "docs/specs/milestone-01b-backend-health.md"
  - "docs/specs/milestone-01c-worker-health.md"
  - "docs/specs/milestone-01d-frontend-shell.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  ok, so go ahead and split it as you described
```

## 3. System Interpretation

```yaml
system_translation: |
  Add the final verification and human setup documentation for Milestone 1.
  Create a bash health script that checks the running local stack and write a
  README that accurately explains setup, ports, commands, current limitations,
  and how to verify that the scaffold works.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create scripts/check-health.sh."
    - "Check backend /health."
    - "Check Qdrant health on port 6333."
    - "Check Redis PING."
    - "Check worker container status."
    - "Optionally check frontend availability on port 5173."
    - "Create README.md with project overview, setup, Docker usage, ports, health checks, and MVP limitations."
    - "Document that Milestone 1 does not implement RAG workflows yet."
  out_of_scope:
    - "Do not create a frontend health/status page."
    - "Do not implement monitoring, metrics, tracing, or production observability."
    - "Do not add cloud deployment instructions."
    - "Do not document nonexistent ingestion, Q&A, summary, comparison, or audit behavior as working."
```

## 5. Affected Entities

```yaml
affected_entities:
  root:
    files:
      - "README.md"
      - "scripts/check-health.sh"
      - "docker-compose.yml"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "PROJECT_DECISIONS.md requires a bash script for checking service health/status."
  - "The script should check backend, Qdrant, Redis, and worker."
  - "README must match real commands and ports."
  - "README must not claim unimplemented features are available."

coding_rules:
  - "Use bash with clear output and non-zero exit code on failure."
  - "Avoid fragile parsing when a direct command or endpoint check is available."
  - "Use English for script messages and documentation."
  - "Do not require secrets for health checks."
```

## 7. Contract Requirements

```yaml
contracts:
  script_contracts:
    - name: "scripts/check-health.sh"
      request_shape: "bash scripts/check-health.sh from repository root"
      response_shape: "Clear service-by-service status lines and process exit code"
      compatibility: "must preserve"
    - name: "Failure behavior"
      invariant: "If any required service check fails, the script exits non-zero."
    - name: "Success behavior"
      invariant: "If all required service checks pass, the script exits 0."

  documentation_contracts:
    - name: "README setup"
      invariant: "A new developer can follow README commands to start and verify the Milestone 1 stack."
    - name: "README limitations"
      invariant: "README clearly states that RAG workflows are not implemented in Milestone 1."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect implemented services"
    action: "Read docker-compose.yml, backend health route, worker setup, and frontend package."
    expected_output: "Health script checks match actual service names and endpoints."
  - step: 2
    name: "Create health script"
    action: "Implement scripts/check-health.sh with backend, Qdrant, Redis, worker, and optional frontend checks."
    expected_output: "Script reports clear pass/fail status."
  - step: 3
    name: "Create README"
    action: "Document overview, requirements, startup, ports, health verification, and current limitations."
    expected_output: "README matches Milestone 1 behavior."
  - step: 4
    name: "Validate docs and script"
    action: "Run shellcheck if available, bash script after docker compose up, and manual README review."
    expected_output: "Script works and docs are accurate."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "bash scripts/check-health.sh checks backend, Qdrant, Redis, and worker."
    - "The health script exits 0 when all services are healthy."
    - "The health script exits non-zero when any required service is unavailable."
    - "README explains docker compose up --build."
    - "README lists default ports 5173, 8000, 6333, and 6379."
  architectural:
    - "No frontend health/status page is added."
    - "No production/cloud deployment assumptions are introduced."
    - "Docs remain consistent with PROJECT_DECISIONS.md."
  quality:
    - "README commands are copy-pastable from the repository root."
    - "Script messages identify which service failed."
    - "Script does not require real API keys."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "bash -n scripts/check-health.sh"
      cwd: "."
      purpose: "Validate bash syntax."
      success_condition: "Command exits with code 0."
    - command: "docker compose config"
      cwd: "."
      purpose: "Validate final Compose config."
      success_condition: "Compose config renders successfully."
    - command: "docker compose up --build"
      cwd: "."
      purpose: "Start all services for final Milestone 1 verification."
      success_condition: "All services start successfully."
    - command: "bash scripts/check-health.sh"
      cwd: "."
      purpose: "Verify backend, Qdrant, Redis, worker, and optionally frontend."
      success_condition: "Script exits with code 0."
  manual_checks:
    - "Confirm README setup steps match actual commands."
    - "Confirm README does not describe unimplemented RAG workflows as working."
    - "Confirm no secrets are present in README or scripts."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Health script may depend on tools not installed on the host."
    severity: "medium"
    mitigation: "Prefer curl and docker compose commands; document prerequisites."
  - risk: "Redis host port may be unavailable due to a local conflict."
    severity: "medium"
    mitigation: "Use docker compose exec redis redis-cli ping when possible."
  - risk: "Qdrant health endpoint path can differ by image version."
    severity: "low"
    mitigation: "Use the endpoint supported by the selected image and document it."

unknowns:
  - question: "Should frontend availability be required by the health script?"
    resolution_strategy: "Include it if implemented reliably; backend, Qdrant, Redis, and worker are mandatory from PROJECT_DECISIONS.md."
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
    - "docker-compose.yml"
    - "backend/app/api/routes/health.py"
    - "backend/app/worker/main.py"
  files_changed:
    - "README.md"
    - "scripts/check-health.sh"
  commands_run:
    - command: "bash -n scripts/check-health.sh"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "docker compose config"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "docker compose up --build"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "bash scripts/check-health.sh"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
  validation:
    passed: []
    failed: []
  remaining_risks: []
  next_recommended_action: "Milestone 1 implementation review and final validation"
```
