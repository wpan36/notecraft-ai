export function backendBaseURL() {
  const internal = process.env.BACKEND_INTERNAL_URL;
  if (internal && internal.trim()) return internal.trim();

  const pub = process.env.NEXT_PUBLIC_API_BASE;
  if (pub && pub.trim()) return pub.trim();

  return 'http://backend:8080';
}
