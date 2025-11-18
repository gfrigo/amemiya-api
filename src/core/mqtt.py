import json
import os

import paho.mqtt.publish as publish

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))


def publish_event(topic: str, payload: dict, qos: int = 1, retain: bool = False) -> None:
    """Publica um evento MQTT simples usando paho-mqtt.

    Essa função é síncrona e pensada para chamadas não-críticas de teste.
    Para produção/alto throughput, use um cliente assíncrono ou um publisher dedicado.
    """
    publish.single(topic, payload=json.dumps(payload), hostname=MQTT_BROKER, port=MQTT_PORT, qos=qos, retain=retain)
