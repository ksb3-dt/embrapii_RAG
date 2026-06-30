from typing import Literal

from pydantic import BaseModel

DependencyStatus = Literal["ok", "unavailable", "not_configured"]


class DependenciesHealth(BaseModel):
    redis: DependencyStatus
    qdrant: DependencyStatus


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["backend"]
    version: str
    dependencies: DependenciesHealth
