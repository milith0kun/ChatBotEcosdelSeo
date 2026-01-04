# 🤖 ChatBot WhatsApp - Ecos del SEO

Sistema de chatbot inteligente para WhatsApp con IA (DeepSeek) para automatizar ventas.

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno

Edita `backend/.env`:

```env
DEEPSEEK_API_KEY=tu-api-key-de-deepseek
MONGODB_URL=tu-url-de-mongodb-atlas
```

### 2. Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 3. Ejecutar el Servidor

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Probar el ChatBot

**Opción A - Script interactivo:**
```bash
python test_chat.py
```

**Opción B - API directa:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/test" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola","phone_number":"51999888777","name":"Test"}'
```

**Opción C - Documentación interactiva:**
Abre en el navegador: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
ChatBotEcosdelSeo/
├── backend/
│   ├── app/
│   │   ├── config.py          # Configuración y prompts
│   │   ├── main.py            # FastAPI entry point
│   │   ├── database/          # MongoDB connection
│   │   ├── models/            # Pydantic schemas
│   │   ├── routes/            # API endpoints
│   │   └── services/          # Lógica de negocio
│   ├── .env                   # Variables de entorno
│   ├── requirements.txt       # Dependencias
│   └── test_chat.py           # Script de prueba
└── docker/
    ├── docker-compose.yml     # Para Evolution API
    └── .env                   # Variables Docker
```

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado del servidor |
| GET | `/docs` | Documentación Swagger |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/chat/test` | Probar chat (sin WhatsApp) |
| GET | `/api/v1/chat/history/{phone}` | Ver historial |
| POST | `/api/v1/webhook/whatsapp` | Webhook Evolution API |

## 🛠 Stack Tecnológico

- **Backend:** Python 3.11 + FastAPI
- **IA:** DeepSeek (compatible con OpenAI SDK)
- **Base de Datos:** MongoDB Atlas
- **WhatsApp:** Evolution API (próximo paso)

## 📝 Próximos Pasos

1. ✅ Backend funcionando
2. ✅ Integración con DeepSeek
3. ✅ MongoDB Atlas conectado
4. ⏳ Configurar Evolution API para WhatsApp
5. ⏳ Desplegar en AWS/VPS

## 👤 Autor

**Edmil** - Ingeniería de Sistemas, UNSAAC
