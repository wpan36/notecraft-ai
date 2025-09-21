# NoteCraft.AI

A minimal end-to-end AI note-taking app:

- React (Next.js) frontend + Python (FastAPI) backend
- Postgres persistence (users / notes / tags)
- Full-text search via generated tsvector + GIN index, title trigram index
- One-click OpenAI API summaries

---
## Quick Start
1. In the repo root, create `.env`:
```text
POSTGRES_USER=notecraft
POSTGRES_PASSWORD=notecraft
POSTGRES_DB=notecraft

OPENAI_API_KEY=sk-xxxx                 # required
OPENAI_MODEL=gpt-4o-mini               # optional
```
2. Start everything:
```text
docker compose up -d --build
```
3. Open the app:
- Frontend: http://localhost:8081
- Backend health: http://localhost:8080/healthz

---
## What you can do
- Create & edit notes in the UI (inline editor)
- AI summarize any note (`Summarize` button on the detail page)
- Search notes (keyword / full-text) via `/search` page
