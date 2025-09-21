import uuid
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class SearchHit(BaseModel):
    note_id: uuid.UUID
    title: str
    snippet: Optional[str] = None
    score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class SearchResponse(BaseModel):
    total: Optional[int] = None
    items: List[SearchHit]
