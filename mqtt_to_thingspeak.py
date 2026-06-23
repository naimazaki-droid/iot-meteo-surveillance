"""
Système de surveillance météorologique basé sur l'IoT
Étape 4 : pont MQTT -> ThingSpeak

Ce script s'abonne au topic MQTT publié par mqtt_publisher.py sur le broker
local (amqtt), puis transfère chaque mesure vers le canal
ThingSpeak (Field1 = Température, Field2 = Humidité).

IMPORTANT avant de publier ce projet sur GitHub :
Ne laisse pas ta vraie clé API en clair dans un fichier versionné. Le plus
simple est de définir une variable d'environnement sur ton PC :

    Windows (cmd) :  set THINGSPEAK_API_KEY=AOODRJWRR87R9EKY
    Windows (PowerShell) :  $env:THINGSPEAK_API_KEY="AOODRJWRR87R9EKY"

et de laisser le code ci-dessous tel quel (il lit déjà la variable
d'environnement, avec la clé donnée comme valeur par défaut juste pour que
tu puisses tester rapidement).
"""

import os
import time
import json
import requests
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/meteo/super_albar"

THINGSPEAK_API_KEY = os.environ.get("THINGSPEAK_API_KEY", "JHQGVDCJW7U78RCO")
THINGSPEAK_URL = "https://api.thingspeak.com/update"

INTERVALLE_MIN_THINGSPEAK = 15  # secondes, limite du compte gratuit ThingSpeak
_derniere_maj = 0.0


def envoyer_vers_thingspeak(temperature, humidite):
    global _derniere_maj
    maintenant = time.time()
    if maintenant - _derniere_maj < INTERVALLE_MIN_THINGSPEAK:
        print("Ignoré (trop tôt pour ThingSpeak, limite 15s)")
        return

    params = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": temperature,
        "field2": humidite,
    }
    try:
        reponse = requests.get(THINGSPEAK_URL, params=params, timeout=10)
        if reponse.text.strip() == "0":
            print("ThingSpeak a refusé la mise à jour (clé invalide ou trop rapide)")
        else:
            print(f"Envoyé à ThingSpeak (entrée n°{reponse.text.strip()}) : "
                  f"temp={temperature}, hum={humidite}")
        _derniere_maj = maintenant
    except requests.RequestException as e:
        print(f"Erreur réseau vers ThingSpeak : {e}")


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Connecté au broker {BROKER}, abonnement à {TOPIC}")
        client.subscribe(TOPIC)
    else:
        print(f"Échec de connexion, code {reason_code}")


def on_message(client, userdata, msg):
    try:
        donnees = json.loads(msg.payload.decode())
        temperature = donnees["temperature"]
        humidite = donnees["humidity"]
        print(f"Reçu sur {msg.topic} : temp={temperature}, hum={humidite}")
        envoyer_vers_thingspeak(temperature, humidite)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Message MQTT invalide ignoré : {e}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
