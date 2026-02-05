"""
DÉTECTION DES YEUX FERMÉS AVEC MEDIAPIPE + CONTRÔLE ARDUINO
===========================================================

Ce script détecte les yeux fermés en temps réel avec MediaPipe Face Mesh
et active une LED et un buzzer via Arduino lorsque les yeux sont fermés
pendant plus de N frames consécutifs.

Implémentation basée sur le calcul EAR (Eye Aspect Ratio) optimisé.

Dépendances:
- opencv-python
- mediapipe
- pyserial

Branchement Arduino:
- LED: Pin 13 (ou à modifier dans le code)
- Buzzer: Pin 12 (ou à modifier dans le code)
"""

import cv2
import mediapipe as mp
import numpy as np
from serial import Serial
import time
import sys
import importlib
from collections import deque
from typing import List, Tuple
from config import CONFIG

# Fallback pour mp.solutions (différentes versions de MediaPipe)
try:
    mp_solutions = mp.solutions
except Exception:
    try:
        mp_solutions = importlib.import_module("mediapipe.python.solutions")
    except Exception:
        mp_solutions = None


def _euclid(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Calcule la distance euclidienne entre deux points"""
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def eye_aspect_ratio(landmarks: List[Tuple[float, float]], indices: List[int]) -> float:
    """
    Calcule le ratio d'aspect des yeux (EAR)
    
    Formule: EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    
    Args:
        landmarks: Liste de tous les landmarks du visage
        indices: Les 6 indices des points clés de l'œil
        
    Returns:
        float: Ratio d'aspect (faible = yeux fermés, élevé = yeux ouverts)
    """
    p1 = landmarks[indices[0]]
    p2 = landmarks[indices[1]]
    p3 = landmarks[indices[2]]
    p4 = landmarks[indices[3]]
    p5 = landmarks[indices[4]]
    p6 = landmarks[indices[5]]

    vertical1 = _euclid(p2, p6)
    vertical2 = _euclid(p3, p5)
    horizontal = _euclid(p1, p4)
    
    if horizontal == 0:
        return 0.0
    
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear


class EyeClosureDetector:
    """Détecteur de fermeture des yeux avec MediaPipe Face Mesh"""
    
    def __init__(self, min_detection_confidence=0.5):
        """Initialise le détecteur MediaPipe"""
        
        if mp_solutions is None:
            raise RuntimeError(
                "MediaPipe 'solutions' submodule not found. "
                "Install mediapipe in the active environment."
            )
        
        # MediaPipe Face Mesh
        mp_face_mesh = mp_solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=0.5
        )
        
        self.mp_drawing = mp_solutions.drawing_utils
        
        # Indices MediaPipe pour les yeux (landmarks 468)
        # Les meilleurs indices pour EAR stablement
        self.LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_IDX = [263, 387, 385, 362, 380, 373]
        
        # Buffer pour lissage (moyenne mobile)
        self.ear_buffer = deque(maxlen=CONFIG['smoothing_window'])
        
        # Compteurs et état
        self.eyes_closed_frames = 0
        self.eyes_open_frames = 0
        self.is_alarming = False
        self.alarm_start_time = None
    
    def process_frame(self, frame):
        """
        Traite une frame pour détecter les yeux fermés
        
        Args:
            frame: Image OpenCV (BGR)
            
        Returns:
            dict: Résultats de la détection avec clés:
                - eyes_closed: bool
                - left_ear: float
                - right_ear: float
                - ear_avg: float
                - ear_smooth: float
                - eyes_closed_frames: int
                - face_detected: bool
                - frame: np.ndarray
        """
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Détecte les landmarks faciaux
        results = self.face_mesh.process(rgb_frame)
        
        result = {
            'eyes_closed': False,
            'left_ear': None,
            'right_ear': None,
            'ear_avg': None,
            'ear_smooth': None,
            'eyes_closed_frames': self.eyes_closed_frames,
            'face_detected': False,
            'frame': frame
        }
        
        if results.multi_face_landmarks:
            result['face_detected'] = True
            
            # Extrait les landmarks du visage
            pts = [(int(lm.x * w), int(lm.y * h)) for lm in results.multi_face_landmarks[0].landmark]
            
            # Calcule l'EAR pour chaque œil
            left_ear = eye_aspect_ratio(pts, self.LEFT_EYE_IDX)
            right_ear = eye_aspect_ratio(pts, self.RIGHT_EYE_IDX)
            
            result['left_ear'] = left_ear
            result['right_ear'] = right_ear
            
            # Moyenne des deux yeux
            ear_avg = (left_ear + right_ear) / 2.0
            result['ear_avg'] = ear_avg
            
            # Ajoute au buffer pour lissage
            self.ear_buffer.append(ear_avg)
            ear_smooth = np.mean(self.ear_buffer) if self.ear_buffer else ear_avg
            result['ear_smooth'] = ear_smooth
            
            # Détecte si les yeux sont fermés
            if ear_smooth < CONFIG['eye_closed_threshold']:
                result['eyes_closed'] = True
                self.eyes_closed_frames += 1
                self.eyes_open_frames = 0
            else:
                self.eyes_open_frames += 1
                self.eyes_closed_frames = 0
            
            result['eyes_closed_frames'] = self.eyes_closed_frames
            
            # Dessine les yeux pour debug
            left_eye_pts = [pts[i] for i in self.LEFT_EYE_IDX]
            right_eye_pts = [pts[i] for i in self.RIGHT_EYE_IDX]
            
            eye_color = (0, 0, 255) if result['eyes_closed'] else (0, 255, 0)
            cv2.polylines(frame, [np.array(left_eye_pts)], True, eye_color, 2)
            cv2.polylines(frame, [np.array(right_eye_pts)], True, eye_color, 2)
        
        return result


class ArduinoController:
    """Gère la communication avec Arduino"""
    
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Initialise la connexion série avec Arduino
        
        Args:
            port: Port série (ex: '/dev/ttyUSB0', 'COM3')
            baudrate: Vitesse de communication
            timeout: Timeout de communication
        """
        self.port = port or CONFIG['arduino_port']
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connected = False
        
        self.connect()
    
    def connect(self):
        """Établit la connexion avec Arduino"""
        try:
            self.ser = Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Attend que Arduino redémarre après connexion
            self.connected = True
            print(f"✓ Connecté à Arduino sur {self.port}")
        except Exception as e:
            print(f"✗ Erreur de connexion Arduino: {e}")
            self.connected = False
    
    def send_command(self, command):
        """
        Envoie une commande à Arduino
        
        Args:
            command: 'ON' pour activer, 'OFF' pour désactiver
        """
        if not self.connected:
            print("✗ Arduino non connecté")
            return False
        
        try:
            self.ser.write((command + '\n').encode())
            return True
        except Exception as e:
            print(f"✗ Erreur d'envoi: {e}")
            return False
    
    def activate_alarm(self):
        """Active la LED et le buzzer"""
        return self.send_command('ON')
    
    def deactivate_alarm(self):
        """Désactive la LED et le buzzer"""
        return self.send_command('OFF')
    
    def close(self):
        """Ferme la connexion"""
        if self.ser:
            self.ser.close()
            self.connected = False
            print("✓ Connexion Arduino fermée")


def main():
    """Fonction principale"""
    
    print("\n" + "=" * 70)
    print("  DÉTECTION YEUX FERMÉS + CONTRÔLE ARDUINO (LED & BUZZER)")
    print("=" * 70 + "\n")
    
    # Vérifie que MediaPipe est installé
    if mp_solutions is None:
        print("✗ MediaPipe non disponible. Veuillez installer: pip install mediapipe")
        sys.exit(1)
    
    # Initialise le détecteur et Arduino
    try:
        detector = EyeClosureDetector()
        print("✓ Détecteur MediaPipe initialisé")
    except Exception as e:
        print(f"✗ Erreur détecteur: {e}")
        sys.exit(1)
    
    arduino = ArduinoController()
    if not arduino.connected:
        print("⚠️  Arduino non connecté - mode simulation")
    
    # Capture vidéo
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG['video_width'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG['video_height'])
    cap.set(cv2.CAP_PROP_FPS, CONFIG['video_fps'])
    
    if not cap.isOpened():
        print("✗ Impossible d'ouvrir la webcam")
        arduino.close()
        return
    
    print("✓ Webcam ouverte")
    print(f"✓ Résolution: {CONFIG['video_width']}x{CONFIG['video_height']}")
    print(f"✓ Seuil EAR (yeux fermes): {CONFIG['eye_closed_threshold']}")
    print(f"✓ Frames consécutives requises: {CONFIG['eyes_closed_frames_threshold']}")
    print("\nAppuyez sur 'q' pour quitter\n")
    
    alarm_active = False
    frame_count = 0
    prev_time = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✗ Erreur lecture webcam")
                break
            
            frame_count += 1
            
            # Traite la frame
            result = detector.process_frame(frame)
            
            # Variables
            eyes_closed_count = result['eyes_closed_frames']
            left_ear = result['left_ear']
            right_ear = result['right_ear']
            ear_avg = result['ear_avg']
            ear_smooth = result['ear_smooth']
            face_detected = result['face_detected']
            
            # Vérifie si les yeux sont fermés depuis assez longtemps
            should_alarm = eyes_closed_count >= CONFIG['eyes_closed_frames_threshold']
            
            # Change l'état de l'alarme
            if should_alarm and not alarm_active:
                print(f"🔴 ALARME: Yeux fermes detectes ({eyes_closed_count} frames)!")
                arduino.activate_alarm()
                alarm_active = True
            
            elif not should_alarm and alarm_active:
                print(f"🟢 Yeux ouverts: Alarme désactivee")
                arduino.deactivate_alarm()
                alarm_active = False
            
            # Affichage sur la frame
            h, w = frame.shape[:2]
            
            # Infos EAR (haut à gauche)
            if face_detected and ear_avg is not None:
                info_text = f"EAR L:{left_ear:.2f} R:{right_ear:.2f} Moy:{ear_smooth:.2f}"
                cv2.putText(frame, info_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Aucun visage détecte", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Statut alarme (haut à droite)
            status_color = (0, 0, 255) if alarm_active else (0, 255, 0)
            status_text = "ALARME ACTIVE!" if alarm_active else "NORMAL"
            cv2.putText(frame, status_text, (w - 300, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)
            
            # Frames fermées (milieu à gauche)
            frame_text = f"Frames fermees: {eyes_closed_count}/{CONFIG['eyes_closed_frames_threshold']}"
            bar_color = (0, 0, 255) if should_alarm else (0, 255, 0)
            cv2.putText(frame, frame_text, (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, bar_color, 2)
            
            # Barre de progression des frames fermées
            bar_width = int((eyes_closed_count / max(CONFIG['eyes_closed_frames_threshold'], 1)) * 200)
            cv2.rectangle(frame, (10, 90), (210, 110), (200, 200, 200), 2)
            cv2.rectangle(frame, (10, 90), (10 + bar_width, 110), bar_color, -1)
            
            # FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time
            cv2.putText(frame, f"FPS: {int(fps)}", (10, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Affiche la frame
            cv2.imshow("Detection Yeux Fermes + Arduino (Appuyez sur 'q' pour quitter)", frame)
            
            # Quitter avec 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption utilisateur")
    
    finally:
        # Nettoyage
        print("\n" + "=" * 70)
        print("Fermeture du programme...")
        arduino.deactivate_alarm()
        arduino.close()
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Programme terminé")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
