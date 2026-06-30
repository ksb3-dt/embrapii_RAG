# Milestone 01d: Frontend Shell

## 1. Metadata

```yaml
format_version: "agentic_sdd.v1"
task_id: "milestone-01d-frontend-shell"
title: "Frontend Vite React Shell"
created_at_utc: "2026-06-30T20:34:00Z"
author: "agent"
target_mode: "new_project"
priority: "p0"
risk_level: "low"
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
  Create a minimal React + TypeScript + Vite frontend scaffold that runs in
  Docker on port 5173 and displays an honest MVP shell. The UI should identify
  the EMBRAPII Reports RAG app and make it clear that RAG workflows are planned,
  not yet functional in Milestone 1.
```

## 4. Scope

```yaml
scope:
  in_scope:
    - "Create frontend package using npm."
    - "Create Vite React TypeScript entrypoint."
    - "Create minimal App component."
    - "Create global CSS."
    - "Create frontend Dockerfile."
    - "Configure build, dev, lint, and preview scripts where practical."
    - "Ensure Vite listens on 0.0.0.0 for Docker."
  out_of_scope:
    - "Do not build chat, upload, document list, summary, comparison, audit, or evaluation screens."
    - "Do not implement API client calls except optional static display of expected backend URL."
    - "Do not add routing unless needed for the shell."
    - "Do not include an in-app PDF viewer."
```

## 5. Affected Entities

```yaml
affected_entities:
  frontend:
    files:
      - "frontend/Dockerfile"
      - "frontend/package.json"
      - "frontend/package-lock.json"
      - "frontend/index.html"
      - "frontend/tsconfig.json"
      - "frontend/tsconfig.node.json"
      - "frontend/vite.config.ts"
      - "frontend/src/main.tsx"
      - "frontend/src/App.tsx"
      - "frontend/src/styles/globals.css"
    components:
      - "App"
  root:
    files:
      - "docker-compose.yml"
```

## 6. Architecture And Coding Rules

```yaml
architecture_rules:
  - "Use React + TypeScript + Vite + npm."
  - "Keep the initial UI small and easy to replace with the chat-centered MVP layout later."
  - "Do not create final workflow components prematurely."
  - "Do not add in-app PDF viewing."

coding_rules:
  - "Use English for identifiers and technical documentation."
  - "Use accessible HTML structure."
  - "Avoid text overflow and fragile fixed layouts."
  - "Use CSS that keeps the shell readable on common laptop screen sizes."
```

## 7. UI Contract

```yaml
contracts:
  ui_contracts:
    - name: "Frontend availability"
      requirement: "Opening http://localhost:5173 displays the EMBRAPII Reports RAG shell."
    - name: "Honest feature status"
      requirement: "The shell must not imply that upload, Q&A, summary, comparison, or audit workflows are working yet."
    - name: "Future MVP orientation"
      requirement: "The shell may list planned MVP workflows as upcoming capabilities."
```

## 8. Execution Plan

```yaml
execution_plan:
  - step: 1
    name: "Create npm project"
    action: "Create package.json and install React/Vite/TypeScript dependencies."
    expected_output: "npm scripts are available."
  - step: 2
    name: "Create Vite config"
    action: "Configure Vite for React and Docker-friendly host/port."
    expected_output: "Dev server can bind to 0.0.0.0:5173."
  - step: 3
    name: "Create frontend source"
    action: "Add main.tsx, App.tsx, and global CSS."
    expected_output: "Application shell renders."
  - step: 4
    name: "Create Dockerfile"
    action: "Build frontend image that serves Vite dev server or production preview consistently for MVP local use."
    expected_output: "Frontend service starts in Compose."
  - step: 5
    name: "Validate"
    action: "Run npm install, npm run build, and Docker runtime check when possible."
    expected_output: "Frontend builds and is reachable."
```

## 9. Acceptance Criteria

```yaml
acceptance_criteria:
  functional:
    - "npm run build completes successfully."
    - "The frontend Docker service listens on port 5173."
    - "http://localhost:5173 displays a visible EMBRAPII Reports RAG shell."
  architectural:
    - "No unfinished RAG workflow is presented as functional."
    - "No in-app PDF viewer is added."
    - "The app remains easy to evolve into the chat-centered MVP UI."
  quality:
    - "TypeScript build passes."
    - "Frontend dependencies are captured in package-lock.json."
```

## 10. Validation Protocol

```yaml
validation_protocol:
  required_commands:
    - command: "npm install"
      cwd: "frontend"
      purpose: "Install dependencies and create/update package-lock.json."
      success_condition: "npm exits with code 0."
    - command: "npm run build"
      cwd: "frontend"
      purpose: "Validate frontend TypeScript and Vite build."
      success_condition: "Build completes without errors."
    - command: "docker compose config"
      cwd: "."
      purpose: "Validate frontend service in Compose."
      success_condition: "Compose config renders successfully."
  runtime_checks:
    - name: "Frontend page"
      method: "browser or curl"
      expected: "http://localhost:5173 serves the app shell."
```

## 11. Risks And Unknowns

```yaml
risks:
  - risk: "Frontend shell may drift into implementing real workflows too early."
    severity: "medium"
    mitigation: "Keep UI as an honest placeholder and defer workflow components."
  - risk: "Vite may bind to localhost only inside Docker."
    severity: "medium"
    mitigation: "Configure host 0.0.0.0 and expose port 5173."

unknowns:
  - question: "Should the frontend use dev server or production preview in Docker for local MVP?"
    resolution_strategy: "Use the simplest stable option documented in README; ensure docker compose up --build works."
```

## 12. Minimal Output Contract

```yaml
agent_result:
  status: "<completed | failed | blocked>"
  summary: "<short factual summary>"
  files_read:
    - "docs/specs/milestone-01-overview.md"
    - "docs/specs/milestone-01a-root-docker-compose.md"
  files_changed:
    - "frontend/Dockerfile"
    - "frontend/package.json"
    - "frontend/package-lock.json"
    - "frontend/index.html"
    - "frontend/tsconfig.json"
    - "frontend/vite.config.ts"
    - "frontend/src/main.tsx"
    - "frontend/src/App.tsx"
    - "frontend/src/styles/globals.css"
    - "docker-compose.yml"
  commands_run:
    - command: "npm install"
      cwd: "frontend"
      exit_code: "<exit code>"
      result: "<short result>"
    - command: "npm run build"
      cwd: "frontend"
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
  next_recommended_action: "Implement docs/specs/milestone-01e-health-script-readme.md"
```
