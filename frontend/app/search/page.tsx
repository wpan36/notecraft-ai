'use client';

import { useState } from 'react';
import { searchNotes } from '../../lib/api';
import { SearchHit } from '../../lib/types';
import SearchBar from '../../components/SearchBar';
import ResultsList from '../../components/ResultsList';

export default function SearchPage() {
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function onSearch(q: string) {
    try {
      setLoading(true);
      setErr(null);
      const res = await searchNotes(q);
      setHits(res.items || []);
    } catch (e: any) {
      setErr(e?.message || 'Search failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="stack">
      <section className="card">
        <h2>Search notes</h2>
        <SearchBar onSearch={onSearch} />
        {loading && <p>Searching...</p>}
        {err && <p className="error">{err}</p>}
      </section>

      <section className="card">
        <ResultsList items={hits} />
      </section>
    </div>
  );
}
