// Accès protégé (HTTP Basic) tant que la vitrine n'est pas publique.
// Le mot de passe vient de la variable d'environnement SITE_PASSWORD (jamais du code).
export default async (request: Request, context: { next: () => Promise<Response> }) => {
  const expected = Netlify.env.get("SITE_PASSWORD");
  if (!expected) return new Response("Accès fermé : SITE_PASSWORD non configuré.", { status: 503 });
  const header = request.headers.get("authorization") || "";
  if (header.startsWith("Basic ")) {
    try {
      const decoded = atob(header.slice(6));
      const password = decoded.slice(decoded.indexOf(":") + 1);
      if (password === expected) return context.next();
    } catch (_) { /* en-tête invalide */ }
  }
  return new Response("Accès réservé — ENERVIA", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="ENERVIA", charset="UTF-8"', "Cache-Control": "no-store" },
  });
};

export const config = { path: "/*" };
