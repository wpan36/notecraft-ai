import { NoteOut, SummaryOut, SearchResponse } from './types';

const BASE = ''; 

async function http<T>(url: string, init?: RequestInit): Promise<T> {
  const r = await fetch(url, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...(init?.headers || {})
    }
  });
  if (!r.ok) {
    let msg = r.statusText;
    try {
      const j = await r.json();
      msg = j?.detail || msg;
    } catch { /* ignore */ }
    throw new Error(msg);
  }
  return r.json() as Promise<T>;
}

// Notes
export async function listNotes({ limit = 20, offset = 0 }: { limit?: number; offset?: number; }): Promise<NoteOut[]> {
  const q = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  return http<NoteOut[]>(`${BASE}/api/notes?${q.toString()}`);
}

export async function createNote(payload: { title: string; content: string; tag_names?: string[]; }): Promise<NoteOut> {
  return http<NoteOut>(`${BASE}/api/notes`, { method: 'POST', body: JSON.stringify(payload) });
}

export async function getNote(id: string): Promise<NoteOut> {
  return http<NoteOut>(`${BASE}/api/notes/${id}`);
}

export async function updateNote(id: string, payload: Partial<{ title: string; content: string; tag_names: string[] }>): Promise<NoteOut> {
  return http<NoteOut>(`${BASE}/api/notes/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
}

// AI
export async function summarizeNote(id: string): Promise<SummaryOut> {
  return http<SummaryOut>(`${BASE}/api/notes/${id}/ai`, { method: 'POST' });
}

// Search
export async function searchNotes(q: string): Promise<SearchResponse> {
  const qs = new URLSearchParams({ q });
  return http<SearchResponse>(`${BASE}/api/search?${qs.toString()}`);
}
