/* Service worker TasetyGrid : la page reste consultable hors connexion.
   - Pages HTML : réseau d'abord (contenu à jour), cache en secours.
   - Fichiers statiques et polices : cache d'abord, mis à jour en arrière-plan.
   La version change à chaque build : les anciens caches sont supprimés. */
const VERSION = "206fb51c142d";
const CACHE = "tasetygrid-" + VERSION;
const PRECACHE = ["./", "./en/", "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png", "manifest.webmanifest"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("tasetygrid-") && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const memeOrigine = url.origin === self.location.origin;
  const police = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (!memeOrigine && !police) return;

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => { const copie = res.clone(); caches.open(CACHE).then((c) => c.put(req, copie)); return res; })
        .catch(() => caches.match(req).then((r) => r || caches.match(new URL("./", self.registration.scope).href)))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((enCache) => {
      const reseau = fetch(req)
        .then((res) => {
          if (res && (res.ok || res.type === "opaque")) { const copie = res.clone(); caches.open(CACHE).then((c) => c.put(req, copie)); }
          return res;
        })
        .catch(() => enCache);
      return enCache || reseau;
    })
  );
});
