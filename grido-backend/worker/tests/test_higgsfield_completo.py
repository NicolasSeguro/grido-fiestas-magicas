"""
Test completo de Higgsfield - Prueba el flujo completo de generación de video.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.higgsfield_video import HiggsfieldVideoProvider
from papa_noel_config import generate_frame3_script

# Configuración
HIGGSFIELD_API_KEY_ID = os.getenv("HIGGSFIELD_API_KEY_ID", "a242bf13-bfe5-4aa4-af63-245d05d48d22")
HIGGSFIELD_API_KEY_SECRET = os.getenv("HIGGSFIELD_API_KEY_SECRET", "19b359462d24010924f52a74048d9ab190f2d0336f48a758bd0f1ccc242b4b1a")

def test_higgsfield_completo():
    """Prueba completa de Higgsfield con script real."""
    print("=" * 60)
    print("🧪 TEST COMPLETO DE HIGGSFIELD")
    print("=" * 60)
    print()
    
    # Verificar credenciales
    if not HIGGSFIELD_API_KEY_ID or not HIGGSFIELD_API_KEY_SECRET:
        print("❌ Credenciales de Higgsfield no configuradas")
        print()
        print("Configura las variables de entorno:")
        print("export HIGGSFIELD_API_KEY_ID=tu_key_id")
        print("export HIGGSFIELD_API_KEY_SECRET=tu_key_secret")
        return False
    
    print(f"✅ API Key ID configurada: {HIGGSFIELD_API_KEY_ID[:20]}...")
    print(f"✅ API Key Secret configurada: {HIGGSFIELD_API_KEY_SECRET[:20]}...")
    print()
    
    # Inicializar provider
    provider = HiggsfieldVideoProvider(
        api_key_id=HIGGSFIELD_API_KEY_ID,
        api_key_secret=HIGGSFIELD_API_KEY_SECRET
    )
    
    if not provider.is_available():
        print("❌ Higgsfield no está disponible")
        return False
    
    print("✅ Higgsfield está disponible")
    print()
    
    # Generar script de prueba
    form_data = {
        "nombre": "Juan",
        "parentesco": "papá",
        "queHizo": "aprendió a andar en bicicleta",
        "recuerdoEspecial": "la primera vez que lo logró",
        "pedidoNocheMagica": "una bicicleta nueva",
    }
    
    script = generate_frame3_script(form_data)
    print(f"📝 Script generado:")
    print(f"   {script[:200]}...")
    print()
    
    # Generar video
    print("🎬 Generando video con Higgsfield...")
    print("   Esto puede tardar varios minutos...")
    print()
    
    output_path = Path("storage/test_higgsfield_output.mp4")
    avatar_id = "papa_noel"  # Puede que Higgsfield no use avatar_id
    
    try:
        result_path = provider.generate_video(
            script=script,
            avatar_id=avatar_id,
            output_path=output_path,
            duration=10,  # 10 segundos
        )
        
        print()
        print("=" * 60)
        print("✅ VIDEO GENERADO")
        print("=" * 60)
        print()
        print(f"📁 Video generado: {result_path}")
        print(f"   Tamaño: {result_path.stat().st_size / 1024 / 1024:.2f} MB")
        print()
        print("🎉 ¡Prueba exitosa!")
        print()
        print("Para ver el video:")
        print(f"   open {result_path}")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR EN GENERACIÓN DE VIDEO")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Posibles causas:")
        print("  1. Credenciales inválidas o expiradas")
        print("  2. Endpoint incorrecto (verificar documentación de Higgsfield)")
        print("  3. Estructura de datos incorrecta")
        print("  4. Problema de red o timeout")
        print("  5. Límite de API alcanzado")
        print()
        print("💡 Próximos pasos:")
        print("  1. Verificar credenciales en dashboard de Higgsfield")
        print("  2. Revisar documentación de API actualizada")
        print("  3. Verificar logs de error para más detalles")
        print()
        return False


if __name__ == "__main__":
    success = test_higgsfield_completo()
    sys.exit(0 if success else 1)

