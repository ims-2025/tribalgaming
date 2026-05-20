# Deploying TribalGaming.com to GitHub + Vercel

A complete, step-by-step guide. About 15 minutes end-to-end if your accounts already exist.

---

## Step 0 — Configure your services (do this first)

Open `assets/js/config.js` and fill in your account credentials. **This is the one file you edit**; the whole site reads from it.

You need three things:

### Newsletter — pick one provider

| Provider | Cost | Why | Sign up |
|----------|------|-----|---------|
| **Buttondown** (recommended) | Free up to 100 subscribers | Cleanest API; built for newsletters | [buttondown.email](https://buttondown.email) |
| Mailchimp | Free up to 500 contacts | Most ubiquitous; more features | [mailchimp.com](https://mailchimp.com) |
| ConvertKit | Free up to 10,000 subscribers (without automations) | Strong for creators | [convertkit.com](https://convertkit.com) |

Whichever you pick, edit the matching `provider:` and credential in `config.js`.

### Contact form — Formspree

1. Sign up at [formspree.io](https://formspree.io) (free: 50 submissions/month)
2. Click "New form" → name it "TribalGaming Contact"
3. Copy the 8-character form ID (looks like `xabczxyz` from the URL `formspree.io/f/xabczxyz`)
4. Paste it into `config.js` → `contact.formspree.formId` and set `contact.provider: "formspree"`

### Analytics — pick one

| Provider | Cost | Why | Sign up |
|----------|------|-----|---------|
| **Plausible** (recommended) | $9/mo for one site | Privacy-friendly, no cookie banner, GDPR-clean | [plausible.io](https://plausible.io) |
| Google Analytics 4 | Free | Most data, most integrations | [analytics.google.com](https://analytics.google.com) |

For Plausible, the domain is just `tribalgaming.com`. For GA4, copy the `G-XXXXXXXXXX` measurement ID from Admin → Data Streams. Paste it into `config.js` and set the matching `provider:` value.

**Save `config.js` and commit it.** (It contains no secrets — these IDs are designed to be public.)

---

## Step 1 — Push to GitHub

From the project folder (`/Users/cg/Documents/Claude/Projects/TribalGaming`):

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit — TribalGaming.com MVP"

# Create a new private repo on github.com (use the web UI:
# https://github.com/new — name it "tribalgaming")
# Then connect this local folder to it:

git remote add origin git@github.com:YOUR_GITHUB_USERNAME/tribalgaming.git
git branch -M main
git push -u origin main
```

If you'd rather use HTTPS instead of SSH, swap the remote URL to `https://github.com/YOUR_GITHUB_USERNAME/tribalgaming.git`.

---

## Step 2 — Connect Vercel to the GitHub repo

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository" and authorize Vercel to access your GitHub account if you haven't already
3. Find `tribalgaming` in the list and click "Import"
4. On the Configure Project screen:
   - **Framework Preset**: select "Other" (it's a plain static site — no build step needed)
   - **Root Directory**: leave as `./`
   - **Build Command**: leave empty
   - **Output Directory**: leave empty (defaults to repo root, which is what we want)
   - **Install Command**: leave empty
5. Click "Deploy"

Vercel will read `vercel.json` automatically. In ~30 seconds you'll have a live URL like `tribalgaming-abc123.vercel.app`. Open it and click around — every page should work.

---

## Step 3 — Point `tribalgaming.com` at Vercel

In Vercel:

1. Open your project → Settings → Domains
2. Add `tribalgaming.com` and `www.tribalgaming.com`
3. Vercel will show you DNS records to add at your registrar (Namecheap, GoDaddy, Cloudflare, etc.):
   - An `A` record for the apex pointing to `76.76.21.21`
   - A `CNAME` record for `www` pointing to `cname.vercel-dns.com`
4. Add those records at your registrar. DNS propagation usually takes 5–30 minutes.
5. Once Vercel detects the records, it will provision SSL automatically.

You're live.

---

## Step 4 — Post-launch tasks

These take roughly an hour total and should be done within the first week:

- [ ] **Google Search Console** — Verify domain ownership, submit `https://tribalgaming.com/sitemap.xml`. [Sign in](https://search.google.com/search-console)
- [ ] **Bing Webmaster Tools** — Same thing. [Sign in](https://www.bing.com/webmasters)
- [ ] **Test the contact form** — Fill it out from a fresh browser, confirm Formspree forwards the message to your inbox
- [ ] **Test the newsletter** — Subscribe with a personal email, confirm you receive the double opt-in
- [ ] **Test the OG images** — Paste your homepage URL into the [Open Graph Debugger](https://www.opengraph.xyz/) and confirm the preview card renders
- [ ] **Test on mobile** — Open the site on your phone, scroll through every page
- [ ] **Claim social handles** — `@tribalgaming` on X and LinkedIn (the meta tags reference these handles)

---

## How updates work after launch

When you (or anyone with repo access) push to the `main` branch of the GitHub repo, Vercel auto-deploys within ~30 seconds. Workflow:

```bash
# Make edits in any editor
git add .
git commit -m "Update Legal Guide with Q2 2026 revisions"
git push
# Vercel deploys automatically
```

Pull requests also auto-create **preview deployments** at unique URLs — useful if you want to review a major change before it goes live.

---

## Troubleshooting

**"Page Not Found" on `/directory/` after deploy.**
Vercel handles trailing-slash directory URLs natively via `trailingSlash: true` in `vercel.json` — this should just work. If it doesn't, check the Deployments tab for build errors.

**Forms don't submit.**
Check the browser console. The most common cause is `config.js` still says `provider: "none"` for the relevant form.

**Analytics not showing data.**
For Plausible: the script loads asynchronously and only fires after the page is interactive — wait 30 seconds and refresh your dashboard. For GA4: data has a ~24-hour delay before appearing in standard reports (Realtime should work instantly).

**Image previews don't show on social shares.**
Some platforms (LinkedIn especially) cache OG images aggressively. Run the URL through the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) and click "Refresh" to force a re-fetch.

---

## What this build does NOT include yet

These are post-launch builds, prioritized in the project README:

1. Individual tribe profile pages (`/directory/{slug}/`) — high-leverage SEO move, ~2 days of focused work
2. State-level hub pages (`/directory/california/`, etc.)
3. Two more news articles teased on the news hub
4. Real client-side search (Pagefind drops in with one build step)
5. Newsletter archive page

When you're ready to build any of these, the patterns are established and the data is in `assets/data/tribes.js`.
