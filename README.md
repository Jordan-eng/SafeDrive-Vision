# SafeDrive-Vision
Un système en temps réel qui détecte les yeux fermés via webcam (MediaPipe) et active une LED et un buzzer via Arduino.

# 🎥 Détection Yeux Fermés + Contrôle Arduino

**Utilité:** Alarme pour prévenir la fatigue oculaire, détecter les somnolences au volant, surveillance d'attention, etc.

<img width="848" height="724" alt="image" src="https://github.com/user-attachments/assets/4fb3e0d8-2196-441b-a718-3efa098259b5" />

---

## 📋 Prérequis

### Python
- Python 3.8+
- Webcam

### Dépendances Python
```bash
pip install opencv-python mediapipe pyserial numpy
```

### Matériel Arduino
- Carte Arduino (Uno, Nano, Mega, etc.)
- 1 LED (5mm)
- 1 Buzzer passif ou actif
- 1 Résistance 220Ω (pour LED)
- Câbles de connexion
- Câble USB pour programmer Arduino

---

## 🔧 Installation

### 1. Préparez le matériel

#### Schéma de branchement (Arduino Uno)

```
        +5V ─────────────────┬─────────────────┬─────────────────┬─── GND
                             │                 │                 │
                          [220Ω]           [Buzzer]              │
                             │                 │                 │
        Pin 13 ──────────────┴─ Anode LED    Pin 12 ──────────────┴─ Cathode/GND
        GND ────────────────────────────────────────────────────────────────
```

**Détails du branchement:**

**LED (Pin 13):**
- Broche plus longue (anode) → Pin 13 via résistance 220Ω
- Broche plus courte (cathode) → GND

**Buzzer (Pin 12):**
- Broche positive (si buzzer actif) → Pin 12
- Broche négative → GND

### 2. Chargez le code Arduino

1. Ouvrez [Arduino IDE](https://www.arduino.cc/en/software)
2. Copier-collez le code de `arduino_code.ino`
3. Sélectionnez votre carte: `Outils → Carte`
4. Sélectionnez le port: `Outils → Port` (ex: `/dev/ttyUSB0` ou `COM3`)
5. Cliquez sur **Téléverser** (bouton flèche)

**Vérifiez:** Le message "LED built-in" devrait clignoter rapidement

### 3. Configurez Python

Éditez `config.py`:

```python
# Trouvez le port correct:
# Linux/Mac: ls /dev/ttyUSB* ou ls /dev/ttyACM*
# Windows: Regardez dans le Gestionnaire de périphériques

ARDUINO_PORT = '/dev/ttyUSB0'  # À ajuster selon votre système

# Ajustez les seuils de sensibilité si nécessaire
EYE_CLOSED_THRESHOLD = 0.2           # Plus bas = plus sensible
EYES_CLOSED_FRAMES_THRESHOLD = 10    # Frames consécutives
```

### 4. Lancez le script

```bash
python detection_yeux_fermes_arduino.py
```

---

## 📝 Fichiers du projet

- **`detection_yeux_fermes_arduino.py`** - Script principal Python
- **`config.py`** - Fichier de configuration
- **`arduino_code.ino`** - Code Arduino
- **`README.md`** - Ce fichier

---

## 🎮 Utilisation

1. Lancez le script
2. Accordez l'accès webcam si demandé
3. Une fenêtre OpenCV s'affiche

**Affichage:**
- **EAR** = Eye Aspect Ratio (plus bas = yeux plus fermés)
- **Frames fermées** = Nombre de frames consécutives avec yeux fermés
- **Statut** = "OK" ou "ALARME!"

**Comportement:**
- ✅ Yeux ouverts → LED et buzzer OFF
- 🔴 Yeux fermés > N frames → LED et buzzer ON
- 🟢 Yeux rouverts → LED et buzzer OFF

**Pour quitter:** Appuyez sur `Q`

---

## 🔧 Configuration avancée

### Ajustement des seuils (config.py)

**`EYE_CLOSED_THRESHOLD`**
- **Valeur actuelle:** 0.2
- **Augmenter si:** L'alarme se déclenche trop souvent (yeux à moitié fermés)
- **Diminuer si:** L'alarme ne se déclenche pas assez vite

**`EYES_CLOSED_FRAMES_THRESHOLD`**
- **Valeur actuelle:** 10 (≈0.33s à 30 FPS)
- **Augmenter si:** Trop de faux positifs (clignements normaux)
- **Diminuer si:** Vous voulez une détection plus rapide

**`SMOOTHING_WINDOW`**
- **Valeur actuelle:** 5
- **Augmente:** Lisse les tremblements, mais ajoute du délai
- **Diminue:** Réponse plus rapide, mais plus bruyant

### Modification des broches

Si vous utilisez des broches différentes:

**Arduino (arduino_code.ino):**
```cpp
const int LED_PIN = 13;      // Changez 13 par votre broche
const int BUZZER_PIN = 12;   // Changez 12 par votre broche
```

**Python:** Pas de modification nécessaire (gérée par Arduino)

### Utiliser le PWM pour l'intensité

Pour contrôler l'intensité avec PWM (variateur):

**Arduino:**
- Utilisez les fonctions `activateAlarmPWM()` et `deactivateAlarmPWM()`
- Les broches doivent supporter PWM: 3, 5, 6, 9, 10, 11
- Valeurs: 0-255 (0=OFF, 255=MAX)

---

## 📊 Dépannage

### "Impossible d'ouvrir la webcam"
```bash
# Vérifiez que la webcam fonctionne
# Linux:
ls -la /dev/video*

# Donnez les permissions
sudo usermod -a -G video $USER
```

### "Port Arduino non trouvé"
```bash
# Lister les ports disponibles
# Linux/Mac:
ls /dev/ttyUSB* /dev/ttyACM*

# Windows:
# Allez dans Gestionnaire de périphériques → Ports COM

# Modifiez config.py avec le bon port
ARDUINO_PORT = '/dev/ttyUSB0'  # À adapter
```

### "Arduino non connecté"
1. Vérifiez le câble USB
2. Regardez le port dans Arduino IDE: `Outils → Port`
3. Essayez un redémarrage: Débranchez/rebranchez Arduino

### La LED/Buzzer ne s'allume pas
1. Vérifiez le branchement (inversez si buzzer ne fait rien)
2. Testez manuellement dans Arduino IDE:
```cpp
digitalWrite(LED_PIN, HIGH);   // Allume
digitalWrite(LED_PIN, LOW);    // Éteint
```

### Faux positifs (alarme trop souvent)
- Augmentez `EYE_CLOSED_THRESHOLD` à 0.25-0.3
- Augmentez `EYES_CLOSED_FRAMES_THRESHOLD` à 15-20
- Améliorez l'éclairage de la caméra

### Faux négatifs (alarme ne se déclenche pas)
- Diminuez `EYE_CLOSED_THRESHOLD` à 0.15-0.18
- Diminuez `EYES_CLOSED_FRAMES_THRESHOLD` à 5-8
- Assurez-vous que MediaPipe détecte bien le visage

---

## 📚 Ressources

### MediaPipe
- [Face Mesh Documentation](https://google.github.io/mediapipe/solutions/face_mesh.html)
- [468 Landmarks Diagram](https://raw.githubusercontent.com/google/mediapipe/master/mediapipe/python/solutions/face_mesh_connections.py)

### Arduino
- [Arduino Official Site](https://www.arduino.cc/)
- [Arduino Serial Communication](https://docs.arduino.cc/tutorials/communication/serial-communication)

### PySerial
- [PySerial Documentation](https://pyserial.readthedocs.io/)

---

## 🔐 Améliorations possibles

1. **Enregistrement vidéo** - Sauvegarder les moments critiques
2. **Statistiques** - Tracer les périodes d'yeux fermés
3. **Notifications** - Envoyer des emails/SMS
4. **Interface GUI** - Panel de contrôle avec PyQt/Tkinter
5. **Machine Learning** - Classification des expressions faciales
6. **Base de données** - Logger les événements

---

## ⚖️ Licence

Libre d'utilisation et de modification.

---

## 💡 Tips

- **Améliora la précision:** Utilisez un bon éclairage frontal
- **Performance:** Diminuez la résolution vidéo (320x240) si lent
- **Fiabilité:** Testez plusieurs personnes et angles de vue
- **Arduino:** Gardez les distances de câble courtes pour éviter les interférences

---

**Besoin d'aide?** Consultez les logs en activant `DEBUG_MODE = True` dans config.py

---

*Créé pour les projets Python + Arduino avec MediaPipe*
