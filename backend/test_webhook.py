"""
Simulador de Webhook de Evolution API
=====================================
Simula un mensaje entrante de WhatsApp para probar el backend sin necesitar un teléfono real.
"""
import asyncio
import httpx
import json

WEBHOOK_URL = "http://localhost:8000/api/v1/webhook/whatsapp"

# Payload de ejemplo de Evolution API (versión simplificada)
SAMPLE_PAYLOAD = {
    "event": "messages.upsert",
    "instance": "ecos_whatsapp",
    "data": {
        "key": {
            "remoteJid": "51999888777@s.whatsapp.net",
            "fromMe": False,
            "id": "TestMessage123"
        },
        "pushName": "Cliente de Prueba",
        "message": {
            "conversation": "Hola, me interesa el servicio de desarrollo web"
        },
        "messageTimestamp": 1675200000
    },
    "destination": "51900000000@s.whatsapp.net",
    "date_time": "2025-01-01T12:00:00.000Z",
    "sender": "51999888777@s.whatsapp.net"
}

async def simulate_webhook():
    print(f"📡 Enviando webhook simulado a: {WEBHOOK_URL}")
    print(f"📝 Mensaje: {SAMPLE_PAYLOAD['data']['message']['conversation']}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(WEBHOOK_URL, json=SAMPLE_PAYLOAD)
            
            if response.status_code == 200:
                print("\n✅ Webhook recibido correctamente por el backend.")
                print("🔍 Revisa los logs del backend para ver la respuesta generada.")
            else:
                print(f"\n❌ Error {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_webhook())
