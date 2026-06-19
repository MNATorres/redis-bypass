from fastapi import FastAPI
from app.routes import router

# Initialize FastAPI with the architectural laboratory title
app = FastAPI(title="Redis Bypass Laboratory")

# Include the router with all application endpoints
app.include_router(router)