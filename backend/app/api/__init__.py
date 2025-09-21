from fastapi import APIRouter
from app.api import health, notes, ai, search

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router, tags=["health"])
api_router.include_router(notes.router, tags=["notes"])
api_router.include_router(ai.router, tags=["ai"])
api_router.include_router(search.router, tags=["search"])

__all__ = ["api_router"]
