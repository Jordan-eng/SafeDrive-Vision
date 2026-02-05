"""
CONTRÔLE MANUEL ARDUINO - POUR TESTS
====================================

Permet de tester la LED et le buzzer sans la détection vidéo.
Utile pour vérifier que le branchement Arduino fonctionne correctement.
"""

from serial import Serial
import time
import sys
from config import CONFIG


class ArduinoTester:
    """Testeur Arduino simple"""
    
    def __init__(self):
        self.port = CONFIG['arduino_port']
        self.baudrate = CONFIG['arduino_baudrate']
        self.ser = None
        self.connect()
    
    def connect(self):
        """Connexion Arduino"""
        try:
            self.ser = Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            print(f"✓ Connecté à {self.port}")
            return True
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def send(self, command):
        """Envoie une commande"""
        try:
            self.ser.write((command + '\n').encode())
            response = self.ser.readline().decode().strip()
            return response
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return None
    
    def close(self):
        """Ferme la connexion"""
        if self.ser:
            self.ser.close()
            print("✓ Connexion fermée")


def main():
    print("\n" + "=" * 50)
    print("  TESTEUR ARDUINO - LED & BUZZER")
    print("=" * 50 + "\n")
    
    tester = ArduinoTester()
    if not tester.ser:
        print("✗ Impossible de se connecter à Arduino")
        return
    
    print("\nCommandes disponibles:")
    print("  ON      - Allume LED et Buzzer")
    print("  OFF     - Éteint LED et Buzzer")
    print("  STATUS  - Affiche l'état")
    print("  TEST    - Test automatique (2 secondes)")
    print("  QUIT    - Quitter")
    print()
    
    while True:
        try:
            cmd = input(">>> ").strip().upper()
            
            if cmd == "QUIT":
                break
            
            if cmd in ["ON", "OFF", "STATUS", "TEST"]:
                response = tester.send(cmd)
                if response:
                    print(f"Réponse: {response}\n")
            else:
                print("Commande inconnue. Utilisez: ON, OFF, STATUS, TEST, QUIT\n")
        
        except KeyboardInterrupt:
            print("\n\nInterruption utilisateur")
            break
    
    tester.close()
    print("\n✓ Programme terminé\n")


if __name__ == "__main__":
    main()
