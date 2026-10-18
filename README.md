# meotomo.com/me — Tran Duc Phu

Personal site + blog. Plain HTML/CSS/JS, no framework, no server-side build.
Live: https://meotomo.com/me/ · Blog: https://meotomo.com/me/blog/

## Publish a post

1. Create `posts/<slug>.md`:
   ```markdown
   ---
   title: "My post"
   date: 2026-10-20
   tags: [AI, Tech]          # topics: Tech, AI, Books, Philosophy, Psychology, Life/Other
   summary: "One or two sentences for cards, RSS and social previews."
   cover: /me/assets/my-cover.webp   # optional
   draft: false                      # optional; true = skipped
   ---
   Markdown body. ## headings build the table of contents; ```python fences get highlighted.
   ```
2. `pip install -r requirements.txt` (once), then `python build.py`
   → regenerates `index.html` (Latest writing), `blog/`, `blog/posts.json`, `blog/feed.xml`, `sitemap.xml`.
3. Preview: `python -m http.server 8000` → http://localhost:8000/
4. `git add -A && git commit -m "post: My post" && git push`
5. `vercel deploy --prod` (git auto-deploy is not connected).

Generated files are committed. Edit the homepage in `templates/home.html`, styling in `assets/style.css`,
page chrome in `build.py` (`layout()`). All internal links are relative so the site works under `/me/`
(vercel.json rewrites `/me/*` → `/*`) and on the bare vercel.app domain.
