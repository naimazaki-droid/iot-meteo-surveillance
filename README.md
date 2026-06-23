# 🌡️ Système de Surveillance Météorologique basé sur l'IoT

> **Module Internet des Objets** — Master IAO, Université Mohammed V  
> Encadré par **Pr. Hafssa BENABOUD**

---

## 📋 Description

Système IoT complet de surveillance météorologique permettant de :
- Collecter des données de **température** et **humidité** via un circuit simulé (Tinkercad)
- Transmettre les données en temps réel via le protocole **MQTT**
- Visualiser les données sur un tableau de bord cloud **ThingSpeak**

---

## 🏗️ Architecture

```
Tinkercad (Arduino + TMP36 + Potentiomètre)
        ↓ Moniteur série (simulation)
mqtt_publisher.py  →  Broker MQTT local (amqtt, localhost:1883)
                              ↓
                   mqtt_to_thingspeak.py
                              ↓
                   ThingSpeak (Canal 3411510)
                   ├── Field 1 : Température (°C)
                   └── Field 2 : Humidité (%)
```

---

## 🛠️ Outils utilisés

| Outil | Rôle |
|-------|------|
| [Tinkercad](https://www.tinkercad.com/) | Simulation du circuit Arduino + capteurs |
| [ThingSpeak](https://thingspeak.mathworks.com/) | Stockage et visualisation des données IoT |
| [amqtt](https://pypi.org/project/amqtt/) | Broker MQTT local (Python) |
| [paho-mqtt](https://pypi.org/project/paho-mqtt/) | Client MQTT Python |
| Python 3.x | Scripts de publication et de transfert |

---

## 📦 Fichiers du projet

```
├── meteo_iot.ino           # Code Arduino (Tinkercad)
├── mqtt_publisher.py       # Publication des données sur MQTT
├── mqtt_to_thingspeak.py   # Transfert MQTT → ThingSpeak
└── README.md               # Ce fichier
```

---

## ⚙️ Installation

### Prérequis

- Python 3.x installé sur Windows
- Compte ThingSpeak (gratuit) : https://thingspeak.mathworks.com/

### Installation des dépendances

```bash
pip install paho-mqtt requests amqtt
```

---

## 🚀 Lancement du système

Le système nécessite **3 terminaux** ouverts simultanément :

### Terminal 1 — Démarrer le broker MQTT local

```bash
# Windows (chemin complet si amqtt n'est pas dans le PATH)
C:\Users\<votre_nom>\AppData\Roaming\Python\Python3xx\Scripts\amqtt.exe
```

Résultat attendu :
```
INFO - Listener 'default' bind to 0.0.0.0:1883
```

### Terminal 2 — Publier les données sur MQTT

```bash
python mqtt_publisher.py
```

Résultat attendu :
```
Connecté au broker localhost:1883
Publié sur iot/meteo/super_albar : {"temperature": 23.14, "humidity": 51.82}
```

### Terminal 3 — Transférer les données vers ThingSpeak

```bash
python mqtt_to_thingspeak.py
```

Résultat attendu :
```
Connecté au broker localhost, abonnement à iot/meteo/super_albar
Reçu sur iot/meteo/super_albar : temp=23.14, hum=51.82
Envoyé à ThingSpeak (entrée n°4) : temp=23.14, hum=51.82
```

---

## 🔒 Configuration de la clé API ThingSpeak

La clé API ThingSpeak est lue depuis une variable d'environnement pour éviter de l'exposer sur GitHub.

**Windows (PowerShell) :**
```powershell
$env:THINGSPEAK_API_KEY="VOTRE_CLE_API"
```

**Windows (cmd) :**
```cmd
set THINGSPEAK_API_KEY=VOTRE_CLE_API
```

> Sans cette variable, le script utilise la valeur par défaut dans le code (à remplacer par votre propre clé).

---

## 📡 Configuration ThingSpeak

| Paramètre | Valeur |
|-----------|--------|
| Channel ID | 3411510 |
| Field 1 | Temperature (°C) |
| Field 2 | Humidity (%) |
| Topic MQTT | `iot/meteo/super_albar` |
| Fréquence de mise à jour | 15 secondes (limite compte gratuit) |

---

## 🔌 Câblage Tinkercad

### TMP36 (capteur de température)
- Broche gauche → **5V** (Arduino)
- Broche centrale (Vout) → **A1** (Arduino)
- Broche droite → **GND** (Arduino)

### Potentiomètre (humidité simulée)
- Broche gauche → **5V** (Arduino)
- Broche centrale (curseur) → **A2** (Arduino)
- Broche droite → **GND** (Arduino)

