"""
Health Check Endpoints
"""
from fastapi import APIRouter
from app.config import get_settings
from app.database.mongodb import db

router = APIRouter()


@router.get("/health")
async def health_check():
    """Verificación de salud"""
    settings = get_settings()
    
    mongo_status = "ok"
    try:
        await db.client.admin.command('ping')
    except Exception:
        mongo_status = "error"
    
    return {
        "status": "healthy" if mongo_status == "ok" else "degraded",
        "app": settings.app_name,
        "version": settings.app_version,
        "mongodb": mongo_status
    }
