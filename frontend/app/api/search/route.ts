import { NextRequest } from 'next/server';
import { backendBaseURL } from '../_backend';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const qs = searchParams.toString();
  const url = `${backendBaseURL()}/api/search${qs ? `?${qs}` : ''}`;
  const r = await fetch(url, { method: 'GET' });
  const body = await r.text();
  return new Response(body, { status: r.status, headers: { 'content-type': r.headers.get('content-type') || 'application/json' } });
}
