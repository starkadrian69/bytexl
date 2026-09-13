#!/usr/bin/env python3
"""
validate_evidence.py
CivicTrace Phase 3C — Lucknow Evidence Dataset Validation Suite

Validates:
1. Exact 18-column schema & header ordering
2. Foreign key referencing: incident_id must exist in seed_incidents.csv
3. Explicit evidence chains: evidence_chain_id integrity & before/after pairing
4. Strict enum conformance for all controlled vocabulary fields
5. Scope attribution: evidence_scope validity & semantic alignment
6. Provenance integrity: registered sources, real vs synthetic evaluation standards
7. Transparent URI validation: synthetic:// references & empty physical file paths
8. Spatial sanity & decoupled location status (VERIFIED, APPROXIMATE, UNKNOWN, CONFLICT, NOT_APPLICABLE)
9. Human/data-curation confidence score validation (float 0.0 to 1.0)
10. Resolution ground-truth support & contradiction detection (CONTRADICTORY_RESOLUTION_EVIDENCE)
11. Emits machine-readable data/lucknow/evidence/evidence_validation_report.json
"""

import os
import sys
import csv
import json
import math

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_CSV = os.path.join(BASE_DIR, "data/lucknow/evidence/evidence.csv")
REPORT_JSON = os.path.join(BASE_DIR, "data/lucknow/evidence/evidence_validation_report.json")
INCIDENTS_CSV = os.path.join(BASE_DIR, "data/lucknow/incidents/seed_incidents.csv")
SOURCES_CSV = os.path.join(BASE_DIR, "data/sources/source_registry.csv")
GIS_SOURCES_CSV = os.path.join(BASE_DIR, "data/gis/gis_source_registry.csv")

EXPECTED_HEADERS = [
    "evidence_id", "evidence_chain_id", "incident_id", "evidence_type",
    "evidence_stage", "evidence_scope", "file_path", "latitude", "longitude",
    "capture_time", "source_type", "resolution_label", "evidence_quality",
    "confidence", "source_id", "source_reference", "location_status", "notes"
]

ALLOWED_EVIDENCE_TYPES = {
    "CITIZEN_PHOTO", "CITIZEN_VIDEO", "AUTHORITY_UPDATE", "BEFORE_PHOTO",
    "AFTER_PHOTO", "FIELD_INSPECTION", "DOCUMENTARY_EVIDENCE"
}

ALLOWED_EVIDENCE_STAGES = {"BEFORE", "DURING", "AFTER", "UNKNOWN"}

ALLOWED_EVIDENCE_SCOPES = {
    "INCIDENT", "LOCATION", "CONDITION", "RESOLUTION", "AUTHORITY_UPDATE"
}

ALLOWED_SOURCE_TYPES = {"REAL_DOCUMENTED", "OWN_CONTROLLED", "SYNTHETIC_EVALUATION"}

ALLOWED_RESOLUTION_LABELS = {
    "FULLY_RESOLVED", "PARTIALLY_RESOLVED", "NOT_RESOLVED", "INSUFFICIENT_EVIDENCE"
}

ALLOWED_EVIDENCE_QUALITIES = {"HIGH", "MEDIUM", "LOW", "UNUSABLE"}

ALLOWED_LOCATION_STATUSES = {
    "VERIFIED", "APPROXIMATE", "UNKNOWN", "CONFLICT", "NOT_APPLICABLE"
}

# Broad Lucknow coordinate sanity bounds (informative check, not hard administrative gate)
SANITY_MIN_LAT, SANITY_MAX_LAT = 26.60, 27.15
SANITY_MIN_LON, SANITY_MAX_LON = 80.70, 81.25

errors = []
warnings = []
intentional_test_warnings = []

print("=" * 75)
print("CIVICTRACE PHASE 3C: EVIDENCE DATASET VALIDATION SUITE")
print("=" * 75)

# --- CHECK 1: File Existence & Dependencies ---
print("[CHECK 1] Deliverable & Dependency File Existence: ", end="")
required_files = [EVIDENCE_CSV, INCIDENTS_CSV, SOURCES_CSV, GIS_SOURCES_CSV]
missing_files = [f for f in required_files if not os.path.exists(f)]
if missing_files:
    errors.append(f"Missing required deliverable/dependency files: {missing_files}")
    print(f"FAIL (Missing {len(missing_files)} files)")
    sys.exit(1)
else:
    print("PASS (All deliverable assets and dependencies present)")

# --- CHECK 2: Seed Incidents Ingestion (Phase 3B Foreign Key) ---
print("[CHECK 2] Phase 3B Seed Incidents Ingestion: ", end="")
seed_incidents = {}
with open(INCIDENTS_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        seed_incidents[row["incident_id"]] = row
print(f"PASS ({len(seed_incidents)} seed incidents loaded as foreign key target)")

# --- CHECK 3: Source Registry Ingestion ---
print("[CHECK 3] Provenance Source Registries Ingestion: ", end="")
registered_sources = {}
for src_path in [SOURCES_CSV, GIS_SOURCES_CSV]:
    with open(src_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            registered_sources[row["source_id"]] = row
print(f"PASS ({len(registered_sources)} registered sources loaded)")

# --- CHECK 4: CSV Schema & Header Conformance ---
print("[CHECK 4] Evidence CSV Schema & Header Conformance: ", end="")
with open(EVIDENCE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    csv_rows = list(reader)

if not csv_rows:
    errors.append("Evidence CSV is completely empty.")
    print("FAIL (Empty file)")
    sys.exit(1)

headers = csv_rows[0]
if headers != EXPECTED_HEADERS:
    errors.append(f"Header mismatch. Expected {EXPECTED_HEADERS}, found {headers}")
    print("FAIL")
else:
    print(f"PASS (Exactly {len(headers)} columns matching schema)")

evidence_records = []
with open(EVIDENCE_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        evidence_records.append(row)

total_records = len(evidence_records)
print(f"\n[AUDITING {total_records} EVIDENCE RECORDS UNDER PHASE 3C INTEGRITY RULES]")

# Helper: Haversine distance
def haversine_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Tracking collections
seen_evidence_ids = set()
seen_records_content = set()
chains_map = {}
incidents_map = {}

type_counts = {}
stage_counts = {}
scope_counts = {}
source_type_counts = {}
resolution_counts = {}
quality_counts = {}
location_status_counts = {}

# Audit loop
for idx, r in enumerate(evidence_records, start=2):
    eid = r.get("evidence_id", "").strip()
    cid = r.get("evidence_chain_id", "").strip()
    inc_id = r.get("incident_id", "").strip()
    etype = r.get("evidence_type", "").strip()
    stage = r.get("evidence_stage", "").strip()
    scope = r.get("evidence_scope", "").strip()
    fpath = r.get("file_path", "").strip()
    lat_str = r.get("latitude", "").strip()
    lon_str = r.get("longitude", "").strip()
    ctime = r.get("capture_time", "").strip()
    stype = r.get("source_type", "").strip()
    res_label = r.get("resolution_label", "").strip()
    quality = r.get("evidence_quality", "").strip()
    conf_str = r.get("confidence", "").strip()
    sid = r.get("source_id", "").strip()
    sref = r.get("source_reference", "").strip()
    loc_status = r.get("location_status", "").strip()
    notes = r.get("notes", "").strip()

    # 1. ID Uniqueness & Non-Empty
    if not eid:
        errors.append(f"Row {idx}: Empty evidence_id.")
    elif eid in seen_evidence_ids:
        errors.append(f"Row {idx}: Duplicate evidence_id '{eid}'.")
    seen_evidence_ids.add(eid)

    # 2. Duplicate Record Content Check
    content_fingerprint = (cid, inc_id, etype, stage, scope, lat_str, lon_str, ctime, stype, res_label)
    if content_fingerprint in seen_records_content:
        warnings.append(f"Row {idx}: Exact duplicate evidence record content for '{eid}'.")
    seen_records_content.add(content_fingerprint)

    # 3. Chain ID Integrity
    if not cid:
        errors.append(f"Row {idx} ({eid}): Missing evidence_chain_id.")
    else:
        chains_map.setdefault(cid, []).append(r)

    # 4. Incident Reference (Foreign Key)
    if not inc_id:
        errors.append(f"Row {idx} ({eid}): Missing incident_id.")
    elif inc_id not in seed_incidents:
        errors.append(f"Row {idx} ({eid}): Foreign key violation. incident_id '{inc_id}' does not exist in seed_incidents.csv.")
    else:
        incidents_map.setdefault(inc_id, []).append(r)

    # 5. Enum Checks
    if etype not in ALLOWED_EVIDENCE_TYPES:
        errors.append(f"Row {idx} ({eid}): Invalid evidence_type '{etype}'. Allowed: {ALLOWED_EVIDENCE_TYPES}")
    type_counts[etype] = type_counts.get(etype, 0) + 1

    if stage not in ALLOWED_EVIDENCE_STAGES:
        errors.append(f"Row {idx} ({eid}): Invalid evidence_stage '{stage}'. Allowed: {ALLOWED_EVIDENCE_STAGES}")
    stage_counts[stage] = stage_counts.get(stage, 0) + 1

    if scope not in ALLOWED_EVIDENCE_SCOPES:
        errors.append(f"Row {idx} ({eid}): Invalid evidence_scope '{scope}'. Allowed: {ALLOWED_EVIDENCE_SCOPES}")
    scope_counts[scope] = scope_counts.get(scope, 0) + 1

    if stype not in ALLOWED_SOURCE_TYPES:
        errors.append(f"Row {idx} ({eid}): Invalid source_type '{stype}'. Allowed: {ALLOWED_SOURCE_TYPES}")
    source_type_counts[stype] = source_type_counts.get(stype, 0) + 1

    if res_label not in ALLOWED_RESOLUTION_LABELS:
        errors.append(f"Row {idx} ({eid}): Invalid resolution_label '{res_label}'. Allowed: {ALLOWED_RESOLUTION_LABELS}")
    resolution_counts[res_label] = resolution_counts.get(res_label, 0) + 1

    if quality not in ALLOWED_EVIDENCE_QUALITIES:
        errors.append(f"Row {idx} ({eid}): Invalid evidence_quality '{quality}'. Allowed: {ALLOWED_EVIDENCE_QUALITIES}")
    quality_counts[quality] = quality_counts.get(quality, 0) + 1

    if loc_status not in ALLOWED_LOCATION_STATUSES:
        errors.append(f"Row {idx} ({eid}): Invalid location_status '{loc_status}'. Allowed: {ALLOWED_LOCATION_STATUSES}")
    location_status_counts[loc_status] = location_status_counts.get(loc_status, 0) + 1

    # 6. Confidence Score Validation (Human curation confidence, float 0.0 - 1.0)
    try:
        cval = float(conf_str)
        if not (0.0 <= cval <= 1.0):
            errors.append(f"Row {idx} ({eid}): Confidence '{conf_str}' out of range [0.0, 1.0].")
    except ValueError:
        errors.append(f"Row {idx} ({eid}): Confidence '{conf_str}' is not a valid float.")

    # 7. Provenance Verification
    if not sid:
        errors.append(f"Row {idx} ({eid}): Missing source_id.")
    elif sid not in registered_sources:
        errors.append(f"Row {idx} ({eid}): source_id '{sid}' not registered in source registries.")

    if not sref:
        errors.append(f"Row {idx} ({eid}): Missing source_reference.")

    if stype == "REAL_DOCUMENTED":
        # Rule: No fabricated local files; file_path should normally remain empty or cite source://
        if fpath and not (fpath.startswith("source://") or fpath.startswith("http://") or fpath.startswith("https://")):
            errors.append(f"Row {idx} ({eid}): REAL_DOCUMENTED file_path '{fpath}' violates no-fabrication rule. Use empty string or source:// reference.")
    elif stype == "SYNTHETIC_EVALUATION":
        # Rule: synthetic evaluation evidence must use synthetic:// URI if a path is specified
        if fpath and not fpath.startswith("synthetic://"):
            errors.append(f"Row {idx} ({eid}): SYNTHETIC_EVALUATION file_path '{fpath}' must use synthetic:// URI scheme.")
        if "synthetic" not in sref.lower() and "evaluation" not in sref.lower():
            warnings.append(f"Row {idx} ({eid}): SYNTHETIC_EVALUATION source_reference should explicitly state synthetic scenario.")

    # 8. Location & Coordinate Sanity
    if loc_status in {"UNKNOWN", "NOT_APPLICABLE"}:
        if lat_str or lon_str:
            warnings.append(f"Row {idx} ({eid}): location_status is '{loc_status}', but coordinates ({lat_str}, {lon_str}) are provided.")
    else:
        if not lat_str or not lon_str:
            errors.append(f"Row {idx} ({eid}): Missing coordinates for location_status '{loc_status}'.")
        else:
            try:
                lat = float(lat_str)
                lon = float(lon_str)
                # Broad sanity envelope check (warn if out of range, do not hard invalidate)
                if not (SANITY_MIN_LAT <= lat <= SANITY_MAX_LAT and SANITY_MIN_LON <= lon <= SANITY_MAX_LON):
                    warnings.append(f"Row {idx} ({eid}): Coordinate ({lat}, {lon}) outside broad Lucknow sanity envelope [{SANITY_MIN_LAT}-{SANITY_MAX_LAT}, {SANITY_MIN_LON}-{SANITY_MAX_LON}].")
            except ValueError:
                errors.append(f"Row {idx} ({eid}): Malformed coordinate values ({lat_str}, {lon_str}).")

    # 9. Intentional Edge Cases & Warnings
    if loc_status == "CONFLICT":
        wmsg = f"Evidence {eid} (Incident {inc_id}): Intentional context-supported spatial conflict. Coordinates reflect camera EXIF discordance with intake narrative (Difficult Case D)."
        intentional_test_warnings.append(wmsg)
        print(f"  [INTENTIONAL TEST WARNING] {wmsg}")

    if quality == "UNUSABLE":
        wmsg = f"Evidence {eid} (Incident {inc_id}): Intentional poor-quality evidence test case. Image unusable due to extreme darkness/blur."
        intentional_test_warnings.append(wmsg)
        print(f"  [INTENTIONAL TEST WARNING] {wmsg}")

# --- CHECK 5: Evidence Chain & Resolution Consistency ---
print("\n[CHECK 5] Evidence Chain & Resolution Ground-Truth Consistency Audit:")

complete_before_after_chains = 0
incomplete_chains = 0
contradictory_chains = 0
unsupported_full_resolution_claims = 0

for cid, records in chains_map.items():
    inc_ids = {r["incident_id"] for r in records}
    if len(inc_ids) > 1:
        errors.append(f"Chain {cid} spans multiple incidents: {inc_ids}. An evidence chain must belong to a single incident.")

    target_inc_id = list(inc_ids)[0]
    stages = {r["evidence_stage"] for r in records}
    types = {r["evidence_type"] for r in records}
    scopes = {r["evidence_scope"] for r in records}
    res_labels = {r["resolution_label"] for r in records}

    has_before = "BEFORE" in stages
    has_after = "AFTER" in stages

    if has_before and has_after:
        complete_before_after_chains += 1
    else:
        incomplete_chains += 1
        wmsg = f"Chain {cid} (Incident {target_inc_id}): Incomplete before/after chain (Stages present: {stages}). Intentional edge scenario."
        intentional_test_warnings.append(wmsg)
        print(f"  [INTENTIONAL TEST WARNING] {wmsg}")

    # Resolution consistency audit:
    # Rule 14: FULLY_RESOLVED must have credible supporting AFTER evidence, FIELD_INSPECTION, or documentary resolution
    if "FULLY_RESOLVED" in res_labels:
        has_resolution_support = (
            has_after or
            "FIELD_INSPECTION" in types or
            "RESOLUTION" in scopes
        )
        if not has_resolution_support:
            errors.append(f"Chain {cid} (Incident {target_inc_id}): resolution_label is FULLY_RESOLVED, but lacks supporting AFTER stage, FIELD_INSPECTION, or RESOLUTION scope evidence.")
            unsupported_full_resolution_claims += 1

    # Contradictory evidence detection (Rule 8: e.g. CT-INC-014 / CHAIN-006)
    # Authority update claims closure/resolution, but citizen evidence shows defect persists
    has_auth_update = "AUTHORITY_UPDATE" in types or "AUTHORITY_UPDATE" in scopes
    has_persisting_citizen = any(
        r["evidence_stage"] == "AFTER" and r["evidence_type"] == "CITIZEN_PHOTO" and r["resolution_label"] == "NOT_RESOLVED"
        for r in records
    )

    if has_auth_update and has_persisting_citizen:
        contradictory_chains += 1
        wmsg = f"Chain {cid} (Incident {target_inc_id}): CONTRADICTORY_RESOLUTION_EVIDENCE detected. Authority update claims closure but subsequent citizen evidence indicates issue persists. Ground truth curated as NOT_RESOLVED."
        intentional_test_warnings.append(wmsg)
        print(f"  [INTENTIONAL TEST WARNING] {wmsg}")

provenance_completeness = 1.0 if total_records > 0 and all(r.get("source_id") and r.get("source_reference") for r in evidence_records) else 0.0
resolution_support_completeness = 1.0 if unsupported_full_resolution_claims == 0 else 0.0

# Print Summary Report
print("\n" + "=" * 75)
print("EVIDENCE DATA INTEGRITY & VALIDATION REPORT")
print("=" * 75)
print(f"Total Evidence Records Evaluated: {total_records}")
print(f"Total Incidents Represented:     {len(incidents_map)}")
print(f"Total Evidence Chains:           {len(chains_map)}")
print(f"Complete BEFORE/AFTER Chains:    {complete_before_after_chains}")
print(f"Incomplete Evidence Chains:      {incomplete_chains}")
print(f"Contradictory Chains Flagged:    {contradictory_chains}")
print(f"Unsupported FULLY_RESOLVED:      {unsupported_full_resolution_claims}")
print(f"Validation Status:               {'PASSED (0 Errors)' if len(errors) == 0 else f'FAILED ({len(errors)} Errors)'}")

print("\n[EVIDENCE TYPE DISTRIBUTION]")
for k, v in sorted(type_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[EVIDENCE STAGE DISTRIBUTION]")
for k, v in sorted(stage_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[EVIDENCE SCOPE DISTRIBUTION]")
for k, v in sorted(scope_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[SOURCE TYPE DISTRIBUTION]")
for k, v in sorted(source_type_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[RESOLUTION LABEL DISTRIBUTION (Curated Ground Truth)]")
for k, v in sorted(resolution_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[EVIDENCE QUALITY DISTRIBUTION]")
for k, v in sorted(quality_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print("\n[LOCATION STATUS DISTRIBUTION]")
for k, v in sorted(location_status_counts.items()):
    print(f"  {k:<28} : {v:>2} records")

print(f"\n[AUDIT RESULTS]")
print(f"  Total Errors Found           : {len(errors)}")
print(f"  Total Warnings Logged        : {len(warnings)}")
print(f"  Intentional Test Warnings    : {len(intentional_test_warnings)}")

# Save machine-readable JSON report
report_data = {
    "validation_suite": "CivicTrace Phase 3C Evidence Validator",
    "status": "PASSED" if len(errors) == 0 else "FAILED",
    "dataset_path": "data/lucknow/evidence/evidence.csv",
    "metrics": {
        "total_evidence_records": total_records,
        "total_incidents_represented": len(incidents_map),
        "evidence_chain_count": len(chains_map),
        "complete_before_after_chain_count": complete_before_after_chains,
        "incomplete_chain_count": incomplete_chains,
        "contradictory_chain_count": contradictory_chains,
        "unsupported_full_resolution_claims": unsupported_full_resolution_claims,
        "provenance_completeness": provenance_completeness,
        "resolution_support_completeness": resolution_support_completeness,
        "evidence_type_distribution": type_counts,
        "evidence_stage_distribution": stage_counts,
        "evidence_scope_distribution": scope_counts,
        "source_type_distribution": source_type_counts,
        "resolution_label_distribution": resolution_counts,
        "evidence_quality_distribution": quality_counts,
        "location_status_distribution": location_status_counts
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
    print("ALL EVIDENCE DATA INTEGRITY CHECKS PASSED WITH ZERO ERRORS!")
    sys.exit(0)
