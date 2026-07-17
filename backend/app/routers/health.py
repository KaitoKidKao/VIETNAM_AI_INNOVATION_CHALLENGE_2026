from fastapi import APIRouter
from app.config import APP_ENV
import time

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": int(time.time()), "environment": APP_ENV}
