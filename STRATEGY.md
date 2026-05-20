# TribalGaming.com — 360 SEO & Content Strategy

A 12-month plan to turn this premium one-word domain into the dominant search and reference destination for tribal gaming in the U.S. and Canada.

---

## 1. The opportunity and the moat

Tribal gaming is a **$41 billion industry covered by no professional trade publication**. Casino.org and similar consumer sites won't touch the policy depth. Legal trade press (Law360, Bloomberg Law) hits the topic occasionally but charges $5K/year. NIGA and NIGC publish to their members. There is no Bloomberg, no Politico Pro, no Variety for tribal gaming.

That gap is our moat. The domain `tribalgaming.com` does half the work for us — it's the exact-match brand for the category. The other half is execution: depth, frequency, and trust.

**Strategic positioning:** TribalGaming.com is the *industry of record* for tribal gaming — the publication tribal leaders, regulators, attorneys, and operators read first. Not a consumer review site. Not an affiliate. A trade publication on a premium domain.

---

## 2. Keyword strategy

We compete in four keyword tiers. We win on tiers 1 and 2, build authority in tier 3, and ignore tier 4.

### Tier 1 — Branded & exact-intent (we should rank #1 within 90 days)

| Keyword | Monthly volume (est.) | Why we win |
|---------|---|---|
| tribal gaming | 4,400 | Exact-match domain |
| Indian gaming | 3,200 | Definitive Legal Guide |
| tribal casinos | 6,600 | Directory page |
| tribal casino directory | 720 | We literally built one |
| largest tribal casinos | 1,000 | Compare tool + ranking content |
| IGRA | 2,400 | Most comprehensive guide online |
| Indian Gaming Regulatory Act | 1,300 | Same |
| tribal-state compact | 590 | Owned via Legal Guide § 6 |

### Tier 2 — State / nation specific (high-value, low competition, build via state hub pages)

Geography is the biggest unclaimed SEO opportunity. Build a state hub for each of the 29 tribal-gaming states + 5 Canadian provinces.

| Pattern | Volume per state (typical) | Notes |
|---------|---|---|
| `[state] tribal casinos` | 200–4,000/mo | Owns the local-discovery query |
| `tribal casinos in [state]` | 300–2,500/mo | Same query, different word order |
| `Native American casinos [state]` | 150–800/mo | Vocabulary varies by region |
| `largest casino in [state]` | 500–8,000/mo | Most-clicked tribal casino is usually the answer |
| `[tribe name] casino` | 100–6,000/mo | Owned via individual tribe pages |

A California hub alone could pull 30,000+ monthly organic visits.

### Tier 3 — Topical authority (cumulative, build through news cadence)

| Cluster | Example queries |
|---------|---|
| Policy & compacts | "Seminole compact," "West Flagler ruling," "California sports betting tribal" |
| Sovereignty | "tribal sovereignty," "domestic dependent nation," "Cabazon decision" |
| Economics | "tribal gaming revenue," "Indian gaming GDP," "tribal employment casinos" |
| Sports betting | "tribal sports betting states," "tribal mobile sports betting" |
| Canada | "First Nations casinos Canada," "SIGA Saskatchewan," "Casino Rama revenue sharing" |
| Regulation | "NIGC MICS," "Title 31 tribal casinos," "tribal gaming compliance" |

### Tier 4 — Skip these

- "Online casino" / "best slots" / "casino bonuses" — wrong intent, wrong moat
- Affiliate-style "best tribal casino bonuses" — incompatible with editorial positioning
- Foreign-language casino terms — wrong audience entirely

---

## 3. Site architecture moves (the SEO multipliers)

These three site-architecture builds are the highest-leverage SEO moves available. They each transform one of the existing pages into a hub that ranks across dozens of long-tail queries.

### A. Individual tribe profile pages (46 → eventually 245)

**Current:** Directory page lists 46 operators with a single description per row.
**Move:** Each operator gets its own URL at `/directory/{slug}/` with a structured profile.

**Template per page (~800–1,500 words):**
- Tribe name, federally recognized status, year, location
- Reservation map + tribal-government link
- IGRA class, compact summary (link to Legal Guide)
- Property list with addresses, sizes, opening dates, games offered
- Management company (if applicable) and ownership structure
- Headline economic figures (GGR if disclosed, employees, revenue-sharing payments)
- Recent news (auto-populated from our news section by tag)
- Compact history / amendments
- "Compare with…" widget (uses existing Compare tool)

**SEO returns:** Each tribe page ranks for `{tribe name} casino`, `{property name}`, `{tribe} compact`, `{property} hotel`, `{property} games` — typically 30–80 long-tail queries per page.

**Schema.org additions per profile:** `Organization` (for the tribe), `LocalBusiness` for each property, `Place` for the reservation.

**Effort:** ~3 hours per profile if you have the data already; ~6 hours with research. Start with the top 25 by GGR (Seminole, Chickasaw, Choctaw OK, Cherokee Nation, EBCI, Mohegan, Mashantucket, Pechanga, San Manuel, Morongo, Agua Caliente, Yaamava'/San Manuel, Coushatta, Mississippi Choctaw, Shakopee, Soaring Eagle/Saginaw Chippewa, Four Winds/Pokagon, Tulalip, Muckleshoot, Puyallup, Cowlitz/ilani, Snoqualmie, Mohawk Akwesasne, SIGA Saskatchewan, Casino Rama/Rama FN). After top 25, scale to remainder over the next 6 months.

### B. State / province hub pages (34 pages)

**URL pattern:** `/directory/california/`, `/directory/oklahoma/`, `/directory/saskatchewan/`

**Template per state (~1,200–2,000 words):**
- "Tribal gaming in {state}: complete guide" H1
- Top-of-page stats: number of tribes, properties, estimated GGR, jobs supported
- Permitted-gaming summary with state-specific compact details
- Map (filtered slice of our existing US/Canada map)
- All tribes in the state with one-card-each (linking to their profile)
- Notable properties (largest by floor)
- State-specific compliance / regulatory notes
- Recent state-related news (auto-pulled by tag)
- FAQ section answering 5–8 common queries
- Links out to the relevant state gaming commission

**SEO returns:** Each hub ranks for `{state} tribal casinos`, `Indian casinos in {state}`, `Native American casinos {state}`, `tribal gaming {state}`, and 20–50 related queries.

**Effort:** ~4 hours per state.

**Priority order (by traffic potential, biggest first):**
1. California — largest tribal market
2. Oklahoma — most tribes
3. Florida — Seminole monopoly, sports betting
4. Connecticut — Foxwoods + Mohegan Sun
5. Michigan — most online activity
6. Arizona — fast-growing sports betting
7. Washington
8. Minnesota
9. Wisconsin
10. New York
11. New Mexico
12. North Carolina (EBCI)
13. Mississippi
14. Alabama (Poarch)
15. Louisiana
16. Other 14 US states + Canadian provinces

### C. Legal Guide subpage breakup

**Current:** Everything lives in one /legal-guide/ URL.
**Move:** Each major section becomes its own URL while the umbrella page becomes a structured index that links out and ranks for the broad term.

**New URLs to create:**
- `/legal-guide/igra/` — IGRA explained
- `/legal-guide/class-i-gaming/`
- `/legal-guide/class-ii-gaming/` — bingo & technologic aid
- `/legal-guide/class-iii-gaming/` — Class III + compacts
- `/legal-guide/sports-betting/` — Murphy, hub-and-spoke, by-state
- `/legal-guide/online-gaming/` — iGaming + state-by-state
- `/legal-guide/canada/` — Criminal Code § 207 framework
- `/legal-guide/section-20/` — newly acquired lands
- `/legal-guide/revenue-sharing/` — RAPs and state shares
- `/legal-guide/bank-secrecy-act/` — Title 31 obligations
- `/legal-guide/nigc-mics/` — Minimum Internal Control Standards

Each gets 1,500–3,500 words of substantive content (we already have most of it — it's a matter of breaking apart, expanding, and adding examples).

**SEO returns:** Each subpage independently ranks for its core term and dozens of long-tail variations. The original Legal Guide URL still ranks for the umbrella term ("tribal gaming legal guide") and serves as a hub.

**Schema additions:** `Article` per subpage with `about` properties referencing the statute.

**Effort:** ~6 hours per subpage. Do 2 per week → done in 6 weeks.

---

## 4. Content cadence (news + evergreen)

### News — minimum 3 articles/week, target 5/week

**Why cadence matters more than perfection:** Google's news algorithm rewards consistency. A site publishing 5 articles/week (even short ones) outranks a site publishing one long article every two weeks. We have to publish frequently.

**Editorial calendar:**

| Day | Beat | Format |
|-----|------|--------|
| Monday | Policy & compacts | 600–1,500 words |
| Tuesday | Canada / First Nations | 500–1,200 words |
| Wednesday | Property / operator news | 400–800 words |
| Thursday | Long-form analysis | 1,500–3,500 words |
| Friday | Week-in-review + Morning Brief lead | 800–1,200 words |

**Article types to rotate:**
- Compact-amendment coverage (every new one is a story)
- NIGC enforcement actions and bulletins
- State legislative tracking (when bills affect tribal gaming)
- Court rulings and appeals (federal, state, tribal)
- Property openings, expansions, closures, sales
- Sports-betting handle and revenue announcements
- M&A and JV announcements
- People moves (CEO/GC/Chair appointments)
- Quarterly earnings (for tribes/operators that disclose)
- Conference recaps (NIGA, G2E, OIGA, CNIGA, WIGA)
- Annual reports analysis (NIGC, AGA, NIGA, state agencies)

**Where to source ideas every Monday:**
- NIGC website (notices, enforcement actions, MICS bulletins)
- State gaming commission newsletters
- Federal Register tribal-affairs notices
- PACER filings (federal court tribal-gaming dockets)
- Tribal-newspaper feeds (Indian Country Today, Native News Online)
- Twitter/X lists (tribal communications staff, gaming attorneys)
- LinkedIn (tribal-government appointments)

### Evergreen pillar content (one per month, indefinitely)

These are big rocks — research-heavy, link-bait pieces that earn backlinks and keep ranking for years.

**First 12 to publish, in order:**

1. **"The 25 largest tribal casinos by GGR, 2026"** — annual flagship ranking. The kind of post Forbes would write if they covered the industry.
2. **"Tribal gaming: a complete history 1979–2026"** — long-form historical narrative, citing primary sources. Will rank for "history of Indian gaming" forever.
3. **"Every tribal-state compact, ranked by revenue share to the state"** — original data analysis.
4. **"How tribal casinos work, in plain English"** — 101 explainer for general readers + journalists. Easy to link to.
5. **"The 10 most important federal Indian-law cases for gaming attorneys"** — Cabazon → Seminole → Murphy → West Flagler.
6. **"Tribal gaming employment: who works at tribal casinos"** — labor-market piece.
7. **"Sports betting compact tracker: every state, every tribe"** — data-rich, regularly updated.
8. **"What tribal gaming revenue actually pays for"** — community-investment piece. Photo-rich.
9. **"The compact-negotiation playbook"** — interviews with attorneys who've negotiated them.
10. **"Class II vs Class III: a player's guide"** — technical but useful for journalists too.
11. **"First Nations gaming in Canada: a province-by-province guide"** — parallel to U.S. state hubs.
12. **"Tribal gaming's biggest M&A deals, 1990–2026"** — historical with current implications.

**Effort:** 8–20 hours each. Don't ship 1–12 in order one a month — that's slow. Front-load #1, #4, and #7 in months 1–2; they're the highest-traffic pieces and they're not as research-heavy as the historical pieces.

### Original data products (one per quarter)

These are the *industry-of-record* moves — original research no one else publishes, which earns press citations and high-quality backlinks for years.

**Year-1 plan:**
- **Q2 2026:** "TribalGaming.com Revenue Index" — a quarterly aggregated GGR estimate by region, methodology disclosed. Compete with the NIGC's annual report (we publish quarterly).
- **Q3 2026:** "TribalGaming.com Compact Tracker" — interactive table tracking every active compact, term, renewal date, revenue share, sports-betting authorization, online authorization. Updated continuously.
- **Q4 2026:** "Annual State of Tribal Gaming" report — 40-page PDF, gated for email signup. Major link bait + newsletter acquisition channel.
- **Q1 2027:** "Tribal Gaming Career Survey" — anonymous compensation data for the industry. Annual.

---

## 5. Technical SEO checklist

Most of this is done. The remaining tightening:

### Already in place
- [x] Sitemap, robots.txt, RSS feed
- [x] Canonical URLs on every page
- [x] Open Graph + Twitter Card tags
- [x] JSON-LD: Organization, WebSite, Article, NewsArticle, BreadcrumbList, CollectionPage
- [x] Mobile-responsive design
- [x] Semantic HTML5
- [x] Security headers via vercel.json
- [x] One-year asset caching

### To add (in priority order)

**Week 1**
- Submit `https://tribalgaming.com/sitemap.xml` to Google Search Console (free, takes 2 min)
- Submit to Bing Webmaster Tools (mirrors automatically to Yandex, DuckDuckGo)
- Add Google Search Console verification meta tag to homepage
- Set up Plausible or GA4 (the config.js wiring is already there)

**Week 2–4**
- Add `FAQPage` schema to the Legal Guide FAQ section (already structured for it — just needs the JSON-LD)
- Add `JobPosting` schema to each job-board listing (huge traffic potential — these show in Google's Jobs widget)
- Add `Event` schema to each event-calendar entry (qualifies for Google's Events widget)
- Add `LocalBusiness` schema to tribe profile pages as they're built
- Add author bio pages with `Person` schema (E-E-A-T signal — "Expertise, Experience, Authoritativeness, Trustworthiness")

**Month 2**
- Install Pagefind for client-side search (no backend, free, replaces the dead `/search` form)
- Build an XML sitemap index (split sitemap by section once we exceed 200 URLs)
- Add hreflang tags if/when Canadian-French content launches
- Consider RSS-to-newsletter automation (Buttondown supports this)
- Implement reading-progress tracking → reading-time average per page (Plausible custom events)

**Month 3+**
- Core Web Vitals tuning. Current state is fine (we use only Google Fonts + one small JS file) but worth tracking. Add a CrUX dashboard in Search Console.
- AMP — skip. Google has effectively deprecated AMP for editorial content.
- Web Stories — skip until we have 100+ articles.

---

## 6. Authority building (the slowest, most important channel)

SEO at scale is downstream of authority. Without backlinks from sites Google trusts, the content above ranks slowly. Three plays:

### A. Be a primary source

Tribal-gaming reporting is full of citations to NIGA press releases and AP wire copy. Most reporters can't reach NIGC enforcement actions, can't read PACER, can't track all 245 tribes. We can. **Every article must cite a primary source.** When we're the only place that links to a specific NIGC notice or court ruling, journalists writing about that ruling will eventually link to us.

### B. Outreach plays

- **HARO / Qwoted / Help A B2B Writer** — sign up; respond to 3 queries/week on Indian gaming. Most queries get picked up; each pickup is a backlink from a journalist's article.
- **Indian-law school partnerships** — University of New Mexico, Arizona State, Lewis & Clark, University of Tulsa have Indian-law programs. Offer to write a guest column for their alumni newsletter. They'll link back.
- **NAJA & SPJ** — pitch the Native American Journalists Association and the Society of Professional Journalists about coverage standards in tribal gaming. Offer a styleguide contribution.
- **State Indian Gaming Associations** — CNIGA, OIGA, WIGA all have member-resources sections. Get TribalGaming.com added to "industry resources."
- **Wikipedia citations** — many tribal-gaming Wikipedia articles cite weak sources. Edit them with primary-source citations and link to our Legal Guide where appropriate. **Be careful — Wikipedia editors hate promotional editing. Stick to verifiable, sourced edits.**

### C. Be quotable

Every quote we publish from an attorney, regulator, or tribal official should reach that person before publication for accuracy verification. They will share the article. Their colleagues will link to it. This is the slowest part of authority-building but it compounds.

---

## 7. Distribution (own the audience, don't rent it from Google)

SEO is one channel. Newsletter, email, and social are the others. Concretely:

### Morning Brief newsletter
- **Cadence:** five days a week, Mon–Fri, in-box by 7 a.m. Eastern.
- **Format:** 5 top stories with 60-word summaries + links. Single sponsor slot up top.
- **Acquisition channels:**
  - Footer signup on every page (already wired)
  - Article-end "Get this in your inbox" CTA (add to every article)
  - Lead-magnet PDFs (the annual State of Tribal Gaming report) gated behind signup
  - Conference badge swap (offer trade subscriptions to conference attendees in exchange for email)
- **Goal:** 5,000 subscribers by month 6, 15,000 by month 12.

### LinkedIn
- This is the right platform for our professional audience.
- Post every article + a 300-word commentary takeaway.
- Engage with tribal-government LinkedIn accounts (they post regularly and have small reach — we can amplify).
- Goal: 2,500 followers in 90 days.

### X / Twitter
- Lower priority but still relevant for breaking news.
- Auto-post via the RSS feed; manual breaking news only.

### RSS
- Already published. Many tribal-government communications offices use RSS aggregators. Make sure feed includes full content (not just titles) so they can republish excerpts with attribution.

### Aggregator submissions
- Submit articles to Google News Publisher Center (Google News inclusion takes 2–4 weeks)
- Submit to Apple News Publisher (free, takes 5 minutes)
- Bing News Submission (free)
- Memeorandum / Techmeme — not relevant. Skip.

---

## 8. Measurement & KPIs

Track weekly, review monthly. Boring; essential.

**North-star metrics:**
- Organic monthly sessions
- Newsletter subscribers
- Indexed pages in Google Search Console
- Average position for tier-1 keywords

**Diagnostic metrics:**
- Domain Authority (Moz) / Domain Rating (Ahrefs) — backlink proxy
- Average reading time per page
- Bounce rate by section
- Newsletter open rate (target 35%+ — possible because the audience is highly engaged)
- Newsletter click-through rate (target 8%+)
- Pages per session (target 2.5+)

**6-month targets (assuming 5 articles/week + state hubs + tribe profiles shipping on schedule):**
- 75,000 organic monthly sessions
- 8,000 newsletter subscribers
- Rank #1–3 for: "tribal gaming," "tribal casinos," "IGRA," "tribal casino directory"
- Rank top-10 for 200+ tier-2 keywords

**12-month targets:**
- 250,000 organic monthly sessions
- 20,000 newsletter subscribers
- Domain Authority 35+ (from 0 today)
- Rank top-3 for every "tribal casinos in {state}" query for the 29 tribal-gaming states

---

## 9. Sequencing — what to do in what order

### Month 1 — Foundation + state hubs (highest leverage)

**Week 1:**
- Submit sitemap to Google Search Console + Bing
- Wire up Buttondown + Formspree + Plausible (the config.js plumbing is ready)
- Publish 3 news articles (just whatever's in the news that week — start the cadence)
- Build California, Oklahoma, Florida state hubs

**Week 2:**
- Build Connecticut, Michigan, Arizona, Washington state hubs
- Publish 4 news articles
- Add FAQPage schema to Legal Guide

**Week 3:**
- Build Minnesota, Wisconsin, New York, New Mexico hubs
- Publish 4 news articles
- Start pillar article #1 ("25 largest tribal casinos by GGR")

**Week 4:**
- Build North Carolina, Mississippi, Alabama, Louisiana hubs (14 of 29 states done)
- Publish 4 news articles
- Ship pillar #1
- Begin tribe-profile template build (top 5: Seminole, Chickasaw, Choctaw OK, Cherokee Nation, EBCI)

### Month 2 — Tribe profiles + Legal Guide breakup

- Build remaining 15 state hubs (29 of 29 done)
- Build tribe profiles 6–25 (top 25 by GGR done)
- Break up the Legal Guide into 11 subpages
- Continue news cadence (4–5/week)
- Ship pillar #4 ("How tribal casinos work")

### Month 3 — Compact tracker + Canadian provinces

- Build Canadian province hubs (Saskatchewan, Ontario, Alberta, British Columbia, Manitoba, Quebec — 6 pages)
- Build tribe profiles 26–60
- Launch the Compact Tracker (pillar #7) as a structured-data page
- Continue news cadence
- Begin Q1 data product: TribalGaming.com Revenue Index

### Months 4–6 — Scale + first data product

- Finish all 245 tribe profiles (this is a big push but it pays for a decade)
- Publish pillar articles #2, #3, #5, #6
- Launch the Revenue Index
- Conference outreach for NIGA Mid-Year (May) — get speaker slot or panel discussion
- Continue news cadence
- Goal: cross 50,000 monthly organic sessions

### Months 7–12 — Authority + flagship report

- Quarterly Revenue Index updates
- Ship pillar articles #8, #9, #10, #11, #12
- Begin the annual "State of Tribal Gaming" report (publishes January)
- Career Survey launches Q1 2027
- Hire freelance contributors (2–3 part-time) to maintain news cadence as you scale other work
- Goal: cross 150,000 monthly organic sessions, 12,000 newsletter subscribers

---

## 10. Costs (rough order-of-magnitude)

Most of this can run on $0–$500/month with the founder doing the work. Bigger spend buys speed, not capability.

| Item | Lean | Funded |
|---|---|---|
| Hosting (Vercel) | $0 (hobby tier OK for first 6 months) | $20/mo (Pro) once >100GB bandwidth |
| Analytics (Plausible) | $9/mo | $19/mo |
| Newsletter (Buttondown) | $9/mo | $29/mo at 5K subscribers |
| Forms (Formspree) | $0 | $10/mo |
| Domain (already owned) | — | — |
| Freelance writers | $0 (founder writes all) | $500–1,500/article × 4–8/mo = $2K–12K/mo |
| Data tools (Ahrefs/Semrush) | $0 (use Google Search Console only) | $99/mo for Ahrefs Lite |
| Research subscriptions (PACER, etc.) | ~$30/mo PACER + free NIGC | Same |
| Image / icon licensing | $0 (SVG illustrations like ours) | $200/mo stock |
| Total | **~$50/mo** | **~$3,000/mo at scale** |

The big spend is your time. A founder-written version of this strategy is 20–40 hours/week. With one part-time freelance writer at $1,500/article × 4/mo = $6,000/mo, you can drop founder time to 15 hours/week and ship the same volume.

---

## 11. What to skip

I'll save you from rabbit holes:

- **Pinterest, TikTok, Instagram** — wrong audience.
- **YouTube** — only worth it if you commit. Don't half-do it. Possibly month 12+.
- **Paid Google Ads** — for tier-1 branded terms, you'll rank organically faster than you can profitably bid.
- **Programmatic SEO** (generating thousands of templated pages from a database) — Google penalizes this for editorial sites. Build the 245 tribe profiles as real, hand-edited pages. The directory data file (tribes.js) is a starting point, not a substitute.
- **AI-generated articles at scale** — Google's recent updates demote sites that publish unedited AI content. Use AI for research support, never for the final copy.
- **Comments** — moderation cost is high, value is low for a B2B trade pub. Skip.
- **Forum / community** — same.
- **Crypto / Web3 angles** — irrelevant to the audience.

---

## 12. The one-line version

**Build state hubs and tribe profiles, ship news 5x/week, publish one original-research pillar per month, and the domain will do the rest.**

---

*Last updated: 2026-04-23. Maintained as a living document — open a PR or send corrections to editor@tribalgaming.com.*
