import asyncio
import json
import os
import traceback

from asyncio_mqtt import Client

from src.core.database import start_connection, start_cursor
from src.core.config import settings


BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", 1883))


async def handle_message(msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        topic = msg.topic
        print("[MQTT-WORKER] Received topic=", topic)
        print("[MQTT-WORKER] payload=", data)

        # try to parse company_id and device_id from topic: amemiya/{company_id}/device/{device_id}/telemetry
        parts = topic.split('/')
        company_id = None
        device_id = None
        try:
            if len(parts) >= 4:
                company_id = int(parts[1])
                device_id = parts[3]
        except Exception:
            pass

        # attempt to persist into MySQL (table `Telemetry` expected)
        try:
            creds = settings.db_credentials
            with start_connection(creds) as conn:
                with start_cursor(conn) as cursor:
                    insert_stmt = "INSERT INTO Telemetry (company_id, device_id, payload, created_at) VALUES (%s, %s, %s, NOW())"
                    cursor.execute(insert_stmt, (company_id, device_id, json.dumps(data)))
                    conn.commit()
                    print("[MQTT-WORKER] persisted telemetry to DB")
        except Exception as e:
            print("[MQTT-WORKER] Failed to persist telemetry to DB (table may not exist) ->", e)
            traceback.print_exc()

    except Exception as e:
        print("[MQTT-WORKER] Error handling message", e)
        traceback.print_exc()


async def main():
    print(f"[MQTT-WORKER] Connecting to {BROKER}:{PORT}")
    async with Client(BROKER, PORT) as client:
        await client.subscribe("amemiya/+/device/+/telemetry", qos=1)
        async with client.unfiltered_messages() as messages:
            async for message in messages:
                await handle_message(message)


if __name__ == "__main__":
    asyncio.run(main())
