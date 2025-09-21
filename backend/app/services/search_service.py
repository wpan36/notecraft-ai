from __future__ import annotations
from typing import Optional, List
from sqlalchemy import select, func, literal_column
from sqlalchemy.orm import Session
from app.models import Note
from app.schemas.search import SearchHit, SearchResponse


def _snippet_from_text(text: Optional[str], length: int = 160) -> str:
    text = (text or "").strip()
    return text[:length]


def search_notes(
    db: Session,
    q: Optional[str],
    limit: int = 20,
    offset: int = 0,
) -> SearchResponse:
    q = (q or "").strip()
    items: List[SearchHit] = []

    if not q:
        rows = db.execute(
            select(Note.id, Note.title, Note.content)
            .order_by(Note.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        for note_id, title, content in rows:
            items.append(SearchHit(
                note_id=note_id,
                title=title,
                snippet=_snippet_from_text(content),
                score=None
            ))
        return SearchResponse(total=len(items), items=items)

    search_col = literal_column("search_tsv")
    tsquery = func.plainto_tsquery("english", q)
    snippet_expr = func.ts_headline("english", Note.content, tsquery)
    score_expr = func.ts_rank_cd(search_col, tsquery)

    stmt = (
        select(
            Note.id,
            Note.title,
            snippet_expr.label("snippet"),
            score_expr.label("score"),
        )
        .where(search_col.op("@@")(tsquery))
        .order_by(score_expr.desc())
        .limit(limit)
        .offset(offset)
    )

    rows = db.execute(stmt).all()
    for row in rows:
        items.append(SearchHit(
            note_id=row.id,
            title=row.title,
            snippet=row.snippet,
            score=float(row.score) if row.score is not None else None,
        ))

    return SearchResponse(total=len(items), items=items)
