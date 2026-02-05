#!/bin/bash

# 🚀 SCRIPT D'INSTALLATION RAPIDE
# ==============================
# Installe toutes les dépendances et prépare l'environnement

echo "╔════════════════════════════════════════════════════════╗"
echo "║  🚀 Installation - Détection Yeux Fermés + Arduino     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Vérify Python
echo "📌 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 non trouvé. Installez-le avec:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION trouvé"
echo ""

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
echo "  - opencv-python"
echo "  - mediapipe"
echo "  - pyserial"
echo "  - numpy"
echo ""

pip3 install opencv-python mediapipe pyserial numpy

if [ $? -eq 0 ]; then
    echo "✓ Dépendances installées avec succès"
else
    echo "✗ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "✓ INSTALLATION TERMINÉE!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📝 Prochaines étapes:"
echo ""
echo "1️⃣  Chargez le code Arduino:"
echo "   - Ouvrez Arduino IDE"
echo "   - Copier-collez le contenu de arduino_code.ino"
echo "   - Cliquez sur Téléverser"
echo ""
echo "2️⃣  Configurez le port Arduino:"
echo "   - Éditez config.py"
echo "   - Trouvez votre port: ls /dev/ttyUSB* ou ls /dev/ttyACM*"
echo "   - Modifiez ARDUINO_PORT avec le bon port"
echo ""
echo "3️⃣  Testez l'installation:"
echo "   python3 test_diagnostic.py"
echo ""
echo "4️⃣  Lancez le système:"
echo "   python3 detection_yeux_fermes_arduino.py"
echo ""
echo "📚 Documentation: Consultez README.md"
echo ""
