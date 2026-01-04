"""
Modelos de Lead
===============
Esquemas para calificación y gestión de leads
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from bson import ObjectId


class LeadScore(BaseModel):
    """Puntuación detallada del lead"""
    budget: int = Field(default=0, ge=0, le=25)  # ¿Tiene presupuesto?
    urgency: int = Field(default=0, ge=0, le=25)  # ¿Urgencia del proyecto?
    authority: int = Field(default=0, ge=0, le=25)  # ¿Puede tomar decisiones?
    need: int = Field(default=0, ge=0, le=25)  # ¿Necesidad real del servicio?
    
    @property
    def total(self) -> int:
        """Puntuación total (0-100)"""
        return self.budget + self.urgency + self.authority + self.need
    
    @property
    def classification(self) -> Literal["hot", "warm", "cold"]:
        """Clasificación del lead basada en puntuación"""
        total = self.total
        if total >= 80:
            return "hot"
        elif total >= 50:
            return "warm"
        return "cold"


class Lead(BaseModel):
    """Modelo completo de un lead"""
    id: Optional[str] = Field(default=None, alias="_id")
    phone_number: str
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    
    # Scoring
    score: LeadScore = Field(default_factory=LeadScore)
    
    # Estado
    status: Literal["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"] = "new"
    
    # Intereses
    services_interested: List[str] = []
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    
    # Fuente
    source: str = "whatsapp"
    campaign: Optional[str] = None
    
    # Notas
    notes: List[str] = []
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_contact_at: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class LeadUpdate(BaseModel):
    """Modelo para actualización parcial de lead"""
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    score: Optional[LeadScore] = None
    status: Optional[str] = None
    services_interested: Optional[List[str]] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    notes: Optional[List[str]] = None
