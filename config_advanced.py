"""
CONFIGURATION AVANCÉE
====================

Paramètres additionnels pour utilisateurs avancés
"""

# ============= CALIBRATION =============
# Calibration automatique à chaque démarrage?
AUTO_CALIBRATION = False

# Durée de calibration (secondes)
CALIBRATION_DURATION = 10

# ============= LOGGING =============
# Activer les logs fichier?
ENABLE_LOGGING = False

# Fichier de log
LOG_FILE = "detection_log.txt"

# Niveau de log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# ============= DÉTECTION AVANCÉE =============
# Utiliser la main pour détecter aussi?
DETECT_HAND_GESTURES = False

# Détecter les mouvements de tête?
DETECT_HEAD_MOVEMENT = False

# Angle max toléré (degrés)
MAX_HEAD_ANGLE = 45

# ============= PERFORMANCE =============
# Réduire la résolution pour plus de FPS?
REDUCE_RESOLUTION = False

# Facteur de réduction (2 = 50% résolution)
RESOLUTION_FACTOR = 2

# Traiter que 1 frame sur N
SKIP_FRAMES = 1

# Nb de threads pour traitement
NUM_THREADS = 1

# ============= PWM (Pour broches PWM) =============
# Utiliser PWM pour contrôle graduel?
USE_PWM = False

# Broche PWM LED
PWM_LED_PIN = 3  # ou 5, 6, 9, 10, 11

# Broche PWM Buzzer
PWM_BUZZER_PIN = 9  # ou 3, 5, 6, 10, 11

# Intensité LED (0-255)
PWM_LED_INTENSITY = 255

# Fréquence buzzer (Hz) - Si buzzer capable PWM
PWM_BUZZER_FREQ = 1000

# ============= TIMEOUTS ET SÉCURITÉ =============
# Timeout de commande (ms) - Force OFF si pas de commande
COMMAND_TIMEOUT = 5000

# Désactiver l'alarme après X secondes (0 = jamais)
AUTO_ALARM_TIMEOUT = 0

# ============= NOTIFICATIONS =============
# Notifications desktop?
DESKTOP_NOTIFICATIONS = True

# Commande notification (Linux: notify-send, etc)
NOTIFICATION_CMD = "notify-send"

# Sons d'alerte locaux?
LOCAL_SOUND = False

# Fichier son d'alerte
ALERT_SOUND_FILE = "alarm.wav"

# ============= DATABASE =============
# Enregistrer dans une base de données?
USE_DATABASE = False

# Type: "sqlite" ou "mysql"
DATABASE_TYPE = "sqlite"

# Fichier SQLite
SQLITE_DB = "detections.db"

# Connexion MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "eye_detection"

# ============= FACES MULTIPLES =============
# Détecter plusieurs visages?
MULTI_FACE_MODE = False

# Nombre max de visages
MAX_FACES = 5

# ============= CALIBRATION PAR PERSONNE =============
# Profils de calibration
PROFILES = {
    "default": {
        "eye_closed_threshold": 0.2,
        "eyes_closed_frames_threshold": 10,
    },
    "sensible": {
        "eye_closed_threshold": 0.25,
        "eyes_closed_frames_threshold": 15,
    },
    "rapide": {
        "eye_closed_threshold": 0.15,
        "eyes_closed_frames_threshold": 5,
    },
}

# Profil actif
ACTIVE_PROFILE = "default"

# ============= EXPORT / IMPORT =============
# Format export vidéo
VIDEO_FORMAT = "mp4v"  # ou "MJPG", "X264"
VIDEO_QUALITY = 95  # 0-100

# Exporter les frames de détection?
EXPORT_FRAMES = False

# Dossier export
EXPORT_DIR = "./export"

# ============= DEBUG DÉTAILLÉ =============
# Afficher les landmark points?
SHOW_LANDMARKS = True

# Afficher les boîtes de détection?
SHOW_DETECTION_BOX = True

# FPS counter?
SHOW_FPS = True

# Historique EAR?
SHOW_EAR_HISTORY = False

# Afficher les seuils?
SHOW_THRESHOLDS = False
