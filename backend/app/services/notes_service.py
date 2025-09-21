from __future__ import annotations
import uuid
from typing import List, Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from app.models import Note, Tag
from app.schemas.note import NoteCreate, NoteUpdate


def _normalize_names(tag_names: Optional[List[str]]) -> List[str]:
    if not tag_names:
        return []
    cleaned = [n.strip() for n in tag_names if isinstance(n, str) and n.strip()]
    seen = set()
    ordered = []
    for n in sorted(cleaned, key=lambda x: x.lower()):
        low = n.lower()
        if low not in seen:
            seen.add(low)
            ordered.append(n)
    return ordered


def upsert_tags(db: Session, tag_names: Optional[List[str]]) -> List[Tag]:
    names = _normalize_names(tag_names)
    if not names:
        return []

    lower_names = [n.lower() for n in names]

    existing: List[Tag] = (
        db.execute(
            select(Tag).where(func.lower(Tag.name).in_(lower_names))
        ).scalars().all()
    )
    existing_map = {t.name.lower(): t for t in existing}

    to_create: List[Tag] = [
        Tag(name=n) for n in names if n.lower() not in existing_map
    ]
    if to_create:
        db.add_all(to_create)
        db.flush() 
        existing.extend(to_create)
        for t in to_create:
            existing_map[t.name.lower()] = t

    ordered: List[Tag] = [existing_map[n.lower()] for n in names]
    return ordered


def create_note(db: Session, payload: NoteCreate) -> Note:
    note = Note(
        user_id=payload.user_id,
        title=payload.title,
        content=payload.content,
    )
    if payload.tag_names:
        note.tags = upsert_tags(db, payload.tag_names)

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: uuid.UUID, payload: NoteUpdate) -> Optional[Note]:
    note: Optional[Note] = db.get(Note, note_id)
    if not note:
        return None

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    if payload.tag_names is not None:
        note.tags = upsert_tags(db, payload.tag_names)

    db.commit()
    db.refresh(note)
    return note


def get_note(db: Session, note_id: uuid.UUID) -> Optional[Note]:
    stmt = (
        select(Note)
        .options(selectinload(Note.tags))
        .where(Note.id == note_id)
    )
    return db.execute(stmt).scalars().first()


def list_notes(
    db: Session,
    user_id: Optional[uuid.UUID] = None,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Note]:
    stmt = (
        select(Note)
        .options(selectinload(Note.tags))
        .order_by(Note.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if user_id:
        stmt = stmt.where(Note.user_id == user_id)

    return db.execute(stmt).scalars().all()
