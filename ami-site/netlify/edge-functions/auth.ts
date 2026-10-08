// HTTP Basic authentication for the reviewers-only site. Fails closed.
// The SHA-256 hash of the password lives in ../lib/password-hash.ts, generated at deploy time by
// stage.py and git-ignored (never committed). AMI_SITE_PASSWORD, if set (Functions scope), wins.
import type { Config } from "@netlify/edge-functions";
import { PASSWORD_SHA256 } from "../lib/password-hash.ts";

const REALM = 'Basic realm="Africa Mineral Insights", charset="UTF-8"';

async function sha256Hex(text: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function safeEqual(a: string, b: string): boolean {
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

export default async (request: Request) => {
  const envPassword = Netlify.env.get("AMI_SITE_PASSWORD");
  const expected = envPassword ? await sha256Hex(envPassword) : PASSWORD_SHA256;
  if (!/^[0-9a-f]{64}$/.test(expected)) return new Response("Site non configuré.", { status: 503 });

  const header = request.headers.get("authorization") ?? "";
  if (header.startsWith("Basic ")) {
    let decoded = "";
    try {
      decoded = new TextDecoder().decode(Uint8Array.from(atob(header.slice(6)), (c) => c.charCodeAt(0)));
    } catch {
      decoded = "";
    }
    if (decoded.includes(":")) {
      const password = decoded.slice(decoded.indexOf(":") + 1);
      if (safeEqual(await sha256Hex(password), expected)) return; // continue to the static file
    }
  }
  return new Response("Accès réservé aux relecteurs.", {
    status: 401,
    headers: { "WWW-Authenticate": REALM, "Cache-Control": "no-store", "X-Robots-Tag": "noindex" },
  });
};

export const config: Config = { path: "/*" };
