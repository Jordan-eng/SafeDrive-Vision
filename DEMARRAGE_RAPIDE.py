"""
GUIDE DE DÉMARRAGE RAPIDE
========================

Suivez ces étapes pour faire fonctionner le système
"""

ETAPES = """

╔═══════════════════════════════════════════════════════════════╗
║                   🚀 DÉMARRAGE RAPIDE 🚀                     ║
╚═══════════════════════════════════════════════════════════════╝

ÉTAPE 1️⃣  - PRÉPARATION
════════════════════════════════════════════════════════════════

[ ] Installer Arduino IDE (https://www.arduino.cc/en/software)
[ ] Connecter votre carte Arduino via USB
[ ] Installer les dépendances Python:
    bash install.sh

ÉTAPE 2️⃣  - BRANCHEMENT ÉLECTRONIQUE
════════════════════════════════════════════════════════════════

Schéma pour Arduino Uno:

    +5V ───────┬─────────────┬─────────────┬─── GND
              │             │             │
           [220Ω]       [Buzzer]         │
              │             │             │
    Pin 13 ───┴─LED+    Pin 12 ──────────┴─ Buzzer-
    GND ───────────────────────────────────────────

✓ LED (broche 13):
  - Longue broche (anode) via résistance 220Ω
  - Courte broche (cathode) vers GND

✓ Buzzer (broche 12):
  - Broche positive vers Pin 12
  - Broche négative vers GND

ÉTAPE 3️⃣  - CHARGER LE CODE ARDUINO
════════════════════════════════════════════════════════════════

1. Ouvrir Arduino IDE
2. Copier le contenu de "arduino_code.ino"
3. Coller dans un nouveau sketch
4. Sélectionner votre carte: Outils → Carte
5. Sélectionner le port: Outils → Port → /dev/ttyUSB0 (ou autre)
6. Cliquer sur Téléverser (bouton flèche)

✓ Vous devriez voir les messages:
  "Téléversement effectué avec succès"

ÉTAPE 4️⃣  - CONFIGURATION PYTHON
════════════════════════════════════════════════════════════════

Éditez "config.py" et trouvez votre port Arduino:

Linux/Mac:
  $ ls /dev/ttyUSB*      # Affiche: /dev/ttyUSB0 (ou autre)
  $ ls /dev/ttyACM*      # Alternative

Windows:
  Gestionnaire de périphériques → Ports COM

Modifiez ensuite config.py:
  ARDUINO_PORT = '/dev/ttyUSB0'  # À adapter

ÉTAPE 5️⃣  - TESTS
════════════════════════════════════════════════════════════════

✓ Test 1 - Diagnostic complet:
  python3 test_diagnostic.py

✓ Test 2 - Contrôle manuel Arduino:
  python3 test_arduino_manual.py
  Entrez: ON, OFF, STATUS, TEST

✓ Les DEL/Buzzer doivent réagir!

ÉTAPE 6️⃣  - LANCEMENT DU SYSTÈME
════════════════════════════════════════════════════════════════

python3 detection_yeux_fermes_arduino.py

✓ Une fenêtre vidéo s'affiche
✓ Affichage en temps réel:
  - EAR (Eye Aspect Ratio)
  - Nombre de frames avec yeux fermés
  - Statut (OK / ALARME)

Fermez les yeux quelques secondes:
  → LED s'allume
  → Buzzer sonne
  → Affichage passe à "ALARME"

Rouvrez les yeux:
  → LED s'éteint
  → Buzzer s'arrête
  → Affichage revient à "OK"

═════════════════════════════════════════════════════════════════

🎯 UTILISATION QUOTIDIENNE

1. Lancez le script:
   python3 detection_yeux_fermes_arduino.py

2. Attendez la calibration (quelques frames)

3. Travaillez normalement - l'alarme se déclenche si yeux fermés

4. Appuyez sur 'Q' pour quitter

═════════════════════════════════════════════════════════════════

⚙️ AJUSTEMENT DE LA SENSIBILITÉ (config.py)

Trop de faux positifs (alarme trop souvent)?
  ↑ Augmentez EYE_CLOSED_THRESHOLD à 0.25-0.3

Pas assez sensible?
  ↓ Diminuez EYE_CLOSED_THRESHOLD à 0.15-0.18

Réaction trop lente?
  ↓ Diminuez EYES_CLOSED_FRAMES_THRESHOLD à 5-8

Réaction trop rapide (clignements)?
  ↑ Augmentez EYES_CLOSED_FRAMES_THRESHOLD à 15-20

═════════════════════════════════════════════════════════════════

❌ DÉPANNAGE

❌ "Port Arduino non trouvé"
  → Vérifiez le câble USB
  → Lancez: ls /dev/ttyUSB* ou COM*
  → Modifiez config.py

❌ "LED/Buzzer ne s'allument pas"
  → Vérifiez le branchement
  → Testez avec test_arduino_manual.py
  → Inversez les fils (surtout le buzzer)

❌ "Détection qui ne marche pas"
  → Bonne lumière sur le visage
  → Visage bien centré dans la webcam
  → Lunettes/masques peuvent gêner

❌ "Aucun visage détecté"
  → Vous rapprochez de la caméra
  → Meilleure lumière
  → Vérifiez que OpenCV/MediaPipe sont bien installés

═════════════════════════════════════════════════════════════════

📞 SUPPORT

Consultez README.md pour la documentation complète
Consultez les commentaires dans les fichiers .py

═════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(ETAPES)
