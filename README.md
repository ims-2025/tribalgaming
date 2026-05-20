# TribalGaming.com

The leading industry portal for tribal gaming news, policy, and directory in the United States and Canada.

## Quick start — one-file configuration

You only need to edit one file to get everything working: **`assets/js/config.js`**.

Open it and follow the comments. You'll paste in:

1. A newsletter service username (Buttondown/Mailchimp/ConvertKit)
2. A Formspree form ID for the contact form
3. An analytics ID (Plausible domain or GA4 measurement ID)

Every form on every page reads from this one file — nothing else to edit.

## Deploying

The fastest path is **Netlify drag-and-drop** — free, deploys in 30 seconds, gives you a working HTTPS URL you can point your domain at.

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag this entire folder onto the page
3. Wait ~20 seconds
4. Click "Domain settings" and add `tribalgaming.com`
5. Update DNS at your registrar per Netlify's instructions

Cloudflare Pages, Vercel, GitHub Pages, and AWS S3 + CloudFront all work the same way — the site is pure static HTML. `netlify.toml`, `_redirects`, and `vercel.json` are included to make pretty URLs and security headers work out of the box on any of them.

## What's in this build

### Pages (16 total)

Homepage, Legal Guide, Casino Directory (with interactive map), News hub + 3 full pillar articles, Compare tool, Events & Jobs, About, Contact, Editorial Standards, Advertise, Privacy Policy, Terms of Service, 404.

### Assets

- `assets/css/styles.css` — complete design system (~33 KB, includes premium polish layer)
- `assets/js/config.js` — **the one file you edit** to configure services
- `assets/js/main.js` — global interactions (form handling, analytics loader, nav)
- `assets/js/directory.js` — directory filtering, search, and map logic
- `assets/data/tribes.js` — directory data (46 operators, US + Canada)
- `assets/img/favicon.svg`, `favicon.ico`, `apple-touch-icon.png` — icons
- `assets/img/og-default.png`, `og-legal.png`, `og-directory.png`, `og-seminole.png` — 1200×630 social-share images

### SEO & infrastructure

- `sitemap.xml` — all 15 current pages
- `robots.txt` — explicitly allows GPTBot, ClaudeBot, Google-Extended, PerplexityBot
- `rss.xml` — news feed
- `netlify.toml`, `_redirects`, `vercel.json` — one-click deploy configs
- JSON-LD structured data on every content page (Organization, WebSite, Article, BreadcrumbList, CollectionPage)
- Open Graph + Twitter Card meta on every page
- Canonical URLs on every page
- Semantic HTML5, mobile-responsive (breakpoints at 900 / 800 px)

## Pre-launch checklist

- [ ] Edit `assets/js/config.js` — plug in your newsletter, Formspree, and analytics IDs
- [ ] Deploy to Netlify/Cloudflare/Vercel
- [ ] Point `tribalgaming.com` DNS at the host
- [ ] Submit `sitemap.xml` to [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ ] Claim `@tribalgaming` on X and LinkedIn — the meta tags already reference these handles
- [ ] Send yourself test submissions through the contact form and newsletter to confirm they route correctly

## What to build next (prioritised)

1. **Individual tribe profile pages** — the Directory links to 46 tribe slugs but the profile pages don't exist yet. This is the single highest-impact next build: it turns the Directory from a listing into a database.
2. **Two more news articles** — the News hub references "Tenth Circuit affirms broad scope of Class II 'technologic aid'" and "Seven takeaways from NIGA 2026" as teasers. Write them.
3. **State-level hub pages** (`/directory/california/`, `/directory/oklahoma/`, etc.) — major SEO lever for the premium domain.
4. **Deep Legal Guide subpages** — break `/legal-guide/#igra`, `/legal-guide/#class-iii`, etc. into their own URLs for individual SEO ranking.
5. **News cadence** — ship 3–5 articles/week; this is what turns a site into a publication.
6. **Real search** — [Pagefind](https://pagefind.app/) is free, static-site friendly, and drops in with one build step.
7. **Directory data licensing product** — sell the dataset to law firms, analysts, and investment banks.

## File layout

```
/
├── index.html                              # Homepage
├── 404.html
├── sitemap.xml · robots.txt · rss.xml
├── netlify.toml · _redirects · vercel.json # One-click deploy
├── README.md
│
├── about/index.html · contact/index.html
├── advertise/index.html · editorial-standards/index.html
├── privacy/index.html · terms/index.html
├── compare/index.html · directory/index.html
├── events/index.html · legal-guide/index.html
│
├── news/index.html
│   ├── seminole-compact-2026-analysis/index.html
│   ├── economic-impact-report-2025/index.html
│   └── saskatchewan-siga-expansion/index.html
│
└── assets/
    ├── css/styles.css
    ├── js/
    │   ├── config.js        ← edit this one file
    │   ├── main.js
    │   └── directory.js
    ├── data/tribes.js
    └── img/
        ├── favicon.svg · favicon.ico · apple-touch-icon.png
        └── og-*.svg · og-*.png
```

## Editorial tone

The site is written in the voice of a **leading industry portal** — think Bloomberg Law or Politico Pro, not a casino-review consumer site. Tribes are framed as governments, not businesses. Sources are cited. The Legal Guide is reviewed by outside counsel before each quarterly update (the reminder is written into the page). Before launching, have a federal Indian-law attorney review the Legal Guide for any final factual corrections you'd want to ship with.
