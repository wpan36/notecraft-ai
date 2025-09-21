import uuid
from typing import Optional, List, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut
from app.services import create_note, update_note, get_note, list_notes

router = APIRouter()

@router.post("/notes", response_model=NoteOut)
def create_note_api(payload: NoteCreate, db: Session = Depends(get_db)):
    note = create_note(db, payload)
    return note  

@router.get("/notes/{note_id}", response_model=NoteOut)
def get_note_api(note_id: uuid.UUID, db: Session = Depends(get_db)):
    note = get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteOut)
def update_note_api(note_id: uuid.UUID, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = update_note(db, note_id, payload)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note

@router.get("/notes", response_model=List[NoteOut])
def list_notes_api(
    user_id: Optional[uuid.UUID] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    notes: Sequence = list_notes(db, user_id=user_id, limit=limit, offset=offset)
    return list(notes)
