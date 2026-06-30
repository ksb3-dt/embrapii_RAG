from fastapi import FastAPI

from app.api.routes import API_ROUTERS
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="EMBRAPII Reports RAG", version=settings.app_version)

for router in API_ROUTERS:
    app.include_router(router)
