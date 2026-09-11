import asyncio
from aiokafka import AIOKafkaConsumer

async def consume():
    consumer = AIOKafkaConsumer(
        "call-events",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("Received event:", msg.value.decode("utf-8"))
    finally:
        await consumer.stop()

asyncio.run(consume())