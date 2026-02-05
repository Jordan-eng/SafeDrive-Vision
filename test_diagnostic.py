"""
SCRIPT DE TEST ET DIAGNOSTIC
============================

Vérifie que toutes les dépendances et configurations sont correctes
avant de lancer le système de détection principal.
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Affiche un en-tête"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_status(success, message):
    """Affiche le statut"""
    symbol = "✓" if success else "✗"
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {message}")


def test_python_version():
    """Teste la version Python"""
    print_header("1. VERSION PYTHON")
    version = sys.version
    required = (3, 8)
    current = sys.version_info[:2]
    
    success = current >= required
    print_status(success, f"Python {current[0]}.{current[1]} (requis: {required[0]}.{required[1]}+)")
    if version:
        print(f"  Détails: {version.split()[0]}")
    return success


def test_imports():
    """Teste les imports des dépendances"""
    print_header("2. DÉPENDANCES PYTHON")
    
    dependencies = [
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("numpy", "NumPy"),
        ("serial", "PySerial"),
    ]
    
    all_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print_status(True, f"{display_name} ✓")
        except ImportError:
            print_status(False, f"{display_name} ✗ - Installez avec: pip install {display_name.lower()}")
            all_ok = False
    
    return all_ok


def test_config():
    """Teste le fichier de configuration"""
    print_header("3. FICHIER DE CONFIGURATION")
    
    try:
        from config import CONFIG
        
        required_keys = [
            'arduino_port',
            'eye_closed_threshold',
            'eyes_closed_frames_threshold',
            'smoothing_window',
            'video_width',
            'video_height',
        ]
        
        all_present = True
        for key in required_keys:
            if key in CONFIG:
                value = CONFIG[key]
                print_status(True, f"{key}: {value}")
            else:
                print_status(False, f"{key}: MANQUANT")
                all_present = False
        
        return all_present
    
    except ImportError as e:
        print_status(False, f"Impossible d'importer config.py: {e}")
        return False


def test_arduino_port():
    """Teste la disponibilité du port Arduino"""
    print_header("4. CONFIGURATION ARDUINO")
    
    try:
        from config import CONFIG
        import serial
        
        port = CONFIG['arduino_port']
        print(f"Port configuré: {port}")
        
        # Liste les ports disponibles
        try:
            import serial.tools.list_ports as list_ports
            ports = list(list_ports.comports())
            
            if ports:
                print("\nPorts série détectés:")
                for p in ports:
                    print(f"  - {p.device}: {p.description}")
            else:
                print("⚠ Aucun port série détecté (Arduino non connecté?)")
            
            # Teste la connexion
            try:
                ser = serial.Serial(port, 9600, timeout=1)
                ser.close()
                print_status(True, f"Port {port} accessible")
                return True
            except Exception as e:
                print_status(False, f"Impossible de se connecter à {port}: {e}")
                print("  💡 Assurez-vous que Arduino est:")
                print("     - Connecté via USB")
                print("     - Le bon port dans config.py")
                print("     - Pas utilisé par un autre programme")
                return False
        
        except ImportError:
            print("⚠ Impossible de lister les ports (pyserial pas installé)")
            return False
    
    except Exception as e:
        print_status(False, f"Erreur: {e}")
        return False


def test_webcam():
    """Teste l'accès à la webcam"""
    print_header("5. WEBCAM")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print_status(True, f"Webcam accessible ({w}x{h})")
                cap.release()
                return True
            else:
                print_status(False, "Impossible de lire la frame webcam")
                cap.release()
                return False
        else:
            print_status(False, "Impossible d'ouvrir la webcam")
            return False
    
    except Exception as e:
        print_status(False, f"Erreur webcam: {e}")
        return False


def test_mediapipe():
    """Teste MediaPipe"""
    print_header("6. MEDIAPIPE")
    
    try:
        import mediapipe as mp
        from mediapipe.python.solutions import face_mesh
        
        print_status(True, f"MediaPipe version: {mp.__version__}")
        
        # Teste l'initialisation
        fm = face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        print_status(True, "FaceMesh initialisé avec succès")
        return True
    
    except Exception as e:
        print_status(False, f"Erreur MediaPipe: {e}")
        return False


def test_files():
    """Teste la présence des fichiers nécessaires"""
    print_header("7. FICHIERS DU PROJET")
    
    files_required = [
        "detection_yeux_fermes_arduino.py",
        "config.py",
        "arduino_code.ino",
        "README.md",
    ]
    
    current_dir = Path(".")
    all_present = True
    
    for filename in files_required:
        file_path = current_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print_status(True, f"{filename} ({size} bytes)")
        else:
            print_status(False, f"{filename} MANQUANT")
            all_present = False
    
    return all_present


def main():
    """Fonction principale de test"""
    
    print("\n" * 2)
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🔍 DIAGNOSTIC SYSTÈME - Détection Yeux Fermés  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    results = {
        "Python": test_python_version(),
        "Imports": test_imports(),
        "Config": test_config(),
        "Arduino": test_arduino_port(),
        "Webcam": test_webcam(),
        "MediaPipe": test_mediapipe(),
        "Fichiers": test_files(),
    }
    
    # Résumé
    print_header("📊 RÉSUMÉ")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        print_status(result, test_name)
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n" + "=" * 60)
        print("✓ TOUS LES TESTS RÉUSSIS!")
        print("✓ Vous pouvez lancer: python detection_yeux_fermes_arduino.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ CERTAINS TESTS ONT ÉCHOUÉ")
        print("✗ Corrigez les erreurs avant de lancer le programme principal")
        print("=" * 60)
    
    print("\n")
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
