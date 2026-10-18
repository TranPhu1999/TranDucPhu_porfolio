#!/usr/bin/env python3
"""Static blog builder for meotomo.com/me/.

Reads posts/*.md (YAML front matter + Markdown) and templates/home.html, then writes:
  index.html, blog/index.html, blog/<slug>/index.html, blog/posts.json,
  blog/feed.xml, sitemap.xml
Usage: python build.py
"""
import datetime as dt
import html
import json
import math
import re
import shutil
from email.utils import format_datetime
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
BLOG_DIR = ROOT / "blog"
SITE = "https://meotomo.com/me/"
AUTHOR = "Tran Duc Phu"
SITE_TITLE = "Tran Duc Phu"
SITE_DESC = "Tran Duc Phu (Albert) — AI Engineer working on LLMs, agentic systems and applied machine learning. Portfolio and blog."
TOPICS = ["Tech", "AI", "Books", "Philosophy", "Psychology", "Life/Other"]
E = html.escape

ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'


def topics_for(tags):
    found = []
    for t in tags:
        low = t.lower()
        for top in TOPICS:
            if low == top.lower() or (top == "Life/Other" and low in ("life", "other", "meta")):
                if top not in found:
                    found.append(top)
    return found or ["Life/Other"]


def human_date(d):
    return d.strftime("%b %-d, %Y")


def layout(*, title, desc, root, canonical, body, active="", og_type="website", extra_head="", scripts=""):
    """root = relative path prefix to site root ('' / '../' / '../../')."""
    nav = [("Home", f"{root}#home", "home"), ("About", f"{root}#about", "about"),
           ("Projects", f"{root}#projects", "projects"), ("Blog", f"{root}blog/", "blog"),
           ("Contact", f"{root}#contact", "contact")]
    nav_html = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{n}</a></li>' for n, h, k in nav)
    year = dt.date.today().year
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}assets/avatar.jpg">
<meta property="og:site_name" content="{SITE_TITLE}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}assets/avatar.jpg">
<meta name="theme-color" content="#4f46e5">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{SITE_TITLE} — Blog" href="{SITE}blog/feed.xml">
<script>(function(){{try{{var t=localStorage.getItem('theme');}}catch(e){{}}if(!t)t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <nav class="container nav-inner" aria-label="Main">
    <a class="brand" href="{root}"><img src="{root}assets/favicon.svg" alt="" width="28" height="28">Tran Duc Phu</a>
    <div style="display:flex;align-items:center">
      <ul class="nav-links" id="nav-links">{nav_html}</ul>
      <button class="icon-btn theme-toggle" type="button" aria-label="Toggle theme">{ICON_MOON}{ICON_SUN}</button>
      <button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-controls="nav-links" aria-expanded="false">{ICON_MENU}</button>
    </div>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="container">
    <span>&copy; {year} Tran Duc Phu</span>
    <span><a href="https://github.com/TranPhu1999">GitHub</a> · <a href="https://www.linkedin.com/in/tran-duc-phu-505841192/">LinkedIn</a> · <a href="{root}blog/feed.xml">RSS</a></span>
  </div>
</footer>
<script src="{root}assets/main.js" defer></script>
{scripts}</body>
</html>
"""


def tags_html(tags, root):
    return '<ul class="tags">' + "".join(
        f'<li><a class="tag" href="{root}blog/?topic={E(t)}">{E(t)}</a></li>' if t in TOPICS
        else f'<li class="tag">{E(t)}</li>' for t in tags) + "</ul>"


def card(p, href, heading="h3"):
    return (f'<a class="card post-card reveal" href="{href}">'
            f'<div class="meta"><time datetime="{p["date"]}">{p["date_human"]}</time> · {p["reading_time"]} min read</div>'
            f'<{heading}>{E(p["title"])}</{heading}><p>{E(p["summary"])}</p>'
            '<ul class="tags">' + "".join(f'<li class="tag">{E(t)}</li>' for t in p["tags"]) + "</ul></a>")


def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"{f}: missing YAML front matter")
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("draft"):
            continue
        body = m.group(2)
        md = markdown.Markdown(extensions=["fenced_code", "codehilite", "tables", "toc", "smarty", "footnotes"],
                               extension_configs={"codehilite": {"css_class": "hl", "guess_lang": False},
                                                  "toc": {"permalink": "#", "permalink_class": "headerlink",
                                                          "toc_depth": "2-3"}})
        content = md.convert(body)
        date = meta["date"]
        if isinstance(date, str):
            date = dt.date.fromisoformat(date)
        words = len(re.findall(r"\w+", body))
        tags = [str(t) for t in meta.get("tags", [])]
        posts.append({
            "slug": f.stem, "title": meta["title"], "date": date.isoformat(), "date_obj": date,
            "date_human": human_date(date), "tags": tags, "topics": topics_for(tags),
            "summary": meta.get("summary", ""), "cover": meta.get("cover"),
            "reading_time": max(1, math.ceil(words / 220)), "words": words,
            "html": content, "toc_tokens": md.toc_tokens,
        })
    posts.sort(key=lambda p: p["date_obj"], reverse=True)
    return posts


def toc_html(tokens):
    if not tokens:
        return ""
    def walk(ts):
        return "<ul>" + "".join(
            f'<li><a href="#{t["id"]}">{E(html.unescape(t["name"]))}</a>{walk(t["children"]) if t["children"] else ""}</li>'
            for t in ts) + "</ul>"
    return walk(tokens)


def build_post(p, prev_p, next_p):
    root = "../../"
    url = f"{SITE}blog/{p['slug']}/"
    count = sum(1 + len(t["children"]) for t in p["toc_tokens"])
    toc = (f'<aside class="toc" aria-label="Table of contents"><div class="label">On this page</div>{toc_html(p["toc_tokens"])}</aside>'
           if count >= 3 else "")
    cover = f'<img src="{E(p["cover"])}" alt="" style="margin:24px 0;border-radius:14px">' if p.get("cover") else ""
    from urllib.parse import quote
    q_url, q_title = quote(url, safe=""), quote(p["title"], safe="")
    share = (f'<div class="share"><span class="muted">Share:</span>'
             f'<a class="btn" href="https://twitter.com/intent/tweet?url={q_url}&amp;text={q_title}" rel="noopener" target="_blank">X / Twitter</a>'
             f'<a class="btn" href="https://www.linkedin.com/sharing/share-offsite/?url={q_url}" rel="noopener" target="_blank">LinkedIn</a>'
             f'<a class="btn" href="mailto:?subject={q_title}&amp;body={q_url}">Email</a>'
             f'<button class="btn" type="button" data-copy="{url}">Copy link</button></div>')
    pager = '<nav class="pager" aria-label="More posts">'
    pager += (f'<a class="card prev" href="../{next_p["slug"]}/"><div class="label">← Older</div><strong>{E(next_p["title"])}</strong></a>'
              if next_p else "<span></span>")
    pager += (f'<a class="card next" href="../{prev_p["slug"]}/"><div class="label">Newer →</div><strong>{E(prev_p["title"])}</strong></a>'
              if prev_p else "<span></span>")
    pager += "</nav>"
    body = f"""<div class="progress" aria-hidden="true"></div>
<article>
  <header class="container narrow article-head">
    <a href="../" class="meta">← All posts</a>
    <h1 style="margin-top:16px">{E(p['title'])}</h1>
    <div class="meta"><time datetime="{p['date']}">{p['date_human']}</time> · {p['reading_time']} min read</div>
    {tags_html(p['tags'], root)}
    {cover}
  </header>
  <div class="container article-layout">
    <div>
      <div class="prose">{p['html']}</div>
      {share}
      {pager}
    </div>
    {toc}
  </div>
</article>"""
    ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
                     "datePublished": p["date"], "author": {"@type": "Person", "name": AUTHOR},
                     "description": p["summary"], "url": url})
    out = layout(title=f"{p['title']} — {SITE_TITLE}", desc=p["summary"] or SITE_DESC, root=root,
                 canonical=url, body=body, active="blog", og_type="article",
                 extra_head=f'<meta property="article:published_time" content="{p["date"]}">\n'
                            f'<script type="application/ld+json">{ld}</script>\n')
    d = BLOG_DIR / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")


def build_blog_index(posts):
    root = "../"
    chips = "".join(f'<button class="filter" type="button" data-topic="{t}" aria-pressed="{"true" if t == "All" else "false"}">{t}</button>'
                    for t in ["All"] + TOPICS)
    cards = "".join(card(p, f"{p['slug']}/", "h2").replace(" reveal", "") for p in posts)
    body = f"""<section class="blog-head" style="padding-bottom:0">
  <div class="container narrow">
    <span class="eyebrow">Blog</span>
    <h1>Writing</h1>
    <p class="muted" style="font-size:1.15rem">Notes on AI engineering, the books I'm reading, and the occasional detour into philosophy and psychology. <a href="feed.xml">RSS</a></p>
    <label for="search" class="skip" style="position:static;left:auto;background:none;color:var(--muted);padding:0;display:block;margin:24px 0 8px;font-size:.9rem">Search posts</label>
    <input id="search" class="search" type="search" placeholder="Search posts…" autocomplete="off">
    <div class="filters" role="group" aria-label="Filter by topic">{chips}</div>
    <p id="count" class="meta" aria-live="polite">{len(posts)} posts</p>
    <div id="post-list" class="post-list">{cards}</div>
  </div>
</section>"""
    out = layout(title=f"Blog — {SITE_TITLE}", desc="Writing by Tran Duc Phu on AI, tech, books, philosophy and psychology.",
                 root=root, canonical=f"{SITE}blog/", body=body, active="blog",
                 scripts=f'<script src="{root}assets/blog.js" defer></script>\n')
    (BLOG_DIR / "index.html").write_text(out, encoding="utf-8")
    data = [{k: p[k] for k in ("slug", "title", "date", "date_human", "tags", "topics", "summary", "reading_time")}
            for p in posts]
    (BLOG_DIR / "posts.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def build_home(posts):
    tpl = (ROOT / "templates" / "home.html").read_text(encoding="utf-8")
    latest = "".join(card(p, f"blog/{p['slug']}/") for p in posts[:3]) or '<p class="muted">Posts coming soon.</p>'
    body = tpl.replace("{{LATEST_POSTS}}", latest)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": AUTHOR, "jobTitle": "AI Engineer",
                     "url": SITE, "sameAs": ["https://github.com/TranPhu1999",
                                             "https://www.linkedin.com/in/tran-duc-phu-505841192/"]})
    out = layout(title="Tran Duc Phu — AI Engineer", desc=SITE_DESC, root="", canonical=SITE, body=body,
                 active="", extra_head=f'<script type="application/ld+json">{ld}</script>\n')
    (ROOT / "index.html").write_text(out, encoding="utf-8")


def build_feed(posts):
    now = format_datetime(dt.datetime.now(dt.timezone.utc))
    items = ""
    for p in posts[:20]:
        url = f"{SITE}blog/{p['slug']}/"
        pub = format_datetime(dt.datetime.combine(p["date_obj"], dt.time(9, 0), dt.timezone(dt.timedelta(hours=7))))
        cats = "".join(f"<category>{E(t)}</category>" for t in p["tags"])
        items += (f"<item><title>{E(p['title'])}</title><link>{url}</link><guid isPermaLink=\"true\">{url}</guid>"
                  f"<pubDate>{pub}</pubDate>{cats}<description>{E(p['summary'])}</description>"
                  f"<content:encoded><![CDATA[{p['html'].replace(']]>', ']]]]><![CDATA[>')}]]></content:encoded></item>\n")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
<title>{SITE_TITLE} — Blog</title>
<link>{SITE}blog/</link>
<atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>
<description>Writing on AI, tech, books, philosophy and psychology.</description>
<language>en</language>
<lastBuildDate>{now}</lastBuildDate>
{items}</channel>
</rss>
"""
    (BLOG_DIR / "feed.xml").write_text(xml, encoding="utf-8")


def build_sitemap(posts):
    today = dt.date.today().isoformat()
    urls = [(SITE, today), (f"{SITE}blog/", posts[0]["date"] if posts else today)]
    urls += [(f"{SITE}blog/{p['slug']}/", p["date"]) for p in posts]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n',
        encoding="utf-8")


def main():
    posts = load_posts()
    if BLOG_DIR.exists():
        shutil.rmtree(BLOG_DIR)
    BLOG_DIR.mkdir()
    for i, p in enumerate(posts):
        build_post(p, posts[i - 1] if i > 0 else None, posts[i + 1] if i + 1 < len(posts) else None)
    build_blog_index(posts)
    build_home(posts)
    build_feed(posts)
    build_sitemap(posts)
    print(f"Built {len(posts)} posts -> blog/, index.html, blog/feed.xml, sitemap.xml")


if __name__ == "__main__":
    main()
