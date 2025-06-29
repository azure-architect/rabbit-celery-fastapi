"""
API v1 router
"""
from fastapi import APIRouter
from app.api.api_v1.endpoints import tasks, health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
