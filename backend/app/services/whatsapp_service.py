"""
WhatsApp Service - Evolution API Integration
"""
import httpx
from loguru import logger
from typing import Optional, Dict, Any
from app.config import get_settings


class WhatsAppService:
    """Servicio para comunicación con WhatsApp via Evolution API"""
    
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.evolution_api_url
        self.api_key = settings.evolution_api_key
        self.instance_name = settings.evolution_instance_name
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}
    
    async def send_text_message(self, phone_number: str, message: str) -> Dict:
        """Envía un mensaje de texto"""
        number = self._format_phone_number(phone_number)
        payload = {"number": number, "text": message}
        return await self._make_request("POST", f"/message/sendText/{self.instance_name}", payload)
    
    async def send_presence(self, phone_number: str, presence: str = "composing"):
        """Envía estado de presencia (escribiendo)"""
        number = self._format_phone_number(phone_number)
        payload = {"number": number, "presence": presence}
        return await self._make_request("POST", f"/chat/updatePresence/{self.instance_name}", payload)
    
    async def mark_as_read(self, phone_number: str, message_id: str):
        """Marca un mensaje como leído"""
        number = self._format_phone_number(phone_number)
        payload = {"readMessages": [{"remoteJid": f"{number}@s.whatsapp.net", "id": message_id}]}
        return await self._make_request("POST", f"/chat/markMessageAsRead/{self.instance_name}", payload)
    
    async def get_instance_status(self) -> Dict:
        """Obtiene el estado de la instancia"""
        return await self._make_request("GET", f"/instance/connectionState/{self.instance_name}")
    
    async def get_qr_code(self) -> Optional[str]:
        """Obtiene el código QR para vincular WhatsApp"""
        try:
            response = await self._make_request("GET", f"/instance/connect/{self.instance_name}")
            return response.get("base64")
        except Exception as e:
            logger.error(f"Error obteniendo QR: {e}")
            return None
    
    def _format_phone_number(self, phone_number: str) -> str:
        """Formatea el número de teléfono"""
        number = "".join(filter(str.isdigit, phone_number))
        if len(number) == 9:
            number = f"51{number}"  # Código Perú
        return number
    
    async def _make_request(self, method: str, endpoint: str, payload: Dict = None) -> Dict:
        """Realiza petición HTTP a Evolution API"""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "GET":
                    response = await client.get(url, headers=self.headers)
                else:
                    response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error en Evolution API: {e}")
            raise


_whatsapp_service: Optional[WhatsAppService] = None

def get_whatsapp_service() -> WhatsAppService:
    global _whatsapp_service
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppService()
    return _whatsapp_service
