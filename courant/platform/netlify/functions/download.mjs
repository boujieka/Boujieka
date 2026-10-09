// Serve a protected file only to a signed-in Supabase user whose tier allows it.
// Env: SUPABASE_URL, SUPABASE_ANON_KEY (public values). The user's own token is used for every Supabase call,
// so the function never holds a service key; row-level security limits each user to reading their own profile.
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const RANK = { public: 0, registered: 1, institutional: 2 };
const TYPES = { '.html': 'text/html; charset=utf-8', '.csv': 'text/csv; charset=utf-8', '.json': 'application/json', '.pdf': 'application/pdf' };
const BASE = path.resolve(process.cwd(), 'protected');

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });

export default async (req) => {
  const url = new URL(req.url);
  const rel = url.searchParams.get('path') || '';
  if (!/^[a-z0-9-]+\/[a-z0-9.-]+$/.test(rel)) return json(400, { error: 'bad path' });
  const manifest = JSON.parse(await readFile(path.join(BASE, 'manifest.json'), 'utf8'));
  const need = manifest[rel];
  if (!need) return json(404, { error: 'not found' });

  const auth = req.headers.get('authorization') || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : '';
  const SB = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY;
  if (!SB || !KEY) return json(503, { error: 'auth not configured' });
  if (!token) return json(401, { error: 'sign in required' });

  const u = await fetch(`${SB}/auth/v1/user`, { headers: { apikey: KEY, authorization: `Bearer ${token}` } });
  if (!u.ok) return json(401, { error: 'invalid session' });
  const user = await u.json();
  const p = await fetch(`${SB}/rest/v1/profiles?id=eq.${encodeURIComponent(user.id)}&select=tier`, { headers: { apikey: KEY, authorization: `Bearer ${token}` } });
  const rows = p.ok ? await p.json() : [];
  const tier = rows[0]?.tier || 'registered';
  if (RANK[tier] < RANK[need]) return json(403, { error: 'tier too low', need, tier });

  const file = path.join(BASE, rel);
  if (!file.startsWith(BASE + path.sep)) return json(400, { error: 'bad path' });
  const body = await readFile(file);
  return new Response(body, { status: 200, headers: {
    'content-type': TYPES[path.extname(file)] || 'application/octet-stream',
    'content-disposition': `attachment; filename="${path.basename(file)}"`,
    'cache-control': 'private, no-store',
  } });
};
