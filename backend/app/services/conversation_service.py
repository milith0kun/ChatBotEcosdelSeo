"""
Conversation Service - Gestión de conversaciones
"""
from datetime import datetime
from typing import Optional, List, Dict
from loguru import logger
from bson import ObjectId

from app.database.mongodb import get_database


class ConversationService:
    """Servicio para gestionar conversaciones"""
    
    def __init__(self):
        self.db = None
    
    def _get_db(self):
        if self.db is None:
            self.db = get_database()
        return self.db
    
    async def get_or_create_conversation(self, phone_number: str, name: str = None) -> Dict:
        """Obtiene o crea una conversación"""
        db = self._get_db()
        
        conversation = await db.conversations.find_one({"phone_number": phone_number})
        
        if conversation:
            conversation["_id"] = str(conversation["_id"])
            return conversation
        
        new_conversation = {
            "phone_number": phone_number,
            "name": name,
            "status": "active",
            "messages_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.conversations.insert_one(new_conversation)
        new_conversation["_id"] = str(result.inserted_id)
        
        logger.info(f"📱 Nueva conversación: {phone_number}")
        return new_conversation
    
    async def add_message(self, conversation_id: str, role: str, content: str, 
                          message_type: str = "text", whatsapp_id: str = None) -> Dict:
        """Agrega mensaje a la conversación"""
        db = self._get_db()
        
        message = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "message_type": message_type,
            "whatsapp_message_id": whatsapp_id,
            "created_at": datetime.utcnow()
        }
        
        result = await db.messages.insert_one(message)
        message["_id"] = str(result.inserted_id)
        
        # Actualizar conversación
        await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$inc": {"messages_count": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return message
    
    async def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Obtiene historial en formato OpenAI"""
        db = self._get_db()
        
        cursor = db.messages.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", -1).limit(limit)
        
        messages = []
        async for msg in cursor:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        messages.reverse()
        return messages


_conversation_service: Optional[ConversationService] = None

def get_conversation_service() -> ConversationService:
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService()
    return _conversation_service
