#!/usr/bin/env python3
"""
TEST WEBCAM ET PERFORMANCES
===========================

Teste la caméra et analyse les performances du système
"""

import cv2
import time
import numpy as np


def test_camera():
    """Test de la caméra"""
    
    print("\n" + "=" * 60)
    print("TEST DE LA CAMÉRA")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Caméra non accessible")
        return False
    
    print("✓ Caméra ouverte")
    
    # Propriétés
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"  Résolution: {width}x{height}")
    print(f"  FPS: {fps}")
    
    # Test capture
    print("\nCapture 30 frames...")
    start = time.time()
    
    for i in range(30):
        ret, frame = cap.read()
        if not ret:
            print(f"✗ Erreur à la frame {i}")
            cap.release()
            return False
    
    elapsed = time.time() - start
    actual_fps = 30 / elapsed
    
    print(f"✓ 30 frames capturées en {elapsed:.2f}s")
    print(f"  FPS réel: {actual_fps:.1f}")
    
    cap.release()
    return True


def test_opencv():
    """Test OpenCV"""
    
    print("\n" + "=" * 60)
    print("TEST OPENCV")
    print("=" * 60)
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        
        # Test opérations
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.circle(img, (320, 240), 50, (0, 255, 0), -1)
        
        print("✓ Opérations basiques: OK")
        
        return True
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_numpy():
    """Test NumPy"""
    
    print("\n" + "=" * 60)
    print("TEST NUMPY")
    print("=" * 60)
    
    try:
        arr = np.random.rand(1000, 1000)
        
        start = time.time()
        result = np.linalg.norm(arr)
        elapsed = time.time() - start
        
        print(f"✓ NumPy version: {np.__version__}")
        print(f"✓ Calcul norm 1000x1000: {elapsed*1000:.2f}ms")
        
        return True
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_mediapipe():
    """Test MediaPipe"""
    
    print("\n" + "=" * 60)
    print("TEST MEDIAPIPE")
    print("=" * 60)
    
    try:
        import mediapipe as mp
        
        print(f"✓ MediaPipe version: {mp.__version__}")
        
        # Init FaceMesh
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        print("✓ FaceMesh initialisé")
        
        # Test avec image vide
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        result = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        print("✓ Traitement d'image: OK")
        
        return True
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_serial():
    """Test PySerial"""
    
    print("\n" + "=" * 60)
    print("TEST PYSERIAL")
    print("=" * 60)
    
    try:
        import serial
        print(f"✓ PySerial importé")
        
        # Liste ports
        try:
            import serial.tools.list_ports
            ports = list(serial.tools.list_ports.comports())
            
            if ports:
                print(f"✓ {len(ports)} port(s) détecté(s):")
                for p in ports:
                    print(f"    - {p.device}")
            else:
                print("⚠️  Aucun port série détecté")
        
        except ImportError:
            print("⚠️  Impossible de lister les ports")
        
        return True
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def benchmark_mediapipe():
    """Benchmark MediaPipe"""
    
    print("\n" + "=" * 60)
    print("BENCHMARK MEDIAPIPE")
    print("=" * 60)
    
    try:
        import mediapipe as mp
        
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Caméra non accessible")
            return
        
        print("Traitement 60 frames...")
        times = []
        
        for i in range(60):
            ret, frame = cap.read()
            if not ret:
                break
            
            start = time.time()
            result = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            elapsed = time.time() - start
            times.append(elapsed)
        
        cap.release()
        
        times = np.array(times)
        print(f"\n✓ Résultats:")
        print(f"  Temps moyen: {np.mean(times)*1000:.1f}ms")
        print(f"  Min: {np.min(times)*1000:.1f}ms")
        print(f"  Max: {np.max(times)*1000:.1f}ms")
        print(f"  FPS moyen: {1/np.mean(times):.1f}")
        
    except Exception as e:
        print(f"✗ Erreur: {e}")


def main():
    """Fonction principale"""
    
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 TEST SYSTÈME  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    results = {
        "Caméra": test_camera(),
        "OpenCV": test_opencv(),
        "NumPy": test_numpy(),
        "MediaPipe": test_mediapipe(),
        "PySerial": test_serial(),
    }
    
    print("\n" + "=" * 60)
    print("BENCHMARK")
    print("=" * 60)
    benchmark_mediapipe()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    for test_name, result in results.items():
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n{passed}/{total} tests réussis")
    
    if passed == total:
        print("\n✓ SYSTÈME PRÊT À FONCTIONNER!")
    else:
        print("\n✗ Certains composants ne fonctionnent pas")
    
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Interrompu")
