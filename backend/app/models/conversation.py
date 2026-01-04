"""
Modelos de Conversación
=======================
Esquemas para gestionar conversaciones y mensajes
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from bson import ObjectId


class Message(BaseModel):
    """Modelo de un mensaje individual"""
    id: Optional[str] = Field(default=None, alias="_id")
    conversation_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    message_type: Literal["text", "image", "audio", "video", "document"] = "text"
    whatsapp_message_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class Conversation(BaseModel):
    """Modelo de una conversación completa"""
    id: Optional[str] = Field(default=None, alias="_id")
    phone_number: str  # Número de WhatsApp del cliente
    name: Optional[str] = None  # Nombre del contacto si está disponible
    status: Literal["active", "waiting", "closed", "transferred"] = "active"
    lead_id: Optional[str] = None  # Referencia al lead
    messages_count: int = 0
    context: dict = Field(default_factory=dict)  # Contexto adicional de la conversación
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class ConversationContext(BaseModel):
    """Contexto de conversación para IA"""
    phone_number: str
    name: Optional[str] = None
    messages: List[dict] = []  # Lista de mensajes para OpenAI format
    lead_score: Optional[int] = None
    services_interested: List[str] = []
    last_intent: Optional[str] = None
