from __future__ import annotations

import json
import os
import re
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Note
from app.schemas.ai import SummaryOut, Citation
from openai import OpenAI

_client: Optional[OpenAI] = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return _client


_OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "note_summary",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "todos": {"type": "array", "items": {"type": "string"}},
                "tags": {"type": "array", "items": {"type": "string"}},
                "citations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["summary"],
            "additionalProperties": False,
        },
    },
}


def _build_messages(note: Note) -> list:
    system = (
        "You summarize user notes and return JSON strictly matching the schema. "
        "Write a concise 3-5 sentence summary in the note's language, "
        "extract TODOs (short, actionable), and 1-5 topical tags. "
        "If the note contains explicit TODO lines like '-', '*', '•', or 'TODO', prefer them. "
        "For citations, include short verbatim snippets that support the summary."
    )
    content = (note.content or "")[:8000]
    user = f"Note title: {note.title}\nNote content:\n\"\"\"\n{content}\n\"\"\""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _simple_sent_split(text: str) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    parts = re.split(r"(?<=[\.\!\?。！？])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _summarize_locally(text: str, max_sentences: int = 3) -> str:
    sents = _simple_sent_split(text)
    return " ".join(sents[:max_sentences])


def _extract_todos(text: str, max_items: int = 5) -> List[str]:
    todos: List[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.lower().startswith("todo") or s.startswith(("- ", "* ", "• ")):
            s = re.sub(r"^(todo[:：]?\s*|- |\* |• )", "", s, flags=re.IGNORECASE).strip()
            if s:
                todos.append(s)
        if len(todos) >= max_items:
            break
    return todos


def summarize_note(note: Note) -> SummaryOut:
    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model=_OPENAI_MODEL,
            messages=_build_messages(note),
            response_format=_RESPONSE_FORMAT,  
            temperature=0.2,
        )
        raw = resp.choices[0].message.content or "{}"
        data = json.loads(raw)

        summary = str(data.get("summary", "")).strip()
        todos = data.get("todos") or None
        tags = data.get("tags") or None

        citations_json = data.get("citations") or []
        citations: List[Citation] = []
        for c in citations_json:
            if isinstance(c, dict) and c.get("text"):
                citations.append(Citation(text=str(c["text"])))

        return SummaryOut(
            summary=summary,
            todos=todos if todos else None,
            tags=tags if tags else None,
            citations=citations or None,
        )
    except Exception:
        summary = _summarize_locally(note.content, max_sentences=3)
        todos = _extract_todos(note.content) or None
        return SummaryOut(summary=summary, todos=todos)


def summarize_note_by_id(db: Session, note_id: uuid.UUID) -> Optional[SummaryOut]:
    note = db.get(Note, note_id)
    if not note:
        return None
    return summarize_note(note)
