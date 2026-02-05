/*
 * CONTRÔLE LED + BUZZER DEPUIS PYTHON VIA SÉRIE
 * ================================================
 * 
 * Ce code Arduino reçoit des commandes via port série
 * pour activer/désactiver une LED et un buzzer.
 * 
 * BRANCHEMENT:
 * -----------
 * LED:
 *   - Broche positive: Pin 13 (ou modifier LED_PIN)
 *   - Broche négative: GND
 *   - Résistance: 220Ω entre pin et LED
 *
 * BUZZER:
 *   - Broche positive: Pin 12 (ou modifier BUZZER_PIN)
 *   - Broche négative: GND
 *   - Résistance (optionnel): 100Ω
 *
 * PROTOCOLE SÉRIE:
 * ----------------
 * Réception: "ON\n" ou "OFF\n"
 * Envoi: "LED:ON\n" ou "LED:OFF\n"
 * Vitesse: 9600 baud
 */

// ============= CONFIGURATION DES BROCHES =============
const int LED_PIN = 13;      // Broche pour la LED (PWM: 3, 5, 6, 9, 10, 11)
const int BUZZER_PIN = 12;   // Broche pour le buzzer (PWM: 3, 5, 6, 9, 10, 11)

// ============= VARIABLES D'ÉTAT =============
bool alarm_active = false;
unsigned long last_command_time = 0;
const unsigned long COMMAND_TIMEOUT = 5000;  // Timeout 5 secondes

// ============= SETUP =============
void setup() {
  // Initialise les broches
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Broches au repos
  digitalWrite(LED_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  
  // Initialise la liaison série
  Serial.begin(9600);
  
  // Message de démarrage
  delay(1000);  // Attendez que Arduino redémarre
  Serial.println("ARDUINO_READY");
  Serial.println("Configuration: LED=13, BUZZER=12");
  Serial.println("Envoyez 'ON' ou 'OFF' pour contrôler");
}

// ============= BOUCLE PRINCIPALE =============
void loop() {
  // Vérifie les données reçues
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Enlève les espaces
    command.toUpperCase();  // Convertit en majuscules
    
    last_command_time = millis();
    
    // Traite la commande
    if (command == "ON") {
      activateAlarm();
    }
    else if (command == "OFF") {
      deactivateAlarm();
    }
    else if (command == "STATUS") {
      sendStatus();
    }
    else if (command == "TEST") {
      testAlarm();
    }
    else {
      Serial.println("ERREUR: Commande inconnue - Utilisez ON, OFF, STATUS ou TEST");
    }
  }
  
  // Sécurité: désactive l'alarme si pas de commande depuis longtemps
  if (alarm_active && (millis() - last_command_time) > COMMAND_TIMEOUT) {
    Serial.println("TIMEOUT: Alarme désactivée automatiquement");
    deactivateAlarm();
  }
  
  delay(10);  // Petit délai pour éviter surcharge CPU
}

// ============= FONCTIONS =============

void activateAlarm() {
  if (!alarm_active) {
    digitalWrite(LED_PIN, HIGH);      // Allume la LED
    digitalWrite(BUZZER_PIN, HIGH);   // Active le buzzer
    alarm_active = true;
    
    Serial.println("ALARME_ACTIVE");
    Serial.print("LED: ON | BUZZER: ON | Temps: ");
    Serial.println(millis());
  }
}

void deactivateAlarm() {
  if (alarm_active) {
    digitalWrite(LED_PIN, LOW);       // Éteint la LED
    digitalWrite(BUZZER_PIN, LOW);    // Désactive le buzzer
    alarm_active = false;
    
    Serial.println("ALARME_INACTIVE");
    Serial.print("LED: OFF | BUZZER: OFF | Temps: ");
    Serial.println(millis());
  }
}

void sendStatus() {
  Serial.print("STATUS: ");
  Serial.print("LED=");
  Serial.print(digitalRead(LED_PIN) ? "ON" : "OFF");
  Serial.print(" | BUZZER=");
  Serial.println(digitalRead(BUZZER_PIN) ? "ON" : "OFF");
}

void testAlarm() {
  Serial.println("TEST: Activation pendant 2 secondes...");
  activateAlarm();
  delay(2000);
  deactivateAlarm();
  Serial.println("TEST: Terminé");
}

// ============= VERSION PWM (OPTIONNEL) =============
/*
 * Pour contrôler l'intensité avec PWM (Pulse Width Modulation),
 * utilisez ces fonctions à la place:

void activateAlarmPWM(int led_brightness = 255, int buzzer_volume = 255) {
  analogWrite(LED_PIN, led_brightness);
  analogWrite(BUZZER_PIN, buzzer_volume);
  alarm_active = true;
  Serial.print("ALARME_PWM: LED=");
  Serial.print(led_brightness);
  Serial.print(" BUZZER=");
  Serial.println(buzzer_volume);
}

void deactivateAlarmPWM() {
  analogWrite(LED_PIN, 0);
  analogWrite(BUZZER_PIN, 0);
  alarm_active = false;
  Serial.println("ALARME_PWM_OFF");
}

 * Dans setup(), remplacez pinMode par:
 *   pinMode(LED_PIN, OUTPUT);
 *   pinMode(BUZZER_PIN, OUTPUT);
 */
