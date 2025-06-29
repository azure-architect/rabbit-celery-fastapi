"""
Health check endpoints
"""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rabbit-celery-fastapi",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check endpoint"""
    # TODO: Add actual health checks for dependencies
    return {
        "status": "healthy",
        "service": "rabbit-celery-fastapi",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "dependencies": {
            "database": "connected",  # TODO: Implement actual check
            "redis": "connected",     # TODO: Implement actual check
            "rabbitmq": "connected",  # TODO: Implement actual check
        },
        "timestamp": "2025-06-29T00:00:00Z",  # TODO: Use actual timestamp
    }
