"""
Système de surveillance météorologique basé sur l'IoT
Étape 3 : Envoi des données vers le cloud (MQTT)

Tinkercad simule la carte Arduino entièrement dans le navigateur : il n'y a
donc pas de port série réel accessible depuis ce PC. Ce script reproduit la
même logique de mesure que meteo_iot.ino (température + humidité simulée)
et publie le résultat sur un broker MQTT local (amqtt), lancé sur ce PC
avec la commande "amqtt".

Si tu obtiens une vraie carte Arduino Uno avec ce même code chargé dessus,
remplace juste la fonction lire_capteurs() par la version "lecture série"
donnée en commentaire plus bas : tout le reste du script reste identique.
"""

import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/meteo/super_albar"
INTERVALLE = 5  # secondes entre deux mesures

# --- État simulé (variation réaliste, comme le potentiomètre qu'on tourne à la main) ---
_temperature = 23.0
_humidite = 50.0


def lire_capteurs():
    """Génère une nouvelle mesure, avec une légère variation aléatoire
    (mêmes plages que le TMP36 + potentiomètre dans Tinkercad)."""
    global _temperature, _humidite
    _temperature += random.uniform(-0.3, 0.3)
    _temperature = max(18.0, min(30.0, _temperature))
    _humidite += random.uniform(-5, 5)
    _humidite = max(0.0, min(100.0, _humidite))
    return round(_temperature, 2), round(_humidite, 2)


# --- Pour une vraie carte Arduino branchée en USB, remplacer lire_capteurs() par : ---
#
# import serial
# ser = serial.Serial("COM5", 9600, timeout=2)  # adapter le port COM
#
# def lire_capteurs():
#     ligne = ser.readline().decode(errors="ignore").strip()
#     # ligne ressemble à "TEMP:24.71,HUM:65.00"
#     temp = float(ligne.split(",")[0].split(":")[1])
#     hum = float(ligne.split(",")[1].split(":")[1])
#     return temp, hum


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Connecté au broker {BROKER}:{PORT}")
    else:
        print(f"Échec de connexion, code {reason_code}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            temperature, humidite = lire_capteurs()
            payload = json.dumps({"temperature": temperature, "humidity": humidite})
            client.publish(TOPIC, payload, qos=1)
            print(f"Publié sur {TOPIC} : {payload}")
            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        print("Arrêt du script")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
