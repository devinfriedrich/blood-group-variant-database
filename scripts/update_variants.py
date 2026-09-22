"""
Quarterly variant update script for GitHub Actions.
Searches PubMed for new non-coding variant publications for all 8 blood group
systems and updates data/variants_raw.json (the source-of-truth, per-system
table). After this script runs, `normalize_data.py` regenerates
data/variants.json and assets/data.js, which is what the site actually reads.

STATUS: placeholder. The real search-and-merge logic (query PubMed via
Biopython's Entrez module, diff against existing variant_id entries, append
new candidates with audit_status="UNAUDITED" for manual review) has not been
implemented yet. Configure this before relying on the scheduled workflow.
"""
print("Quarterly update script: configure with full PubMed search logic before deploying to GitHub")
