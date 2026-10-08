# Africa Mineral Insights — reviewers site

Static site built from `docs/AFRICA_MINERAL_INSIGHTS.md` and `docs/cameroon/*.md`, deployed to the
Netlify project `africa-mineral-insights` (https://africa-mineral-insights.netlify.app).

Access is restricted to reviewers by HTTP Basic authentication in the edge function
`netlify/edge-functions/auth.ts`. It fails closed. The password itself is never committed: `stage.py`
writes only its SHA-256 hash to `netlify/lib/password-hash.ts` (git-ignored) in a staging directory.
Netlify's built-in password protection is not used (refused on the current plan).

```bash
pip install markdown
python ami-site/build.py                                 # writes ami-site/dist/ (git-ignored)
python ami-site/stage.py <staging_dir> <password_file>   # deployable copy, outside git
# then deploy <staging_dir> to the Netlify project africa-mineral-insights
```

After each deploy, check that `/` answers 401 without credentials and 200 with them.
