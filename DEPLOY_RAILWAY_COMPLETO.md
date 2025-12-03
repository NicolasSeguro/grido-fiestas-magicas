# 🚂 Guía Completa de Deploy en Railway - Proyecto Grido Fiestas Mágicas

**Fecha:** Diciembre 2024

---

## ⚠️ Limitación Importante: Railway NO tiene GPU

**Railway actualmente NO soporta GPU nativamente.** Esto significa:

- ✅ **SÍ puedes deployar:** Frontend, Worker (sin GPU), Redis, Storage
- ❌ **NO puedes deployar:** Worker con GPU (MuseTalk/Wav2Lip local)
- ✅ **Alternativa:** Usar servicios externos (Sync Labs API) para lip-sync

---

## 🏗️ Arquitectura en Railway

### Opción 1: Todo en Railway (Sin GPU) ⭐ RECOMENDADA

```
┌─────────────────────────────────────────┐
│         RAILWAY (Frontend)               │
│  ✅ Next.js App                          │
│  ✅ API Routes                           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      RAILWAY REDIS (Queue)              │
│  ✅ Redis incluido                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      RAILWAY (Worker SIN GPU)           │
│  ✅ Procesamiento de video              │
│  ✅ Estrategia 3 (audio + video base)   │
│  ✅ Sync Labs API (lip-sync externo)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    RAILWAY VOLUMES (Storage)             │
│  ✅ Almacenamiento local                 │
│  O Cloudflare R2 (recomendado)          │
└─────────────────────────────────────────┘
```

**Ventajas:**
- ✅ Todo en una plataforma
- ✅ Fácil de configurar
- ✅ Redis incluido
- ✅ Deploy desde GitHub

**Desventajas:**
- ❌ Sin GPU (no puede usar MuseTalk/Wav2Lip local)
- ✅ Pero puede usar Sync Labs API (lip-sync externo)

---

## 📋 Paso 1: Preparar el Proyecto para Railway

### 1.1 Estructura del Proyecto

Railway puede deployar múltiples servicios desde un mismo repositorio:

```
grido-fiestas-magicas/
├── grido_front/              ← Servicio 1: Frontend
│   ├── package.json
│   └── ...
├── grido-backend/
│   └── worker/               ← Servicio 2: Worker
│       ├── requirements.txt
│       ├── video-worker.py
│       └── ...
└── railway.json              ← Configuración de Railway
```

### 1.2 Crear railway.json

Crea `railway.json` en la raíz del proyecto:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "echo 'No build needed'"
  },
  "deploy": {
    "startCommand": "echo 'Configured per service'",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 📋 Paso 2: Deploy del Frontend en Railway

### 2.1 Crear Proyecto en Railway

1. **Ir a Railway Dashboard:**
   - https://railway.app
   - Click en "New Project"
   - "Deploy from GitHub repo"
   - Seleccionar `grido-fiestas-magicas`

### 2.2 Crear Servicio Frontend

1. **Add Service** → **GitHub Repo**
2. **Configuración:**
   - **Root Directory:** `grido_front`
   - **Build Command:** `pnpm install && pnpm build`
   - **Start Command:** `pnpm start`
   - **Port:** `3000` (Railway lo detecta automáticamente)

### 2.3 Variables de Entorno

En Railway Dashboard → Variables:

```
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx
VIDEO_API_SECRET=tu-secreto-seguro
NODE_ENV=production
```

### 2.4 Generar Dominio

Railway genera un dominio automáticamente:
- `https://tu-proyecto-frontend.up.railway.app`

---

## 📋 Paso 3: Configurar Redis en Railway

### 3.1 Agregar Redis Service

1. En tu proyecto Railway
2. **Add Service** → **Database** → **Add Redis**
3. Railway crea automáticamente un Redis

### 3.2 Obtener Variables de Redis

Railway genera automáticamente:
- `REDIS_URL` (automático)
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

**Nota:** Railway expone estas variables automáticamente a todos los servicios del proyecto.

---

## 📋 Paso 4: Deploy del Worker en Railway

### 4.1 Crear Servicio Worker

1. **Add Service** → **GitHub Repo** (mismo repo)
2. **Configuración:**
   - **Root Directory:** `grido-backend/worker`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python video-worker.py`
   - **Python Version:** `3.11`

### 4.2 Variables de Entorno del Worker

```
# Redis (automático desde Railway Redis)
REDIS_URL=${{Redis.REDIS_URL}}

# Storage
STORAGE_TYPE=railway
# O usar R2:
STORAGE_TYPE=r2
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
S3_BUCKET=grido-papa-noel-videos
AWS_REGION=auto

# Email
RESEND_API_KEY=re_xxx

# TTS
ELEVENLABS_API_KEY=xxx

# Lip-sync (usar API externa, no local)
SYNCLABS_API_KEY=xxx
DISABLE_MUSETALK=true
DISABLE_WAV2LIP=true

# Video providers
HIGGSFIELD_API_KEY_ID=xxx
HIGGSFIELD_API_KEY_SECRET=xxx
HEYGEN_API_KEY=xxx
```

### 4.3 Configurar Volúmenes (Opcional)

Si quieres almacenar videos localmente:

1. **Add Volume** en el servicio Worker
2. **Mount Path:** `/app/storage`
3. Actualizar `LOCAL_STORAGE_PATH=/app/storage`

---

## 📋 Paso 5: Configurar Storage

### Opción A: Railway Volumes (Local)

**Ventajas:**
- ✅ Gratis
- ✅ Fácil de configurar

**Desventajas:**
- ❌ No es persistente entre deploys
- ❌ No es público (necesitas API para servir videos)

### Opción B: Cloudflare R2 (Recomendado) ⭐

**Ventajas:**
- ✅ Persistente
- ✅ URLs públicas
- ✅ Egress gratis
- ✅ CDN integrado

**Configuración:**
1. Crear bucket en Cloudflare R2
2. Crear API token
3. Agregar variables al Worker (ver Paso 4.2)

---

## 📋 Paso 6: Configurar Resend (Email)

1. Crear cuenta en Resend: https://resend.com
2. Obtener API key
3. Agregar `RESEND_API_KEY` al Worker

---

## ✅ Configuración Completa

### Servicios en Railway:

1. **Frontend Service:**
   - Root: `grido_front`
   - Build: `pnpm install && pnpm build`
   - Start: `pnpm start`

2. **Worker Service:**
   - Root: `grido-backend/worker`
   - Build: `pip install -r requirements.txt`
   - Start: `python video-worker.py`

3. **Redis Service:**
   - Automático desde Railway

### Variables de Entorno:

**Frontend:**
```
UPSTASH_REDIS_REST_URL (o usar Railway Redis)
UPSTASH_REDIS_REST_TOKEN (o usar Railway Redis)
VIDEO_API_SECRET
```

**Worker:**
```
REDIS_URL=${{Redis.REDIS_URL}}
STORAGE_TYPE=r2
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ENDPOINT_URL
S3_BUCKET
RESEND_API_KEY
ELEVENLABS_API_KEY
SYNCLABS_API_KEY
DISABLE_MUSETALK=true
DISABLE_WAV2LIP=true
```

---

## 🎯 Estrategia sin GPU

El worker funcionará con:

1. **Estrategia 1:** TTS + Sync Labs API (lip-sync externo) ✅
2. **Estrategia 2:** Higgsfield/HeyGen (video completo) ✅
3. **Estrategia 3:** TTS + Video base (sin lip-sync) ✅

**No funcionará:**
- ❌ MuseTalk local (requiere GPU)
- ❌ Wav2Lip local (requiere GPU)

**Solución:** Usar Sync Labs API para lip-sync (no requiere GPU local)

---

## 💰 Costos Estimados en Railway

### Hobby Plan ($5/mes):
- 500 horas de ejecución
- 8GB RAM
- 100GB storage
- **Ideal para:** Testing y bajo volumen

### Pro Plan ($20/mes + uso):
- Ejecución ilimitada
- Más RAM y CPU
- **Ideal para:** Producción

### Costos Adicionales:
- **Cloudflare R2:** ~$0.015/GB storage
- **Resend:** $0 (100 emails/día) o $20/mes
- **Sync Labs:** Pay-per-use (~$0.01-0.02 por video)

**Total estimado (1,000 videos/mes):**
- Railway Hobby: $5
- R2: ~$1
- Sync Labs: ~$10-20
- Resend: $0
- **Total: ~$16-26/mes**

---

## 🚀 Pasos de Deploy

### 1. Preparar Repositorio

```bash
cd /Users/nikoseguro/Documents/grido-fiestas-magicas
git add railway.json
git commit -m "Agregar configuración de Railway"
git push
```

### 2. Crear Proyecto en Railway

1. Ir a https://railway.app
2. New Project → Deploy from GitHub
3. Seleccionar repositorio

### 3. Crear Servicios

1. **Frontend Service:**
   - Root: `grido_front`
   - Configurar variables de entorno

2. **Redis Service:**
   - Add Database → Redis

3. **Worker Service:**
   - Root: `grido-backend/worker`
   - Configurar variables de entorno
   - Deshabilitar MuseTalk/Wav2Lip

### 4. Configurar Storage

- Opción A: Railway Volumes (local)
- Opción B: Cloudflare R2 (recomendado)

### 5. Deploy

Railway hace deploy automático al hacer push a `main`.

---

## 📝 Archivos Necesarios

### railway.json (raíz del proyecto)

```json
{
  "$schema": "https://railway.app/railway.schema.json"
}
```

### Procfile (opcional, para Worker)

```
worker: cd grido-backend/worker && python video-worker.py
```

### nixpacks.toml (opcional, para Worker)

```toml
[phases.setup]
nixPkgs = ["python311", "ffmpeg"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python video-worker.py"
```

---

## ⚠️ Limitaciones y Consideraciones

### Sin GPU:
- ❌ No puede usar MuseTalk local
- ❌ No puede usar Wav2Lip local
- ✅ Puede usar Sync Labs API (lip-sync externo)
- ✅ Puede usar Estrategia 3 (sin lip-sync perfecto)

### Alternativas:
1. **Usar Sync Labs API** (recomendado) - Lip-sync externo, no requiere GPU
2. **Usar servicios de video completo** (Higgsfield/HeyGen) - No requiere GPU local
3. **Estrategia 3** - Funciona sin GPU, sin lip-sync perfecto

---

## 🆚 Comparación: Railway vs Vercel + Modal

| Aspecto | Railway | Vercel + Modal |
|---------|---------|----------------|
| **Frontend** | ✅ Sí | ✅ Sí |
| **Worker sin GPU** | ✅ Sí | ✅ Sí (pero no recomendado) |
| **Worker con GPU** | ❌ No | ✅ Sí (Modal) |
| **Redis** | ✅ Incluido | ⚠️ Upstash (separado) |
| **Todo en uno** | ✅ Sí | ❌ No |
| **Costo (bajo volumen)** | $5-20/mes | $0-10/mes |
| **Costo (alto volumen)** | $20-50/mes | $20-70/mes |
| **Complejidad** | Media | Alta |

---

## 💡 Recomendación

**Para Railway:**
- ✅ Usa si quieres todo en una plataforma
- ✅ Usa si no necesitas GPU local (puedes usar Sync Labs API)
- ✅ Usa si prefieres simplicidad

**Para Vercel + Modal:**
- ✅ Usa si necesitas GPU local (MuseTalk/Wav2Lip)
- ✅ Usa si quieres mejor escalabilidad
- ✅ Usa si prefieres pay-per-use

---

## ✅ Checklist de Deploy

- [ ] Proyecto creado en Railway
- [ ] Frontend service configurado
- [ ] Redis service agregado
- [ ] Worker service configurado
- [ ] Variables de entorno configuradas
- [ ] Storage configurado (R2 o Volumes)
- [ ] Resend configurado
- [ ] Sync Labs API key configurada
- [ ] MuseTalk/Wav2Lip deshabilitados
- [ ] Deploy exitoso
- [ ] Prueba end-to-end

---

## 🚀 Comandos Útiles

### Ver Logs
```bash
railway logs
```

### Ver Variables
```bash
railway variables
```

### Deploy Manual
```bash
railway up
```

---

**Railway puede deployar todo el proyecto, pero sin GPU local. Usa Sync Labs API para lip-sync.** ✅

