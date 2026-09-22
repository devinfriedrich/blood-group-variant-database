"""
One-time content cleanup, 2026-08-15. See changelog.html for the summary.

1. RHD-NC-003 had "AI-prioritized regulatory variant" sitting in
   `alternative_notation` (meant for legacy nomenclature, not a discovery-
   method note) -- same class of issue as RHD-NC-001, fixed the same way:
   moved into `molecular_mechanism` as a bracketed [AUDIT NOTE: ...],
   alternative_notation cleared. Checked the rest of RHD (69 records) for
   the same pattern; no other instances found.
2. Em dashes removed from every data field, dataset-wide:
   - Lone "-" placeholders (420 fields) standardized to "N/A", matching the
     convention already used elsewhere in the same records (the dataset
     inconsistently mixed em-dash-as-placeholder and "N/A" for "no data").
   - "label -- explanation" clause separators (316 fields, e.g.
     "CORRECTED -- URL fixed") changed to "label: explanation".
   (The literal em-dash character doesn't survive in this docstring's ASCII
   comment; see the regex below for the actual character replaced.)

Run once: python3 apply_content_fixes_2026-08-15.py
Then: python3 normalize_data.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "variants_raw.json"

EM_DASH = "—"

raw = json.loads(RAW_PATH.read_text())

# 1. RHD-NC-003 alternative_notation cleanup
for v in raw["RHD"]["variants"]:
    if v["variant_id"] == "RHD-NC-003":
        v["molecular_mechanism"] = (
            v["molecular_mechanism"]
            + " [AUDIT NOTE: Identified via AI-driven regulatory-variant "
            "prioritization rather than a primary literature report.]"
        )
        v["alternative_notation"] = None
        print("Cleaned RHD-NC-003 alternative_notation / molecular_mechanism")

# 2. Em dash removal, dataset-wide
placeholder_fixed = 0
clause_fixed = 0
other_fixed = 0
for sys, table in raw.items():
    for v in table["variants"]:
        for k, val in list(v.items()):
            if not isinstance(val, str) or EM_DASH not in val:
                continue
            if val.strip() == EM_DASH:
                v[k] = "N/A"
                placeholder_fixed += 1
            elif f" {EM_DASH} " in val:
                v[k] = val.replace(f" {EM_DASH} ", ": ")
                clause_fixed += 1
            else:
                v[k] = val.replace(EM_DASH, "-")
                other_fixed += 1

print(f"Placeholder em dashes -> N/A: {placeholder_fixed}")
print(f"Clause-separator em dashes -> colon: {clause_fixed}")
print(f"Other em dashes -> hyphen: {other_fixed}")

RAW_PATH.write_text(json.dumps(raw, indent=2))
print("Done.")
