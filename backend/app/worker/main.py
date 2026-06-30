"""Worker process entrypoint.

Milestone 1 placeholder only. Real Redis + RQ background jobs arrive in the
Background Jobs milestone.
"""

from __future__ import annotations

import logging
import signal
import sys
import threading
from dataclasses import dataclass

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

WORKER_SERVICE_NAME = "worker"
PLACEHOLDER_MESSAGE = (
    "Milestone 1 placeholder worker started. "
    "Background jobs (RQ) will be implemented in a later milestone."
)


@dataclass(frozen=True)
class WorkerStatus:
    """Simple worker health/status snapshot for logs and future health checks."""

    service: str
    status: str
    version: str
    redis_url_configured: bool
    qdrant_url_configured: bool
    message: str


def build_worker_status(settings: Settings | None = None) -> WorkerStatus:
    """Build worker status without starting the long-running process loop."""
    config = settings or get_settings()
    return WorkerStatus(
        service=WORKER_SERVICE_NAME,
        status="placeholder",
        version=config.app_version,
        redis_url_configured=bool(config.redis_url),
        qdrant_url_configured=bool(config.qdrant_url),
        message=PLACEHOLDER_MESSAGE,
    )


def log_startup(settings: Settings | None = None) -> WorkerStatus:
    """Log placeholder startup details and return the worker status."""
    status = build_worker_status(settings)
    logger.info("Worker service: %s", status.service)
    logger.info("Worker status: %s (Milestone 1 placeholder)", status.status)
    logger.info("App version: %s", status.version)
    logger.info(
        "Redis URL configured: %s",
        "yes" if status.redis_url_configured else "no",
    )
    logger.info(
        "Qdrant URL configured: %s",
        "yes" if status.qdrant_url_configured else "no",
    )
    logger.info("%s", status.message)
    return status


def run_forever() -> None:
    """Block until SIGTERM/SIGINT without a busy loop."""
    stop = threading.Event()

    def handle_signal(signum: int, _frame: object | None) -> None:
        logger.info("Received signal %s, shutting down worker.", signum)
        stop.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    stop.wait()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )
    log_startup()
    run_forever()


if __name__ == "__main__":
    main()
