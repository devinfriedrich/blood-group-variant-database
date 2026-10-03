"""
Builds a single self-contained demo.html from the real multi-page site, for
sharing as a Claude Artifact (which requires one inlined file, no separate
CSS/JS/data requests). Not a separate design, this assembles the exact same
page markup the real site ships, with page-to-page navigation reimplemented
as JS show/hide of sections instead of real HTTP navigation (an Artifact is
one URL, so real multi-page navigation isn't possible there).

Run from scripts/: python3 build_demo.py
Output: ../demo/demo.html (gitignored; not part of the deployable site)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index", "stats", "methods", "download-cite", "about", "changelog"]
OUT_DIR = ROOT / "demo"
OUT_DIR.mkdir(exist_ok=True)

style_css = (ROOT / "assets" / "style.css").read_text()
app_js = (ROOT / "assets" / "app.js").read_text()
data_js = (ROOT / "assets" / "data.js").read_text()

nav_html = None
footer_html = None
drawer_html = None
page_sections = []

for page in PAGES:
    text = (ROOT / f"{page}.html").read_text()

    nav_match = re.search(r"<nav class=\"site-nav\">.*?</nav>", text, re.DOTALL)
    footer_match = re.search(r"<footer class=\"site-footer\">.*?</footer>", text, re.DOTALL)
    drawer_overlay = re.search(r'<div class="drawer-overlay".*?</aside>', text, re.DOTALL)

    if page == "index" and nav_match:
        nav_html = nav_match.group(0)
    if page == "index" and footer_match:
        footer_html = footer_match.group(0)
    if drawer_overlay:
        drawer_html = drawer_overlay.group(0)

    # Grab everything between </nav> (end of the nav block) and <footer
    body_start = text.index("</nav>") + len("</nav>")
    body_end = text.index('<footer class="site-footer">')
    page_body = text[body_start:body_end]
    # Drop the drawer markup from the page body if present (it's hoisted once, globally)
    page_body = re.sub(r'<div class="drawer-overlay".*?</aside>', "", page_body, flags=re.DOTALL)
    if page == "download-cite":
        # The shared preview is viewed inside a sandbox that never allows file downloads,
        # so a download button there would silently do nothing. Say so instead.
        for label, href in (("Download CSV", "data/variants.csv"), ("Download JSON", "data/variants.json")):
            btn = f'<a class="btn btn-primary" href="{href}" download>{label}</a>'
            assert btn in page_body, f"{label} button not found on download-cite.html"
            page_body = page_body.replace(btn, '<span class="demo-note">Downloads are turned off in this preview. They work in the full site.</span>')

    display = "block" if page == "index" else "none"
    page_sections.append(f'<div class="demo-page" data-page="{page}" style="display:{display}">\n{page_body}\n</div>')

nav_html = re.sub(r' aria-current="page"', '', nav_html)

demo_css = """
.demo-banner {
  position: sticky; top: 0; z-index: 50; background: var(--ink); color: var(--paper);
  text-align: center; padding: 7px 16px; font-size: 12.5px; font-weight: 600;
  letter-spacing: 0.01em;
}
.demo-banner span { opacity: .78; font-weight: 500; }
.demo-note { font-size: 12.5px; color: var(--muted); }
"""

PAGES_JS = "[" + ", ".join(f"'{p}'" for p in PAGES) + "]"

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blood Group Variant Database: Demo</title>
<style>
{style_css}
{demo_css}
</style>
</head>
<body>
<div class="demo-banner">DEMO PREVIEW &middot; <span>single-file snapshot of the real multi-page site, for review only</span></div>

{nav_html}

{chr(10).join(page_sections)}

{drawer_html}

{footer_html}

<script>
{data_js}
</script>
<script>
{app_js}
</script>
<script>
(function () {{
  var PAGES = {PAGES_JS};

  // Light is the default. The hosting viewer may stamp its own theme onto the page,
  // so light is asserted on load and once more after 1.5 s, unless the visitor has
  // already used the site's own toggle (the toggle must keep working).
  var toggled = false;
  function forceLight() {{ if (!toggled) document.documentElement.setAttribute('data-theme', 'light'); }}
  forceLight();
  setTimeout(forceLight, 1500);
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) {{
    b.addEventListener('click', function () {{ toggled = true; }});
  }});

  function showPage(name, anchor) {{
    document.querySelectorAll('.demo-page').forEach(function (el) {{
      el.style.display = el.dataset.page === name ? 'block' : 'none';
    }});
    document.querySelectorAll('.nav-links a').forEach(function (a) {{
      var target = (a.getAttribute('href') || '').split('#')[0].replace('.html', '');
      if (target === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }});
    var el = anchor ? document.getElementById(anchor) : null;
    if (el) el.scrollIntoView(); else window.scrollTo({{ top: 0 }});
  }}

  // Every in-site link (nav, footer, hero, quick-nav buttons, inline links) is
  // intercepted: "page.html", "page.html#anchor", or a bare "#anchor" on the
  // page being shown. External links are left alone.
  document.querySelectorAll('a[href]').forEach(function (a) {{
    var href = a.getAttribute('href') || '';
    if (/^(https?:|mailto:|data:)/.test(href)) return;
    var parts = href.split('#');
    var page = parts[0].replace('.html', '');
    var anchor = parts[1] || '';
    if (page && PAGES.indexOf(page) === -1) return;
    a.addEventListener('click', function (e) {{
      e.preventDefault();
      var current = (document.querySelector('.demo-page[style*="block"]') || {{ dataset: {{}} }}).dataset.page;
      showPage(page || current || 'index', anchor);
    }});
  }});
}})();
</script>
</body>
</html>
"""

out_path = OUT_DIR / "demo.html"
out_path.write_text(html)
print(f"Wrote {out_path} ({len(html):,} bytes)")
