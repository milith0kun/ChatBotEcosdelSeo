"""
MongoDB Atlas Connection Manager
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger
from typing import Optional

from app.config import get_settings


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


db = MongoDB()


async def connect_to_mongo():
    """Conectar a MongoDB Atlas"""
    settings = get_settings()
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_uri)
        db.db = db.client[settings.mongodb_db_name]
        
        # Verificar conexión
        await db.client.admin.command('ping')
        logger.info(f"📦 MongoDB Atlas conectado: {settings.mongodb_db_name}")
        
        # Crear índices
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB Atlas: {e}")
        raise


async def close_mongo_connection():
    """Cerrar conexión MongoDB"""
    if db.client:
        db.client.close()
        logger.info("📦 MongoDB desconectado")


async def create_indexes():
    """Crear índices necesarios"""
    try:
        await db.db.conversations.create_index("phone_number", unique=True)
        await db.db.messages.create_index("conversation_id")
        await db.db.leads.create_index("phone_number", unique=True)
        logger.info("📑 Índices creados")
    except Exception as e:
        logger.warning(f"⚠️ Índices ya existen o error: {e}")


def get_database() -> AsyncIOMotorDatabase:
    return db.db
