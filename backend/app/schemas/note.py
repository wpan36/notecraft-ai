import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from .tag import TagOut

class NoteCreate(BaseModel):
    title: str = Field(min_length=0)
    content: str = Field(min_length=0)
    user_id: Optional[uuid.UUID] = None
    tag_names: Optional[List[str]] = None 

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_names: Optional[List[str]] = None


class NoteOut(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    title: str
    content: str
    created_at: datetime
    tags: List[TagOut] = []

    model_config = ConfigDict(from_attributes=True)
