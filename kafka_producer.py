from aiokafka import AIOKafkaProducer
import json
import os

producer = None
KAFKA_ENABLED = os.getenv("KAFKA_ENABLED", "true").lower() == "true"

async def start_producer():
    global producer
    if not KAFKA_ENABLED:
        print("Kafka disabled, skipping producer startup")
        return
    try:
        producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await producer.start()
    except Exception as e:
        print(f"Kafka unavailable, continuing without it: {e}")
        producer = None

async def stop_producer():
    if producer:
        await producer.stop()

async def send_call_event(candidate_id: str, source: str):
    if not producer:
        return
    event = {"candidate_id": candidate_id, "source": source}
    await producer.send_and_wait("call-events", json.dumps(event).encode("utf-8"))