"""
Chat Endpoints - Testing y Debug
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.services.ai_service import get_ai_service
from app.services.conversation_service import get_conversation_service
from app.services.lead_service import get_lead_service

router = APIRouter()


class ChatRequest(BaseModel):
    """Petición de chat para testing"""
    message: str
    phone_number: str = "test_user"
    name: Optional[str] = "Usuario Test"


class ChatResponse(BaseModel):
    """Respuesta del chat"""
    response: str
    conversation_id: str
    messages_count: int


@router.post("/test", response_model=ChatResponse)
async def test_chat(request: ChatRequest):
    """Endpoint para probar el chat sin WhatsApp"""
    ai_service = get_ai_service()
    conv_service = get_conversation_service()
    lead_service = get_lead_service()
    
    # Obtener o crear conversación
    conversation = await conv_service.get_or_create_conversation(
        request.phone_number, 
        request.name
    )
    await lead_service.get_or_create_lead(request.phone_number, request.name)
    
    conv_id = conversation["_id"]
    
    # Guardar mensaje del usuario
    await conv_service.add_message(conv_id, "user", request.message)
    
    # Obtener historial
    history = await conv_service.get_conversation_history(conv_id)
    
    # Generar respuesta
    context = {"name": request.name}
    response = await ai_service.generate_response(request.message, history, context)
    
    # Guardar respuesta
    await conv_service.add_message(conv_id, "assistant", response)
    
    return ChatResponse(
        response=response,
        conversation_id=conv_id,
        messages_count=len(history) + 2
    )


@router.get("/history/{phone_number}")
async def get_history(phone_number: str, limit: int = 20):
    """Obtiene el historial de una conversación"""
    conv_service = get_conversation_service()
    
    conversation = await conv_service.get_or_create_conversation(phone_number)
    history = await conv_service.get_conversation_history(conversation["_id"], limit)
    
    return {
        "phone_number": phone_number,
        "conversation_id": conversation["_id"],
        "messages": history
    }


@router.delete("/history/{phone_number}")
async def clear_history(phone_number: str):
    """Limpia el historial de una conversación (para testing)"""
    from app.database.mongodb import get_database
    
    db = get_database()
    conv = await db.conversations.find_one({"phone_number": phone_number})
    
    if conv:
        await db.messages.delete_many({"conversation_id": str(conv["_id"])})
        await db.conversations.delete_one({"_id": conv["_id"]})
        return {"status": "deleted", "phone_number": phone_number}
    
    return {"status": "not_found", "phone_number": phone_number}
