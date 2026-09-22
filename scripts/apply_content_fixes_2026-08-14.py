"""
One-time data corrections from the NIH-convention / domain-accuracy audit,
2026-08-14. See changelog.html for the summary.

1. Kell-null phenotype was written "K0" (numeral zero) on the 4 KellOther
   records vs. the field-standard "Ko" (letter O) used correctly on all 12
   KEL records. Fixes the inconsistency.
2. RHD-NC-001's `alternative_notation` field held an internal curatorial/QA
   note (AI-scoring/policy-review commentary) rather than alternate variant
   nomenclature, which is what that field is documented to hold. Moved the
   note into `molecular_mechanism` as a bracketed [AUDIT NOTE: ...], matching
   the precedent already used elsewhere in the dataset (e.g. ABO-NC-012).

Run once: python3 apply_content_fixes_2026-08-14.py
Then: python3 normalize_data.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "variants_raw.json"

raw = json.loads(RAW_PATH.read_text())

# 1. K0 -> Ko
fixed = 0
for v in raw["KellOther"]["variants"]:
    if "K0" in (v.get("resulting_phenotype") or ""):
        v["resulting_phenotype"] = v["resulting_phenotype"].replace("K0", "Ko")
        fixed += 1
print(f"Fixed K0 -> Ko on {fixed} KellOther records")

# 2. RHD-NC-001 alternative_notation cleanup
for v in raw["RHD"]["variants"]:
    if v["variant_id"] == "RHD-NC-001":
        v["molecular_mechanism"] = (
            v["molecular_mechanism"]
            + " [AUDIT NOTE: AlphaGenome AI pathogenicity score was low for this "
            "variant; retained in the dataset because CRISPR base-editing "
            "validation (K562 cells) was still performed. A policy review of "
            "AI-low-score retention criteria is recommended.]"
        )
        v["alternative_notation"] = None
        print("Cleaned RHD-NC-001 alternative_notation / molecular_mechanism")

RAW_PATH.write_text(json.dumps(raw, indent=2))
print("Done.")
