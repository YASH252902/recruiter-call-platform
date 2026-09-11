from fastapi import FastAPI
from redis_client import get_cached_value, set_cached_value
from kafka_producer import start_producer, stop_producer, send_call_event
from llm_client import generate_call_script
from tracing import setup_tracing
from prometheus_fastapi_instrumentator import Instrumentator
from logging_setup import setup_logging

app = FastAPI()
tracer = setup_tracing(app)
Instrumentator().instrument(app).expose(app)
logger = setup_logging()

@app.on_event("startup")
async def startup_event():
    await start_producer()
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer()
    logger.info("Application shutting down")

@app.get("/")
def read_root():
    return {"message": "Recruiter Call Platform is alive"}

@app.get("/candidate/{candidate_id}")
async def get_candidate(candidate_id: str):
    cache_key = f"candidate:{candidate_id}"

    cached = get_cached_value(cache_key)
    if cached:
        logger.info(f"Cache hit for candidate {candidate_id}")
        await send_call_event(candidate_id, "cache")
        return {"source": "cache", "data": cached}

    fake_data = f"Profile data for {candidate_id}"
    set_cached_value(cache_key, fake_data)
    logger.info(f"Cache miss for candidate {candidate_id}, computed fresh data")
    await send_call_event(candidate_id, "computed")

    return {"source": "computed", "data": fake_data}

@app.get("/call/{candidate_id}")
async def make_call(candidate_id: str):
    logger.info(f"Generating call script for candidate {candidate_id}")
    script = generate_call_script(candidate_id)
    await send_call_event(candidate_id, "llm_call")
    return {"candidate_id": candidate_id, "call_script": script}