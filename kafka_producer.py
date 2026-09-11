from aiokafka import AIOKafkaProducer
import json

producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()

async def stop_producer():
    await producer.stop()

async def send_call_event(candidate_id: str, source: str):
    event = {"candidate_id": candidate_id, "source": source}
    await producer.send_and_wait("call-events", json.dumps(event).encode("utf-8"))