"""
Webhook Endpoints - Evolution API
"""
from fastapi import APIRouter, Request, BackgroundTasks
from loguru import logger
from typing import Dict, Any

from app.models.webhook import WhatsAppWebhook
from app.services.ai_service import get_ai_service
from app.services.whatsapp_service import get_whatsapp_service
from app.services.conversation_service import get_conversation_service
from app.services.lead_service import get_lead_service

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Recibe webhooks de Evolution API"""
    try:
        body = await request.json()
        logger.debug(f"📥 Webhook recibido: {body.get('event', 'unknown')}")
        
        webhook = WhatsAppWebhook(**body)
        
        # Solo procesar mensajes nuevos
        if webhook.event == "messages.upsert":
            message = webhook.get_message()
            
            if message and not message.is_from_me and message.text_content:
                # Procesar en background para responder rápido
                background_tasks.add_task(
                    process_incoming_message,
                    phone_number=message.phone_number,
                    text=message.text_content,
                    name=message.pushName,
                    message_id=message.message_id
                )
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"❌ Error procesando webhook: {e}")
        return {"status": "error", "message": str(e)}


async def process_incoming_message(phone_number: str, text: str, name: str = None, message_id: str = None):
    """Procesa un mensaje entrante"""
    try:
        logger.info(f"💬 Mensaje de {phone_number}: {text[:50]}...")
        
        # Servicios
        ai_service = get_ai_service()
        whatsapp = get_whatsapp_service()
        conv_service = get_conversation_service()
        lead_service = get_lead_service()
        
        # Obtener o crear conversación y lead
        conversation = await conv_service.get_or_create_conversation(phone_number, name)
        await lead_service.get_or_create_lead(phone_number, name)
        
        conv_id = conversation["_id"]
        
        # Guardar mensaje del usuario
        await conv_service.add_message(conv_id, "user", text, whatsapp_id=message_id)
        
        # Obtener historial
        history = await conv_service.get_conversation_history(conv_id)
        
        # Contexto
        context = {"name": name or conversation.get("name")}
        
        # Mostrar "escribiendo..."
        try:
            await whatsapp.send_presence(phone_number, "composing")
        except:
            pass
        
        # Generar respuesta con IA
        response = await ai_service.generate_response(text, history, context)
        
        # Guardar respuesta
        await conv_service.add_message(conv_id, "assistant", response)
        
        # Enviar respuesta por WhatsApp
        await whatsapp.send_text_message(phone_number, response)
        
        logger.info(f"✅ Respuesta enviada a {phone_number}")
        
    except Exception as e:
        logger.error(f"❌ Error procesando mensaje: {e}")
        
        # Intentar enviar mensaje de error
        try:
            whatsapp = get_whatsapp_service()
            await whatsapp.send_text_message(
                phone_number,
                "Disculpa, tuve un problema técnico. ¿Podrías repetir tu mensaje? 🙏"
            )
        except:
            pass
