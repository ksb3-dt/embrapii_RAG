# Milestone 01a: Root Docker Compose

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01a-root-docker-compose"
title: "Root Docker Compose And Project Directories"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "medium"
parent_spec: "docs/specs/milestone-01-overview.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  ok, so go ahead and split it as you described
```

## 3. System Interpretation

```yaml
system_translation: |
  Create the root Docker Compose and repository-level foundation for the local
  EMBRAPII Reports RAG MVP. This spec should define the service topology,
  ports, shared environment variables, and persistent local directories. It
  should not implement backend, frontend, or worker internals beyond what is
  needed for Compose references to be valid once child specs are complete.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create docker-compose.yml with services for frontend, backend, worker, redis, and qdrant."
    - "Use default ports: frontend 5173, backend 8000, Qdrant 6333, Redis 6379."
    - "Persist Qdrant data under data/qdrant/."
    - "Create data/documents/ as the future local PDF storage directory."
    - "Create .env.example with non-secret local configuration."
    - "Create or update .gitignore for generated, local, cache, database, and secret files."
    - "Create placeholder root directories needed by later child specs only when useful."
  out_of_scope:
    - "Do not implement FastAPI routes."
    - "Do not implement React UI."
    - "Do not implement worker logic."
    - "Do not create PDF ingestion, embeddings, Qdrant collections, or LLM integrations."
    - "Do not add real secrets or provider API keys."
```

## 5. Affected Entities

```yaml
affected_entities:
  root:
    files:
      - "docker-compose.yml"
      - ".env.example"
      - ".gitignore"
    directories:
      - "data/documents/"
      - "data/qdrant/"
      - "backend/"
      - "frontend/"
      - "scripts/"
  tests:
    integration:
      - "docker compose config"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Follow PROJECT_DECISIONS.md for service names, ports, and local data paths."
  - "Use Docker Compose as the single local stack entrypoint."
  - "Frontend, backend, and worker should be separate Compose services."
  - "Worker may share the backend image, but must be a separate service."
  - "Qdrant must persist data at data/qdrant/."
  - "No committed file may contain secrets."

coding_rules:
  - "Use English for filenames and technical documentation."
  - "Keep .env.example explicit but non-secret."
  - "Keep Compose readable; avoid production-only cloud assumptions."
```

## 7. Data / Contract Requirements

```yaml
contracts:
  docker_services:
    - name: "frontend"
      port: "5173:5173"
      depends_on:
        - "backend"
    - name: "backend"
      port: "8000:8000"
      depends_on:
        - "redis"
        - "qdrant"
    - name: "worker"
      depends_on:
        - "redis"
        - "qdrant"
    - name: "redis"
      port: "6379:6379"
    - name: "qdrant"
      port: "6333:6333"
      volume: "./data/qdrant:/qdrant/storage"

  environment:
    - name: "BACKEND_HOST"
      example: "0.0.0.0"
    - name: "BACKEND_PORT"
      example: "8000"
    - name: "FRONTEND_PORT"
      example: "5173"
    - name: "REDIS_URL"
      example: "redis://redis:6379/0"
    - name: "QDRANT_URL"
      example: "http://qdrant:6333"
    - name: "DOCUMENTS_DIR"
      example: "/app/data/documents"
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect repo decisions"
    action: "Read PROJECT_DECISIONS.md and AGENTS.md."
    expected_output: "Confirmed ports, services, and data paths."
  - step: 2
    name: "Create root directories"
    action: "Create data/documents, data/qdrant, backend, frontend, and scripts as needed."
    expected_output: "Expected root folders exist."
  - step: 3
    name: "Create environment template"
    action: "Write .env.example with non-secret local defaults."
    expected_output: ".env.example documents runtime variables."
  - step: 4
    name: "Create gitignore"
    action: "Ignore local databases, caches, env files, generated data, and dependency folders."
    expected_output: ".gitignore prevents accidental commits of local artifacts."
  - step: 5
    name: "Create Compose file"
    action: "Define frontend, backend, worker, redis, and qdrant services."
    expected_output: "docker-compose.yml resolves once child specs provide Dockerfiles."
  - step: 6
    name: "Validate Compose"
    action: "Run docker compose config."
    expected_output: "Compose syntax is valid."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "docker-compose.yml defines frontend, backend, worker, redis, and qdrant."
    - "Default host ports match PROJECT_DECISIONS.md."
    - "data/documents/ and data/qdrant/ exist."
    - ".env.example contains only non-secret local defaults."
  architectural:
    - "Worker is a separate service from backend."
    - "No RAG behavior is implemented."
    - "No provider keys or secrets are added."
  quality:
    - "docker compose config succeeds after dependent child specs create referenced Dockerfiles."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "docker compose config"
      cwd: "."
      purpose: "Validate Compose syntax and service wiring."
      success_condition: "Compose config renders without errors."
  manual_checks:
    - "Confirm .env.example has no real secrets."
    - "Confirm Qdrant volume points at data/qdrant/."
    - "Confirm no public port deviates from PROJECT_DECISIONS.md."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Compose validation may fail until backend/frontend Dockerfiles exist."
    severity: "low"
    mitigation: "Run final compose validation after child specs 01b, 01c, and 01d."
  - risk: "Accidentally committing local data."
    severity: "medium"
    mitigation: "Add .gitignore entries for local databases, Qdrant storage contents, and env files."

unknowns:
  - question: "Should data/qdrant contents be ignored while keeping the directory?"
    resolution_strategy: "Prefer keeping the directory via .gitkeep and ignoring generated contents."
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
  files_changed:
    - "docker-compose.yml"
    - ".env.example"
    - ".gitignore"
    - "data/documents/.gitkeep"
    - "data/qdrant/.gitkeep"
  commands_run:
    - command: "docker compose config"
      cwd: "."
      exit_code: "<exit code>"
      result: "<short result>"
  validation:
    passed: []
    failed: []
  remaining_risks: []
  next_recommended_action: "Implement docs/specs/milestone-01b-backend-health.md"
```
