# Blood Group Non-Coding Variant Database

A static, searchable website cataloging **229 non-coding and regulatory
variants** across 8 blood group systems: ABO, RHD, RHCE, Duffy (ACKR1),
Kell (KEL), Kidd (SLC14A1), MNS (GYPA/GYPB), and Kell Other Antigens
(Kp<sup>a</sup>/Kp<sup>b</sup>, Js<sup>a</sup>/Js<sup>b</sup>).

Built for the **Chai Lab**, Department of Pathology, Brigham and Women's
Hospital / Harvard Medical School. Data compiled and curated by **Jun Liu,
MD, PhD**.

## What's here

**Pages**
- `index.html`: the variant browser: search, filter by system / category /
  validation tier / audit status, sortable table, per-variant detail drawer.
- `stats.html`: dataset statistics (coverage by system, category, evidence
  tier, audit status, base-editing feasibility), computed live from the same
  data the browser reads.
- `downloads.html`: CSV and JSON download of the full dataset, with schema
  documentation.
- `methods.html`: scope, data provenance, evidence-tier and audit-status
  legends, base-editing feasibility methodology, disclaimer.
- `citation.html`: how to cite the database and individual variant entries.
- `about.html`: what this resource is for, who maintains it, contact.
- `changelog.html`: dated log of data corrections and site changes
  (linked from the footer on every page, not the top nav, to keep the nav
  short).

**Code & data**
- `assets/style.css`, `assets/app.js`: all styling and browser/stats/nav
  logic, no build step, no external dependencies. Light/dark mode, working
  mobile navigation menu.
- `assets/data.js`: the dataset as a plain `<script>` global
  (`window.VARIANT_DATA`), so the site works when opened directly from disk
  (double-click `index.html`) with no local server required.
- `data/variants_raw.json`: source-of-truth data, one table per system, as
  originally compiled (kept for audit trail / to feed future updates).
- `data/variants.json` / `data/variants.csv`: the same data normalized into
  one flat schema, as JSON and CSV (the files linked from Downloads).
- `scripts/normalize_data.py`: regenerates `data/variants.json`,
  `assets/data.js`, and `data/variants.csv` from `data/variants_raw.json`.
  Run this after editing the raw data:
  ```
  python3 scripts/normalize_data.py
  ```
- `scripts/apply_citation_fixes_2026-08-13.py`: one-time record of the full
  citation audit's corrections (15 fixed, 3 flagged); see `changelog.html`
  for the summary. Kept as documentation, not meant to be re-run.
- `scripts/update_variants.py`: placeholder for the quarterly PubMed search
  script (not yet implemented; see file header).
- `scripts/build_demo.py`: builds `demo/demo.html`, a single self-contained
  file (inlined CSS/JS/data, page-to-page nav reimplemented as JS show/hide)
  for sharing as a Claude Artifact preview. Not part of the deployable site;
  `demo/` is gitignored. Rebuild after any real page/style change:
  ```
  python3 scripts/build_demo.py
  ```
- `.github/workflows/quarterly-update.yml`: scheduled GitHub Action that
  would run the update + normalize scripts and commit the result, once
  `update_variants.py` is filled in.
- `CITATION.cff`: machine-readable citation metadata (GitHub reads this
  automatically and offers a "Cite this repository" button).

## Editing the data

1. Edit `data/variants_raw.json` (grouped by system: `ABO`, `RHD`, `RHCE`,
   `Duffy`, `Kell`, `Kidd`, `MNS`, `KellOther`, each with a `meta`, `headers`,
   and `variants` array).
2. Run `python3 scripts/normalize_data.py` from the `scripts/` directory.
3. Refresh `index.html` in a browser to check the change.

## Hosting

Plain static HTML/CSS/JS: deployable to GitHub Pages, any web server, or
BWH/Harvard-hosted web space. No build step required.

## Before this goes live

- [ ] Decide on a permanent URL and update the `[database URL]` placeholders
      in `citation.html` and `CITATION.cff`.
- [ ] Decide on a reuse license for the compiled dataset (see
      `citation.html` → Usage & license) and update that section.
- [ ] Fill in `scripts/update_variants.py` if the quarterly auto-update
      workflow should actually run.
- [ ] Resolve the 3 records still flagged from the full citation audit
      (see `changelog.html` → 2026-08-13): ABO-NC-036, and one reference
      each on ACKR1-NC-002 and KELLOTHER-NC-010, whose cited PMIDs don't
      match their descriptions and couldn't be confidently replaced by
      search alone.
- [ ] All 88 unique cited PMIDs have been checked against real PubMed
      metadata (author/journal/year); gnomAD v4 and TOPMed allele
      frequencies themselves have **not** been independently re-verified
      against gnomAD: worth a spot-check before treating those numbers as
      launch-ready.
