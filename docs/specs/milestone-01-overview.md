# Milestone 01 Overview: Project Scaffold And Docker

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01-overview"
title: "Project Scaffold And Docker Overview"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "medium"
```

## 2. Original User Request

```yaml
raw_user_request: |
  ok, so go ahead and split it as you described

previous_decision: |
  Split Milestone 1 into one overview spec plus smaller executable specs
  suitable for Cursor Composer sessions.

source_project_decision: |
  1. Project Scaffold And Docker
     - Create frontend, backend, worker, Redis, and Qdrant containers.
     - Add health checks.
```

## 3. System Interpretation

```yaml
system_translation: |
  Milestone 1 establishes the local Docker-based foundation for the EMBRAPII
  Reports RAG MVP. This overview is the parent coordination spec. Composer
  should not implement the entire milestone from this file alone. Instead,
  implement the child specs in dependency order and validate each one before
  moving to the next.

  Expected user-visible result:
    - docker compose up --build starts the MVP stack.
    - The frontend opens at http://localhost:5173.
    - The backend health endpoint responds at http://localhost:8000/health.
    - Redis, Qdrant, and the worker have clear health/status checks.

  Expected engineering result:
    - A clean baseline repo structure that later ingestion, retrieval, Q&A,
      audit, summary, comparison, and evaluation milestones can extend.
```

## 4. Composer Execution Strategy

```yaml
composer_strategy:
  use_this_file_for:
    - "Overall milestone context"
    - "Dependency order"
    - "Cross-spec acceptance criteria"
    - "Architecture and scope guardrails"
  do_not_use_this_file_for:
    - "One-shot implementation of all Milestone 1 code"
  execute_child_specs_in_order:
    - "docs/specs/milestone-01a-root-docker-compose.md"
    - "docs/specs/milestone-01b-backend-health.md"
    - "docs/specs/milestone-01c-worker-health.md"
    - "docs/specs/milestone-01d-frontend-shell.md"
    - "docs/specs/milestone-01e-health-script-readme.md"
  review_after_each_spec:
    - "Inspect every diff before accepting."
    - "Run the spec's validation commands."
    - "Do not start the next spec until the current one is accepted or intentionally revised."
```

## 5. Business / Product Context

```yaml
business_context:
  user_problem: "The MVP needs a reliable local foundation before RAG workflows are implemented."
  target_user: "Internal managers, evaluators, and developers working on the EMBRAPII Reports RAG MVP."
  expected_outcome: "The full local stack starts consistently with Docker and exposes basic health signals."
  product_surface:
    - "Local development workflow"
    - "Docker Compose stack"
    - "Backend health API"
    - "Frontend shell"
    - "Worker process"
    - "Service health script"
```

## 6. Global Scope

```yaml
scope:
  in_scope:
    - "Root Docker Compose setup for frontend, backend, worker, Redis, and Qdrant."
    - "Minimal FastAPI backend with /health endpoint."
    - "Minimal worker container/process with health/status behavior."
    - "Minimal React + TypeScript + Vite frontend shell."
    - "Qdrant data persistence under data/qdrant/."
    - "Local document directory under data/documents/."
    - "Health-check script for backend, Qdrant, Redis, and worker."
    - "README setup instructions and non-secret .env.example."
  out_of_scope:
    - "PDF ingestion."
    - "Embeddings and Qdrant indexing."
    - "Dense retrieval, keyword retrieval, and Reciprocal Rank Fusion."
    - "Q&A, citations, summaries, comparisons, evidence audit, and evaluation."
    - "LLM provider calls or API key persistence."
    - "OCR, advanced table extraction, auth, permissions, or production cloud deployment."
```

## 7. Global Architecture Rules

```yaml
architecture_rules:
  project_specific_rules:
    - "PROJECT_DECISIONS.md is the source of truth for MVP architecture and constraints."
    - "Use React + TypeScript + Vite + npm for frontend."
    - "Use Python + FastAPI + uv for backend."
    - "The Docker stack must include frontend, backend, worker, Redis, and Qdrant."
    - "Default local ports are frontend 5173, backend 8000, Qdrant 6333, and Redis 6379."
    - "Qdrant data should persist at data/qdrant/."
    - "Use data/documents/ for local PDF storage in later milestones."
    - "Keep FastAPI routes thin."
    - "Wire mostly static dependencies in backend/app/core/dependencies.py."
    - "Do not hardcode or persist provider API keys."
    - "Use English for code identifiers and technical documentation."
    - "Use Portuguese for code comments only."
```

## 8. Milestone Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "docker compose up --build starts frontend, backend, worker, Redis, and Qdrant services."
    - "The frontend is reachable at http://localhost:5173 and displays the MVP shell."
    - "The backend is reachable at http://localhost:8000/health and returns status ok."
    - "Qdrant is reachable on port 6333."
    - "Redis responds to PING on port 6379 or inside the Docker network."
    - "The worker container starts and is distinguishable from the backend."
    - "scripts/check-health.sh reports all Milestone 1 services as healthy."

  architectural:
    - "The scaffold matches the pragmatic hexagonal layout expected by later milestones."
    - "No fake ingestion, retrieval, citation, or LLM behavior is implemented."
    - "Service names, ports, and data paths align with PROJECT_DECISIONS.md."

  quality:
    - "Backend health tests pass."
    - "Backend lint/format checks pass where configured."
    - "Frontend build passes."
    - "docker compose config validates."
    - "README instructions match actual commands."
```

## 9. Milestone Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "uv run pytest -q"
      cwd: "backend"
      purpose: "Validate backend health behavior."
      success_condition: "All selected tests pass."
    - command: "uv run ruff check ."
      cwd: "backend"
      purpose: "Validate backend lint rules."
      success_condition: "Ruff exits with code 0."
    - command: "uv run ruff format --check ."
      cwd: "backend"
      purpose: "Validate backend formatting."
      success_condition: "Ruff exits with code 0."
    - command: "npm run build"
      cwd: "frontend"
      purpose: "Validate frontend production build."
      success_condition: "Build completes without TypeScript or Vite errors."
    - command: "docker compose config"
      cwd: "."
      purpose: "Validate Docker Compose syntax."
      success_condition: "Compose config renders successfully."
    - command: "docker compose up --build"
      cwd: "."
      purpose: "Start the full local stack."
      success_condition: "All Milestone 1 services start successfully."
    - command: "bash scripts/check-health.sh"
      cwd: "."
      purpose: "Verify the running stack."
      success_condition: "All checks pass and script exits with code 0."
```

## 10. Risks and Guardrails

```yaml
risks:
  - risk: "A one-shot Composer run may create a large, hard-to-review diff."
    severity: "medium"
    mitigation: "Use child specs as bounded Composer sessions."
  - risk: "Milestone 1 may accidentally grow into ingestion or RAG behavior."
    severity: "medium"
    mitigation: "Keep later workflows documented only; do not fake them."
  - risk: "Docker may not run in the agent environment."
    severity: "medium"
    mitigation: "Run non-Docker validation and report Docker startup as manually pending if blocked."

guardrails:
  - "Do not implement multiple child specs in one Composer prompt."
  - "Do not start child spec 01e until the services it checks exist."
  - "If a child spec changes a shared contract, update dependent specs or stop and ask."
  - "Review and accept/reject each Composer diff before continuing."
```

## 11. Deliverables

```yaml
deliverables:
  specs:
    - "docs/specs/milestone-01-overview.md"
    - "docs/specs/milestone-01a-root-docker-compose.md"
    - "docs/specs/milestone-01b-backend-health.md"
    - "docs/specs/milestone-01c-worker-health.md"
    - "docs/specs/milestone-01d-frontend-shell.md"
    - "docs/specs/milestone-01e-health-script-readme.md"
```
