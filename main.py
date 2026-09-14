from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

stats = {
    "total_requests": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "calls_made": 0,
}

@app.on_event("startup")
async def startup_event():
    await start_producer()
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer()
    logger.info("Application shutting down")

@app.get("/api/health")
def read_root():
    return {"message": "Recruiter Call Platform is alive"}

@app.get("/api/stats")
def get_stats():
    return stats

@app.get("/api/candidate/{candidate_id}")
async def get_candidate(candidate_id: str):
    stats["total_requests"] += 1
    cache_key = f"candidate:{candidate_id}"

    cached = get_cached_value(cache_key)
    if cached:
        stats["cache_hits"] += 1
        logger.info(f"Cache hit for candidate {candidate_id}")
        await send_call_event(candidate_id, "cache")
        return {"source": "cache", "data": cached}

    fake_data = f"Profile data for {candidate_id}"
    set_cached_value(cache_key, fake_data)
    stats["cache_misses"] += 1
    logger.info(f"Cache miss for candidate {candidate_id}, computed fresh data")
    await send_call_event(candidate_id, "computed")

    return {"source": "computed", "data": fake_data}

@app.get("/api/call/{candidate_id}")
async def make_call(candidate_id: str):
    stats["total_requests"] += 1
    stats["calls_made"] += 1
    logger.info(f"Generating call script for candidate {candidate_id}")
    script = generate_call_script(candidate_id)
    await send_call_event(candidate_id, "llm_call")
    return {"candidate_id": candidate_id, "call_script": script}

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")