# Checklist de Deploy en Railway - Datos Necesarios

**Fecha:** Diciembre 2024

---

## 📋 Datos que Necesito de Ti

### 1. API Keys y Credenciales (Ya tienes algunas)

#### ✅ Ya Configuradas (verificar que funcionen):
- [ ] **ELEVENLABS_API_KEY** - Para TTS (voz de Papá Noel)
- [ ] **SYNCLABS_API_KEY** - Para lip-sync externo (no requiere GPU)
- [ ] **HIGGSFIELD_API_KEY_ID** - Para video completo
- [ ] **HIGGSFIELD_API_KEY_SECRET** - Para video completo
- [ ] **HEYGEN_API_KEY** - Para video completo (opcional, puede no funcionar)

#### ⚠️ Necesitas Crear/Configurar:
- [ ] **RESEND_API_KEY** - Para envío de emails
  - Crear cuenta: https://resend.com/signup
  - Obtener API key del dashboard

- [ ] **Cloudflare R2 Credenciales** (para storage de videos)
  - AWS_ACCESS_KEY_ID (de R2)
  - AWS_SECRET_ACCESS_KEY (de R2)
  - AWS_ENDPOINT_URL (de R2, ej: `https://xxx.r2.cloudflarestorage.com`)
  - S3_BUCKET (nombre del bucket en R2)

---

## 🔧 Archivos de Configuración (Ya Creados)

He creado estos archivos para Railway:

1. ✅ `railway.json` (raíz del proyecto)
2. ✅ `grido-backend/worker/nixpacks.toml` (configuración del worker)
3. ✅ `grido-front/railway.json` (configuración del frontend)

---

## 📝 Variables de Entorno Necesarias

### Frontend (grido_front):

```
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx
VIDEO_API_SECRET=tu-secreto-seguro-aqui
NODE_ENV=production
```

**Nota:** Si usas Railway Redis, puedes usar las variables automáticas de Railway en lugar de Upstash.

### Worker (grido-backend/worker):

```
# Redis (automático desde Railway Redis)
REDIS_URL=${{Redis.REDIS_URL}}

# Storage (Cloudflare R2)
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

# Lip-sync (API externa, no requiere GPU)
SYNCLABS_API_KEY=xxx
DISABLE_MUSETALK=true
DISABLE_WAV2LIP=true

# Video providers (opcionales)
HIGGSFIELD_API_KEY_ID=xxx
HIGGSFIELD_API_KEY_SECRET=xxx
HEYGEN_API_KEY=xxx
```

---

## 🚀 Pasos para el Deploy

### Paso 1: Crear Cuentas (si no las tienes)

1. **Railway:**
   - https://railway.app/signup
   - Conectar con GitHub

2. **Resend:**
   - https://resend.com/signup
   - Obtener API key

3. **Cloudflare R2:**
   - https://dash.cloudflare.com/sign-up
   - Crear bucket
   - Crear API token

### Paso 2: Preparar Repositorio

```bash
# Ya está hecho, solo verificar
git status
git add railway.json grido-front/railway.json grido-backend/worker/nixpacks.toml
git commit -m "Agregar configuración para Railway"
git push
```

### Paso 3: Crear Proyecto en Railway

1. Ir a https://railway.app
2. New Project → Deploy from GitHub
3. Seleccionar `grido-fiestas-magicas`

### Paso 4: Crear Servicios

Te guiaré paso a paso cuando tengas las credenciales.

---

## ✅ Lo que Ya Está Listo

- ✅ Archivos de configuración creados
- ✅ Código preparado para Railway
- ✅ Worker configurado para funcionar sin GPU
- ✅ Sistema de fallback implementado

---

## ❓ Preguntas para Ti

1. **¿Tienes cuenta en Resend?** (para emails)
   - Si no, puedo ayudarte a crearla

2. **¿Tienes cuenta en Cloudflare?** (para R2 storage)
   - Si no, puedo ayudarte a crearla

3. **¿Prefieres usar Railway Redis o Upstash Redis?**
   - Railway Redis: Incluido, más fácil
   - Upstash Redis: Serverless, puede ser más barato

4. **¿Tienes todas las API keys listadas arriba?**
   - Verificar que funcionen

---

## 🎯 Próximo Paso

Una vez que tengas:
- ✅ Cuenta en Railway
- ✅ Cuenta en Resend (o API key)
- ✅ Cuenta en Cloudflare R2 (o credenciales)
- ✅ Todas las API keys verificadas

**Te guío paso a paso para hacer el deploy completo.** 🚀

---

## 📝 Resumen de lo que Necesito

**Cuentas:**
- [ ] Railway (conectar GitHub)
- [ ] Resend (para emails)
- [ ] Cloudflare (para R2 storage)

**API Keys:**
- [ ] RESEND_API_KEY
- [ ] Cloudflare R2 credenciales (3 valores)
- [ ] Verificar que las demás API keys funcionen

**Decisión:**
- [ ] ¿Railway Redis o Upstash Redis?

**Una vez que tengas esto, podemos hacer el deploy completo.** ✅

