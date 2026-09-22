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
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index", "stats", "downloads", "methods", "citation", "about", "changelog"]
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
    if page == "downloads":
        csv_b64 = base64.b64encode((ROOT / "data" / "variants.csv").read_bytes()).decode()
        json_b64 = base64.b64encode((ROOT / "data" / "variants.json").read_bytes()).decode()
        page_body = page_body.replace('href="data/variants.csv"', f'href="data:text/csv;base64,{csv_b64}"')
        page_body = page_body.replace('href="data/variants.json"', f'href="data:application/json;base64,{json_b64}"')

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
"""

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
  function showPage(name) {{
    document.querySelectorAll('.demo-page').forEach(function (el) {{
      el.style.display = el.dataset.page === name ? 'block' : 'none';
    }});
    document.querySelectorAll('.nav-links a, .nav-mobile a').forEach(function (a) {{
      var target = (a.getAttribute('href') || '').replace('.html', '');
      if (target === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }});
    window.scrollTo({{ top: 0 }});
  }}
  document.querySelectorAll('.nav-links a, .nav-mobile a, footer a').forEach(function (a) {{
    var href = a.getAttribute('href') || '';
    if (!href.endsWith('.html')) return;
    var target = href.replace('.html', '').replace('#browse', '');
    a.addEventListener('click', function (e) {{
      e.preventDefault();
      showPage(target || 'index');
      var nav = document.querySelector('.site-nav');
      if (nav) nav.classList.remove('is-open');
    }});
  }});
  // "Browse variants" / "Read the methods" hero buttons and inline links that
  // point at other pages need the same interception (already covered above
  // since they're plain <a href="*.html"> tags picked up by the loop).
}})();
</script>
</body>
</html>
"""

out_path = OUT_DIR / "demo.html"
out_path.write_text(html)
print(f"Wrote {out_path} ({len(html):,} bytes)")
