import { NextRequest } from 'next/server';
import { backendBaseURL } from '../../_backend';

export async function GET(_req: NextRequest, { params }: { params: { id: string } }) {
  const url = `${backendBaseURL()}/api/notes/${params.id}`;
  const r = await fetch(url, { method: 'GET' });
  const body = await r.text();
  return new Response(body, { status: r.status, headers: { 'content-type': r.headers.get('content-type') || 'application/json' } });
}

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const url = `${backendBaseURL()}/api/notes/${params.id}`;
  const r = await fetch(url, {
    method: 'PUT',
    headers: { 'content-type': 'application/json' },
    body: await req.text()
  });
  const body = await r.text();
  return new Response(body, { status: r.status, headers: { 'content-type': r.headers.get('content-type') || 'application/json' } });
}
