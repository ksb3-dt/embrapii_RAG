# Milestone 02a: Backend Package Layout

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-02a-backend-package-layout"
title: "Backend Hexagonal Package Layout"
created_at_utc: "2026-06-30T23:10:00Z"
author: "agent"
target_mode: "existing_repo"
priority: "p0"
risk_level: "low"
parent_spec: "docs/specs/milestone-02-overview.md"
depends_on:
  - "docs/specs/milestone-01-overview.md"
```

## 2. Original User Request

```yaml
raw_user_request: |
  use the skill spec-generator to generate specs for the milestone 2. Divide it into different specs so I can build each one in a separate composer 2.5 session without troubles with it's context window.
```

## 3. System Interpretation

```yaml
system_translation: |
  Create the backend package directory skeleton for pragmatic hexagonal
  architecture without adding business behavior. This spec establishes importable
  package boundaries that later Milestone 2 child specs can fill with models,
  ports, routes, services, and dependency wiring.

  Expected user-visible result:
    - No user-facing behavior changes except the existing backend still starts.

  Expected engineering result:
    - The backend has stable package directories and __init__.py files for the
      planned architecture.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create missing backend package directories for api, application, domain, ports, infrastructure, and worker submodules."
    - "Add __init__.py files where needed so modules are importable."
    - "Keep existing backend/app/main.py and /health behavior working."
    - "Add a focused import smoke test for the package layout."
  out_of_scope:
    - "Do not create domain models, policy logic, port protocols, API route placeholders, application services, or infrastructure adapters in this spec."
    - "Do not change Docker Compose, frontend files, or health script behavior."
    - "Do not add new runtime dependencies unless import tests require a dev-only test dependency already accepted by the repo."
```

## 5. Affected Entities

```yaml
affected_entities:
  backend:
    files:
      - "backend/app/application/__init__.py"
      - "backend/app/application/prompts/__init__.py"
      - "backend/app/application/services/__init__.py"
      - "backend/app/application/use_cases/__init__.py"
      - "backend/app/domain/__init__.py"
      - "backend/app/domain/models/__init__.py"
      - "backend/app/domain/policies/__init__.py"
      - "backend/app/ports/__init__.py"
      - "backend/app/infrastructure/__init__.py"
      - "backend/app/infrastructure/parsers/__init__.py"
      - "backend/app/infrastructure/embeddings/__init__.py"
      - "backend/app/infrastructure/retrieval/__init__.py"
      - "backend/app/infrastructure/llms/__init__.py"
      - "backend/app/infrastructure/persistence/__init__.py"
      - "backend/app/infrastructure/storage/__init__.py"
      - "backend/app/infrastructure/qdrant/__init__.py"
      - "backend/tests/test_package_layout.py"
  tests:
    unit:
      - "backend/tests/test_package_layout.py"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Follow the package names from PROJECT_DECISIONS.md unless an existing repo pattern requires a smaller equivalent."
  - "Package files must not import concrete infrastructure at this stage."
  - "The existing FastAPI app entrypoint must keep importing cleanly."
  - "Directory creation must not imply implemented behavior."

coding_rules:
  - "Use English filenames and module names."
  - "Use Portuguese comments only if intent is non-obvious; empty __init__.py files are acceptable."
  - "Keep tests simple and deterministic."
```

## 7. Contracts

```yaml
contracts:
  package_contracts:
    - name: "Backend architecture packages"
      invariant: "Each planned package can be imported without side effects."
    - name: "Health compatibility"
      invariant: "backend/app/main.py still exposes the existing FastAPI app and health route."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Inspect current backend"
    action: "Read backend/app, backend/tests, pyproject.toml, and existing health route."
    expected_output: "Current package map and any existing modules are known."
  - step: 2
    name: "Create missing package folders"
    action: "Add directories and __init__.py files for planned architecture layers."
    expected_output: "All planned packages are importable."
  - step: 3
    name: "Add package layout smoke test"
    action: "Test imports for key packages and existing app import."
    expected_output: "Test fails if a package is missing or app import breaks."
  - step: 4
    name: "Validate"
    action: "Run backend tests and ruff checks."
    expected_output: "Validation passes."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "The backend app imports successfully."
    - "The existing /health tests still pass."
    - "Architecture packages are importable."
  architectural:
    - "No workflow, domain, API, or infrastructure behavior is implemented."
    - "No new coupling is introduced between domain/application and infrastructure."
  quality:
    - "backend/tests/test_package_layout.py passes."
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
      purpose: "Validate package imports and existing health tests."
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
  - risk: "Creating all planned folders may look like implemented architecture without behavior."
    severity: "low"
    mitigation: "Keep files empty or minimal and let later specs fill them with tested contracts."
  - risk: "A folder from PROJECT_DECISIONS.md may already exist with different contents."
    severity: "low"
    mitigation: "Read existing files first and preserve existing behavior."

unknowns:
  - question: "Should optional use_case wrappers be created now or later?"
    resolution_strategy: "Create only package folders now; later service/use-case specs decide concrete files."
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
    - "backend/pyproject.toml"
  files_changed:
    - "backend/app/application/**/__init__.py"
    - "backend/app/domain/**/__init__.py"
    - "backend/app/ports/__init__.py"
    - "backend/app/infrastructure/**/__init__.py"
    - "backend/tests/test_package_layout.py"
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
  next_recommended_action: "Implement docs/specs/milestone-02b-domain-models-and-policies.md"
```
