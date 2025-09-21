'use client';

import { useState, useEffect } from 'react';

export default function NoteEditor({
  title,
  content,
  onSave,
  saving
}: {
  title: string;
  content: string;
  onSave: (title: string, content: string) => Promise<void> | void;
  saving?: boolean;
}) {
  const [t, setT] = useState(title);
  const [c, setC] = useState(content);

  useEffect(() => setT(title), [title]);
  useEffect(() => setC(content), [content]);

  return (
    <div className="form">
      <label>
        Title
        <input value={t} onChange={e => setT(e.target.value)} placeholder="Title" />
      </label>
      <label>
        Content
        <textarea value={c} onChange={e => setC(e.target.value)} placeholder="Write something..." rows={10} />
      </label>
      <button disabled={saving} onClick={() => onSave(t, c)}>
        {saving ? 'Saving...' : 'Save'}
      </button>
    </div>
  );
}
