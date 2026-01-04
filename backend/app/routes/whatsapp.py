"""
WhatsApp Management Endpoints
"""
from fastapi import APIRouter, HTTPException
from loguru import logger
import httpx

from app.config import get_settings

router = APIRouter()


@router.post("/create-instance")
async def create_instance():
    """Crea una nueva instancia de WhatsApp"""
    settings = get_settings()
    
    url = f"{settings.evolution_api_url}/instance/create"
    headers = {"apikey": settings.evolution_api_key, "Content-Type": "application/json"}
    
    payload = {
        "instanceName": settings.evolution_instance_name,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 201 or response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Instancia creada: {settings.evolution_instance_name}")
                return {
                    "status": "success",
                    "instance": settings.evolution_instance_name,
                    "qrcode": data.get("qrcode", {}).get("base64"),
                    "message": "Escanea el QR con WhatsApp para conectar"
                }
            else:
                return {"status": "error", "detail": response.text}
                
    except Exception as e:
        logger.error(f"Error creando instancia: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/qr-code")
async def get_qr_code():
    """Obtiene el código QR para conectar WhatsApp"""
    settings = get_settings()
    
    url = f"{settings.evolution_api_url}/instance/connect/{settings.evolution_instance_name}"
    headers = {"apikey": settings.evolution_api_key}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                qr_base64 = data.get("base64")
                
                if qr_base64:
                    return {
                        "status": "waiting_qr",
                        "qrcode_base64": qr_base64,
                        "message": "Escanea este QR con WhatsApp"
                    }
                else:
                    return {
                        "status": "connected",
                        "message": "WhatsApp ya está conectado"
                    }
            else:
                return {"status": "error", "detail": response.text}
                
    except Exception as e:
        logger.error(f"Error obteniendo QR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_connection_status():
    """Obtiene el estado de conexión de WhatsApp"""
    settings = get_settings()
    
    url = f"{settings.evolution_api_url}/instance/connectionState/{settings.evolution_instance_name}"
    headers = {"apikey": settings.evolution_api_key}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "instance": settings.evolution_instance_name,
                    "state": data.get("state", "unknown"),
                    "connected": data.get("state") == "open"
                }
            else:
                return {"status": "error", "detail": response.text}
                
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/logout")
async def logout_instance():
    """Desconecta WhatsApp"""
    settings = get_settings()
    
    url = f"{settings.evolution_api_url}/instance/logout/{settings.evolution_instance_name}"
    headers = {"apikey": settings.evolution_api_key}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(url, headers=headers)
            return {"status": "disconnected", "detail": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
