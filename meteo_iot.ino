/*
 * Système de surveillance météorologique basé sur l'IoT
 * Étape 2 : Simulation des capteurs et du microcontrôleur (Tinkercad)
 *
 * Capteurs :
 *  - TMP36         -> broché sur A1 (mesure de température)
 *  - Potentiomètre -> broché sur A2 (simulation de l'humidité)
 *
 * Sortie : moniteur série, format "TEMP:xx.xx,HUM:xx.xx"
 *          (lu ensuite par mqtt_publisher.py sur le PC)
 */

const int pinTemp = A1;   // TMP36
const int pinHum  = A2;   // Potentiomètre

void setup() {
  Serial.begin(9600);
}

void loop() {
  // --- Lecture température (TMP36) ---
  int lectureTemp = analogRead(pinTemp);
  float tensionTemp = lectureTemp * (5.0 / 1024.0);   // conversion en volts
  float temperatureC = (tensionTemp - 0.5) * 100.0;   // formule TMP36

  // --- Lecture humidité simulée (potentiomètre) ---
  int lectureHum = analogRead(pinHum);
  float humidite = map(lectureHum, 0, 1023, 0, 100);  // ramené en %

  // --- Envoi sur le moniteur série ---
  Serial.print("TEMP:");
  Serial.print(temperatureC, 2);
  Serial.print(",HUM:");
  Serial.println(humidite, 2);

  delay(2000); // une mesure toutes les 2 secondes
}
