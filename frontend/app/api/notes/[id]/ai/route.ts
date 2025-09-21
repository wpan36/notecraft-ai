import { NextRequest } from 'next/server';
import { backendBaseURL } from '../../../_backend';

export async function POST(_req: NextRequest, { params }: { params: { id: string } }) {
  const url = `${backendBaseURL()}/api/notes/${params.id}/ai`;
  const r = await fetch(url, { method: 'POST' });
  const body = await r.text();
  return new Response(body, { status: r.status, headers: { 'content-type': r.headers.get('content-type') || 'application/json' } });
}
