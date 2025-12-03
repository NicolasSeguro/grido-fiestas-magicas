# 🚀 Guía Completa de Deploy en Vercel - Proyecto Grido Fiestas Mágicas

**Fecha:** Diciembre 2024

---

## ✅ ¿Qué se puede deployar en Vercel?

### ✅ SÍ va a Vercel:
- **Frontend Next.js** (`grido_front/`)
- **API Routes** (`grido_front/src/app/api/`)
- **Assets estáticos** (imágenes, videos, etc.)

### ❌ NO va a Vercel:
- **Worker Python** (`grido-backend/worker/`) - Necesita GPU, va a **Modal**
- **Dependencias Python** - Se instalan en Modal
- **Modelos de IA** - Se descargan en Modal

---

## 🏗️ Arquitectura Completa

```
┌─────────────────────────────────────────┐
│         VERCEL (Frontend)                │
│  ✅ Next.js App                          │
│  ✅ API Route (/api/generate-video)      │
│  ✅ Variables de entorno                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      UPSTASH REDIS (Queue)              │
│  ✅ Cola de trabajos                    │
│  ✅ Serverless Redis                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         MODAL (Worker GPU)              │
│  ✅ Procesamiento de video              │
│  ✅ Lip-sync (MuseTalk)                 │
│  ✅ GPU serverless                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    CLOUDFLARE R2 (Storage)              │
│  ✅ Almacenamiento de videos            │
│  ✅ URLs públicas                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         RESEND (Email)                  │
│  ✅ Envío de emails                     │
└─────────────────────────────────────────┘
```

---

## 📋 Paso 1: Deploy del Frontend en Vercel

### 1.1 Preparar el Repositorio

```bash
cd /Users/nikoseguro/Documents/grido-fiestas-magicas
git status
git add -A
git commit -m "Preparar para deploy en Vercel"
git push
```

### 1.2 Crear Proyecto en Vercel

1. **Ir a Vercel Dashboard:**
   - https://vercel.com/dashboard
   - Click en "Add New..." → "Project"

2. **Importar Repositorio:**
   - Selecciona: `grido-fiestas-magicas`
   - Click en "Import"

3. **⚠️ CONFIGURACIÓN CRÍTICA:**
   
   - **Framework Preset:** Next.js (auto-detectado)
   - **Root Directory:** `grido_front` ⚠️ **ESTO ES CRÍTICO**
   - **Build Command:** `pnpm build`
   - **Output Directory:** `.next`
   - **Install Command:** `pnpm install`

4. **Variables de Entorno:**
   
   En "Environment Variables", agrega:
   
   ```
   UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
   UPSTASH_REDIS_REST_TOKEN=xxx
   VIDEO_API_SECRET=tu-secreto-seguro-aqui
   ```

5. **Deploy:**
   - Click en "Deploy"
   - Espera a que termine (2-3 minutos)

### 1.3 Verificar Deploy

- URL: `https://tu-proyecto.vercel.app`
- Verifica que la página carga
- Prueba el formulario

---

## 📋 Paso 2: Configurar Upstash Redis

### 2.1 Crear Cuenta

1. Ir a: https://console.upstash.com/register
2. Crear cuenta (gratis)
3. Crear database:
   - **Name:** `grido-queue`
   - **Type:** Redis
   - **Region:** Más cercana a tus usuarios
   - **Tier:** Free (10,000 comandos/día)

### 2.2 Obtener Credenciales

- Copiar `UPSTASH_REDIS_REST_URL`
- Copiar `UPSTASH_REDIS_REST_TOKEN`

### 2.3 Agregar a Vercel

En Vercel → Settings → Environment Variables:
- Agregar ambas variables
- **Redeploy** el proyecto

---

## 📋 Paso 3: Configurar Modal (Worker GPU)

### 3.1 Crear Cuenta

1. Ir a: https://modal.com/signup
2. Crear cuenta (requiere tarjeta)
3. Instalar CLI:
   ```bash
   pip install modal
   modal token new
   ```

### 3.2 Verificar Worker

```bash
cd grido-backend/worker
ls -la modal_worker.py
```

### 3.3 Configurar Secretos

En Modal Dashboard → Secrets → Create Secret:

**Nombre:** `grido-secrets`

**Variables:**
```
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx
REDIS_URL=redis://default:xxx@xxx.upstash.io:6379

AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
S3_BUCKET=grido-papa-noel-videos
AWS_REGION=auto

RESEND_API_KEY=re_xxx

ELEVENLABS_API_KEY=xxx
SYNCLABS_API_KEY=xxx
HIGGSFIELD_API_KEY_ID=xxx
HIGGSFIELD_API_KEY_SECRET=xxx
```

### 3.4 Deploy Worker

```bash
cd grido-backend/worker
modal deploy modal_worker.py
```

---

## 📋 Paso 4: Configurar Cloudflare R2

### 4.1 Crear Bucket

1. Ir a: https://dash.cloudflare.com
2. R2 → Create bucket
3. **Nombre:** `grido-papa-noel-videos`

### 4.2 Crear API Token

1. R2 → Manage R2 API Tokens
2. Create API Token
3. Permisos: Object Read & Write
4. Copiar credenciales

### 4.3 Agregar a Modal

Agregar a `grido-secrets`:
```
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
S3_BUCKET=grido-papa-noel-videos
AWS_REGION=auto
```

---

## 📋 Paso 5: Configurar Resend

### 5.1 Crear Cuenta

1. Ir a: https://resend.com/signup
2. Crear cuenta (gratis: 100 emails/día)
3. Obtener API key

### 5.2 Agregar a Modal

Agregar a `grido-secrets`:
```
RESEND_API_KEY=re_xxx
```

---

## ✅ Checklist Final

- [ ] Frontend deployado en Vercel
- [ ] Variables de entorno en Vercel
- [ ] Upstash Redis configurado
- [ ] Modal worker deployado
- [ ] Secretos en Modal configurados
- [ ] Cloudflare R2 bucket creado
- [ ] Resend API key configurada

---

## 🧪 Probar el Sistema

1. **Abrir landing:** `https://tu-proyecto.vercel.app`
2. **Completar formulario:** Llenar y enviar
3. **Monitorear:**
   - Logs en Vercel (API call)
   - Logs en Modal (procesamiento)
4. **Verificar email:** Debe llegar con link al video

---

## 💰 Costos Estimados

**Free Tier (1,000 videos/mes):**
- Vercel: $0
- Upstash: $0
- Modal: ~$1-2
- R2: ~$1
- Resend: $0
- **Total: ~$2-3/mes**

**Pro Tier (10,000 videos/mes):**
- Vercel: $20
- Upstash: $0-5
- Modal: ~$10-20
- R2: ~$5
- Resend: $20
- **Total: ~$55-70/mes**

---

## 🚀 Comandos Rápidos

### Deploy Frontend (Vercel)
```bash
# Desde la raíz del proyecto
cd grido_front
vercel
```

### Deploy Worker (Modal)
```bash
cd grido-backend/worker
modal deploy modal_worker.py
```

### Ver Logs
```bash
# Vercel
vercel logs

# Modal
modal app logs grido-video-worker
```

---

## 📝 Resumen

**✅ SÍ en Vercel:**
- Frontend Next.js
- API Routes
- Variables de entorno del frontend

**❌ NO en Vercel:**
- Worker Python (va a Modal)
- GPU processing (va a Modal)
- Storage de videos (va a R2)

**El proyecto completo funciona con:**
- Vercel (frontend) + Modal (worker) + Upstash (queue) + R2 (storage) + Resend (email)

---

**¿Listo para hacer el deploy?** Empieza con el Paso 1 (Frontend en Vercel). ✅
