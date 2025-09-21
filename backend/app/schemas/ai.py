from typing import List, Optional
from pydantic import BaseModel

class Citation(BaseModel):
    chunk_index: Optional[int] = None
    text: Optional[str] = None

class SummaryOut(BaseModel):
    summary: str
    todos: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    citations: Optional[List[Citation]] = None
