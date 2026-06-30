from fastapi import APIRouter

from app.api.schemas.health import DependenciesHealth, DependencyStatus, HealthResponse
from app.core.dependencies import SettingsDep

router = APIRouter(tags=["health"])


def _dependency_placeholder(url: str) -> DependencyStatus:
    if not url:
        return "not_configured"
    # Sem cliente real neste milestone; verificação ativa virá em milestones futuros.
    return "not_configured"


@router.get("/health", response_model=HealthResponse)
def health_check(settings: SettingsDep) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="backend",
        version=settings.app_version,
        dependencies=DependenciesHealth(
            redis=_dependency_placeholder(settings.redis_url),
            qdrant=_dependency_placeholder(settings.qdrant_url),
        ),
    )
