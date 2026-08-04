#!/usr/bin/env python3
"""
publish_daily.py — Publish a batch of TribalGaming.com articles.

Usage:
    python3 scripts/publish_daily.py manifest.json [--date YYYY-MM-DD] [--no-push] [--no-commit]

Manifest format (JSON list of 5 article specs):
[
  {
    "slug": "navajo-nation-arizona-compact-talks",
    "title": "Navajo Nation opens compact talks with Arizona governor",
    "description": "Short meta description (~155 chars) for SEO.",
    "dek": "One-line subheadline shown under H1 on the article page.",
    "kicker": "Policy · 5 min",
    "section": "policy",        // one of: policy, economy, canada, sports, properties, regulation
    "category_label": "Policy", // shown above the article H3 in the news card
    "author": "Elena Ruiz",
    "keywords": "navajo nation, arizona compact, tribal sports betting",
    "read_minutes": 5,
    "body_html": "<p>Lead paragraph...</p><h2>Section heading</h2><p>...</p>",
    "internal_links": [
      {"href": "../../directory/arizona/index.html", "label": "Arizona state hub"},
      {"href": "../../legal-guide/index.html", "label": "Legal Guide"}
    ],
    "og_image_path": "assets/img/og-default.png"  // optional, defaults to og-default.png
  },
  ...
]

The script:
  * Picks 5 distinct random timestamps spread across publish day (06:00–19:30 local),
    with a minimum 75-minute gap so they look naturally distributed.
  * Generates /news/{slug}/index.html for each article.
  * Inserts each article's URL into sitemap.xml.
  * Prepends each article's <item> into rss.xml.
  * Prepends a card for each article into the matching section of news/index.html.
  * Stages, commits, and pushes to git (unless --no-commit / --no-push).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, date, time, timezone, timedelta
from pathlib import Path

# ---- Constants -------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = REPO_ROOT / "news"
SITEMAP = REPO_ROOT / "sitemap.xml"
RSS = REPO_ROOT / "rss.xml"
NEWS_INDEX = REPO_ROOT / "news" / "index.html"
HOMEPAGE = REPO_ROOT / "index.html"

SECTION_HEADER_PATTERN = {
    "policy":    '<h2 id="policy"',
    "economy":   '<h2 id="economy"',
    "canada":    '<h2 id="canada"',
    # Fall back to policy if a section isn't on the index page yet.
}

PUBLISH_WINDOW_START_HOUR = 6
PUBLISH_WINDOW_END_HOUR = 19  # last time slot ends at 19:30
MIN_GAP_MINUTES = 75

# ---- Helpers ---------------------------------------------------------------

def pick_timestamps(d: date, n: int = 5, seed: int | None = None) -> list[datetime]:
    """Pick `n` distinct datetimes on date `d` between 06:00 and 19:30 local
    time, spaced at least MIN_GAP_MINUTES apart, with second-level jitter."""
    rng = random.Random(seed if seed is not None else f"{d.isoformat()}-tribal-gaming")
    start_minutes = PUBLISH_WINDOW_START_HOUR * 60
    end_minutes = PUBLISH_WINDOW_END_HOUR * 60 + 30
    # Sample evenly within buckets, then jitter.
    bucket_size = (end_minutes - start_minutes) / n
    minutes: list[int] = []
    for i in range(n):
        b_lo = int(start_minutes + i * bucket_size)
        b_hi = int(start_minutes + (i + 1) * bucket_size) - 1
        minutes.append(rng.randint(b_lo, b_hi))
    # Enforce min gap (sample is already monotonic by construction, but guard).
    minutes.sort()
    for i in range(1, n):
        if minutes[i] - minutes[i - 1] < MIN_GAP_MINUTES:
            minutes[i] = minutes[i - 1] + MIN_GAP_MINUTES
    out: list[datetime] = []
    for m in minutes:
        out.append(datetime(d.year, d.month, d.day, m // 60, m % 60, rng.randint(0, 59)))
    return out


def rfc2822(dt: datetime, tz_offset_hours: int = 2) -> str:
    """Format a naive datetime as RFC-2822 with a fixed TZ offset (default +02:00 for CEST)."""
    tz = timezone(timedelta(hours=tz_offset_hours))
    return dt.replace(tzinfo=tz).strftime("%a, %d %b %Y %H:%M:%S %z")


def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def published_display(dt: datetime) -> str:
    return dt.strftime("%B %d, %Y")


def safe_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


# ---- Templates -------------------------------------------------------------

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | TribalGaming.com</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{keywords}" />
<link rel="canonical" href="https://tribalgaming.com/news/{slug}/" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="https://tribalgaming.com/news/{slug}/" />
<meta property="og:image" content="https://tribalgaming.com/{og_image_path}" />
<meta property="article:published_time" content="{iso_published}" />
<meta property="article:author" content="{author}" />
<meta property="article:section" content="{category_label}" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/svg+xml" href="../../assets/img/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+Pro:wght@400;600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/css/styles.css" />

<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"NewsArticle",
  "headline":"{title_js}",
  "description":"{description_js}",
  "image":"https://tribalgaming.com/{og_image_path}",
  "author":{{"@type":"Person","name":"{author}"}},
  "publisher":{{"@type":"NewsMediaOrganization","name":"TribalGaming.com","logo":{{"@type":"ImageObject","url":"https://tribalgaming.com/assets/img/logo.png"}}}},
  "datePublished":"{iso_datetime}","dateModified":"{iso_datetime}",
  "mainEntityOfPage":"https://tribalgaming.com/news/{slug}/"
}}
</script>
</head>
<body>

<div class="topbar"><div class="container"><span class="today">{today_display}</span><span><a href="../../contact/index.html">Subscribe</a> · <a href="../../contact/index.html">Contact</a></span></div></div>
<header class="masthead"><div class="container wrap"><a class="logo" href="../../index.html"><span class="mark" aria-hidden="true"></span><span>TribalGaming<span style="color:var(--brand)">.</span>com<span class="tag">The industry portal</span></span></a></div></header>
<nav class="nav"><div class="container wrap"><a href="../../index.html">Home</a><a href="../../news/index.html" class="active">News</a><a href="../../directory/index.html">Directory</a><a href="../../legal-guide/index.html">Legal Guide</a><a href="../../compare/index.html">Compare</a><a href="../../events/index.html">Events &amp; Jobs</a><a href="../../about/index.html">About</a><span class="spacer"></span><a href="../../contact/index.html" class="cta">Daily Brief →</a></div></nav>
<div class="crumbs"><div class="container"><a href="../../index.html">Home</a><span class="sep">›</span><a href="../../news/index.html">News</a><span class="sep">›</span>{title}</div></div>

<article>
  <div class="article-head">
    <div class="container">
      <span class="kicker">{kicker}</span>
      <h1>{title}</h1>
      <p class="dek">{dek}</p>
      <div class="byline"><span><strong>By {author}</strong></span><span>Published {published_display}</span><span>{read_minutes} min read</span></div>
    </div>
  </div>

  <div class="prose">
{body_html}

    <div class="callout">
      <h4>Related reading on TribalGaming.com</h4>
      <ul>
{related_links}
      </ul>
    </div>
  </div>
</article>

<section class="newsletter">
  <div class="container wrap">
    <div><h2>Never miss the next one</h2><p>Our policy and markets coverage is exclusive to the Morning Brief. Free, five days a week, read by the people who set the rules.</p></div>
    <div><form class="form" onsubmit="event.preventDefault(); this.querySelector('button').textContent='Subscribed ✓'; this.querySelector('input').value='';"><input type="email" required placeholder="you@tribe.gov" aria-label="Email address" /><button type="submit">Subscribe</button></form></div>
  </div>
</section>

<footer class="foot">
  <div class="container">
    <div class="grid">
      <div><div style="color:#fff; font-family:var(--font-serif); font-size:22px; font-weight:800; margin-bottom:12px;">TribalGaming<span style="color:var(--brand)">.</span>com</div><p class="about">The industry portal for tribal gaming in the U.S. and Canada.</p></div>
      <div><h5>Sections</h5><ul><li><a href="../../news/index.html">News</a></li><li><a href="../../directory/index.html">Directory</a></li><li><a href="../../legal-guide/index.html">Legal Guide</a></li><li><a href="../../events/index.html">Events &amp; Jobs</a></li></ul></div>
      <div><h5>Topics</h5><ul><li><a href="../../news/index.html?t=policy">Policy</a></li><li><a href="../../news/index.html?t=sports-betting">Sports betting</a></li><li><a href="../../news/index.html?t=sovereignty">Sovereignty</a></li></ul></div>
      <div><h5>About</h5><ul><li><a href="../../about/index.html">Our mission</a></li><li><a href="../../editorial-standards/index.html">Editorial standards</a></li><li><a href="../../contact/index.html">Contact</a></li></ul></div>
      <div><h5>Follow</h5><ul><li><a href="../../contact/index.html">Morning Brief</a></li><li><a href="../../rss.xml">RSS feed</a></li></ul></div>
    </div>
    <div class="base"><span>© 2026 TribalGaming Media Corp.</span><span><a href="../../privacy/index.html">Privacy</a> · <a href="../../terms/index.html">Terms</a></span></div>
  </div>
</footer>
<script src="../../assets/js/config.js"></script>
<script src="../../assets/js/main.js" defer></script>
</body>
</html>
"""

NEWS_CARD_TEMPLATE = """      <article class="card">
        <div class="body">
          <span class="cat">{category_label}</span>
          <h3><a href="../news/{slug}/index.html">{title}</a></h3>
          <p class="dek">{dek}</p>
          <div class="meta"><span>By {author}</span><span>{short_date}</span><span>{read_minutes} min</span></div>
        </div>
      </article>
"""


# ---- Writers ---------------------------------------------------------------

def write_article(article: dict, dt: datetime) -> Path:
    slug = article["slug"]
    out_dir = NEWS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"

    related_links = "\n".join(
        f'        <li><a href="{lnk["href"]}">{lnk["label"]}</a></li>'
        for lnk in article.get("internal_links", [])
    )

    iso_dt = dt.strftime("%Y-%m-%dT%H:%M:%S+02:00")  # CEST in summer; doc-level

    rendered = ARTICLE_TEMPLATE.format(
        slug=slug,
        title=article["title"],
        title_js=article["title"].replace('"', '\\"'),
        description=article["description"],
        description_js=article["description"].replace('"', '\\"'),
        keywords=article.get("keywords", ""),
        og_image_path=article.get("og_image_path", "assets/img/og-default.png"),
        iso_published=iso_date(dt),
        iso_datetime=iso_dt,
        category_label=article["category_label"],
        author=article["author"],
        kicker=article["kicker"],
        dek=article["dek"],
        published_display=published_display(dt),
        read_minutes=article.get("read_minutes", 5),
        body_html=article["body_html"],
        related_links=related_links,
        today_display=dt.strftime("%A, %B %d, %Y"),
    )
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def update_sitemap(articles: list[dict], datetimes: list[datetime]) -> None:
    text = SITEMAP.read_text(encoding="utf-8")
    new_entries = []
    for art, dt in zip(articles, datetimes):
        lastmod = iso_date(dt)
        new_entries.append(
            f'  <url><loc>https://tribalgaming.com/news/{art["slug"]}/</loc>'
            f'<lastmod>{lastmod}</lastmod><changefreq>monthly</changefreq>'
            f'<priority>0.8</priority></url>'
        )
    # Insert before </urlset>
    if "</urlset>" in text:
        text = text.replace("</urlset>", "\n".join(new_entries) + "\n</urlset>")
        SITEMAP.write_text(text, encoding="utf-8")


def update_rss(articles: list[dict], datetimes: list[datetime]) -> None:
    text = RSS.read_text(encoding="utf-8")
    # Update lastBuildDate to the latest pubDate.
    latest = max(datetimes)
    text = re.sub(
        r"<lastBuildDate>.*?</lastBuildDate>",
        f"<lastBuildDate>{rfc2822(latest)}</lastBuildDate>",
        text, count=1,
    )
    # Build new items.
    items = []
    for art, dt in zip(articles, datetimes):
        items.append(
            "    <item>\n"
            f"      <title>{safe_xml(art['title'])}</title>\n"
            f"      <link>https://tribalgaming.com/news/{art['slug']}/</link>\n"
            f"      <guid>https://tribalgaming.com/news/{art['slug']}/</guid>\n"
            f"      <pubDate>{rfc2822(dt)}</pubDate>\n"
            f"      <description>{safe_xml(art['description'])}</description>\n"
            "    </item>\n"
        )
    items_block = "\n".join(items)
    # Insert just after the channel header (before first existing <item>).
    if "<item>" in text:
        text = text.replace("<item>", items_block + "    <item>", 1)
    else:
        text = text.replace("</channel>", items_block + "  </channel>")
    RSS.write_text(text, encoding="utf-8")


# ---- Homepage rebuild ------------------------------------------------------
#
# The homepage (`/index.html`) has two blocks that must stay fresh:
#   1. "Top stories" — a 5-card grid with a feature card on the left.
#   2. "Today at a glance" — a 5-item bullet list in the hero sidebar.
#
# Both are wrapped in sentinel comments and fully overwritten by this script
# every day. Today's newly-published 5 articles become tomorrow's homepage;
# nothing older than 24 hours ever shows on the front page.

TOP_STORIES_START = "<!-- AUTO:TOP_STORIES:START -->"
TOP_STORIES_END = "<!-- AUTO:TOP_STORIES:END -->"
GLANCE_START = "<!-- AUTO:GLANCE:START -->"
GLANCE_END = "<!-- AUTO:GLANCE:END -->"

# Category → SVG gradient palette. Keeps the feature card visually varied
# without hand-authoring per-article artwork.
_THUMB_PALETTE = {
    "policy":     ("#611d15", "#c98a1b"),  # rust → gold
    "economy":    ("#4a5d3a", "#c98a1b"),  # olive → gold
    "canada":     ("#27506b", "#f3e5c3"),  # slate blue → sand
    "regulation": ("#2a3624", "#c98a1b"),
    "sports":     ("#8a2a1f", "#f3e5c3"),
    "markets":    ("#4a5d3a", "#f3e5c3"),
}

def _thumb_svg(section: str, label: str, feature: bool = False) -> str:
    """Render a small inline SVG thumbnail for a homepage card."""
    c1, c2 = _THUMB_PALETTE.get(section.lower(), _THUMB_PALETTE["policy"])
    grad_id = f"g{abs(hash(label)) % 10000}"
    label_up = label.upper()[:14]
    if feature:
        return (
            f'<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
            f'</linearGradient></defs>'
            f'<rect width="400" height="250" fill="url(#{grad_id})"/>'
            f'<path d="M0 190 L60 160 L120 175 L200 130 L280 155 L340 120 L400 140 L400 250 L0 250 Z" fill="#2a3624" opacity=".85"/>'
            f'<circle cx="320" cy="60" r="28" fill="#f3e5c3" opacity=".9"/>'
            f'<text x="200" y="130" text-anchor="middle" font-family="Source Serif Pro" font-size="22" font-weight="700" fill="#f3e5c3">{label_up}</text>'
            f'</svg>'
        )
    return (
        f'<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="400" height="250" fill="{c1}"/>'
        f'<path d="M0 150 L100 120 L200 140 L300 110 L400 130 L400 250 L0 250Z" fill="#12130f" opacity=".7"/>'
        f'<text x="200" y="130" text-anchor="middle" font-family="Source Serif Pro" font-size="20" fill="{c2}" font-weight="700">{label_up}</text>'
        f'</svg>'
    )


def _replace_between(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    """Replace everything between start_marker and end_marker (markers preserved)."""
    s = text.find(start_marker)
    e = text.find(end_marker)
    if s == -1 or e == -1 or e < s:
        return text  # markers missing — leave file alone
    return text[: s + len(start_marker)] + "\n" + new_block + "\n      " + text[e:]


def _relative_time(dt: datetime, now: datetime) -> str:
    """Return a short 'X min ago' / 'X hrs ago' / 'Yesterday' label."""
    delta = now - dt
    seconds = delta.total_seconds()
    if seconds < 0:
        return "Just now"
    minutes = int(seconds // 60)
    if minutes < 60:
        return f"Updated {max(minutes, 1)} min ago"
    hours = int(minutes // 60)
    if hours < 12:
        return f"Updated {hours} hr{'s' if hours != 1 else ''} ago"
    days = int(hours // 24)
    if days == 0:
        return "Earlier today"
    if days == 1:
        return "Yesterday"
    if days < 7:
        return f"{days} days ago"
    return dt.strftime("%b %-d")


def update_homepage(articles: list[dict], datetimes: list[datetime]) -> None:
    """Rewrite the Top Stories grid and Today at a Glance list on index.html.

    `articles`/`datetimes` are today's newly-published batch, ordered as
    generated. The first article becomes the feature card; the remaining
    four fill the standard grid. If fewer than 5 articles are published,
    remaining slots are simply dropped rather than padded with stale data.
    """
    text = HOMEPAGE.read_text(encoding="utf-8")

    # Sort newest first so most recent shows top-left as feature.
    ordered = sorted(zip(articles, datetimes), key=lambda p: p[1], reverse=True)
    if not ordered:
        return
    feature_art, feature_dt = ordered[0]
    others = ordered[1:5]

    def _card(art: dict, dt: datetime, feature: bool) -> str:
        slug = art["slug"]
        title = html_escape(art["title"])
        dek = html_escape(art["dek"])
        cat = html_escape(art["category_label"])
        author = html_escape(art.get("author", ""))
        read = art.get("read_minutes", 5)
        short_date = dt.strftime("%b %-d, %Y")
        thumb = _thumb_svg(art.get("section", "policy"), cat, feature=feature)
        klass = "card feat" if feature else "card"
        meta_parts = []
        if feature and author:
            meta_parts.append(f"<span>By {author}</span>")
        meta_parts.append(f"<span>{read} min read</span>")
        meta_parts.append(f"<span>{short_date}</span>")
        return (
            f'      <article class="{klass}">\n'
            f'        <a class="thumb" href="news/{slug}/index.html" aria-hidden="true">{thumb}</a>\n'
            f'        <div class="body">\n'
            f'          <span class="cat">{cat}</span>\n'
            f'          <h3><a href="news/{slug}/index.html">{title}</a></h3>\n'
            f'          <p class="dek">{dek}</p>\n'
            f'          <div class="meta">{"".join(meta_parts)}</div>\n'
            f'        </div>\n'
            f'      </article>'
        )

    cards = [_card(feature_art, feature_dt, feature=True)]
    for art, dt in others:
        cards.append(_card(art, dt, feature=False))
    top_stories_block = "\n".join(cards)
    text = _replace_between(text, TOP_STORIES_START, TOP_STORIES_END, top_stories_block)

    # Today at a Glance: 5 short bullets from the same batch (newest first).
    now = max(datetimes)
    glance_lines = []
    for art, dt in ordered[:5]:
        label = html_escape(art["category_label"])
        title = html_escape(art["title"])
        stamp = _relative_time(dt, now)
        glance_lines.append(
            f'        <li><strong>{label}:</strong> {title} <span class="stamp">{stamp}</span></li>'
        )
    glance_block = "\n".join(glance_lines)
    text = _replace_between(text, GLANCE_START, GLANCE_END, glance_block)

    HOMEPAGE.write_text(text, encoding="utf-8")


def html_escape(s: str) -> str:
    """Minimal HTML escape for attribute-safe text nodes."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def update_news_index(articles: list[dict], datetimes: list[datetime]) -> None:
    text = NEWS_INDEX.read_text(encoding="utf-8")
    for art, dt in zip(articles, datetimes):
        section = art.get("section", "policy").lower()
        anchor = SECTION_HEADER_PATTERN.get(section, SECTION_HEADER_PATTERN["policy"])
        card = NEWS_CARD_TEMPLATE.format(
            slug=art["slug"],
            title=art["title"],
            dek=art["dek"],
            author=art["author"],
            category_label=art["category_label"],
            short_date=dt.strftime("%b %-d, %Y"),
            read_minutes=art.get("read_minutes", 5),
        )
        # Find the section's <div class="news-grid"> opening and insert the card right after.
        idx = text.find(anchor)
        if idx == -1:
            # Section missing — fall back to policy
            idx = text.find(SECTION_HEADER_PATTERN["policy"])
        grid_idx = text.find('<div class="news-grid">', idx)
        if grid_idx == -1:
            continue
        insert_at = grid_idx + len('<div class="news-grid">') + 1
        text = text[:insert_at] + card + text[insert_at:]
    NEWS_INDEX.write_text(text, encoding="utf-8")


# ---- Git -------------------------------------------------------------------
#
# We do all git operations inside a fresh /tmp clone, not in REPO_ROOT, for
# two reasons:
#   1. The Cowork sandbox mount may forbid `unlink`, which breaks `git`'s
#      lock-file cleanup. Doing git work in a normal /tmp dir avoids that.
#   2. It keeps the user's local working tree clean even when push fails.
#
# Credentials: pulled from (in order)
#   • env var GITHUB_TOKEN
#   • env var GH_TOKEN
#   • a file at REPO_ROOT/.github_token (gitignored — single line, no newline)
# If none found, push is skipped with a clear instruction message.

CHANGED_PATHS = [
    "sitemap.xml",
    "rss.xml",
    "news/index.html",
    "index.html",
]
# Plus each new news/{slug}/ directory we wrote, tracked in `written`.


def _read_token() -> str | None:
    for env_var in ("GITHUB_TOKEN", "GH_TOKEN"):
        tok = os.environ.get(env_var)
        if tok:
            return tok.strip()
    token_file = REPO_ROOT / ".github_token"
    if token_file.exists():
        return token_file.read_text(encoding="utf-8").strip()
    return None


def _get_remote_url() -> str:
    """Read the remote URL from REPO_ROOT/.git/config (works in read-only mounts)."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Could not read origin URL: {result.stderr.strip()}")
    return result.stdout.strip()


def _authed_url(url: str, token: str) -> str:
    """Embed token into an https GitHub URL."""
    if url.startswith("https://"):
        # Strip any existing user:pass@ then re-embed token
        rest = url[len("https://"):]
        if "@" in rest:
            rest = rest.split("@", 1)[1]
        return f"https://x-access-token:{token}@{rest}"
    return url  # ssh URLs — assume keys already configured


def git_commit_and_push(
    commit_message: str,
    new_slugs: list[str],
    do_commit: bool,
    do_push: bool,
) -> None:
    if not do_commit:
        print("→ Skipping commit (--no-commit)")
        return

    token = _read_token()
    remote_url = _get_remote_url()
    push_url = _authed_url(remote_url, token) if token else remote_url

    with tempfile.TemporaryDirectory(prefix="tg-push-") as workdir:
        # Clone fresh into /tmp clone (always uses authed URL if token present).
        clone_url = _authed_url(remote_url, token) if token else remote_url
        r = subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, workdir],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"git clone failed: {r.stderr.strip() or r.stdout.strip()}")
            print("→ Files are written locally but were not pushed.")
            return

        # Copy each changed file/dir from REPO_ROOT into the clone.
        for rel in CHANGED_PATHS:
            src = REPO_ROOT / rel
            dst = Path(workdir) / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, dst)
        for slug in new_slugs:
            src_dir = REPO_ROOT / "news" / slug
            dst_dir = Path(workdir) / "news" / slug
            if src_dir.is_dir():
                if dst_dir.exists():
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir)

        # Commit.
        env = os.environ.copy()
        env.setdefault("GIT_AUTHOR_NAME", "TribalGaming Auto-Publisher")
        env.setdefault("GIT_AUTHOR_EMAIL", "onlineprojects@pm.me")
        env.setdefault("GIT_COMMITTER_NAME", "TribalGaming Auto-Publisher")
        env.setdefault("GIT_COMMITTER_EMAIL", "onlineprojects@pm.me")

        r = subprocess.run(
            ["git", "-C", workdir, "add", "-A"],
            capture_output=True, text=True, env=env,
        )
        r = subprocess.run(
            ["git", "-C", workdir, "commit", "-m", commit_message],
            capture_output=True, text=True, env=env,
        )
        print(f"git commit: {(r.stdout + r.stderr).strip()}")
        if r.returncode != 0 and "nothing to commit" in (r.stdout + r.stderr):
            return

        if not do_push:
            print("→ Skipping push (--no-push)")
            return
        if not token:
            print(
                "→ No GitHub token found (set $GITHUB_TOKEN, $GH_TOKEN, "
                "or write a token to .github_token in the repo root). "
                "Articles were written locally; run `git pull && git push` "
                "from your terminal to deploy."
            )
            return

        # Push using authed URL (set explicitly to be safe).
        subprocess.run(
            ["git", "-C", workdir, "remote", "set-url", "origin", push_url],
            capture_output=True, text=True, env=env,
        )
        r = subprocess.run(
            ["git", "-C", workdir, "push", "origin", "HEAD:main"],
            capture_output=True, text=True, env=env,
        )
        out = (r.stdout + r.stderr).strip()
        # Redact token if it ever leaks into the output.
        if token:
            out = out.replace(token, "***")
        print(f"git push: {out}")


# ---- Lock-file safety ------------------------------------------------------
#
# When this script runs from the Cowork sandbox, the user's local repo is
# mounted via FUSE. The mount permits writes and renames but DENIES unlink.
# That means if anything in the parent shell session (e.g. an ad-hoc
# `git status` run by the agent before/after this script) leaves behind a
# `.git/index.lock`, the sandbox cannot `rm` it — and the user's next
# commit in GitHub Desktop will fail with "A lock file already exists".
#
# We can't delete the file from the sandbox, but we CAN rename it, which is
# enough to clear git's lock check. Run this at the start of main() and again
# after the script finishes so a clean handoff is guaranteed.

def clear_index_lock() -> None:
    lock = REPO_ROOT / ".git" / "index.lock"
    if not lock.exists():
        return
    # Try a normal unlink first (works on the user's macOS).
    try:
        lock.unlink()
        return
    except OSError:
        pass
    # Fall back to rename (works in the FUSE-mounted sandbox).
    try:
        orphan = REPO_ROOT / ".git" / f"index.lock.orphan-{int(datetime.now().timestamp())}"
        lock.rename(orphan)
    except OSError as e:
        print(f"⚠ Could not clear stale .git/index.lock: {e}", file=sys.stderr)


# ---- Entrypoint ------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--date", type=str, default=None,
                        help="Override publish date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--seed", type=int, default=None,
                        help="Optional seed for deterministic time selection.")
    args = parser.parse_args()

    # Clear any stale .git/index.lock left behind by an earlier session.
    clear_index_lock()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, list) or not manifest:
        print("manifest must be a non-empty JSON list", file=sys.stderr)
        return 2

    pub_date = (
        datetime.strptime(args.date, "%Y-%m-%d").date()
        if args.date else date.today()
    )
    datetimes = pick_timestamps(pub_date, n=len(manifest), seed=args.seed)
    print(f"Publish date: {pub_date.isoformat()}")
    print("Timestamps:", [dt.strftime("%H:%M:%S") for dt in datetimes])

    # Normalize / validate slugs.
    for art in manifest:
        art["slug"] = slugify(art.get("slug") or art["title"])

    # Write each article (skip if directory already exists with content).
    written: list[tuple[dict, datetime]] = []
    for art, dt in zip(manifest, datetimes):
        target = NEWS_DIR / art["slug"] / "index.html"
        if target.exists() and target.stat().st_size > 1000:
            print(f"  · skip (already exists): {art['slug']}")
            continue
        path = write_article(art, dt)
        written.append((art, dt))
        print(f"  + wrote: {path.relative_to(REPO_ROOT)}")

    if not written:
        print("Nothing new to publish.")
        return 0

    new_articles = [a for a, _ in written]
    new_datetimes = [d for _, d in written]

    update_sitemap(new_articles, new_datetimes)
    print("  + updated sitemap.xml")

    update_rss(new_articles, new_datetimes)
    print("  + updated rss.xml")

    update_news_index(new_articles, new_datetimes)
    print("  + updated news/index.html")

    update_homepage(new_articles, new_datetimes)
    print("  + updated homepage top stories + glance")

    commit_message = (
        f"Daily content: {len(new_articles)} article(s) for {pub_date.isoformat()}"
    )
    git_commit_and_push(
        commit_message,
        new_slugs=[a["slug"] for a in new_articles],
        do_commit=not args.no_commit,
        do_push=not args.no_push,
    )
    # Final safety pass: ensure no lock file lingers for the user's next
    # GitHub Desktop commit.
    clear_index_lock()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
