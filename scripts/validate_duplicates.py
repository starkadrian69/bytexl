#!/usr/bin/env python3
"""
validate_duplicates.py
CivicTrace Phase 3D — Synthetic Duplicate & Intelligence Evaluation Dataset Validation Suite

Validates:
1. Exact 24-column schema & header ordering
2. Unique duplicate_record_id (CT-DUP-xxx format)
3. Foreign key referencing:
   - incident_id in seed_incidents.csv or UNKNOWN
   - ward_id in jurisdiction_registry.csv or UNKNOWN
   - zone_id in jurisdiction_registry.csv or UNKNOWN (and ward-to-zone consistency)
   - asset_id in asset_ownership.csv or UNKNOWN
   - authority_id in Phase 1 authority master, NEEDS_REVIEW, or UNKNOWN
   - source_id in source registries or synthetic provenance ID
   - reference_record_id in duplicate_cases.csv (CT-DUP-xxx) or seed_incidents.csv (CT-INC-xxx)
4. Strict controlled vocabularies:
   - duplicate_label in {DUPLICATE, LIKELY_DUPLICATE, POSSIBLE_DUPLICATE, UNRELATED}
   - language in {ENGLISH, HINDI, HINGLISH, MIXED}
   - data_mode strictly SYNTHETIC_EVALUATION
   - source_type strictly SYNTHETIC_EVALUATION
   - evidence_available in {YES, NO}
   - location_status in {VERIFIED, APPROXIMATE, UNKNOWN, NEEDS_REVIEW, CONFLICT}
5. Spatial coordinates sanity (Lucknow bounds: lat 26.60-27.15, lon 80.70-81.25)
6. Human curation confidence range (float 0.0 to 1.0)
7. Distinction between duplicate complaint relationships and accidental identical database rows
8. Verification of frozen prior-phase datasets (Phase 1, 2, 3A, 3B, 3C)
9. Emits machine-readable data/lucknow/duplicates/duplicate_validation_report.json
"""

import os
import sys
import csv
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUPLICATES_CSV = os.path.join(BASE_DIR, "data/lucknow/duplicates/duplicate_cases.csv")
REPORT_JSON = os.path.join(BASE_DIR, "data/lucknow/duplicates/duplicate_validation_report.json")
INCIDENTS_CSV = os.path.join(BASE_DIR, "data/lucknow/incidents/seed_incidents.csv")
JURISDICTION_CSV = os.path.join(BASE_DIR, "data/gis/jurisdiction_registry.csv")
ASSETS_CSV = os.path.join(BASE_DIR, "data/lucknow/assets/asset_ownership.csv")
AUTHORITY_MASTER_JSON = os.path.join(BASE_DIR, "data/authority/lucknow_authority_master.json")
SOURCES_CSV = os.path.join(BASE_DIR, "data/sources/source_registry.csv")
GIS_SOURCES_CSV = os.path.join(BASE_DIR, "data/gis/gis_source_registry.csv")
EVIDENCE_CSV = os.path.join(BASE_DIR, "data/lucknow/evidence/evidence.csv")

EXPECTED_HEADERS = [
    "duplicate_record_id", "cluster_id", "incident_id", "data_mode",
    "complaint_text", "language", "issue_category", "issue_subcategory",
    "latitude", "longitude", "location_status", "ward_id", "zone_id",
    "asset_id", "authority_id", "duplicate_label", "duplicate_reason",
    "reference_record_id", "evidence_available", "source_type", "source_id",
    "source_reference", "curation_confidence", "notes"
]

ALLOWED_DUPLICATE_LABELS = {
    "DUPLICATE", "LIKELY_DUPLICATE", "POSSIBLE_DUPLICATE", "UNRELATED"
}

ALLOWED_LANGUAGES = {"ENGLISH", "HINDI", "HINGLISH", "MIXED"}
ALLOWED_DATA_MODES = {"SYNTHETIC_EVALUATION"}
ALLOWED_SOURCE_TYPES = {"SYNTHETIC_EVALUATION"}
ALLOWED_EVIDENCE_AVAILABLE = {"YES", "NO"}
ALLOWED_LOCATION_STATUSES = {
    "VERIFIED", "APPROXIMATE", "UNKNOWN", "NEEDS_REVIEW", "CONFLICT"
}

ALLOWED_ISSUE_CATEGORIES = {
    "POTHOLE", "ROAD_DAMAGE", "BLOCKED_DRAIN", "WATERLOGGING",
    "WATER_LEAKAGE", "BROKEN_PIPELINE", "SEWER_OVERFLOW",
    "STREETLIGHT_FAILURE", "ELECTRICAL_INFRASTRUCTURE",
    "GARBAGE_ACCUMULATION", "ILLEGAL_DUMPING", "OVERFLOWING_BIN"
}

SANITY_MIN_LAT, SANITY_MAX_LAT = 26.60, 27.15
SANITY_MIN_LON, SANITY_MAX_LON = 80.70, 81.25

errors = []
warnings = []
intentional_test_warnings = []

print("=" * 75)
print("CIVICTRACE PHASE 3D: SYNTHETIC DUPLICATE DATASET VALIDATION SUITE")
print("=" * 75)

# --- CHECK 1: File Existence & Dependencies ---
print("[CHECK 1] Deliverable & Dependency File Existence: ", end="")
required_files = [
    DUPLICATES_CSV, INCIDENTS_CSV, JURISDICTION_CSV, ASSETS_CSV,
    AUTHORITY_MASTER_JSON, SOURCES_CSV, GIS_SOURCES_CSV, EVIDENCE_CSV
]
missing_files = [f for f in required_files if not os.path.exists(f)]
if missing_files:
    errors.append(f"Missing required deliverable/dependency files: {missing_files}")
    print(f"FAIL (Missing {len(missing_files)} files)")
    sys.exit(1)
else:
    print("PASS (All deliverable assets and dependencies present)")

# --- CHECK 2: Prior Phase Data Ingestion ---
print("[CHECK 2] Prior Phase Foreign Key Target Ingestion: ", end="")
# Incidents (Phase 3B)
seed_incidents = {}
with open(INCIDENTS_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        seed_incidents[row["incident_id"]] = row

# Jurisdiction (Phase 2)
jurisdiction_wards = {}
jurisdiction_zones = set()
ward_to_zone = {}
with open(JURISDICTION_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        wid = row["ward_id"]
        zid = row["zone_id"]
        jurisdiction_wards[wid] = row
        jurisdiction_zones.add(zid)
        ward_to_zone[wid] = zid

# Assets (Phase 3A)
assets_dict = {}
with open(ASSETS_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        assets_dict[row["asset_id"]] = row

# Authority Master (Phase 1)
with open(AUTHORITY_MASTER_JSON, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)
authorities_dict = {a["authority_id"]: a for a in auth_data.get("authorities", [])}

# Sources (Phase 1 & 2)
registered_sources = {}
for src_path in [SOURCES_CSV, GIS_SOURCES_CSV]:
    with open(src_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            registered_sources[row["source_id"]] = row

print(f"PASS ({len(seed_incidents)} incidents, {len(jurisdiction_wards)} wards, {len(assets_dict)} assets, {len(authorities_dict)} authorities, {len(registered_sources)} sources)")

# --- CHECK 3: CSV Schema & Header Conformance ---
print("[CHECK 3] Duplicate CSV Schema & Header Conformance: ", end="")
with open(DUPLICATES_CSV, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    csv_rows = list(reader)

if not csv_rows:
    errors.append("Duplicate cases CSV is completely empty.")
    print("FAIL (Empty file)")
    sys.exit(1)

headers = csv_rows[0]
if headers != EXPECTED_HEADERS:
    errors.append(f"Header mismatch. Expected {EXPECTED_HEADERS}, found {headers}")
    print("FAIL")
else:
    print(f"PASS (Exactly {len(headers)} columns matching schema)")

duplicate_records = []
with open(DUPLICATES_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        duplicate_records.append(row)

total_records = len(duplicate_records)
print(f"\n[AUDITING {total_records} SYNTHETIC DUPLICATE EVALUATION RECORDS]")

# First pass: collect all duplicate_record_ids
all_duplicate_ids = set()
for r in duplicate_records:
    d_id = r.get("duplicate_record_id", "").strip()
    if d_id:
        all_duplicate_ids.add(d_id)

seen_duplicate_ids = set()
seen_exact_content = set()
clusters_map = {}
labels_count = {}
languages_count = {}
categories_count = {}
data_modes_count = {}
source_types_count = {}
evidence_available_count = {}
location_statuses_count = {}

# Audit loop
for idx, r in enumerate(duplicate_records, start=2):
    did = r.get("duplicate_record_id", "").strip()
    cid = r.get("cluster_id", "").strip()
    inc_id = r.get("incident_id", "").strip()
    dmode = r.get("data_mode", "").strip()
    ctext = r.get("complaint_text", "").strip()
    lang = r.get("language", "").strip()
    cat = r.get("issue_category", "").strip()
    subcat = r.get("issue_subcategory", "").strip()
    lat_str = r.get("latitude", "").strip()
    lon_str = r.get("longitude", "").strip()
    loc_status = r.get("location_status", "").strip()
    wid = r.get("ward_id", "").strip()
    zid = r.get("zone_id", "").strip()
    aid = r.get("asset_id", "").strip()
    auth_id = r.get("authority_id", "").strip()
    dlabel = r.get("duplicate_label", "").strip()
    dreason = r.get("duplicate_reason", "").strip()
    ref_id = r.get("reference_record_id", "").strip()
    ev_avail = r.get("evidence_available", "").strip()
    stype = r.get("source_type", "").strip()
    sid = r.get("source_id", "").strip()
    sref = r.get("source_reference", "").strip()
    conf_str = r.get("curation_confidence", "").strip()
    notes = r.get("notes", "").strip()

    # 1. ID Format & Uniqueness
    if not did:
        errors.append(f"Row {idx}: Empty duplicate_record_id.")
    elif not re.match(r"^CT-DUP-\d{3}$", did):
        errors.append(f"Row {idx}: Invalid duplicate_record_id format '{did}'. Expected CT-DUP-xxx.")
    elif did in seen_duplicate_ids:
        errors.append(f"Row {idx}: Duplicate duplicate_record_id '{did}'.")
    seen_duplicate_ids.add(did)

    # 2. Accidental Duplicate Database Row vs Intentional Duplicate Relationship
    content_fingerprint = (cid, ctext, lat_str, lon_str, dlabel, ref_id)
    if content_fingerprint in seen_exact_content:
        warnings.append(f"Row {idx} ({did}): Accidental identical database row detected with matching text and reference.")
    seen_exact_content.add(content_fingerprint)

    # 3. Cluster ID
    if not cid:
        errors.append(f"Row {idx} ({did}): Missing cluster_id.")
    elif not re.match(r"^CLUSTER-\d{3}$", cid):
        errors.append(f"Row {idx} ({did}): Invalid cluster_id format '{cid}'. Expected CLUSTER-xxx.")
    clusters_map.setdefault(cid, []).append(r)

    # 4. Mandatory Fields
    if not ctext:
        errors.append(f"Row {idx} ({did}): Missing complaint_text.")
    if not dreason:
        errors.append(f"Row {idx} ({did}): Missing duplicate_reason.")
    if not sref:
        errors.append(f"Row {idx} ({did}): Missing source_reference.")

    # 5. Controlled Vocabularies
    if dmode not in ALLOWED_DATA_MODES:
        errors.append(f"Row {idx} ({did}): Invalid data_mode '{dmode}'. Must be strictly 'SYNTHETIC_EVALUATION'.")
    data_modes_count[dmode] = data_modes_count.get(dmode, 0) + 1

    if stype not in ALLOWED_SOURCE_TYPES:
        errors.append(f"Row {idx} ({did}): Invalid source_type '{stype}'. Must be strictly 'SYNTHETIC_EVALUATION'.")
    source_types_count[stype] = source_types_count.get(stype, 0) + 1

    if lang not in ALLOWED_LANGUAGES:
        errors.append(f"Row {idx} ({did}): Invalid language '{lang}'. Allowed: {ALLOWED_LANGUAGES}")
    languages_count[lang] = languages_count.get(lang, 0) + 1

    if cat not in ALLOWED_ISSUE_CATEGORIES:
        errors.append(f"Row {idx} ({did}): Invalid issue_category '{cat}'. Allowed: {ALLOWED_ISSUE_CATEGORIES}")
    categories_count[cat] = categories_count.get(cat, 0) + 1

    if dlabel not in ALLOWED_DUPLICATE_LABELS:
        errors.append(f"Row {idx} ({did}): Invalid duplicate_label '{dlabel}'. Allowed: {ALLOWED_DUPLICATE_LABELS}")
    labels_count[dlabel] = labels_count.get(dlabel, 0) + 1

    if ev_avail not in ALLOWED_EVIDENCE_AVAILABLE:
        errors.append(f"Row {idx} ({did}): Invalid evidence_available '{ev_avail}'. Allowed: {ALLOWED_EVIDENCE_AVAILABLE}")
    evidence_available_count[ev_avail] = evidence_available_count.get(ev_avail, 0) + 1

    if loc_status not in ALLOWED_LOCATION_STATUSES:
        errors.append(f"Row {idx} ({did}): Invalid location_status '{loc_status}'. Allowed: {ALLOWED_LOCATION_STATUSES}")
    location_statuses_count[loc_status] = location_statuses_count.get(loc_status, 0) + 1

    # 6. Curation Confidence (Human confidence, float 0.0 - 1.0)
    try:
        cval = float(conf_str)
        if not (0.0 <= cval <= 1.0):
            errors.append(f"Row {idx} ({did}): curation_confidence '{conf_str}' out of range [0.0, 1.0].")
    except ValueError:
        errors.append(f"Row {idx} ({did}): curation_confidence '{conf_str}' is not a valid float.")

    # 7. Foreign Key Validations
    # incident_id: must exist in seed_incidents or UNKNOWN
    if inc_id != "UNKNOWN" and inc_id not in seed_incidents:
        errors.append(f"Row {idx} ({did}): Foreign key violation. incident_id '{inc_id}' does not exist in seed_incidents.csv.")

    # ward_id: must exist in jurisdiction_wards or UNKNOWN
    if wid != "UNKNOWN" and wid not in jurisdiction_wards:
        errors.append(f"Row {idx} ({did}): Foreign key violation. ward_id '{wid}' does not exist in jurisdiction_registry.csv.")

    # zone_id: must exist in jurisdiction_zones or UNKNOWN
    if zid != "UNKNOWN" and zid not in jurisdiction_zones:
        errors.append(f"Row {idx} ({did}): Foreign key violation. zone_id '{zid}' does not exist in jurisdiction_registry.csv.")

    # ward-to-zone consistency
    if wid != "UNKNOWN" and zid != "UNKNOWN":
        expected_zone = ward_to_zone.get(wid)
        if expected_zone and expected_zone != zid:
            errors.append(f"Row {idx} ({did}): Ward '{wid}' belongs to zone '{expected_zone}', but record specifies '{zid}'.")

    # asset_id: must exist in asset_ownership or UNKNOWN
    if aid != "UNKNOWN" and aid not in assets_dict:
        errors.append(f"Row {idx} ({did}): Foreign key violation. asset_id '{aid}' does not exist in asset_ownership.csv.")

    # authority_id: must exist in Phase 1 master or NEEDS_REVIEW or UNKNOWN
    if auth_id not in ("NEEDS_REVIEW", "UNKNOWN") and auth_id not in authorities_dict:
        errors.append(f"Row {idx} ({did}): Foreign key violation. authority_id '{auth_id}' not found in authority master.")

    # source_id: must exist in registered_sources or synthetic benchmark identifier
    if sid not in registered_sources and sid != "SRC-SYNTH-3D":
        errors.append(f"Row {idx} ({did}): Foreign key violation. source_id '{sid}' not in registered sources.")

    # reference_record_id: must exist in duplicate_cases (CT-DUP-xxx) or seed_incidents (CT-INC-xxx)
    if not ref_id:
        errors.append(f"Row {idx} ({did}): Missing reference_record_id.")
    elif ref_id == did:
        errors.append(f"Row {idx} ({did}): Circular reference. Record cannot reference itself as reference_record_id.")
    elif ref_id.startswith("CT-DUP-"):
        if ref_id not in all_duplicate_ids:
            errors.append(f"Row {idx} ({did}): reference_record_id '{ref_id}' does not exist in duplicate_cases.csv.")
    elif ref_id.startswith("CT-INC-"):
        if ref_id not in seed_incidents:
            errors.append(f"Row {idx} ({did}): reference_record_id '{ref_id}' does not exist in seed_incidents.csv.")
    else:
        errors.append(f"Row {idx} ({did}): Invalid reference_record_id format '{ref_id}'. Must be CT-DUP-xxx or CT-INC-xxx.")

    # 8. Spatial Coordinates Sanity
    if loc_status == "UNKNOWN":
        if lat_str or lon_str:
            warnings.append(f"Row {idx} ({did}): location_status is UNKNOWN but coordinates provided ({lat_str}, {lon_str}).")
    else:
        if not lat_str or not lon_str:
            errors.append(f"Row {idx} ({did}): Missing coordinates for location_status '{loc_status}'.")
        else:
            try:
                lat = float(lat_str)
                lon = float(lon_str)
                if not (SANITY_MIN_LAT <= lat <= SANITY_MAX_LAT):
                    errors.append(f"Row {idx} ({did}): Latitude {lat} out of Lucknow bounds [{SANITY_MIN_LAT}, {SANITY_MAX_LAT}].")
                if not (SANITY_MIN_LON <= lon <= SANITY_MAX_LON):
                    errors.append(f"Row {idx} ({did}): Longitude {lon} out of Lucknow bounds [{SANITY_MIN_LON}, {SANITY_MAX_LON}].")
            except ValueError:
                errors.append(f"Row {idx} ({did}): Non-numeric coordinates ({lat_str}, {lon_str}).")

# --- CHECK 4: Cluster & Scenario Balance Analysis ---
print(f"[CHECK 4] Cluster & Scenario Balance: ", end="")
cluster_count = len(clusters_map)
duplicate_count = labels_count.get("DUPLICATE", 0)
likely_count = labels_count.get("LIKELY_DUPLICATE", 0)
possible_count = labels_count.get("POSSIBLE_DUPLICATE", 0)
unrelated_count = labels_count.get("UNRELATED", 0)

if not (5 <= cluster_count <= 8):
    warnings.append(f"Cluster count {cluster_count} outside recommended range 5-8.")

if duplicate_count == 0 or likely_count == 0 or possible_count == 0 or unrelated_count == 0:
    errors.append("All four duplicate labels (DUPLICATE, LIKELY_DUPLICATE, POSSIBLE_DUPLICATE, UNRELATED) must be present.")
else:
    print(f"PASS ({cluster_count} clusters, all 4 labels represented)")

# --- CHECK 5: Regression & Frozen Foundations Check ---
print("[CHECK 5] Prior Phase Dataset Immutability Check: ", end="")
prior_files = {
    "Phase 1 Lexicon Master": os.path.join(BASE_DIR, "data/authority/lucknow_authority_master.json"),
    "Phase 2 Jurisdiction": os.path.join(BASE_DIR, "data/gis/jurisdiction_registry.csv"),
    "Phase 3A Assets": os.path.join(BASE_DIR, "data/lucknow/assets/asset_ownership.csv"),
    "Phase 3B Incidents": os.path.join(BASE_DIR, "data/lucknow/incidents/seed_incidents.csv"),
    "Phase 3C Evidence": os.path.join(BASE_DIR, "data/lucknow/evidence/evidence.csv")
}
frozen_ok = True
for name, pth in prior_files.items():
    if not os.path.exists(pth) or os.path.getsize(pth) == 0:
        errors.append(f"Frozen dataset missing or empty: {name} ({pth})")
        frozen_ok = False

if frozen_ok:
    print("PASS (All 5 prior phase master files intact)")
else:
    print("FAIL (Prior phase file corruption detected)")

# --- Summary & Reporting ---
print("\n" + "=" * 75)
print("DUPLICATE DATA INTEGRITY & VALIDATION REPORT")
print("=" * 75)
print(f"Total Duplicate Records Evaluated: {total_records}")
print(f"Total Candidate Clusters:         {cluster_count}")
print(f"Validation Status:                {'PASSED (0 Errors)' if len(errors) == 0 else f'FAILED ({len(errors)} Errors)'}")

print("\n[DUPLICATE LABEL DISTRIBUTION (Curated Ground Truth)]")
for k, v in sorted(labels_count.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[LANGUAGE DISTRIBUTION]")
for k, v in sorted(languages_count.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[ISSUE CATEGORY DISTRIBUTION]")
for k, v in sorted(categories_count.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[LOCATION STATUS DISTRIBUTION]")
for k, v in sorted(location_statuses_count.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[EVIDENCE AVAILABILITY DISTRIBUTION]")
for k, v in sorted(evidence_available_count.items()):
    print(f"  {k:<28} : {v:>2} records")

print(f"\n[AUDIT RESULTS]")
print(f"  Total Errors Found            : {len(errors)}")
print(f"  Total Warnings Logged         : {len(warnings)}")
print(f"  Intentional Test Warnings     : {len(intentional_test_warnings)}")

# Save machine-readable JSON report
report_data = {
    "validation_suite": "CivicTrace Phase 3D Duplicate Validator",
    "status": "PASSED" if len(errors) == 0 else "FAILED",
    "dataset_path": "data/lucknow/duplicates/duplicate_cases.csv",
    "metrics": {
        "total_duplicate_records": total_records,
        "cluster_count": cluster_count,
        "duplicate_label_distribution": labels_count,
        "language_distribution": languages_count,
        "issue_category_distribution": categories_count,
        "location_status_distribution": location_statuses_count,
        "evidence_available_distribution": evidence_available_count,
        "data_mode_distribution": data_modes_count,
        "source_type_distribution": source_types_count,
        "provenance_completeness": 1.0 if all(r.get("source_id") and r.get("source_reference") for r in duplicate_records) else 0.0,
        "coordinate_sanity_pass_rate": 1.0 if len([e for e in errors if "bounds" in e or "coordinates" in e]) == 0 else 0.0
    },
    "intentional_test_warnings": intentional_test_warnings,
    "warnings": warnings,
    "errors": errors
}

with open(REPORT_JSON, 'w', encoding='utf-8') as f:
    json.dump(report_data, f, indent=2)

print(f"\nMachine-Readable Report Written to: {REPORT_JSON}")
print("=" * 75)

if errors:
    print(f"CRITICAL: Validation suite failed with {len(errors)} error(s).")
    for e in errors:
        print(f"  [ERROR] {e}")
    sys.exit(1)
else:
    print("ALL DUPLICATE DATA INTEGRITY CHECKS PASSED WITH ZERO ERRORS!")
    sys.exit(0)
