'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { listNotes, createNote } from '../lib/api';
import { NoteOut } from '../lib/types';

export default function HomePage() {
  const [notes, setNotes] = useState<NoteOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setLoading(true);
      const data = await listNotes({ limit: 20, offset: 0 });
      setNotes(data);
      setError(null);
    } catch (e: any) {
      setError(e?.message || 'Failed to load notes');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      setCreating(true);
      const note = await createNote({ title, content, tag_names: [] });
      setTitle('');
      setContent('');
      await load();
      location.href = `/notes/${note.id}`;
    } catch (e: any) {
      setError(e?.message || 'Create failed');
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="stack">
      <section className="card">
        <h2>Create a note</h2>
        <form onSubmit={onCreate} className="form">
          <label>
            Title
            <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" />
          </label>
          <label>
            Content
            <textarea value={content} onChange={e => setContent(e.target.value)} placeholder="Write something..." rows={6} />
          </label>
          <button disabled={creating || !title.trim()}>{creating ? 'Creating...' : 'Create'}</button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>

      <section className="card">
        <h2>Recent notes</h2>
        {loading ? <p>Loading...</p> : (
          <ul className="list">
            {notes.map(n => (
              <li key={n.id}>
                <Link href={`/notes/${n.id}`}>{n.title || '(untitled)'}</Link>
                <span className="muted"> • {new Date(n.created_at).toLocaleString()}</span>
              </li>
            ))}
            {!notes.length && <li className="muted">No notes yet.</li>}
          </ul>
        )}
      </section>
    </div>
  );
}
