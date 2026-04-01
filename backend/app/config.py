"""
Configuración centralizada del ChatBot
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # App Info
    app_name: str = "ChatBot Ecos del SEO"
    app_version: str = "1.0.0"
    debug: bool = False

    # AI Configuration (Gemini / OpenAI compatible)
    google_api_key: str
    ai_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    ai_model: str = "gemini-1.5-flash"

    # MongoDB Atlas
    mongodb_uri: str
    mongodb_db_name: str = "ecos_chatbot"

    # Admin y Seguridad
    jwt_secret: str = "ecos-del-seo-chatbot-secret-2026"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    admin_email: str = "admin@ecosdelseo.com"
    admin_password: str = "admin123456"
    frontend_url: str = "https://ecodelseo.com"

    # Evolution API
    evolution_api_url: str = "http://localhost:8080"
    evolution_api_key: str = "default-key"
    evolution_instance_name: str = "ecos_whatsapp"
    
    # Chatbot Settings
    max_context_messages: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Servicios de Ecos del SEO
SERVICIOS_ECOS = {
    "desarrollo_web": {
        "nombre": "Desarrollo Web",
        "descripcion": "Sitios web profesionales, landing pages y tiendas online",
        "precio_desde": "$500 USD"
    },
    "marketing_digital": {
        "nombre": "Marketing Digital (SEO/SEM)",
        "descripcion": "Posicionamiento en buscadores, Google Ads y Meta Ads",
        "precio_desde": "$300 USD/mes"
    },
    "diseno_grafico": {
        "nombre": "Diseño Gráfico",
        "descripcion": "Logos, identidad corporativa, material publicitario",
        "precio_desde": "$150 USD"
    },
    "automatizacion": {
        "nombre": "Automatización",
        "descripcion": "Chatbots, CRM, automatización de procesos",
        "precio_desde": "$400 USD"
    },
    "redaccion": {
        "nombre": "Redacción de Contenido",
        "descripcion": "Artículos SEO, copywriting, contenido redes sociales",
        "precio_desde": "$50 USD/artículo"
    },
    "asistente_virtual": {
        "nombre": "Asistente Virtual",
        "descripcion": "Gestión administrativa, atención al cliente",
        "precio_desde": "$200 USD/mes"
    }
}


SYSTEM_PROMPT = """Eres el asistente de ventas de Ecos del SEO, una agencia de marketing digital en Cusco, Perú.

Tu personalidad:
- Profesional pero amigable y cercano
- Entusiasta sobre marketing digital
- Empático con las necesidades del cliente
- Usas español latinoamericano natural
- Usas emojis ocasionalmente de forma profesional 🚀

Objetivos:
1. Dar bienvenida cálida
2. Entender necesidades del cliente
3. Presentar servicios relevantes
4. Calificar leads (presupuesto, urgencia, autoridad, necesidad)
5. Agendar consultas gratuitas de 30 minutos

Servicios:
1. Desarrollo Web - Desde $500
2. Marketing Digital (SEO/SEM) - Desde $300/mes
3. Diseño Gráfico - Desde $150
4. Automatización - Desde $400
5. Redacción de Contenido - Desde $50/artículo
6. Asistente Virtual - Desde $200/mes

Reglas:
- Respuestas concisas (máximo 3-4 oraciones)
- Siempre termina con pregunta o llamado a la acción
- Ofrece auditoría SEO gratuita como gancho
- Si no sabes algo, ofrece conectar con humano
- NO inventes información sobre la empresa
"""
