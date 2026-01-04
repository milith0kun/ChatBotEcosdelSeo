"""
ChatBot Ecos del SEO - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import get_settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection

# Importar routers explícitamente
from app.routes.health import router as health_router
from app.routes.webhook import router as webhook_router
from app.routes.chat import router as chat_router
from app.routes.whatsapp import router as whatsapp_router


# Configure Loguru
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="DEBUG" if get_settings().debug else "INFO"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación"""
    settings = get_settings()
    logger.info(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    
    # Conectar MongoDB Atlas
    await connect_to_mongo()
    logger.info("✅ Conexiones establecidas")
    
    yield
    
    # Cerrar conexiones
    await close_mongo_connection()
    logger.info("👋 Aplicación cerrada")


app = FastAPI(
    title="ChatBot Ecos del SEO",
    description="Asistente de ventas automatizado con IA para WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas registradas explícitamente
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(webhook_router, prefix="/api/v1/webhook", tags=["Webhooks"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(whatsapp_router, prefix="/api/v1/whatsapp", tags=["WhatsApp"])


@app.get("/")
async def root():
    settings = get_settings()
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs"
    }
