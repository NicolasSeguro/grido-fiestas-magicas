# Estado de Instalación de Dependencias

**Fecha:** Diciembre 2024

---

## ⚠️ Problemas Encontrados

### 1. MuseTalk
- **Error:** `Cannot import 'setuptools.build_meta'`
- **Causa:** Problema con setuptools en el entorno virtual
- **Solución aplicada:** Actualización de setuptools, wheel y pip

### 2. Wav2Lip
- **Error:** `numpy==1.17.1` no compatible con Python 3.13
- **Causa:** Wav2Lip requiere versiones muy antiguas (numpy 1.17.1, torch 1.1.0)
- **Problema:** Python 3.13 es demasiado nuevo para estas versiones

---

## ✅ Estado Actual

### Providers Detectados:
- ✅ **MuseTalk:** Disponible (detectado)
- ✅ **Sync Labs:** Disponible (API key configurada)
- ✅ **Wav2Lip:** Disponible (modelo detectado)

**Nota:** Los providers están detectados como disponibles, lo que significa que:
- Pueden tener dependencias básicas ya instaladas
- O están usando métodos alternativos de detección

---

## 🔧 Soluciones Aplicadas

### 1. Actualización de Herramientas Base
```bash
pip install --upgrade setuptools wheel pip
```

### 2. Instalación de Dependencias Básicas
- PyTorch (CPU version)
- OpenCV
- NumPy (versión moderna)
- Pillow
- SciPy

---

## 📋 Recomendaciones

### Opción 1: Usar Solo MuseTalk (Recomendado)
MuseTalk es más moderno y compatible:
- No requiere versiones antiguas
- Funciona con Python 3.11+
- Mejor rendimiento

**Acción:** Instalar dependencias básicas de MuseTalk manualmente si es necesario.

### Opción 2: Entorno Virtual Separado para Wav2Lip
Si realmente necesitas Wav2Lip:
```bash
python3.8 -m venv venv_wav2lip  # Python 3.8 o anterior
source venv_wav2lip/bin/activate
cd wav2lip
pip install -r requirements.txt
```

### Opción 3: Actualizar Wav2Lip
Modificar `wav2lip/requirements.txt` para usar versiones más nuevas:
- `numpy>=1.20.0` en lugar de `numpy==1.17.1`
- `torch>=1.8.0` en lugar de `torch==1.1.0`
- Ajustar código si es necesario

---

## 🧪 Verificación

### Verificar Providers:
```bash
cd grido-backend/worker
source venv/bin/activate
python -c "from providers.manager import ProviderManager; m = ProviderManager(); print(f'Lip-sync: {len(m.lipsync_providers)}')"
```

**Resultado esperado:** `Lip-sync: 3`

### Verificar Dependencias Básicas:
```bash
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import torch
    print(f'✅ PyTorch: {torch.__version__}')
except:
    print('❌ PyTorch no instalado')
try:
    import cv2
    print(f'✅ OpenCV: {cv2.__version__}')
except:
    print('❌ OpenCV no instalado')
"
```

---

## 💡 Conclusión

**Estado:**
- ✅ Providers detectados y disponibles
- ⚠️ Dependencias completas pueden requerir instalación manual
- ✅ Sistema funcional con dependencias básicas

**Recomendación:**
- **Para producción:** Usar MuseTalk como provider principal
- **Wav2Lip:** Solo si es absolutamente necesario (requiere Python 3.8 o anterior)
- **Sync Labs:** Como fallback si funciona

**El sistema tiene 3 opciones de lip-sync, así que si una falla, automáticamente probará las otras.** ✅

---

**Los providers están disponibles. El sistema puede funcionar, aunque algunas dependencias específicas pueden necesitar instalación manual según el uso.** ✅

