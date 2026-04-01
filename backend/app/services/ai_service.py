"""
AI Service - DeepSeek Integration
"""
from openai import AsyncOpenAI
from loguru import logger
from typing import List, Dict, Optional
import json

from app.config import get_settings, SYSTEM_PROMPT


class AIService:
    """Servicio de IA con DeepSeek"""
    
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=settings.google_api_key,
            base_url=settings.ai_base_url
        )
        self.model = settings.ai_model
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Dict = None
    ) -> str:
        """Genera respuesta del chatbot"""
        try:
            messages = self._build_messages(user_message, conversation_history, context)
            
            logger.debug(f"🤖 Enviando a DeepSeek...")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            logger.debug(f"✅ Respuesta: {ai_response[:100]}...")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error AI: {e}")
            return "Disculpa, tuve un problema técnico 🔧 ¿Podrías repetir tu mensaje?"
    
    def _build_messages(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Dict = None
    ) -> List[Dict[str, str]]:
        """Construye mensajes para la API"""
        
        system_content = SYSTEM_PROMPT
        
        if context and context.get("name"):
            system_content += f"\n\nEl cliente se llama: {context['name']}"
        
        messages = [{"role": "system", "content": system_content}]
        
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def analyze_intent(self, message: str) -> Dict:
        """Analiza intención del mensaje"""
        try:
            prompt = f"""Analiza este mensaje y responde SOLO JSON:
Mensaje: "{message}"

{{"intent": "saludo|consulta_servicio|consulta_precio|objecion|interes|despedida|otro",
"service": "desarrollo_web|marketing_digital|diseno_grafico|automatizacion|redaccion|asistente_virtual|null",
"sentiment": "positivo|negativo|neutral",
"urgency": "alta|media|baja"}}"""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            if "```" in result:
                result = result.split("```")[1].replace("json", "").strip()
            
            return json.loads(result)
            
        except Exception as e:
            logger.error(f"Error intent: {e}")
            return {"intent": "otro", "service": None, "sentiment": "neutral", "urgency": "baja"}


_ai_service: Optional[AIService] = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
