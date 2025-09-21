'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getNote, updateNote, summarizeNote } from '../../../lib/api';
import { NoteOut, SummaryOut } from '../../../lib/types';
import NoteEditor from '../../../components/NoteEditor';
import AIPanel from '../../../components/AIPanel';

export default function NoteDetailPage() {
  const params = useParams<{ id: string }>();
  const noteId = params.id;

  const [note, setNote] = useState<NoteOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [summary, setSummary] = useState<SummaryOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setLoading(true);
      const n = await getNote(noteId);
      setNote(n);
      setError(null);
    } catch (e: any) {
      setError(e?.message || 'Failed to load note');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [noteId]);

  async function onSave(nextTitle: string, nextContent: string) {
    if (!note) return;
    try {
      setSaving(true);
      const updated = await updateNote(note.id, { title: nextTitle, content: nextContent });
      setNote(updated);
      setError(null);
    } catch (e: any) {
      setError(e?.message || 'Update failed');
    } finally {
      setSaving(false);
    }
  }

  async function onSummarize() {
    if (!note) return;
    try {
      setSummary(null);
      const res = await summarizeNote(note.id);
      setSummary(res);
    } catch (e: any) {
      setError(e?.message || 'Summarize failed');
    }
  }

  if (loading) return <p>Loading...</p>;
  if (!note) return <p className="error">Not found</p>;

  return (
    <div className="stack">
      <section className="card">
        <h2>Edit note</h2>
        <NoteEditor
          title={note.title}
          content={note.content}
          onSave={onSave}
          saving={saving}
        />
        {error && <p className="error">{error}</p>}
      </section>

      <section className="card">
        <AIPanel summary={summary} onSummarize={onSummarize} />
      </section>
    </div>
  );
}
