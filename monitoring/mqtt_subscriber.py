import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import django
import json
import paho.mqtt.client as mqtt

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "flood_monitoring.settings"
)

django.setup()

from monitoring.models import FloodData
django.setup()

from monitoring.models import FloodData
from monitoring.prediction_engine import *


# ==========================================
# MQTT CONFIG
# ==========================================

BROKER = "localhost"
PORT = 1883
TOPIC = "flood/data"


# ==========================================
# CONNECT
# ==========================================

def on_connect(client, userdata, flags, rc):

    print("Connected to MQTT Broker")

    client.subscribe(TOPIC)


# ==========================================
# RECEIVE MESSAGE
# ==========================================

def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    rain = payload["rain"]

    krl_cm = payload["krl_cm"]

    kai_cm = payload["kai_cm"]


    # ======================================
    # STATUS LOGIC
    # ======================================

    # ======================================
# SENSOR VALIDATION
# ======================================

    if len(water_history) > 0:

        validation = validate_sensor(
            krl_cm,
            water_history[-1]
        )

        if validation == "FALSE DETECTION":

            print("FALSE DETECTION SKIPPED")

            return


    # ======================================
    # SAVE HISTORY
    # ======================================

    water_history.append(krl_cm)


    # ======================================
    # TREND ANALYSIS
    # ======================================

    trend = analyze_trend(
        list(water_history)
    )


    # ======================================
    # PREDICTION
    # ======================================

    status = predict_status(
        krl_cm,
        rain,
        trend
    )

    print("================================")
    print("NEW SENSOR DATA RECEIVED")
    print(payload)
    print("STATUS:", status)
    print("================================")


# ==========================================
# MQTT CLIENT
# ==========================================

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()