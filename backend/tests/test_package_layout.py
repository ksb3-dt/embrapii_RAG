import importlib

ARCHITECTURE_PACKAGES = [
    "app.application",
    "app.application.prompts",
    "app.application.services",
    "app.application.use_cases",
    "app.domain",
    "app.domain.models",
    "app.domain.policies",
    "app.ports",
    "app.infrastructure",
    "app.infrastructure.parsers",
    "app.infrastructure.embeddings",
    "app.infrastructure.retrieval",
    "app.infrastructure.llms",
    "app.infrastructure.persistence",
    "app.infrastructure.storage",
    "app.infrastructure.qdrant",
]


def test_architecture_packages_are_importable() -> None:
    for package_name in ARCHITECTURE_PACKAGES:
        module = importlib.import_module(package_name)
        assert module.__name__ == package_name


def test_fastapi_app_imports_cleanly() -> None:
    main_module = importlib.import_module("app.main")
    assert main_module.app is not None
    assert main_module.app.title == "EMBRAPII Reports RAG"
