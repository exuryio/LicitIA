# LicitIA - Radar de Oportunidades

MVP SaaS para detectar y alertar sobre licitaciones públicas de interventoría vial en Colombia.

## 🎯 Descripción

LicitIA es una plataforma que:
- Detecta automáticamente licitaciones públicas del SECOP (últimos 60 días)
- Hace matching inteligente con la experiencia previa de la empresa
- Filtra licitaciones que coinciden con el historial de proyectos (score ≥ 60%)
- Envía alertas por email y WhatsApp a empresas suscritas (opcional)

## 🏗️ Arquitectura

- **Backend**: FastAPI (Python 3.11+)
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy 2.x + Alembic
- **Jobs en background**: APScheduler
- **Frontend**: React + Vite + TypeScript
- **Containerización**: Docker Compose

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Cuenta de OpenAI (para clasificación)
- (Opcional) Token de Socrata para SECOP API
- (Opcional) Credenciales SMTP para emails
- (Opcional) WhatsApp Cloud API credentials

## 🚀 Inicio Rápido

### 1. Configurar Variables de Entorno

Copia el archivo de ejemplo y completa las variables:

```bash
cp .env.example .env
```

Edita `.env` y completa:
- `SECOP_DATASET_ID`: ID del dataset de SECOP en datos.gov.co
- `OPENAI_API_KEY`: Tu clave de API de OpenAI
- `SMTP_USER` y `SMTP_PASSWORD`: Para enviar emails (opcional)
- Otras configuraciones según necesites

### 2. Ejecutar con Docker Compose

```bash
docker-compose -f docker/docker-compose.yml up --build
```

Esto iniciará:
- PostgreSQL en el puerto 5432
- Backend API en http://localhost:8000
- Frontend en http://localhost:3000

### 3. Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 📁 Estructura del Proyecto

```
Licitia/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Endpoints FastAPI
│   │   ├── core/            # Configuración (DB, logging, scheduler)
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── services/        # Lógica de negocio
│   │   └── tests/           # Tests
│   ├── alembic/             # Migraciones de base de datos
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/             # Cliente API
│   │   ├── components/     # Componentes React
│   │   └── pages/          # Páginas
│   ├── package.json
│   └── Dockerfile
├── docker/
│   └── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Desarrollo Local (sin Docker)

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env con DATABASE_URL apuntando a PostgreSQL local

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 📊 Base de Datos

### Crear Migración

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Modelos Principales

- **Tender**: Licitaciones detectadas del SECOP
- **Subscription**: Empresas suscritas para recibir alertas

## 🔄 Flujo de Trabajo

1. **Job periódico** (cada 2 horas por defecto):
   - `fetch_and_store_new_tenders()` se ejecuta automáticamente
   - Obtiene nuevas licitaciones del SECOP
   - Clasifica relevancia con OpenAI
   - Envía notificaciones a suscripciones activas

2. **API REST**:
   - `GET /api/v1/tenders`: Listar licitaciones con filtros
   - `GET /api/v1/tenders/{id}`: Detalle de licitación
   - `POST /api/v1/subscriptions`: Crear suscripción
   - `GET /api/v1/subscriptions`: Listar suscripciones

3. **Frontend**:
   - Dashboard con tabla de licitaciones
   - Filtros por fecha, departamento, relevancia
   - Enlaces directos a procesos en SECOP

## 🧪 Tests

```bash
cd backend
pytest app/tests/
```

## 🔐 Seguridad (MVP)

Para el MVP, la autenticación es opcional. Si configuras `API_KEY` en `.env`, puedes agregar middleware para proteger endpoints de escritura.

## 📝 Notas Importantes

- **SECOP Dataset**: Necesitas encontrar el dataset correcto en datos.gov.co y ajustar los nombres de campos en `secop_client.py` según el esquema real.
- **OpenAI**: Se usa `gpt-4o-mini` por defecto (modelo económico). Ajusta `OPENAI_MODEL_NAME` si prefieres otro.
- **Clasificación**: Si OpenAI falla, se usa un fallback basado en palabras clave.
- **Notificaciones**: Email y WhatsApp son opcionales. Si no configuras credenciales, simplemente se omiten.

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL esté corriendo
- Revisa `DATABASE_URL` en `.env`

### Error al obtener datos de SECOP
- Verifica `SECOP_DATASET_ID` en `.env`
- Revisa los nombres de campos en `secop_client.py` - pueden variar según el dataset

### Frontend no se conecta al backend
- Verifica que el backend esté corriendo en puerto 8000
- Revisa la configuración de proxy en `vite.config.ts`

## 📚 Próximos Pasos

- [ ] Autenticación completa (JWT)
- [ ] Panel de administración
- [ ] Más filtros y búsqueda avanzada
- [ ] Exportación de datos (CSV, Excel)
- [ ] Dashboard con estadísticas
- [ ] Webhooks para integraciones

## 📄 Licencia

Este es un proyecto MVP. Úsalo como base para tu desarrollo.

