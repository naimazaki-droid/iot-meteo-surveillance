// ========================================
// Système Météo IoT — ThingSpeak
// TMP36 → A0 | Potentiomètre → A1
// API Key : 58FIMZ3BV41AY5X0
// ========================================

String apiKey = "58FIMZ3BV41AY5X0";

int pinTemp  = A0;
int pinHumid = A1;

float temperature = 0;
float humidite    = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("=== Système Météo IoT démarré ===");
  delay(2000);
}

void loop() {

  // --- Lecture TMP36 (température) ---
  int valTemp   = analogRead(pinTemp);
  float voltage = valTemp * (5.0 / 1023.0);
  temperature   = (voltage - 0.5) * 100.0;

  // --- Lecture Potentiomètre (humidité simulée) ---
  int valHumid = analogRead(pinHumid);
  humidite     = map(valHumid, 0, 1023, 0, 100);

  // --- Affichage moniteur série ---
  Serial.println("-----------------------------");
  Serial.print("Température : ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.print("Humidité    : ");
  Serial.print(humidite);
  Serial.println(" %");

  // --- Envoi vers ThingSpeak ---
  Serial.print("Envoi → ThingSpeak | API: ");
  Serial.println(apiKey);
  Serial.print("field1=");
  Serial.print(temperature);
  Serial.print(" | field2=");
  Serial.println(humidite);

  delay(15000); // attendre 15 secondes (limite ThingSpeak)
}
