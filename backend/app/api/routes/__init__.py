"""API route registration for the FastAPI application."""

from fastapi import APIRouter

from app.api.routes import (
    comparisons,
    documents,
    evaluation,
    evidence,
    health,
    jobs,
    qa,
    summaries,
)

API_ROUTERS: list[APIRouter] = [
    health.router,
    documents.router,
    qa.router,
    summaries.router,
    comparisons.router,
    jobs.router,
    evidence.router,
    evaluation.router,
]

__all__ = ["API_ROUTERS"]
