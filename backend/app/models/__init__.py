"""Models module - Pydantic schemas"""
from app.models.conversation import Conversation, Message
from app.models.lead import Lead, LeadScore
from app.models.webhook import WhatsAppWebhook, WebhookMessage
