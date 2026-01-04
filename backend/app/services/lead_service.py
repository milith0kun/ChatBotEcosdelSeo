"""
Lead Service - Gestión de leads y scoring
"""
from datetime import datetime
from typing import Optional, Dict
from loguru import logger
from bson import ObjectId

from app.database.mongodb import get_database


class LeadService:
    """Servicio para gestionar leads"""
    
    def __init__(self):
        self.db = None
    
    def _get_db(self):
        if self.db is None:
            self.db = get_database()
        return self.db
    
    async def get_or_create_lead(self, phone_number: str, name: str = None) -> Dict:
        """Obtiene o crea un lead"""
        db = self._get_db()
        
        lead = await db.leads.find_one({"phone_number": phone_number})
        
        if lead:
            lead["_id"] = str(lead["_id"])
            return lead
        
        new_lead = {
            "phone_number": phone_number,
            "name": name,
            "score": {"budget": 0, "urgency": 0, "authority": 0, "need": 0},
            "status": "new",
            "services_interested": [],
            "source": "whatsapp",
            "notes": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.leads.insert_one(new_lead)
        new_lead["_id"] = str(result.inserted_id)
        
        logger.info(f"🎯 Nuevo lead creado: {phone_number}")
        return new_lead
    
    async def update_score(self, phone_number: str, score: Dict) -> Dict:
        """Actualiza el score del lead"""
        db = self._get_db()
        
        # Calcular total y clasificación
        total = sum(score.values())
        classification = "hot" if total >= 80 else "warm" if total >= 50 else "cold"
        
        result = await db.leads.find_one_and_update(
            {"phone_number": phone_number},
            {
                "$set": {
                    "score": score,
                    "score_total": total,
                    "classification": classification,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
        
        if result:
            logger.info(f"📊 Lead {phone_number} actualizado: {classification} ({total})")
            result["_id"] = str(result["_id"])
        
        return result
    
    async def add_service_interest(self, phone_number: str, service: str):
        """Agrega un servicio de interés"""
        db = self._get_db()
        
        await db.leads.update_one(
            {"phone_number": phone_number},
            {
                "$addToSet": {"services_interested": service},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    async def get_hot_leads(self, limit: int = 10) -> list:
        """Obtiene leads calientes"""
        db = self._get_db()
        
        cursor = db.leads.find(
            {"classification": "hot"}
        ).sort("updated_at", -1).limit(limit)
        
        leads = []
        async for lead in cursor:
            lead["_id"] = str(lead["_id"])
            leads.append(lead)
        
        return leads


_lead_service: Optional[LeadService] = None

def get_lead_service() -> LeadService:
    global _lead_service
    if _lead_service is None:
        _lead_service = LeadService()
    return _lead_service
