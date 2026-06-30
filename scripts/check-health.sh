#!/usr/bin/env bash
# Verifica a saude dos servicos do Milestone 1 (backend, Qdrant, Redis e worker).
# Frontend e opcional; falha nele nao altera o codigo de saida.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

BACKEND_URL="${BACKEND_URL:-http://localhost:8000/health}"
QDRANT_URL="${QDRANT_URL:-http://localhost:6333/healthz}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:5173}"
COMPOSE_SERVICE_WORKER="${COMPOSE_SERVICE_WORKER:-worker}"
COMPOSE_SERVICE_REDIS="${COMPOSE_SERVICE_REDIS:-redis}"

FAILED=0

pass() {
  echo "[PASS] $1"
}

fail() {
  echo "[FAIL] $1"
  FAILED=1
}

warn() {
  echo "[WARN] $1"
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 2
  fi
}

require_command curl
require_command docker

if ! docker compose version >/dev/null 2>&1; then
  echo "Missing required command: docker compose" >&2
  exit 2
fi

echo "Checking Milestone 1 stack health from ${REPO_ROOT}"
echo

# Backend /health
if response="$(curl -fsS "${BACKEND_URL}" 2>/dev/null)"; then
  if grep -Eq '"status"[[:space:]]*:[[:space:]]*"ok"' <<<"${response}"; then
    pass "Backend (${BACKEND_URL})"
  else
    fail "Backend (${BACKEND_URL}) - reachable but status is not ok"
  fi
else
  fail "Backend (${BACKEND_URL}) - not reachable"
fi

# Qdrant
if curl -fsS "${QDRANT_URL}" >/dev/null 2>&1; then
  pass "Qdrant (${QDRANT_URL})"
else
  fail "Qdrant (${QDRANT_URL}) - health check failed"
fi

# Redis PING (prefer exec inside the Compose network)
redis_pong=""
if redis_pong="$(docker compose exec -T "${COMPOSE_SERVICE_REDIS}" redis-cli ping 2>/dev/null)"; then
  :
elif redis_pong="$(redis-cli -p 6379 ping 2>/dev/null)"; then
  :
fi

if [[ "${redis_pong}" == "PONG" ]]; then
  pass "Redis (PING)"
else
  fail "Redis (PING) - no PONG response"
fi

# Worker container status
worker_ids="$(docker compose ps --status running -q "${COMPOSE_SERVICE_WORKER}" 2>/dev/null || true)"
if [[ -n "${worker_ids}" ]]; then
  pass "Worker container (${COMPOSE_SERVICE_WORKER})"
else
  fail "Worker container (${COMPOSE_SERVICE_WORKER}) - not running"
fi

# Frontend (optional)
if curl -fsS "${FRONTEND_URL}" >/dev/null 2>&1; then
  pass "Frontend (${FRONTEND_URL}) [optional]"
else
  warn "Frontend (${FRONTEND_URL}) - not reachable (optional check)"
fi

echo
if [[ "${FAILED}" -eq 0 ]]; then
  echo "All required Milestone 1 health checks passed."
  exit 0
fi

echo "One or more required health checks failed."
exit 1
