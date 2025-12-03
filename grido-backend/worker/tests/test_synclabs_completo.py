"""
Test completo de Sync Labs - Prueba el flujo completo de lip-sync.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.synclabs_lipsync import SyncLabsLipsyncProvider
from providers.elevenlabs_tts import ElevenLabsTTSProvider
from papa_noel_config import generate_frame3_script

# Configuración
SYNCLABS_API_KEY = os.getenv("SYNCLABS_API_KEY", "sk--TYpSgoITA-NougeRyXsmw.wPoj709byT7yLe16FiZiJLgxadbHW3yi")

def test_synclabs_completo():
    """Prueba completa de Sync Labs con video y audio reales."""
    print("=" * 60)
    print("🧪 TEST COMPLETO DE SYNC LABS")
    print("=" * 60)
    print()
    
    # Verificar API key
    if not SYNCLABS_API_KEY:
        print("❌ SYNCLABS_API_KEY no configurada")
        print()
        print("Configura la variable de entorno:")
        print("export SYNCLABS_API_KEY=tu_key")
        return False
    
    print(f"✅ API Key configurada: {SYNCLABS_API_KEY[:20]}...")
    print()
    
    # Inicializar provider
    provider = SyncLabsLipsyncProvider(api_key=SYNCLABS_API_KEY)
    
    if not provider.is_available():
        print("❌ Sync Labs no está disponible")
        return False
    
    print("✅ Sync Labs está disponible")
    print()
    
    # Generar audio de prueba
    print("📝 Generando audio de prueba...")
    tts_provider = ElevenLabsTTSProvider()
    
    if not tts_provider.is_available():
        print("❌ ElevenLabs no está disponible")
        print("   Configura ELEVENLABS_API_KEY")
        return False
    
    # Generar script de prueba
    form_data = {
        "nombre": "Juan",
        "parentesco": "papá",
        "queHizo": "aprendió a andar en bicicleta",
        "recuerdoEspecial": "la primera vez que lo logró",
        "pedidoNocheMagica": "una bicicleta nueva",
    }
    
    script = generate_frame3_script(form_data)
    print(f"📝 Script generado: {script[:100]}...")
    print()
    
    # Generar audio
    audio_path = Path("storage/test_synclabs_audio.mp3")
    try:
        audio_path = tts_provider.generate_audio(script, audio_path)
        print(f"✅ Audio generado: {audio_path}")
        print(f"   Tamaño: {audio_path.stat().st_size / 1024:.2f} KB")
    except Exception as e:
        print(f"❌ Error generando audio: {e}")
        return False
    
    print()
    
    # Buscar video base
    video_base_path = None
    posibles_paths = [
        Path("assets/frame3_santa_base.mp4"),
        Path("assets/frame3_santa_base2.mp4"),
        Path("assets/video_base.mp4"),
        Path("assets/papa_noel_base.mp4"),
        Path("assets/video_intro.mp4"),
        Path("storage/video_base.mp4"),
    ]
    
    for path in posibles_paths:
        if path.exists():
            video_base_path = path
            break
    
    if not video_base_path or not video_base_path.exists():
        print("❌ No se encontró video base")
        print("   Busca un video MP4 en assets/ o storage/")
        print("   Paths probados:")
        for path in posibles_paths:
            print(f"     - {path}")
        return False
    
    print(f"✅ Video base encontrado: {video_base_path}")
    print(f"   Tamaño: {video_base_path.stat().st_size / 1024 / 1024:.2f} MB")
    print()
    
    # Aplicar lip-sync
    print("🎬 Aplicando lip-sync con Sync Labs...")
    print("   Esto puede tardar varios minutos...")
    print()
    
    output_path = Path("storage/test_synclabs_output.mp4")
    
    try:
        result_path = provider.apply_lipsync(
            video=video_base_path,
            audio=audio_path,
            output_path=output_path
        )
        
        print()
        print("=" * 60)
        print("✅ LIP-SYNC COMPLETADO")
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
        print("❌ ERROR EN LIP-SYNC")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Posibles causas:")
        print("  1. API key inválida o expirada")
        print("  2. Endpoint incorrecto (verificar documentación)")
        print("  3. Formato de video/audio no soportado")
        print("  4. Problema de red o timeout")
        print()
        return False


if __name__ == "__main__":
    success = test_synclabs_completo()
    sys.exit(0 if success else 1)

