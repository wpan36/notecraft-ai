from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.search import SearchResponse
from app.services import search_notes

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search_api(
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return search_notes(db, q=q, limit=limit, offset=offset)
