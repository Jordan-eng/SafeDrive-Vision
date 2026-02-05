# 📑 INDEX DU PROJET - Détection Yeux Fermés + Arduino

## 📍 Navigation rapide

### 🚀 **Pour commencer** (commencez ici!)
1. **[DEMARRAGE_RAPIDE.py](DEMARRAGE_RAPIDE.py)** - Guide pas à pas
2. **[RESUME.md](RESUME.md)** - Vue d'ensemble complète
3. **[README.md](README.md)** - Documentation détaillée

### 💻 **Code principal** (À utiliser)
1. **[detection_yeux_fermes_arduino.py](detection_yeux_fermes_arduino.py)** - Le script principal
   - Détecte les yeux fermés
   - Contrôle l'Arduino
   - Affiche vidéo en temps réel

2. **[config.py](config.py)** - Configuration du système
   - Port Arduino
   - Seuils de détection
   - Paramètres vidéo

3. **[arduino_code.ino](arduino_code.ino)** - Code à téléverser sur Arduino
   - Gère LED et Buzzer
   - Protocole série

### 🧪 **Tests et diagnostique** (Pour valider installation)
1. **[test_diagnostic.py](test_diagnostic.py)** - Test complet du système
   - Vérifie toutes les dépendances
   - Teste configuration
   - Vérifie connexion Arduino

2. **[test_arduino_manual.py](test_arduino_manual.py)** - Contrôle manuel Arduino
   - Teste LED/Buzzer directement
   - Utile pour dépannage

3. **[trouve_arduino.py](trouve_arduino.py)** - Localise le port Arduino
   - Liste ports disponibles
   - Teste la connexion

4. **[test_performance.py](test_performance.py)** - Benchmark système
   - Teste caméra
   - Performance MediaPipe
   - Affiche FPS réels

### 🎮 **Exemples** (Pour apprendre)
1. **[exemples_avances.py](exemples_avances.py)** - Exemples d'utilisation avancée
   - Alarme progressive
   - Enregistrement vidéo
   - Statistiques

### ⚙️ **Configuration** (Pour utilisateurs avancés)
1. **[config_advanced.py](config_advanced.py)** - Paramètres avancés
   - Logging
   - Base de données
   - PWM
   - Profils personnalisés

### 📦 **Installation** (Une seule fois)
1. **[install.sh](install.sh)** - Script d'installation
   - Installe les dépendances Python
   - Configure l'environnement

---

## 🗺️ Flux de travail recommandé

```
1. LECTURE
   ├─ DEMARRAGE_RAPIDE.py  ← Lisez d'abord!
   ├─ RESUME.md            ← Vue d'ensemble
   └─ README.md            ← Détails complets

2. INSTALLATION
   ├─ bash install.sh      ← Installez dépendances
   └─ python3 trouve_arduino.py  ← Trouvez port Arduino

3. CONFIGURATION
   ├─ Éditez config.py     ← Mettez le bon port
   └─ Chargez arduino_code.ino sur Arduino

4. TESTS
   ├─ test_diagnostic.py   ← Vérifie tout
   ├─ test_arduino_manual.py  ← Teste LED/Buzzer
   └─ test_performance.py  ← Vérifiez FPS

5. UTILISATION
   └─ python3 detection_yeux_fermes_arduino.py  ← C'est parti!

6. PERSONNALISATION (optionnel)
   ├─ exemples_avances.py  ← Autres fonctionnalités
   └─ config_advanced.py   ← Réglages avancés
```

---

## 📊 Matrice de fichiers

| Catégorie | Fichier | Type | Utilité |
|-----------|---------|------|---------|
| **Documentation** | README.md | Markdown | Guide complet |
| | RESUME.md | Markdown | Vue d'ensemble |
| | DEMARRAGE_RAPIDE.py | Python | Guide interactif |
| | INDEX.md | Markdown | Ce fichier |
| **Principal** | detection_yeux_fermes_arduino.py | Python | Programme principal |
| | config.py | Python | Configuration |
| | arduino_code.ino | Arduino | Code Arduino |
| **Tests** | test_diagnostic.py | Python | Diagnostic complet |
| | test_arduino_manual.py | Python | Contrôle Arduino |
| | test_performance.py | Python | Benchmark |
| | trouve_arduino.py | Python | Localise Arduino |
| **Exemples** | exemples_avances.py | Python | Utilisations avancées |
| **Avancé** | config_advanced.py | Python | Paramètres avancés |
| **Installation** | install.sh | Bash | Script installation |

---

## 🔍 Trouver ce que vous cherchez

### "Comment installer?"
→ [install.sh](install.sh) + [DEMARRAGE_RAPIDE.py](DEMARRAGE_RAPIDE.py)

### "Comment brancher le circuit?"
→ [README.md](README.md) section "Branchement"

### "Le port Arduino ne s'affiche pas"
→ [trouve_arduino.py](trouve_arduino.py)

### "Comment changer la sensibilité?"
→ [config.py](config.py) → `EYE_CLOSED_THRESHOLD`

### "Je veux enregistrer une vidéo"
→ [exemples_avances.py](exemples_avances.py) → Fonction `exemple_sauvegarde_video()`

### "Comment utiliser PWM?"
→ [config_advanced.py](config_advanced.py) + [arduino_code.ino](arduino_code.ino) commentaires PWM

### "Les tests échouent"
→ [test_diagnostic.py](test_diagnostic.py) → Section dépannage

### "Je veux faire un alarme progressive"
→ [exemples_avances.py](exemples_avances.py) → Fonction `exemple_alarme_progressive()`

### "FPS trop bas"
→ [test_performance.py](test_performance.py) puis [config_advanced.py](config_advanced.py) → `REDUCE_RESOLUTION`

---

## 📋 Checklist d'installation complète

- [ ] **Lire:** DEMARRAGE_RAPIDE.py
- [ ] **Installer:** `bash install.sh`
- [ ] **Localiser:** `python3 trouve_arduino.py`
- [ ] **Configurer:** Éditer config.py
- [ ] **Charger:** arduino_code.ino sur Arduino
- [ ] **Tester:** `python3 test_diagnostic.py`
- [ ] **Tester Arduino:** `python3 test_arduino_manual.py`
- [ ] **Lancer:** `python3 detection_yeux_fermes_arduino.py`

---

## 🎯 Structure logique des dépendances

```
detection_yeux_fermes_arduino.py
├─ Dépend: config.py
├─ Dépend: cv2 (OpenCV)
├─ Dépend: mediapipe
├─ Dépend: pyserial
└─ Dépend: numpy

config.py
└─ Paramètres simples (pas de dépendances)

arduino_code.ino
└─ Code Arduino simple (pas de dépendances Python)

test_diagnostic.py
├─ Dépend: config.py
├─ Dépend: cv2, mediapipe, pyserial
└─ Auto-suffisant (tests tout)

exemples_avances.py
├─ Dépend: detection_yeux_fermes_arduino.py
└─ Dépend: config.py
```

---

## ⚡ Commandes rapides

```bash
# Installation
bash install.sh

# Trouvez le port Arduino
python3 trouve_arduino.py

# Testez tout
python3 test_diagnostic.py

# Testez Arduino
python3 test_arduino_manual.py

# Lancez le système
python3 detection_yeux_fermes_arduino.py

# Performance
python3 test_performance.py

# Exemples avancés
python3 exemples_avances.py
```

---

## 📞 Support rapide

| Question | Réponse |
|----------|---------|
| "Où commencer?" | DEMARRAGE_RAPIDE.py |
| "Comment ça marche?" | README.md |
| "Mon Arduino ne se voit pas?" | trouve_arduino.py |
| "LED ne s'allume pas?" | test_arduino_manual.py |
| "Trop de faux positifs?" | config.py → EYE_CLOSED_THRESHOLD |
| "Performance insuffisante?" | test_performance.py |

---

## 🎓 Progression d'apprentissage

### Débutant
1. Lisez DEMARRAGE_RAPIDE.py
2. Installez avec install.sh
3. Lancez detection_yeux_fermes_arduino.py

### Intermédiaire
1. Lisez README.md complètement
2. Modifiez config.py pour affiner
3. Essayez test_arduino_manual.py

### Avancé
1. Utilisez exemples_avances.py
2. Modifiez config_advanced.py
3. Explorez le code source

---

## 📈 Optimisation progressive

1. **Installation de base** → Works? → ✅
2. **Ajuster sensibilité** (config.py) → Better? → ✅
3. **Optimiser FPS** (config_advanced.py) → Faster? → ✅
4. **Ajouter logging** (config_advanced.py) → Traçable? → ✅
5. **Personnaliser** (exemples_avances.py) → Parfait! → ✅

---

**Dernière mise à jour:** 8 décembre 2025
**Version:** 1.0 Complète
**Status:** ✅ Production-ready
