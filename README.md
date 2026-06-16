# iot-meteo-surveillance

Système de surveillance météorologique IoT (simulation Tinkercad)

## Description
Ce projet simule un système IoT qui collecte la température 
et l'humidité via des capteurs Arduino, puis transmet les 
données vers une plateforme cloud (ThingSpeak) pour un 
affichage en temps réel.

## Composants
- Arduino UNO
- Capteur de température TMP36 (broche A0)
- Potentiomètre simulant l'humidité (broche A1)

## Outils utilisés
- Tinkercad : simulation du circuit et programmation Arduino
- ThingSpeak : visualisation des données en temps réel
- Node-RED / MQTT (optionnel) : transmission des données

## Structure du dépôt
- `arduino/meteo_sensor.ino` : code Arduino
- `docs/circuit_schema.png` : schéma du circuit
