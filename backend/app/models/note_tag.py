from __future__ import annotations
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID, INTEGER
from app.models.base import Base

note_tags_association = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", UUID(as_uuid=True), ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", INTEGER, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
