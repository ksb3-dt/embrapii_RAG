from fastapi import FastAPI

from app.api.routes import health
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="EMBRAPII Reports RAG", version=settings.app_version)

app.include_router(health.router)
