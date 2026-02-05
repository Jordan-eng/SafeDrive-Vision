"""
EXEMPLES D'UTILISATION AVANCÉE
==============================

Montre comment utiliser les classes du projet de manière personnalisée
"""

import cv2
import time
from detection_yeux_fermes_arduino import EyeClosureDetector, ArduinoController


# ============= EXEMPLE 1: UTILISATION SIMPLE =============
def exemple_simple():
    """Exemple basique avec les valeurs par défaut"""
    
    detector = EyeClosureDetector()
    arduino = ArduinoController()
    cap = cv2.VideoCapture(0)
    
    print("Exemple simple - Appuyez sur Q pour quitter")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        result = detector.process_frame(frame)
        
        if result['eyes_closed_frames'] > 10:
            arduino.activate_alarm()
        else:
            arduino.deactivate_alarm()
        
        cv2.imshow("Simple", result['frame'])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()


# ============= EXEMPLE 2: ENREGISTREMENT STATISTIQUES =============
def exemple_statistiques():
    """Enregistre les statistiques de détection"""
    
    detector = EyeClosureDetector()
    cap = cv2.VideoCapture(0)
    
    stats = {
        'total_frames': 0,
        'eyes_closed_frames': 0,
        'yeux_fermes_episodes': 0,
        'temps_total_fermes': 0,
        'max_consecutif': 0,
    }
    
    print("Statistiques - Appuyez sur Q pour quitter et voir résultats")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        result = detector.process_frame(frame)
        
        stats['total_frames'] += 1
        
        if result['eyes_closed_frames'] > 0:
            stats['eyes_closed_frames'] += 1
            stats['temps_total_fermes'] += 1
            stats['max_consecutif'] = max(stats['max_consecutif'], result['eyes_closed_frames'])
        else:
            if detector.eyes_closed_frames > 10:
                stats['yeux_fermes_episodes'] += 1
        
        cv2.imshow("Statistiques", result['frame'])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Affiche les résultats
    print("\n" + "=" * 50)
    print("STATISTIQUES DE DÉTECTION")
    print("=" * 50)
    print(f"Total frames: {stats['total_frames']}")
    print(f"Frames yeux fermés: {stats['eyes_closed_frames']}")
    print(f"Pourcentage: {stats['eyes_closed_frames']/max(1, stats['total_frames'])*100:.1f}%")
    print(f"Episodes détectés: {stats['yeux_fermes_episodes']}")
    print(f"Max consécutif: {stats['max_consecutif']} frames")
    print("=" * 50)
    
    cap.release()
    cv2.destroyAllWindows()


# ============= EXEMPLE 3: ALARME PROGRESSIVE =============
def exemple_alarme_progressive():
    """Alarme qui s'intensifie progressivement"""
    
    detector = EyeClosureDetector()
    arduino = ArduinoController()
    cap = cv2.VideoCapture(0)
    
    print("Alarme progressive - Appuyez sur Q pour quitter")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        result = detector.process_frame(frame)
        frames_closed = result['eyes_closed_frames']
        
        # Alarme progressive selon la durée
        if frames_closed < 5:
            arduino.deactivate_alarm()
            status = "OK"
        elif frames_closed < 15:
            arduino.activate_alarm()
            status = "⚠️  ATTENTION (faible)"
        elif frames_closed < 30:
            arduino.activate_alarm()
            status = "🔴 ATTENTION (moyen)"
        else:
            arduino.activate_alarm()
            status = "🔴🔴 DANGER (critique)"
        
        # Affiche le statut
        cv2.putText(frame, status, (10, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("Alarme Progressive", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()


# ============= EXEMPLE 4: DÉTECTION MULTI-FACES (AVANCÉ) =============
def exemple_detection_multiple():
    """Détecte les yeux fermés chez plusieurs personnes (théorique)"""
    
    import mediapipe as mp
    
    print("Exemple détection multiple")
    print("Note: Modifiez EyeClosureDetector pour max_num_faces > 1")
    print("C'est un exemple théorique.")


# ============= EXEMPLE 5: SAUVEGARDE VIDÉO =============
def exemple_sauvegarde_video():
    """Enregistre une vidéo avec la détection"""
    
    detector = EyeClosureDetector()
    cap = cv2.VideoCapture(0)
    
    # Configuration du codec vidéo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    
    out = cv2.VideoWriter('output_detection.mp4', fourcc, fps, frame_size)
    
    print("Enregistrement vidéo - Appuyez sur Q pour arrêter")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Redimensionne si nécessaire
        frame = cv2.resize(frame, frame_size)
        
        result = detector.process_frame(frame)
        frame_count += 1
        
        # Ajoute le numéro de frame
        cv2.putText(result['frame'], f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        out.write(result['frame'])
        
        cv2.imshow("Enregistrement", result['frame'])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print(f"✓ Vidéo enregistrée: output_detection.mp4 ({frame_count} frames)")
    
    out.release()
    cap.release()
    cv2.destroyAllWindows()


# ============= MENU =============
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("EXEMPLES D'UTILISATION AVANCÉE")
    print("=" * 50)
    print("\n1. Exemple simple")
    print("2. Enregistrement statistiques")
    print("3. Alarme progressive")
    print("4. Détection multiple (info)")
    print("5. Sauvegarde vidéo")
    print("0. Quitter")
    print()
    
    while True:
        choix = input("Choisissez un exemple (0-5): ").strip()
        
        if choix == "1":
            exemple_simple()
        elif choix == "2":
            exemple_statistiques()
        elif choix == "3":
            exemple_alarme_progressive()
        elif choix == "4":
            exemple_detection_multiple()
        elif choix == "5":
            exemple_sauvegarde_video()
        elif choix == "0":
            print("✓ Au revoir!")
            break
        else:
            print("Option invalide")
        
        print()
