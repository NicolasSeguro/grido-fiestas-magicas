# Datos Necesarios para Deploy en Railway

**Fecha:** Diciembre 2024

---

## ✅ Lo que Ya Está Listo

- ✅ Archivos de configuración creados:
  - `railway.json` (raíz)
  - `grido_front/railway.json` (frontend)
  - `grido-backend/worker/nixpacks.toml` (worker)
- ✅ Código preparado para Railway
- ✅ Worker configurado para funcionar sin GPU

---

## 📋 Datos que Necesito de Ti

### 1. API Keys y Credenciales

#### ✅ Ya Tienes (Verificar que funcionen):
- [ ] **ELEVENLABS_API_KEY** - Para TTS (voz de Papá Noel)
- [ ] **SYNCLABS_API_KEY** - Para lip-sync externo
- [ ] **HIGGSFIELD_API_KEY_ID** - Para video completo
- [ ] **HIGGSFIELD_API_KEY_SECRET** - Para video completo
- [ ] **HEYGEN_API_KEY** - Para video completo (opcional)

#### ⚠️ Necesitas Crear/Configurar:

**1. RESEND_API_KEY** (Para envío de emails)
- [ ] Crear cuenta: https://resend.com/signup
- [ ] Ir a API Keys → Create API Key
- [ ] Copiar la key (empieza con `re_`)

**2. Cloudflare R2** (Para storage de videos)
- [ ] Crear cuenta: https://dash.cloudflare.com/sign-up
- [ ] Ir a R2 → Create bucket
- [ ] Nombre del bucket: `grido-papa-noel-videos`
- [ ] Ir a R2 → Manage R2 API Tokens → Create API Token
- [ ] Copiar:
  - [ ] `AWS_ACCESS_KEY_ID`
  - [ ] `AWS_SECRET_ACCESS_KEY`
  - [ ] `AWS_ENDPOINT_URL` (de Settings del bucket, ej: `https://xxx.r2.cloudflarestorage.com`)

---

## 🚀 Pasos para el Deploy

### Paso 1: Crear Cuentas (si no las tienes)

**Railway:**
1. Ir a: https://railway.app/signup
2. Conectar con GitHub
3. Autorizar acceso al repositorio

**Resend:**
1. Ir a: https://resend.com/signup
2. Verificar email
3. Obtener API key

**Cloudflare:**
1. Ir a: https://dash.cloudflare.com/sign-up
2. Verificar email
3. Crear bucket R2
4. Crear API token

---

### Paso 2: Preparar Repositorio

```bash
# Verificar que los archivos estén commiteados
git status
git add railway.json grido_front/railway.json grido-backend/worker/nixpacks.toml
git commit -m "Agregar configuración para Railway"
git push
```

---

### Paso 3: Crear Proyecto en Railway

1. **Ir a Railway Dashboard:**
   - https://railway.app/dashboard
   - Click en "New Project"

2. **Deploy from GitHub:**
   - Seleccionar "Deploy from GitHub repo"
   - Seleccionar `grido-fiestas-magicas`
   - Click en "Deploy Now"

---

### Paso 4: Crear Servicios en Railway

Te guiaré paso a paso cuando tengas las credenciales listas.

---

## 📝 Variables de Entorno Necesarias

### Frontend Service:

```
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx
VIDEO_API_SECRET=tu-secreto-seguro-aqui
NODE_ENV=production
```

**Nota:** Si usas Railway Redis, puedes usar variables automáticas.

### Worker Service:

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

# Lip-sync (API externa)
SYNCLABS_API_KEY=xxx
DISABLE_MUSETALK=true
DISABLE_WAV2LIP=true

# Video providers (opcionales)
HIGGSFIELD_API_KEY_ID=xxx
HIGGSFIELD_API_KEY_SECRET=xxx
HEYGEN_API_KEY=xxx
```

---

## ✅ Checklist de Preparación

**Cuentas:**
- [ ] Railway (conectar GitHub)
- [ ] Resend (obtener API key)
- [ ] Cloudflare (crear bucket R2, obtener credenciales)

**API Keys:**
- [ ] RESEND_API_KEY
- [ ] Cloudflare R2: AWS_ACCESS_KEY_ID
- [ ] Cloudflare R2: AWS_SECRET_ACCESS_KEY
- [ ] Cloudflare R2: AWS_ENDPOINT_URL
- [ ] Verificar que las demás API keys funcionen

**Repositorio:**
- [ ] Archivos de configuración commiteados
- [ ] Push a GitHub

---

## 🎯 Una Vez que Tengas Todo

**Dime cuando tengas:**
1. ✅ Cuenta en Railway creada
2. ✅ RESEND_API_KEY
3. ✅ Credenciales de Cloudflare R2 (3 valores)
4. ✅ Repositorio pusheado

**Y te guío paso a paso para:**
- Crear los servicios en Railway
- Configurar las variables de entorno
- Hacer el deploy completo
- Verificar que todo funcione

---

## 💡 Alternativa: Usar Railway Redis

Si prefieres usar Railway Redis en lugar de Upstash:

**Ventajas:**
- ✅ Incluido en Railway
- ✅ Más fácil de configurar
- ✅ Variables automáticas

**Desventajas:**
- ⚠️ Puede ser más caro en alto volumen

**Para usar Railway Redis:**
- No necesitas `UPSTASH_REDIS_REST_URL` y `UPSTASH_REDIS_REST_TOKEN`
- Railway expone `REDIS_URL` automáticamente
- El worker usa `REDIS_URL` directamente

---

**¿Tienes alguna pregunta sobre las credenciales o el proceso?** 🤔

