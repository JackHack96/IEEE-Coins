# IEEE COINS Conference Website

Parametrized static website for the IEEE International Conference on Omni-Layer Intelligent Systems. All content is driven by a single YAML file — no HTML editing required from year to year.

## Project Structure

```
coins-website/
├── conference.yml          ← EDIT THIS EACH YEAR (all content here)
├── build.py                ← Run to regenerate the site
├── CNAME                   ← GitHub Pages custom domain
├── templates/
│   ├── base.html           ← Shared nav + footer (reads from YAML)
│   ├── index.html          ← Homepage
│   ├── cfp.html            ← Call for Papers (tracks auto-generated from YAML)
│   ├── authors.html        ← Author's Guide
│   ├── proposals.html      ← Call for Proposals
│   ├── committee.html      ← Conference Committee (auto-generated from YAML)
│   ├── outreach.html       ← Engagement & Outreach / RAS CARES
│   ├── program.html        ← Full Schedule (tabbed, days from YAML)
│   ├── keynotes.html       ← Keynote Speakers (cards from YAML)
│   ├── tutorials.html      ← Tutorials (from YAML)
│   ├── competitions.html   ← Competitions (from YAML)
│   ├── phd-forum.html      ← PhD & Student Forum (from YAML)
│   ├── workshops.html      ← Workshops (from YAML)
│   ├── registration.html   ← Registration rates (from YAML)
│   ├── venue.html          ← Venue + photo gallery + hotels (from YAML)
│   ├── visa.html           ← VISA Information
│   └── contact.html        ← Contact (program chairs auto-populated)
├── static/
│   ├── css/style.css
│   └── js/main.js
└── dist/                   ← Generated output (deploy this to GitHub Pages)
    ├── index.html
    ├── pages/
    ├── static/
    └── CNAME
```

## Updating for a New Year

**Only edit `conference.yml`.** Every piece of content on the site is sourced from it:

| What to update | YAML key |
|---|---|
| Conference year, dates, location | `meta.edition`, `dates.*`, `venue.*` |
| Submission deadlines | `dates.deadlines[]` |
| Venue photos | `venue.photos[]` |
| Keynote speakers | `keynotes[]` |
| Tutorials | `tutorials[]` |
| Competitions | `competitions[]` |
| PhD Forum chairs | `phd_forum.chairs[]` |
| Committee members | `committee[]` |
| Track topics | `cfp.clusters[].tracks[]` |
| Registration rates | `registration.rates[]` |
| Program schedule | `program.days[].sessions[]` |
| Sponsors | `sponsors[]` |
| Past editions | `past_editions[]` |

Then run:
```bash
python build.py
```

The rebuilt site lands in `dist/`. Push that to GitHub and you're done.

## Local Development

```bash
# Install dependencies (one-time)
pip install pyyaml jinja2

# Build
python build.py

# Preview (Python's built-in server)
cd dist && python -m http.server 8000
# Open http://localhost:8000
```

## GitHub Pages Deployment

### Option A — Automatic (GitHub Actions)
Push the repository. The `.github/workflows/deploy.yml` workflow automatically:
1. Installs Python + dependencies
2. Runs `build.py`
3. Deploys `dist/` to GitHub Pages

### Option B — Manual
```bash
python build.py
cd dist
git init && git add . && git commit -m "Build"
git push -f origin main:gh-pages
```

### Custom Domain
The `CNAME` file in `dist/` is set to `coinsconf.com`. Add these DNS records at your registrar:

**A records** (point to GitHub Pages IPs):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**CNAME record**:
```
www → <your-github-username>.github.io
```

In GitHub: **Settings → Pages → Custom domain → coinsconf.com**.

## Adding a Keynote Speaker

In `conference.yml`, add an entry under `keynotes:`:

```yaml
keynotes:
  - id: "k5"
    type: "Academic Keynote"      # or "Industrial Keynote"
    name: "Jane Smith"
    affiliation: "MIT, USA"
    title: "The Future of AI Systems"
    abstract: "Abstract text here..."
    bio: "Bio text here..."
    photo: "https://example.com/photo.jpg"  # or leave "" for initials avatar
    day: "Monday, September 7, 2026"
    time: "09:00 – 10:00 CEST"
    confirmed: true
```

Run `python build.py`. The keynote card appears on both the homepage teaser and the keynotes page.

## Tech Stack

- **Python** + **Jinja2** — templating engine
- **PyYAML** — YAML parsing
- **Vanilla HTML/CSS/JS** — no frontend framework
- **GitHub Actions** — CI/CD pipeline
- **GitHub Pages** — hosting
