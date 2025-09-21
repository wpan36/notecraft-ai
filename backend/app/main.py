from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.db import test_connection
from app.api import api_router
from app.core.config import settings


app = FastAPI(title="NoteCraft.AI Backend", version="0.1.0")

app.include_router(api_router)

@app.get("/healthz")
def healthz():
    test_connection()  
    return JSONResponse({"status": "ok", "env": settings.APP_ENV})


@app.get("/")
def root():
    return {"service": "notecraft-backend", "status": "ok"}
