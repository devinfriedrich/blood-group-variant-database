# Blood Group Non-Coding Variant Database

A static, searchable website cataloging non-coding and regulatory variants
in the **Rh blood group system** (genes RHD and RHCE; 108 variants in the
current release).

**Displayed scope.** The compiled source data holds more blood group systems
than the site shows. Which systems are published is controlled by one
setting, `SCOPE_SYSTEMS` at the top of `scripts/normalize_data.py` (currently
`["RHD", "RHCE"]`). The website, statistics, and CSV/JSON downloads are all
generated from the filtered data. To publish every system again, set it to
`[]` and run `python3 scripts/normalize_data.py`; the system cards, filter
options, and statistics follow the data. Some descriptive prose (home page,
Methods, About, this README) is written for the Rh scope and would need to be
reworded to match a wider scope.

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
- `download-cite.html`: CSV and JSON download of the full dataset, with schema
  documentation, plus how to cite the database and individual variant entries.
- `methods.html`: scope, data provenance, evidence-tier and audit-status
  legends, base-editing feasibility methodology, disclaimer.
- `about.html`: what this resource is for, who maintains it, contact.
- `changelog.html`: dated log of data corrections and site changes
- `feedback.html`: feedback form; submissions are delivered by formsubmit.co,
  a third-party form service, to the address in the form's `action` attribute
  (linked from the top nav and footer on every page).

**Code & data**
- `assets/style.css`, `assets/app.js`: all styling and browser/stats/nav
  logic, no build step, no external dependencies. Light/dark mode (light by
  default).
- `assets/data.js`: the dataset as a plain `<script>` global
  (`window.VARIANT_DATA`), so the site works when opened directly from disk
  (double-click `index.html`) with no local server required.
- `data/variants_raw.json`: source-of-truth data, one table per system, as
  originally compiled (kept complete, including systems that are not
  currently displayed; for audit trail / to feed future updates).
- `data/variants.json` / `data/variants.csv`: the in-scope data normalized
  into one flat schema, as JSON and CSV (the files linked from Download and
  Cite).
- `scripts/normalize_data.py`: regenerates `data/variants.json`,
  `assets/data.js`, and `data/variants.csv` from `data/variants_raw.json`,
  keeping only the systems listed in `SCOPE_SYSTEMS`.
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
  for sharing as a Claude Artifact preview. Opens in light mode. Not part of the deployable site;
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

1. Edit `data/variants_raw.json` (one table per system, each with a `meta`,
   `headers`, and `variants` array; the Rh tables are `RHD` and `RHCE`).
2. Run `python3 scripts/normalize_data.py` from the repository root (the script locates its own files, so it also runs from other folders).
3. Refresh `index.html` in a browser to check the change.

## Hosting

Plain static HTML/CSS/JS: deployable to GitHub Pages, any web server, or
BWH/Harvard-hosted web space. No build step required.

## Before this goes live

- [ ] Decide on a permanent URL and update the `[database URL]` placeholders
      in `download-cite.html` and `CITATION.cff`.
- [ ] Decide on a reuse license for the compiled dataset (see
      `download-cite.html` → Usage & license) and update that section.
- [ ] Fill in `scripts/update_variants.py` if the quarterly auto-update
      workflow should actually run.
- [ ] Resolve the records still flagged from the full citation audit (see
      `changelog.html` → 2026-08-13). Some flagged records are in the displayed Rh
      scope (filter Browse by Audit Status: Flagged); the rest are in systems that are not
      currently displayed and remain in `data/variants_raw.json`.
- [ ] The 88 unique PMIDs cited as of 2026-08-13 were checked against real PubMed
      metadata (author/journal/year); references added or changed since then have not
      been re-checked; gnomAD v4 and TOPMed allele
      frequencies themselves have **not** been independently re-verified
      against gnomAD: worth a spot-check before treating those numbers as
      launch-ready.
