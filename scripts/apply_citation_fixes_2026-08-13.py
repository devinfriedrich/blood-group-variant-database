"""
One-time citation correction pass, 2026-08-13.

Applies fixes found by cross-checking every PMID cited in data/variants_raw.json
(88 unique PMIDs across 141 citation segments, spanning all 229 variants)
against real PubMed metadata (get_article_metadata / lookup_article_by_citation
/ search_articles). Two rounds: an initial 24-variant sample (found 4 errors),
then a full audit of every citation in the dataset (found 15 more).

Each fix is either:
  - CORRECTED: a confident replacement was found and applied.
  - FLAGGED: the cited PMID does not match its description and no confident
    replacement could be found via PubMed search; left for manual follow-up
    rather than guessed.

Run once: python3 apply_citation_fixes_2026-08-13.py
Then regenerate the site's data with: python3 normalize_data.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "variants_raw.json"

raw = json.loads(RAW_PATH.read_text())


def find(system, variant_id):
    for v in raw[system]["variants"]:
        if v["variant_id"] == variant_id:
            return v
    raise KeyError(f"{variant_id} not found in {system}")


# ---- CORRECTED: confident replacement found and applied ----

v = find("Duffy", "ACKR1-NC-004")
v["key_reference"] = "Höher G et al. Transfus Apher Sci 2020;59(4):102768 (PMID 32276863)"
v["audit_status"] = "CORRECTED: ref author/journal/vol/pages Castilho/Transfusion/60:2148-57 → Höher/Transfus Apher Sci/59(4):102768"

for vid in ("ACKR1-NC-005", "ACKR1-NC-006"):
    v = find("Duffy", vid)
    v["key_reference"] = (
        "Höher G et al. Transfus Apher Sci 2020;59(4):102768 (PMID 32276863); "
        "Flegel WA et al. J Mol Diagn 2020;22(10):1272-1279 (PMID 32688055)"
    )
    v["audit_status"] = (
        "CORRECTED: ref1 Castilho/Transfusion → Höher/Transfus Apher Sci; "
        "ref2 PMID 32738421 (unrelated CRISPR/TB paper) → 32688055 (correct Flegel ACKR1 paper)"
    )

for vid in ("KEL-NC-002",):
    v = find("Kell", vid)
    v["key_reference"] = "Lee et al., J Biol Chem 2001 (PMID 11375401); Körmöczi GF et al., Transfusion 2007 (PMID 17381630)"
    v["audit_status"] = "CORRECTED: ref2 author Poole → Körmöczi (real first author of PMID 17381630)"

for vid in ("KEL-NC-006", "KEL-NC-007"):
    v = find("Kell", vid)
    v["key_reference"] = "Körmöczi GF et al., Transfusion 2007 (PMID 17381630)"
    v["audit_status"] = "CORRECTED: author Poole → Körmöczi (real first author of PMID 17381630)"

v = find("Kidd", "KIDD-NC-002")
v["key_reference"] = "Meng Y 2005, Sci China C Life Sci (PMID 16483143)"
v["audit_status"] = "CORRECTED: journal Transfus Apher Sci → Sci China C Life Sci; year 2006 → 2005"

for vid in ("RHCE-NC-003", "RHCE-NC-014", "RHCE-NC-018"):
    v = find("RHCE", vid)
    extra = "; GenBank FM866412" if vid == "RHCE-NC-003" else ""
    v["key_reference"] = f"Döscher A et al. Transfusion 2009;49(7):1803-1811 (PMID 19453979){extra}"
    v["audit_status"] = "CORRECTED: author Bugert → Döscher; pages 1336-1349 → 1803-1811 (real citation for PMID 19453979)"

v = find("RHCE", "RHCE-NC-007")
v["key_reference"] = "Chérif-Zahar B et al., Blood 1998 (PMID 9657766)"
v["audit_status"] = "CORRECTED: author Huang → Chérif-Zahar (real first author of PMID 9657766)"

v = find("RHCE", "RHCE-NC-023")
v["key_reference"] = "Shao et al. Vox Sang 2023;118:972-979 (PMID 37823181)"
v["audit_status"] = "CORRECTED: journal Transfus Med Hemotherapy → Vox Sang; volume/pages fixed"

v = find("Duffy", "ACKR1-NC-003")
v["key_reference"] = "Písačka M et al. Transfusion 2015;55:2616-9 (PMID 26173389)"
v["audit_status"] = "CORRECTED: author Flegel → Písačka (real first author of PMID 26173389)"

v = find("Kell", "KEL-NC-008")
v["key_reference"] = "Martin-Blanc C et al., Transfusion 2013;53:2859-66 (PMID 23581578)"
v["audit_status"] = "CORRECTED: author Guz → Martin-Blanc; volume/pages added"

v = find("Kell", "KEL-NC-011")
v["key_reference"] = "Boturão-Neto E et al., Transfus Med Hemother 2014;42:52-8 (PMID 25960716)"
v["audit_status"] = "CORRECTED: author Castilho/Mota → Boturão-Neto; year 2015 → 2014"

v = find("MNS", "MNS-NC-016")
v["key_reference"] = "Huang CH et al., Blood 1987;70:1830-5 (PMID 2823938); Blumenfeld 1997 (PMID 9269716)"
v["audit_status"] = "CORRECTED: ref1 author/journal/year Tate/Transfusion/1989 → Huang/Blood/1987"

v = find("MNS", "MNS-NC-022")
v["key_reference"] = "Lapadat AM et al., Transfusion 2021;61:E34-E36 (PMID 33733475)"
v["audit_status"] = "CORRECTED: previously unconfirmed; PMID verified as Lapadat et al. 2021 Transfusion, topically on-point (GYPB S-silencing variants)"

v = find("ABO", "ABO-NC-012")
v["pubmed_source_url"] = "https://pubmed.ncbi.nlm.nih.gov/21592135/"
v["key_reference"] = "Thuresson B et al., Vox Sang 2011;102(1):55-64 (PMID 21592135)"
v["audit_status"] = "CORRECTED: PMID 21348884 (unrelated soil-bacteria paper) → 21592135 (real Thuresson CBF/NF-Y hybrid-allele paper)"
v["molecular_mechanism"] = v["molecular_mechanism"].replace("Thuresson 2012", "Thuresson 2011")

v = find("KellOther", "KELLOTHER-NC-008")
v["key_reference"] = "Singleton BK et al., Br J Haematol 2003;122(4):682-5 (PMID 12899725); Wu PC 2024, Transfusion (PMID 38644556)"
v["audit_status"] = "CORRECTED: ref1 PMID 21263053 (unrelated C. difficile paper) → 12899725 (real Singleton McLeod/XK paper); year/journal fixed"

# ---- FLAGGED: PMID does not match description; no confident replacement found ----

v = find("KellOther", "KELLOTHER-NC-010")
v["key_reference"] = (
    "Peikert K, Hermann A, Danek A. Transfus Med Hemother 2022;49(1):4-12 (PMID 35221863) [review]; "
    "Lomas-Francis C 2011, JNS (PMID 21420691: UNRESOLVED: this PMID resolves to an unrelated Parkinson's "
    "disease paper, not a blood-group reference; needs manual recovery)"
)
v["audit_status"] = (
    "FLAGGED: ref1 corrected (Danek review PMID 34910313 → 35221863); "
    "ref2 still unresolved, cited PMID does not match description"
)

v = find("ABO", "ABO-NC-036")
v["audit_status"] = (
    "FLAGGED: PMID 30488516 does not match description (resolves to an unrelated Muscle & Nerve "
    "neurology paper); needs manual reference recovery. Was previously incorrectly marked VERIFIED."
)

v = find("Duffy", "ACKR1-NC-002")
v["pubmed_source_url"] = "https://pubmed.ncbi.nlm.nih.gov/10738032/"
v["key_reference"] = (
    "Mallinson G et al. Br J Haematol 1999;107:634-7 (PMID 10583269: UNRESOLVED: this PMID resolves to an "
    "unrelated B-cell lymphoma paper, not a Duffy reference; needs manual recovery); "
    "Yazdanbakhsh K et al. Transfusion 2000;40(3):310-20 (PMID 10738032)"
)
v["audit_status"] = (
    "FLAGGED: ref1 (Mallinson) PMID unresolved, needs manual recovery; "
    "ref2 (Yazdanbakhsh) CORRECTED: PMID 10570183 (wrong paper) → 10738032, journal Blood → Transfusion, "
    "vol/pages fixed: topically exact match (Duffy GATA-box/Fy(x) reduced expression)"
)

RAW_PATH.write_text(json.dumps(raw, indent=2))
print("Applied 15 CORRECTED fixes and 3 FLAGGED updates to", RAW_PATH)
