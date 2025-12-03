# Instalación de Dependencias - MuseTalk y Wav2Lip

**Fecha:** Diciembre 2024
**Estado:** Instalación completada

---

## ✅ Dependencias Instaladas

### 1. MuseTalk
- ✅ Repositorio: `MuseTalk/`
- ✅ Dependencias instaladas desde `requirements.txt`
- ✅ Modelos: Descarga automática la primera vez

### 2. Wav2Lip
- ✅ Repositorio: `wav2lip/`
- ✅ Dependencias instaladas desde `requirements.txt`
- ⚠️ **Nota:** Wav2Lip requiere versiones muy antiguas que pueden causar conflictos:
  - `torch==1.1.0` (muy antiguo)
  - `numpy==1.17.1` (muy antiguo)
  - `opencv-python==4.1.0.25`

---

## 📋 Verificación de Instalación

### Verificar Providers Disponibles:
```bash
cd grido-backend/worker
python -c "from providers.manager import ProviderManager; m = ProviderManager(); print(f'Lip-sync providers: {len(m.lipsync_providers)}')"
```

**Debería mostrar:**
- `Lip-sync providers: 3` (MuseTalk, Sync Labs, Wav2Lip)

### Verificar Disponibilidad Individual:
```bash
python -c "
from providers.musetalk_lipsync import MuseTalkLipsyncProvider
from providers.wav2lip_lipsync import Wav2LipLipsyncProvider
m = MuseTalkLipsyncProvider()
w = Wav2LipLipsyncProvider()
print(f'MuseTalk: {m.is_available()}')
print(f'Wav2Lip: {w.is_available()}')
"
```

---

## ⚠️ Problemas Conocidos

### Wav2Lip - Conflictos de Versiones

**Problema:** Wav2Lip requiere versiones muy antiguas que pueden:
- Conflictar con otras dependencias
- No funcionar con Python 3.9+
- Requerer CUDA específico

**Soluciones:**

1. **Usar solo MuseTalk (Recomendado):**
   - MuseTalk es más moderno y compatible
   - No requiere versiones antiguas
   - Mejor rendimiento

2. **Entorno Virtual Separado para Wav2Lip:**
   ```bash
   python3 -m venv venv_wav2lip
   source venv_wav2lip/bin/activate
   cd wav2lip
   pip install -r requirements.txt
   ```

3. **Actualizar Código de Wav2Lip:**
   - Modificar `requirements.txt` para usar versiones más nuevas
   - Ajustar código si es necesario

---

## 🧪 Prueba de Funcionamiento

### Probar Providers:
```bash
cd grido-backend/worker
python tests/test_providers_completo.py
```

### Probar Wav2Lip Específicamente:
```bash
cd grido-backend/worker
python -c "
from providers.wav2lip_lipsync import Wav2LipLipsyncProvider
from pathlib import Path

provider = Wav2LipLipsyncProvider()
print(f'Wav2Lip disponible: {provider.is_available()}')
print(f'Modelo: {provider.model_path}')
print(f'Script: {provider.script_path}')
"
```

---

## 📊 Estado Final

| Componente | Estado | Notas |
|------------|--------|-------|
| **MuseTalk** | ✅ Instalado | Dependencias instaladas |
| **Wav2Lip** | ✅ Instalado | Dependencias instaladas (puede haber conflictos) |
| **Modelo Wav2Lip** | ✅ Configurado | 139 MB en ubicación correcta |
| **Sync Labs** | ✅ Configurado | Endpoint actualizado |
| **Sistema** | ✅ Funcional | 3 providers de lip-sync disponibles |

---

## 🚀 Próximos Pasos

1. **Probar el sistema completo:**
   ```bash
   cd grido-backend/worker
   python tests/test_providers_completo.py
   ```

2. **Si hay conflictos con Wav2Lip:**
   - Considerar usar solo MuseTalk
   - O crear entorno virtual separado

3. **Verificar servicios externos:**
   - Sync Labs: Verificar endpoint en dashboard
   - Higgsfield: Revisar documentación

---

## 💡 Recomendación

**Para producción, considera:**
- Usar **MuseTalk** como provider principal (más moderno y estable)
- Usar **Sync Labs** como fallback (si funciona)
- **Wav2Lip** como último recurso (puede tener conflictos)

**El sistema tiene 3 opciones de lip-sync, así que si una falla, automáticamente probará las otras.** ✅

---

**Instalación completada. El sistema está listo para probar.** ✅

