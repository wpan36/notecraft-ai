from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, text, Computed
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.note_tag import note_tags_association


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False, server_default=text("''"))
    content: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("''"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )


    user = relationship(
        "User",
        back_populates="notes",
        lazy="selectin",
        passive_deletes=True,
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=note_tags_association,
        back_populates="notes",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"Note(id={self.id!s}, title={self.title!r})"
