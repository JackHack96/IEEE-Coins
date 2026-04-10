#!/usr/bin/env python3
"""
IEEE COINS Website Builder
Usage: python build.py
Reads conference.yml, renders Jinja2 templates → dist/
"""
import os, shutil, yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE   = Path(__file__).parent
TMPL   = BASE / "templates"
STATIC = BASE / "static"
DIST   = BASE / "dist"

# ── load conference data ──────────────────────────────────────
with open(BASE / "conference.yml", encoding="utf-8") as f:
    conf = yaml.safe_load(f)

# ── Jinja2 environment ────────────────────────────────────────
env = Environment(
    loader=FileSystemLoader(str(TMPL)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# ── helpers ───────────────────────────────────────────────────
def render(template_name, out_path, extra=None):
    t = env.get_template(template_name)
    ctx = {"conf": conf}
    if extra:
        ctx.update(extra)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(t.render(**ctx), encoding="utf-8")
    print(f"  ✓  {out_path.relative_to(DIST)}")

# ── clean & rebuild dist ──────────────────────────────────────
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

# copy static assets
shutil.copytree(STATIC, DIST / "static")

# copy CNAME
cname = BASE / "CNAME"
if cname.exists():
    shutil.copy(cname, DIST / "CNAME")

# copy GitHub Actions workflow
gha_src = BASE / ".github"
if gha_src.exists():
    shutil.copytree(gha_src, DIST / ".github")

print("\nBuilding IEEE COINS website...\n")

# ── root pages ────────────────────────────────────────────────
render("index.html",        DIST / "index.html")

# ── sub-pages ─────────────────────────────────────────────────
pages = [
    ("cfp.html",            "cfp.html"),
    ("authors.html",        "authors.html"),
    ("proposals.html",      "proposals.html"),
    ("committee.html",      "committee.html"),
    ("outreach.html",       "outreach.html"),
    ("program.html",        "program.html"),
    ("keynotes.html",       "keynotes.html"),
    ("tutorials.html",      "tutorials.html"),
    ("competitions.html",   "competitions.html"),
    ("phd-forum.html",      "phd-forum.html"),
    ("workshops.html",      "workshops.html"),
    ("registration.html",   "registration.html"),
    ("venue.html",          "venue.html"),
    ("visa.html",           "visa.html"),
    ("contact.html",        "contact.html"),
]

for tmpl, out in pages:
    render(tmpl, DIST / "pages" / out)

print(f"\n✅  Build complete → {DIST}\n")
print(f"    Pages generated: {len(pages)+1}")
print(f"    To deploy: push dist/ contents to your GitHub Pages branch.")
