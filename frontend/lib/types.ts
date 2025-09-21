export type UUID = string;

export interface TagOut {
  id: number;
  name: string;
}

export interface NoteOut {
  id: UUID;
  user_id?: UUID | null;
  title: string;
  content: string;
  created_at: string; // ISO string
  tags: TagOut[];
}

export interface SummaryOut {
  summary: string;
  todos?: string[] | null;
  tags?: string[] | null;
  citations?: { text?: string | null }[] | null;
}

export interface SearchHit {
  note_id: UUID;
  title: string;
  snippet?: string | null;
  score?: number | null;
}

export interface SearchResponse {
  total?: number | null;
  items: SearchHit[];
}
