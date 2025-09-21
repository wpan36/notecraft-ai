import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.ai import SummaryOut
from app.services import summarize_note_by_id

router = APIRouter()

@router.post("/notes/{note_id}/ai", response_model=SummaryOut)
def summarize_note_api(note_id: uuid.UUID, db: Session = Depends(get_db)):
    out = summarize_note_by_id(db, note_id)
    if not out:
        raise HTTPException(status_code=404, detail="note not found")
    return out
