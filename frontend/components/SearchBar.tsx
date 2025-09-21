'use client';

import { useState } from 'react';

export default function SearchBar({ onSearch }: { onSearch: (q: string) => void | Promise<void> }) {
  const [q, setQ] = useState('');
  return (
    <div className="form-row">
      <input value={q} onChange={e => setQ(e.target.value)} placeholder="keyword..." />
      <button onClick={() => onSearch(q)} disabled={!q.trim()}>Search</button>
    </div>
  );
}
