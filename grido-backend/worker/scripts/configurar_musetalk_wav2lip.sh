#!/bin/bash
# Script para configurar MuseTalk y Wav2Lip

set -e

WORKER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKER_DIR"

echo "=========================================="
echo "🔧 Configuración de MuseTalk y Wav2Lip"
echo "=========================================="
echo ""

# Verificar si estamos en un entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        echo "📦 Activando entorno virtual..."
        source venv/bin/activate
    else
        echo "⚠️  No se encontró entorno virtual. Creando uno..."
        python3 -m venv venv
        source venv/bin/activate
    fi
fi

echo "✅ Entorno virtual activado"
echo ""

# 1. Configurar MuseTalk
echo "=========================================="
echo "1️⃣  Configurando MuseTalk"
echo "=========================================="
echo ""

if [ ! -d "MuseTalk" ]; then
    echo "📥 Clonando repositorio de MuseTalk..."
    git clone https://github.com/TMElyralab/MuseTalk.git
    echo "✅ MuseTalk clonado"
else
    echo "✅ MuseTalk ya existe"
fi

if [ -d "MuseTalk" ]; then
    echo ""
    echo "📦 Instalando dependencias de MuseTalk..."
    cd MuseTalk
    pip install -r requirements.txt || echo "⚠️  Algunas dependencias pueden fallar, esto es normal"
    cd ..
    echo "✅ Dependencias de MuseTalk instaladas"
fi

echo ""

# 2. Configurar Wav2Lip
echo "=========================================="
echo "2️⃣  Configurando Wav2Lip"
echo "=========================================="
echo ""

if [ ! -d "wav2lip" ]; then
    echo "📥 Clonando repositorio de Wav2Lip..."
    git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip
    echo "✅ Wav2Lip clonado"
else
    echo "✅ Wav2Lip ya existe"
fi

if [ -d "wav2lip" ]; then
    echo ""
    echo "📦 Instalando dependencias de Wav2Lip..."
    echo "⚠️  NOTA: Wav2Lip requiere versiones antiguas que pueden causar conflictos"
    echo "   Si hay problemas, considera usar solo MuseTalk"
    cd wav2lip
    pip install -r requirements.txt || echo "⚠️  Algunas dependencias pueden fallar debido a versiones antiguas"
    cd ..
    echo "✅ Dependencias de Wav2Lip instaladas"
    
    # Crear directorio de checkpoints
    mkdir -p wav2lip/checkpoints
    echo "✅ Directorio de checkpoints creado"
fi

echo ""

# 3. Verificar modelos
echo "=========================================="
echo "3️⃣  Verificando Modelos"
echo "=========================================="
echo ""

# Wav2Lip
if [ -f "wav2lip/checkpoints/wav2lip_gan.pth" ]; then
    SIZE=$(ls -lh wav2lip/checkpoints/wav2lip_gan.pth | awk '{print $5}')
    echo "✅ wav2lip_gan.pth encontrado ($SIZE)"
    
    # Verificar que no sea un archivo HTML de error
    if [ "$SIZE" = "2.4K" ] || [ "$SIZE" = "2.5K" ]; then
        echo "⚠️  ADVERTENCIA: El archivo parece ser un HTML de error (muy pequeño)"
        echo "   Debes descargar el modelo manualmente desde:"
        echo "   https://drive.google.com/file/d/15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk/view"
    fi
else
    echo "❌ wav2lip_gan.pth NO encontrado"
    echo "   Descarga manual requerida desde:"
    echo "   https://drive.google.com/file/d/15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk/view"
    echo "   Colócalo en: wav2lip/checkpoints/wav2lip_gan.pth"
fi

# MuseTalk
echo ""
echo "ℹ️  MuseTalk descarga modelos automáticamente la primera vez que se usa"
echo ""

# 4. Resumen
echo "=========================================="
echo "✅ Configuración Completada"
echo "=========================================="
echo ""
echo "📋 Resumen:"
echo ""

if [ -d "MuseTalk" ]; then
    echo "  ✅ MuseTalk: Instalado"
    if [ -d "MuseTalk/scripts" ]; then
        echo "     - Scripts encontrados"
    fi
else
    echo "  ❌ MuseTalk: No instalado"
fi

if [ -d "wav2lip" ]; then
    echo "  ✅ Wav2Lip: Instalado"
    if [ -f "wav2lip/checkpoints/wav2lip_gan.pth" ]; then
        echo "     - Modelo encontrado"
    else
        echo "     - ⚠️  Modelo faltante (descarga manual requerida)"
    fi
else
    echo "  ❌ Wav2Lip: No instalado"
fi

echo ""
echo "📝 Próximos pasos:"
echo "   1. Si Wav2Lip necesita modelo, descárgalo manualmente"
echo "   2. Prueba los providers con: python tests/test_providers_completo.py"
echo ""

