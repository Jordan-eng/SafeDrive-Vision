#!/usr/bin/env python3
"""
TROUVEUR DE PORTS ARDUINO
=========================

Affiche les ports série disponibles et aide à identifier Arduino
"""

import sys
import platform


def find_serial_ports():
    """Trouve les ports série disponibles"""
    
    system = platform.system()
    ports = []
    
    if system == "Linux":
        import glob
        ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    
    elif system == "Darwin":  # macOS
        import glob
        ports = glob.glob("/dev/tty.usbserial*") + glob.glob("/dev/tty.usbmodem*")
    
    elif system == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"HARDWARE\DEVICEMAP\SERIALCOMM")
            for i in range(winreg.QueryInfoKey(key)[1]):
                name, value, _ = winreg.EnumValue(key, i)
                ports.append(value)
        except:
            pass
    
    return ports


def get_port_info(port):
    """Récupère les infos du port"""
    
    try:
        import serial
        ser = serial.Serial(port, 9600, timeout=0.5)
        
        # Essaie de lire un message Arduino
        ser.write(b"STATUS\n")
        response = ser.read(100).decode('utf-8', errors='ignore')
        
        ser.close()
        
        return True, response.strip() if response else "Pas de réponse"
    
    except Exception as e:
        return False, str(e)


def main():
    """Fonction principale"""
    
    print("\n" + "=" * 60)
    print("  🔍 TROUVEUR DE PORTS ARDUINO")
    print("=" * 60)
    print(f"Système: {platform.system()} {platform.release()}\n")
    
    # Cherche les ports
    print("Recherche des ports série disponibles...\n")
    ports = find_serial_ports()
    
    if not ports:
        print("⚠️  Aucun port série détecté.")
        print("\nVérifiez que:")
        print("  1. Arduino est connecté via USB")
        print("  2. Le câble USB fonctionne")
        print("  3. Les drivers CH340 (ou autre) sont installés")
        print("\nLinux: Essayez aussi:")
        print("  sudo dmesg | tail  (pour voir les messages USB)")
        print("  ls -la /dev/ttyUSB* /dev/ttyACM*")
    else:
        print(f"✓ {len(ports)} port(s) trouvé(s):\n")
        
        for i, port in enumerate(ports, 1):
            print(f"Port {i}: {port}")
            
            # Essaie de se connecter
            success, info = get_port_info(port)
            if success:
                print(f"  ✓ Accessible - {info}")
            else:
                print(f"  ⚠️  Pas accessible - {info}")
            print()
        
        print("=" * 60)
        print("\nFichier config.py:")
        print("-" * 60)
        for i, port in enumerate(ports, 1):
            print(f"  Option {i}: ARDUINO_PORT = '{port}'")
        print("\nChoisissez l'option correspondant à votre Arduino\n")
    
    # Teste la connexion
    if ports:
        print("=" * 60)
        choice = input("\nTester un port? Entrez son chemin (ou ENTER pour skiper): ").strip()
        
        if choice:
            try:
                print("\nTest de connexion...")
                import serial
                ser = serial.Serial(choice, 9600, timeout=1)
                
                print("✓ Connexion établie")
                print("\nEnvoi de TEST...")
                ser.write(b"TEST\n")
                
                import time
                time.sleep(2.5)
                
                response = ser.read(500).decode('utf-8', errors='ignore')
                ser.close()
                
                print(f"\nRéponse Arduino:\n{response}")
                print("✓ Arduino semble fonctionner!")
            
            except Exception as e:
                print(f"✗ Erreur: {e}")
                print("Arduino non trouvé ou port incorrect")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Interrompu par l'utilisateur")
        sys.exit(1)
