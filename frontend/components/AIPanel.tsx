'use client';

import { SummaryOut } from '../lib/types';

export default function AIPanel({
  summary,
  onSummarize
}: {
  summary: SummaryOut | null;
  onSummarize: () => Promise<void> | void;
}) {
  return (
    <div>
      <div className="flex-row">
        <h2 style={{ margin: 0 }}>AI Summary</h2>
        <button onClick={onSummarize} style={{ marginLeft: 'auto' }}>Summarize</button>
      </div>
      {!summary && <p className="muted">Click “Summarize” to generate.</p>}
      {summary && (
        <div className="ai-block">
          <p>{summary.summary}</p>
          {summary.todos && summary.todos.length > 0 && (
            <>
              <h4>TODOs</h4>
              <ul>
                {summary.todos.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            </>
          )}
          {summary.tags && summary.tags.length > 0 && (
            <>
              <h4>Tags</h4>
              <p>{summary.tags.join(', ')}</p>
            </>
          )}
          {summary.citations && summary.citations.length > 0 && (
            <>
              <h4>Citations</h4>
              <ul>
                {summary.citations.map((c, i) => <li key={i}><em>{c.text}</em></li>)}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
