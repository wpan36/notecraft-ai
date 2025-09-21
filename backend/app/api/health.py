from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db
from fastapi import Depends

router = APIRouter()

@router.get("/healthz")
def api_healthz(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "scope": "api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"db not ready: {e}")
