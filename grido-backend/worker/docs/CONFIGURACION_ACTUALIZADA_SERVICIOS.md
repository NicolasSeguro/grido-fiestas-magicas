# Configuración Actualizada de Servicios Externos

**Fecha:** Diciembre 2024
**Estado:** Endpoints actualizados según documentación oficial

---

## 🔄 Cambios Realizados

### 1. Sync Labs - Endpoint Corregido ✅

**Problema anterior:**
- Endpoint incorrecto: `https://api.synclabs.so` (no resuelve DNS)

**Solución aplicada:**
- ✅ Endpoint actualizado a: `https://api.sync.so`
- ✅ Según documentación oficial: https://docs.sync.so

**Código actualizado:**
```python
# providers/synclabs_lipsync.py
self.api_base_url = os.getenv("SYNCLABS_API_BASE_URL", "https://api.sync.so")
```

**Endpoints utilizados:**
- Upload: `POST https://api.sync.so/v1/upload`
- Create job: `POST https://api.sync.so/v1/lipsync`
- Poll status: `GET https://api.sync.so/v1/lipsync/{job_id}`

**Próximo paso:**
- ⚠️ Probar con el nuevo endpoint: `python tests/test_synclabs_completo.py`

---

### 2. Higgsfield - Endpoints a Verificar ⚠️

**Estado actual:**
- Base URL: `https://cloud.higgsfield.ai/api`
- Endpoints probados (todos retornan 404):
  - `/generate`
  - `/v1/generate`
  - `/video/generate`

**Acción requerida:**
1. ⚠️ Revisar documentación oficial: https://docs.higgsfield.ai/
2. ⚠️ Verificar endpoints correctos en el dashboard
3. ⚠️ Actualizar código con endpoints correctos

**Posibles endpoints correctos:**
- Según documentación, puede ser:
  - `https://api.higgsfield.ai/v1/generate`
  - `https://cloud.higgsfield.ai/v1/generate`
  - O estructura diferente según la versión de API

**Autenticación:**
- Usa `HIGGSFIELD_API_KEY_ID` y `HIGGSFIELD_API_KEY_SECRET`
- Headers probados:
  - `Authorization: Bearer {key_id}` + `X-API-Key: {key_secret}`
  - `X-API-Key-ID: {key_id}` + `X-API-Key-Secret: {key_secret}`

---

### 3. MuseTalk/Wav2Lip - Configuración ✅

**Estado:**
- ✅ Repositorios clonados:
  - `MuseTalk/` - Existe
  - `wav2lip/` - Existe

**Script de configuración creado:**
- ✅ `scripts/configurar_musetalk_wav2lip.sh`
- Instala dependencias
- Verifica modelos
- Proporciona instrucciones

**Para ejecutar:**
```bash
cd grido-backend/worker
./scripts/configurar_musetalk_wav2lip.sh
```

**Dependencias:**
- MuseTalk: Requiere `pip install -r requirements.txt` en `MuseTalk/`
- Wav2Lip: Requiere `pip install -r requirements.txt` en `wav2lip/`
  - ⚠️ Wav2Lip usa versiones antiguas que pueden causar conflictos

**Modelos:**
- MuseTalk: Descarga automática la primera vez
- Wav2Lip: Requiere descarga manual de `wav2lip_gan.pth` (350 MB)
  - Link: https://drive.google.com/file/d/15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk/view

---

## 📋 Próximos Pasos

### Prioridad 1: Probar Sync Labs con nuevo endpoint
```bash
cd grido-backend/worker
python tests/test_synclabs_completo.py
```

### Prioridad 2: Verificar Higgsfield
1. Acceder a dashboard de Higgsfield
2. Revisar documentación: https://docs.higgsfield.ai/
3. Verificar endpoints correctos
4. Actualizar código si es necesario

### Prioridad 3: Configurar MuseTalk/Wav2Lip
```bash
cd grido-backend/worker
./scripts/configurar_musetalk_wav2lip.sh
```

---

## 🔍 Verificación de Configuración

### Verificar Sync Labs:
```bash
python -c "from providers.synclabs_lipsync import SyncLabsLipsyncProvider; p = SyncLabsLipsyncProvider(); print(f'Endpoint: {p.api_base_url}')"
# Debe mostrar: https://api.sync.so
```

### Verificar MuseTalk/Wav2Lip:
```bash
python -c "from providers.manager import ProviderManager; m = ProviderManager(); print(f'Lip-sync providers: {len(m.lipsync_providers)}')"
# Debe mostrar: 2 o 3 (dependiendo de qué esté disponible)
```

---

## 📊 Estado Actual

| Servicio | Endpoint | Estado | Acción |
|----------|----------|--------|--------|
| **Sync Labs** | `https://api.sync.so` | ✅ Actualizado | Probar |
| **Higgsfield** | `https://cloud.higgsfield.ai/api` | ⚠️ 404 | Verificar docs |
| **MuseTalk** | Local | ✅ Clonado | Instalar deps |
| **Wav2Lip** | Local | ✅ Clonado | Instalar deps + modelo |

---

## 💡 Notas Importantes

1. **Sync Labs**: El cambio de endpoint debería resolver el problema de DNS
2. **Higgsfield**: Necesita verificación manual de endpoints en documentación
3. **MuseTalk/Wav2Lip**: Ya están clonados, solo falta instalar dependencias y modelos
4. **Sistema actual**: Sigue funcionando con Estrategia 3 (audio + video base)

---

**Última actualización:** Diciembre 2024

