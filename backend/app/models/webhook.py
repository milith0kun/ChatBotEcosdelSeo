"""
Modelos de Webhook
==================
Esquemas para webhooks de Evolution API
"""
from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime


class WebhookMessage(BaseModel):
    """Mensaje recibido via webhook de Evolution API"""
    key: Dict[str, Any]
    message: Dict[str, Any]
    messageTimestamp: int
    pushName: Optional[str] = None
    broadcast: bool = False
    
    @property
    def remote_jid(self) -> str:
        """Obtiene el número de teléfono del remitente"""
        return self.key.get("remoteJid", "")
    
    @property
    def phone_number(self) -> str:
        """Extrae solo el número de teléfono limpio"""
        jid = self.remote_jid
        return jid.split("@")[0] if "@" in jid else jid
    
    @property
    def is_from_me(self) -> bool:
        """Verifica si el mensaje fue enviado por nosotros"""
        return self.key.get("fromMe", False)
    
    @property
    def message_id(self) -> str:
        """ID único del mensaje"""
        return self.key.get("id", "")
    
    @property
    def text_content(self) -> Optional[str]:
        """Extrae el contenido de texto del mensaje"""
        msg = self.message
        
        # Mensaje de texto simple
        if "conversation" in msg:
            return msg["conversation"]
        
        # Mensaje extendido
        if "extendedTextMessage" in msg:
            return msg["extendedTextMessage"].get("text", "")
        
        # Mensaje con botón
        if "buttonsResponseMessage" in msg:
            return msg["buttonsResponseMessage"].get("selectedButtonId", "")
        
        # Mensaje de lista
        if "listResponseMessage" in msg:
            return msg["listResponseMessage"].get("singleSelectReply", {}).get("selectedRowId", "")
        
        return None
    
    @property
    def message_type(self) -> str:
        """Determina el tipo de mensaje"""
        msg = self.message
        
        if "conversation" in msg or "extendedTextMessage" in msg:
            return "text"
        elif "imageMessage" in msg:
            return "image"
        elif "audioMessage" in msg:
            return "audio"
        elif "videoMessage" in msg:
            return "video"
        elif "documentMessage" in msg:
            return "document"
        elif "stickerMessage" in msg:
            return "sticker"
        elif "contactMessage" in msg:
            return "contact"
        elif "locationMessage" in msg:
            return "location"
        else:
            return "unknown"


class WhatsAppWebhook(BaseModel):
    """Payload completo del webhook de Evolution API"""
    event: str
    instance: str
    data: Dict[str, Any]
    destination: Optional[str] = None
    date_time: Optional[str] = None
    sender: Optional[str] = None
    server_url: Optional[str] = None
    apikey: Optional[str] = None
    
    def get_message(self) -> Optional[WebhookMessage]:
        """Extrae el mensaje del payload si existe"""
        if self.event == "messages.upsert" and self.data:
            try:
                return WebhookMessage(**self.data)
            except Exception:
                return None
        return None
