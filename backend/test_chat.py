"""
Script de prueba del ChatBot
Ejecutar: python test_chat.py
"""
import asyncio
import httpx

API_URL = "http://localhost:8000/api/v1/chat/test"

async def chat(message: str, phone: str = "51999888777", name: str = "Usuario"):
    """Envía un mensaje al chatbot"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            API_URL,
            json={
                "message": message,
                "phone_number": phone,
                "name": name
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["response"]
        else:
            return f"Error: {response.text}"


async def main():
    print("=" * 60)
    print("🤖 CHATBOT ECOS DEL SEO - Modo de Prueba")
    print("=" * 60)
    print("Escribe 'salir' para terminar\n")
    
    name = input("Tu nombre: ").strip() or "Usuario"
    phone = "51999888777"
    
    print(f"\n¡Hola {name}! Escribe tu mensaje:\n")
    
    while True:
        user_input = input("Tú: ").strip()
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("\n👋 ¡Hasta luego!")
            break
        
        if not user_input:
            continue
        
        print("⏳ Pensando...")
        response = await chat(user_input, phone, name)
        print(f"\n🤖 Bot: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
