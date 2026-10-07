# Courant landing page

- `landing.html`: source page (claude.ai artifact format). `build.sh` wraps it into `dist/index.html` for static hosting.
- Live: https://courant-africa.lovable.app (Lovable project "Courant Faithful Port", id 01dda390-251e-4cc5-98cc-80508c313f6e).
  The Lovable project is a faithful JSX port of `landing.html`; the pilot-access form writes to the
  Lovable Cloud table `pilot_requests` (anonymous insert only; read submissions from the Lovable dashboard).
- Netlify project `courant-africa` exists with forms enabled but has no deploy yet (team credits exhausted on 2026-10-07).
- Content changes: edit `landing.html` here, then send the same change to the Lovable project so the two stay in sync.
