"""
FICHIER DE CONFIGURATION
========================

Tous les paramètres configurables du projet
"""

# ============= ARDUINO =============
# Port série Arduino (vérifier avec: ls /dev/ttyUSB* ou ls /dev/ttyACM*)
ARDUINO_PORT = '/dev/ttyACM0'  # Linux/Mac
# ARDUINO_PORT = 'COM3'          # Windows
ARDUINO_BAUDRATE = 9600
ARDUINO_TIMEOUT = 1

# ============= DÉTECTION YEUX =============
# Seuil EAR (Eye Aspect Ratio) pour détecter les yeux fermés
# Plus bas = plus sensible
# Typiquement: 0.15-0.25 pour fermés
EYE_CLOSED_THRESHOLD = 0.2

# Nombre de frames consécutives pour valider "yeux fermés"
# Évite les faux positifs sur des clignements rapides
EYES_CLOSED_FRAMES_THRESHOLD = 10  # ~0.3 secondes à 30 FPS

# Fenêtre de lissage (nombre de frames pour moyenne mobile)
SMOOTHING_WINDOW = 5

# ============= VIDÉO =============
# Résolution de la webcam
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_FPS = 30

# ============= AFFICHAGE DEBUG =============
SHOW_LANDMARKS = True  # Affiche les points de repère des yeux
DEBUG_MODE = True      # Affiche les infos de debug

# ============= ALARME =============
# Durée de l'alarme (en secondes) avant arrêt automatique
# 0 = alarme continue tant que les yeux sont fermés
ALARM_DURATION = 0

# Volume du buzzer (0-255 si PWM)
BUZZER_VOLUME = 255

# Intensité de la LED (0-255 si PWM)
LED_BRIGHTNESS = 255


# Dictionnaire de configuration pour accès facile
CONFIG = {
    'arduino_port': ARDUINO_PORT,
    'arduino_baudrate': ARDUINO_BAUDRATE,
    'arduino_timeout': ARDUINO_TIMEOUT,
    'eye_closed_threshold': EYE_CLOSED_THRESHOLD,
    'eyes_closed_frames_threshold': EYES_CLOSED_FRAMES_THRESHOLD,
    'smoothing_window': SMOOTHING_WINDOW,
    'video_width': VIDEO_WIDTH,
    'video_height': VIDEO_HEIGHT,
    'video_fps': VIDEO_FPS,
    'show_landmarks': SHOW_LANDMARKS,
    'debug_mode': DEBUG_MODE,
    'alarm_duration': ALARM_DURATION,
    'buzzer_volume': BUZZER_VOLUME,
    'led_brightness': LED_BRIGHTNESS,
}
