import logging

from app.core.config import Settings
from app.worker.main import (
    PLACEHOLDER_MESSAGE,
    WORKER_SERVICE_NAME,
    build_worker_status,
    log_startup,
)


def test_worker_module_imports() -> None:
    import app.worker.main  # noqa: F401


def test_build_worker_status_with_configured_urls() -> None:
    settings = Settings(
        redis_url="redis://redis:6379/0",
        qdrant_url="http://qdrant:6333",
    )
    status = build_worker_status(settings)

    assert status.service == WORKER_SERVICE_NAME
    assert status.status == "placeholder"
    assert status.version
    assert status.redis_url_configured is True
    assert status.qdrant_url_configured is True
    assert "placeholder" in status.message.lower()


def test_build_worker_status_without_urls() -> None:
    settings = Settings(redis_url="", qdrant_url="")
    status = build_worker_status(settings)

    assert status.redis_url_configured is False
    assert status.qdrant_url_configured is False


def test_log_startup_emits_placeholder_message(caplog) -> None:
    settings = Settings(
        redis_url="redis://redis:6379/0",
        qdrant_url="http://qdrant:6333",
    )

    with caplog.at_level(logging.INFO):
        status = log_startup(settings)

    assert status.service == WORKER_SERVICE_NAME
    assert PLACEHOLDER_MESSAGE in caplog.text
