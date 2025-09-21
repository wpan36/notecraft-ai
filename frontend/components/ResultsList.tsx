'use client';

import Link from 'next/link';
import { SearchHit } from '../lib/types';

export default function ResultsList({ items }: { items: SearchHit[] }) {
  if (!items.length) return <p className="muted">No results.</p>;
  return (
    <ul className="list">
      {items.map((h) => (
        <li key={h.note_id}>
          <Link href={`/notes/${h.note_id}`}>{h.title || '(untitled)'}</Link>
          {h.snippet && <div className="snippet" dangerouslySetInnerHTML={{ __html: h.snippet }} />}
        </li>
      ))}
    </ul>
  );
}
