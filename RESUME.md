# 📋 RÉSUMÉ DU PROJET

## 🎯 Objectif
Créer un système de détection des yeux fermés en temps réel qui active une LED et un buzzer via Arduino.

---

## 📁 Fichiers du projet

### Fichiers Python

| Fichier | Description |
|---------|-------------|
| `detection_yeux_fermes_arduino.py` | **PRINCIPAL** - Détecte les yeux fermés et contrôle Arduino |
| `config.py` | Configuration (port Arduino, seuils, etc.) |
| `test_diagnostic.py` | Teste toutes les dépendances et la configuration |
| `test_arduino_manual.py` | Contrôle manuel LED/Buzzer via commandes |
| `trouve_arduino.py` | Trouve et teste les ports Arduino disponibles |
| `exemples_avances.py` | Exemples d'utilisation avancée |
| `DEMARRAGE_RAPIDE.py` | Guide étape par étape |

### Fichiers Arduino

| Fichier | Description |
|---------|-------------|
| `arduino_code.ino` | Code Arduino - À téléverser sur la carte |

### Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation complète du projet |
| `install.sh` | Script d'installation des dépendances |
| `RESUME.md` | Ce fichier |

---

## ⚡ Démarrage rapide

### 1. Installation (5 min)
```bash
bash install.sh
python3 trouve_arduino.py
```

### 2. Configuration (5 min)
```bash
# Éditez config.py
ARDUINO_PORT = '/dev/ttyUSB0'  # À adapter
```

### 3. Chargement Arduino (10 min)
- Ouvrir Arduino IDE
- Copier `arduino_code.ino`
- Téléverser sur votre carte

### 4. Tests (5 min)
```bash
python3 test_diagnostic.py
python3 test_arduino_manual.py
```

### 5. Lancement
```bash
python3 detection_yeux_fermes_arduino.py
```

---

## 🔧 Branchement Arduino

```
        +5V ─────────────────┬─────────────────┬─── GND
                             │                 │
                          [220Ω]           [Buzzer]
                             │                 │
        Pin 13 ──────────────┴─ Anode LED    Pin 12 ──────────────┴─ Cathode
        GND ────────────────────────────────────────────────────────────────
```

- **LED (Pin 13):** 220Ω résistance + anode vers pin, cathode vers GND
- **Buzzer (Pin 12):** Broche positive vers pin, négative vers GND

---

## ⚙️ Configuration principale (config.py)

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `ARDUINO_PORT` | `/dev/ttyUSB0` | Port série Arduino |
| `EYE_CLOSED_THRESHOLD` | `0.2` | Seuil pour détecter yeux fermés (↓ = plus sensible) |
| `EYES_CLOSED_FRAMES_THRESHOLD` | `10` | Frames consécutives requises (~0.33s à 30 FPS) |
| `SMOOTHING_WINDOW` | `5` | Lissage détection |

---

## 🚀 Fonctionnement

### Détecteur (MediaPipe)
1. Capture vidéo de la webcam
2. Extrait 468 points de repère faciaux
3. Calcule Eye Aspect Ratio (EAR) pour chaque oeil
4. Détecte yeux fermés si EAR < seuil

### Alarme
1. Si yeux fermés > N frames → Active LED + Buzzer
2. Si yeux rouverts → Désactive LED + Buzzer
3. Communication série avec Arduino

---

## 📊 Affichage en temps réel

```
┌─────────────────────────────────┐
│ EAR: 0.15                   ALARME! │
│ Frames fermees: 15/10           │
│ FPS: 30                         │
│ [Vidéo avec points oeil détectés] │
└─────────────────────────────────┘
```

---

## ✅ Checklist d'installation

- [ ] Python 3.8+ installé
- [ ] Dépendances Python installées (`pip install opencv-python mediapipe pyserial`)
- [ ] Arduino connecté via USB
- [ ] Code Arduino téléversé
- [ ] Port Arduino identifié et configuré
- [ ] Branchement LED + Buzzer vérifié
- [ ] Tests passés (`test_diagnostic.py`)
- [ ] Prêt à lancer!

---

## 🎮 Commandes clavier

| Touche | Action |
|--------|--------|
| `Q` | Quitter le programme |

---

## 🔍 Dépannage rapide

| Problème | Solution |
|----------|----------|
| Port Arduino non trouvé | `python3 trouve_arduino.py` |
| LED/Buzzer ne s'allument pas | Vérifier branchement, tester avec `test_arduino_manual.py` |
| Détection ne marche pas | Bonne lumière, visage bien centré |
| Trop de faux positifs | ↑ Augmenter `EYE_CLOSED_THRESHOLD` |
| Pas assez sensible | ↓ Diminuer `EYE_CLOSED_THRESHOLD` |

---

## 📈 Améliorations futures

- [ ] Détection plusieurs personnes
- [ ] Enregistrement vidéo des événements
- [ ] Interface GUI (PyQt/Tkinter)
- [ ] Base de données pour logging
- [ ] PWM pour intensité graduée
- [ ] Notifications email/SMS
- [ ] Machine Learning pour expressions

---

## 📚 Ressources

- **MediaPipe:** https://google.github.io/mediapipe/solutions/face_mesh.html
- **Arduino:** https://www.arduino.cc/
- **PySerial:** https://pyserial.readthedocs.io/
- **OpenCV:** https://opencv.org/

---

## 👨‍💻 Pour commencer

```bash
# 1. Installer les dépendances
bash install.sh

# 2. Trouver le port Arduino
python3 trouve_arduino.py

# 3. Éditer config.py avec le bon port

# 4. Téléverser arduino_code.ino sur votre carte

# 5. Tester
python3 test_diagnostic.py

# 6. Lancer!
python3 detection_yeux_fermes_arduino.py
```

---

**Status:** ✅ Projet complet et prêt à utiliser!
