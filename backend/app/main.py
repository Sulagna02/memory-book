from fastapi import FastAPI
from app.routes import health, upload

app = FastAPI(title="Enterprise Document Intelligence API")

app.include_router(health.router)
app.include_router(upload.router)