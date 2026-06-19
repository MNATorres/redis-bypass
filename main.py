import time
from fastapi import FastAPI, Request
from app.routes import router
from app.utils.logger import logger

# Initialize FastAPI with the architectural laboratory title
app = FastAPI(title="Redis Bypass Laboratory")

# Middleware to intercept and log request initiation and completion details
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method

    # Log request start (Format: date | level | endpoint | method | Request started)
    logger.info(f"{endpoint} | {method} | Request started")

    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000

    # Log request completion with duration (Format: date | level | endpoint | method | Request completed in XX.XX ms)
    logger.info(f"{endpoint} | {method} | Request completed in {duration_ms:.2f} ms")

    return response

# Include the router with all application endpoints
app.include_router(router)