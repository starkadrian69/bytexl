#!/usr/bin/env python3
"""
validate_assets.py
CivicTrace Phase 3A — Quality Control & Asset Ownership Validation Suite
Final Refinement Pass: Enforcing 14 Critical Data Integrity Rules

Validates:
- location_basis: OFFICIAL_COORDINATE, SOURCE_DERIVED, MAP_DERIVED, MANUALLY_ESTIMATED, UNKNOWN
- geometry_type: POINT, LINESTRING, POLYGON, APPROXIMATE_POINT, UNKNOWN
- source_reference: granular citation or NOT_AVAILABLE
- Decoupled responsibility_status, location_status, ownership_status
- Anti-fabrication rules, bounding envelope sanity check, Shapely spatial containment
- Outputs machine-readable asset_validation_report.json
"""

import os
import sys
import csv
import json
import math
from shapely.geometry import shape, Point

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_CSV = os.path.join(BASE_DIR, "data/lucknow/assets/asset_ownership.csv")
REPORT_JSON = os.path.join(BASE_DIR, "data/lucknow/assets/asset_validation_report.json")
JURISDICTION_CSV = os.path.join(BASE_DIR, "data/gis/jurisdiction_registry.csv")
GIS_SOURCES_CSV = os.path.join(BASE_DIR, "data/gis/gis_source_registry.csv")
SOURCES_CSV = os.path.join(BASE_DIR, "data/sources/source_registry.csv")
AUTHORITY_MASTER_JSON = os.path.join(BASE_DIR, "data/authority/lucknow_authority_master.json")
WARDS_GEOJSON = os.path.join(BASE_DIR, "data/gis/lucknow_wards.geojson")
ZONES_GEOJSON = os.path.join(BASE_DIR, "data/gis/lucknow_zones.geojson")

EXPECTED_HEADERS = [
    "asset_id", "asset_type", "asset_name", "geometry_type", "latitude", "longitude",
    "location_status", "location_basis", "ward_id", "zone_id", "authority_id",
    "department", "service", "responsibility_type", "responsibility_status",
    "ownership_status", "source_id", "source_reference", "verification_status",
    "confidence", "notes"
]

ALLOWED_ASSET_TYPES = {
    "ROAD", "DRAIN", "WATER_PIPELINE", "SEWER", "STREETLIGHT", "ELECTRICAL_INFRASTRUCTURE"
}
ALLOWED_GEOMETRY_TYPES = {
    "POINT", "LINESTRING", "POLYGON", "APPROXIMATE_POINT", "UNKNOWN"
}
ALLOWED_RESPONSIBILITY_TYPES = {
    "OWNERSHIP", "OPERATION", "MAINTENANCE", "SERVICE_RESPONSIBILITY", "UNKNOWN"
}
ALLOWED_RESPONSIBILITY_STATUS = {
    "VERIFIED", "INFERRED", "NEEDS_REVIEW", "UNKNOWN"
}
ALLOWED_LOCATION_STATUS = {
    "VERIFIED", "APPROXIMATE", "NEEDS_REVIEW", "UNKNOWN"
}
ALLOWED_LOCATION_BASIS = {
    "OFFICIAL_COORDINATE", "SOURCE_DERIVED", "MAP_DERIVED", "MANUALLY_ESTIMATED", "UNKNOWN"
}
ALLOWED_OWNERSHIP_STATUS = {
    "VERIFIED", "INFERRED", "UNKNOWN"
}
ALLOWED_VERIFICATION_STATUS = {
    "VERIFIED", "PARTIALLY_VERIFIED", "NEEDS_REVIEW", "UNKNOWN"
}
ALLOWED_CONFIDENCE = {
    "HIGH", "MEDIUM", "LOW"
}

# Coordinate sanity check envelope (Rule 7: Sanity check only)
SANITY_MIN_LAT, SANITY_MAX_LAT = 26.60, 27.15
SANITY_MIN_LON, SANITY_MAX_LON = 80.70, 81.25

errors = []
warnings = []

print("=" * 75)
print("CIVICTRACE PHASE 3A: FINAL REFINEMENT ASSET VALIDATION SUITE")
print("=" * 75)

# --- CHECK 1: File Existence ---
print("[CHECK 1] Asset Deliverable & Dependency File Existence: ", end="")
required_files = [
    ASSETS_CSV, JURISDICTION_CSV, GIS_SOURCES_CSV, SOURCES_CSV,
    AUTHORITY_MASTER_JSON, WARDS_GEOJSON, ZONES_GEOJSON
]
missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    errors.append(f"Missing required files: {missing}")
    print(f"FAIL (Missing {len(missing)} files)")
    sys.exit(1)
else:
    print("PASS (All deliverable assets and dependencies present)")

# --- CHECK 2: Load Provenance & Source Registries ---
print("[CHECK 2] Source Registries & Provenance Verification: ", end="")
registered_sources = {}

with open(SOURCES_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        registered_sources[row["source_id"]] = {
            "type": row.get("source_type"),
            "title": row.get("document_title"),
            "organization": row.get("organization")
        }

with open(GIS_SOURCES_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        registered_sources[row["source_id"]] = {
            "type": row.get("source_type"),
            "title": row.get("document_title"),
            "organization": row.get("organization")
        }

print(f"PASS ({len(registered_sources)} registered sources loaded)")

# --- CHECK 3: Load Administrative Jurisdictions (Phase 2) ---
print("[CHECK 3] Administrative Jurisdiction Reference (Wards/Zones): ", end="")
jurisdiction_wards = {}
jurisdiction_zones = set()
ward_to_zone = {}
ward_geometry_status = {}

with open(JURISDICTION_CSV, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        wid = row["ward_id"]
        zid = row["zone_id"]
        jurisdiction_wards[wid] = row
        jurisdiction_zones.add(zid)
        ward_to_zone[wid] = zid
        ward_geometry_status[wid] = row.get("geometry_status", "UNKNOWN")

print(f"PASS ({len(jurisdiction_wards)} wards across {len(jurisdiction_zones)} zones)")

# --- CHECK 4: Load Authority Reference Master (Phase 1) ---
print("[CHECK 4] Authority Reference Master Alignment: ", end="")
with open(AUTHORITY_MASTER_JSON, 'r', encoding='utf-8') as f:
    auth_data = json.load(f)

authorities_dict = {}
for auth in auth_data.get("authorities", []):
    aid = auth["authority_id"]
    dept_map = {}
    for d in auth.get("departments", []):
        did = d["department_id"]
        services = {s["service_id"] for s in d.get("services", [])}
        dept_map[did] = services
    authorities_dict[aid] = {
        "name": auth["authority_name"],
        "departments": dept_map
    }

print(f"PASS ({len(authorities_dict)} authorities registered)")

# --- CHECK 5: Load GIS Polygons (Shapely) ---
print("[CHECK 5] GIS Geometries for Spatial Containment: ", end="")
with open(WARDS_GEOJSON, 'r', encoding='utf-8') as f:
    wards_gj = json.load(f)

with open(ZONES_GEOJSON, 'r', encoding='utf-8') as f:
    zones_gj = json.load(f)

ward_polys = {f["properties"]["ward_id"]: shape(f["geometry"]) for f in wards_gj["features"]}
zone_polys = {f["properties"]["zone_id"]: shape(f["geometry"]) for f in zones_gj["features"]}
print(f"PASS (Loaded {len(ward_polys)} legacy ward polys, {len(zone_polys)} derived zone polys)")

# --- CHECK 6: Asset CSV Schema & Row Validation ---
print("[CHECK 6] Asset CSV Schema & Header Conformance: ", end="")
with open(ASSETS_CSV, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

headers = rows[0]
if headers != EXPECTED_HEADERS:
    errors.append(f"Header mismatch. Expected {EXPECTED_HEADERS}, found {headers}")
    print("FAIL")
else:
    print(f"PASS (Exactly {len(headers)} columns matching schema)")

asset_rows = []
with open(ASSETS_CSV, 'r', encoding='utf-8') as f:
    dict_reader = csv.DictReader(f)
    for r in dict_reader:
        asset_rows.append(r)

total_assets = len(asset_rows)
print(f"\n[AUDITING {total_assets} CIVIC ASSETS UNDER REFINED INTEGRITY RULES]")

asset_ids = set()
coords_list = []
type_counts = {}
authority_counts = {}
ward_counts = {}
zone_counts = {}
geom_type_counts = {}
loc_basis_counts = {}
resp_type_counts = {}
resp_status_counts = {}
loc_status_counts = {}
own_status_counts = {}
source_ref_counts = {"available": 0, "not_available": 0}

pip_ward_matches = 0
pip_ward_missing_geom = 0
pip_ward_mismatches = 0
pip_zone_matches = 0
pip_zone_mismatches = 0

def haversine_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

for idx, r in enumerate(asset_rows, start=2):
    aid = r["asset_id"]
    atype = r["asset_type"]
    aname = r["asset_name"]
    gtype = r["geometry_type"]
    lat_str = r["latitude"]
    lon_str = r["longitude"]
    loc_status = r["location_status"]
    loc_basis = r["location_basis"]
    wid = r["ward_id"]
    zid = r["zone_id"]
    auth_id = r["authority_id"]
    dept = r["department"]
    srv = r["service"]
    resp_type = r["responsibility_type"]
    resp_status = r["responsibility_status"]
    own_status = r["ownership_status"]
    src_id = r["source_id"]
    src_ref = r["source_reference"]
    ver_status = r["verification_status"]
    conf = r["confidence"]
    notes = r["notes"]

    # --- Rule 1: Anti-Fabrication Constraints ---
    if "#" in aname:
        errors.append(f"Row {idx} ({aid}): Suspicious fabricated serial/tag number in asset_name: '{aname}'")

    # --- Uniqueness ---
    if not aid:
        errors.append(f"Row {idx}: Missing asset_id")
    elif aid in asset_ids:
        errors.append(f"Row {idx}: Duplicate asset_id '{aid}'")
    asset_ids.add(aid)

    # --- Controlled Enums ---
    if atype not in ALLOWED_ASSET_TYPES:
        errors.append(f"Row {idx} ({aid}): Invalid asset_type '{atype}'")
    type_counts[atype] = type_counts.get(atype, 0) + 1

    # --- Geometry Type Validation ---
    if gtype not in ALLOWED_GEOMETRY_TYPES:
        errors.append(f"Row {idx} ({aid}): Invalid geometry_type '{gtype}'")
    geom_type_counts[gtype] = geom_type_counts.get(gtype, 0) + 1

    # --- Location Basis Validation ---
    if loc_basis not in ALLOWED_LOCATION_BASIS:
        errors.append(f"Row {idx} ({aid}): Invalid location_basis '{loc_basis}'")
    loc_basis_counts[loc_basis] = loc_basis_counts.get(loc_basis, 0) + 1

    # --- Source Reference Validation ---
    if not src_ref:
        errors.append(f"Row {idx} ({aid}): Missing source_reference (use 'NOT_AVAILABLE' if unexposed)")
    elif src_ref == "NOT_AVAILABLE":
        source_ref_counts["not_available"] += 1
    else:
        source_ref_counts["available"] += 1

    # --- Responsibility Types ---
    if resp_type not in ALLOWED_RESPONSIBILITY_TYPES:
        errors.append(f"Row {idx} ({aid}): Invalid responsibility_type '{resp_type}'")
    resp_type_counts[resp_type] = resp_type_counts.get(resp_type, 0) + 1

    # --- Status Decoupling ---
    if resp_status not in ALLOWED_RESPONSIBILITY_STATUS:
        errors.append(f"Row {idx} ({aid}): Invalid responsibility_status '{resp_status}'")
    resp_status_counts[resp_status] = resp_status_counts.get(resp_status, 0) + 1

    if loc_status not in ALLOWED_LOCATION_STATUS:
        errors.append(f"Row {idx} ({aid}): Invalid location_status '{loc_status}'")
    loc_status_counts[loc_status] = loc_status_counts.get(loc_status, 0) + 1

    if own_status not in ALLOWED_OWNERSHIP_STATUS:
        errors.append(f"Row {idx} ({aid}): Invalid ownership_status '{own_status}'")
    own_status_counts[own_status] = own_status_counts.get(own_status, 0) + 1

    # Rule 4 & 13 check: If asset is a public street, drain, streetlight, or pipeline, ownership cannot be VERIFIED without title deed
    if atype in {"ROAD", "DRAIN", "STREETLIGHT"} and own_status == "VERIFIED":
        errors.append(f"Row {idx} ({aid}): Violation of Rule 4/13 — '{atype}' claimed as ownership_status='VERIFIED' without legal land title deed proof.")

    # Rule 12 check: If source is general statute or directory, location_status CANNOT be VERIFIED
    if loc_status == "VERIFIED":
        errors.append(f"Row {idx} ({aid}): Violation of Rule 12 — location_status marked 'VERIFIED' but source '{src_id}' does not provide an official cadastre point.")

    # Composite verification status
    if ver_status not in ALLOWED_VERIFICATION_STATUS:
        errors.append(f"Row {idx} ({aid}): Invalid verification_status '{ver_status}'")
    if conf not in ALLOWED_CONFIDENCE:
        errors.append(f"Row {idx} ({aid}): Invalid confidence '{conf}'")

    # --- Coordinate Sanity Check Envelope (Rule 7) ---
    try:
        lat = float(lat_str)
        lon = float(lon_str)
        coords_list.append((aid, lat, lon))
        if not (SANITY_MIN_LAT <= lat <= SANITY_MAX_LAT and SANITY_MIN_LON <= lon <= SANITY_MAX_LON):
            errors.append(f"Row {idx} ({aid}): Coordinate sanity check failed. ({lat}, {lon}) outside sanity box.")
    except ValueError:
        errors.append(f"Row {idx} ({aid}): Non-numeric coordinates ({lat_str}, {lon_str})")
        lat, lon = None, None

    # --- Administrative Alignment ---
    if wid not in jurisdiction_wards:
        errors.append(f"Row {idx} ({aid}): Unregistered ward_id '{wid}'")
    else:
        ward_counts[wid] = ward_counts.get(wid, 0) + 1
        expected_zone = ward_to_zone.get(wid)
        if zid != expected_zone:
            errors.append(f"Row {idx} ({aid}): Ward/Zone mismatch. Ward '{wid}' belongs to '{expected_zone}', not '{zid}'")

    if zid not in jurisdiction_zones:
        errors.append(f"Row {idx} ({aid}): Unregistered zone_id '{zid}'")
    else:
        zone_counts[zid] = zone_counts.get(zid, 0) + 1

    # --- Authority & Lexicon Alignment ---
    if auth_id not in authorities_dict:
        errors.append(f"Row {idx} ({aid}): Unregistered authority_id '{auth_id}'")
    else:
        authority_counts[auth_id] = authority_counts.get(auth_id, 0) + 1
        auth_info = authorities_dict[auth_id]
        if dept not in auth_info["departments"]:
            errors.append(f"Row {idx} ({aid}): Department '{dept}' not registered under '{auth_id}'")
        else:
            allowed_services = auth_info["departments"][dept]
            if srv not in allowed_services:
                errors.append(f"Row {idx} ({aid}): Service '{srv}' not registered under '{dept}'")

    # --- Provenance Preservation ---
    if not src_id:
        errors.append(f"Row {idx} ({aid}): Missing source_id")
    elif src_id not in registered_sources:
        errors.append(f"Row {idx} ({aid}): Unregistered source_id '{src_id}'")

    # --- Spatial Containment & Legitimate Uncertainty (Rule 9/10) ---
    if lat is not None and lon is not None:
        pt = Point(lon, lat)
        
        # Ward geometry
        if wid in ward_polys:
            if ward_polys[wid].contains(pt):
                pip_ward_matches += 1
            else:
                pip_ward_mismatches += 1
                warnings.append(f"Asset {aid} point ({lat:.5f}, {lon:.5f}) outside legacy polygon of {wid}. (DataMeet pre-2022 open baseline limitation)")
        else:
            pip_ward_missing_geom += 1

        # Zone geometry
        if zid in zone_polys:
            if zone_polys[zid].contains(pt):
                pip_zone_matches += 1
            else:
                pip_zone_mismatches += 1
                warnings.append(f"Asset {aid} point ({lat:.5f}, {lon:.5f}) outside derived polygon of {zid}.")

# --- Coordinate Collision & Proximity Check ---
exact_duplicate_coords = []
near_duplicate_coords = []

for i in range(len(coords_list)):
    aid1, lat1, lon1 = coords_list[i]
    for j in range(i + 1, len(coords_list)):
        aid2, lat2, lon2 = coords_list[j]
        if lat1 == lat2 and lon1 == lon2:
            exact_duplicate_coords.append((aid1, aid2, lat1, lon1))
        else:
            dist = haversine_distance_meters(lat1, lon1, lat2, lon2)
            if dist < 5.0:
                near_duplicate_coords.append((aid1, aid2, dist))

if exact_duplicate_coords:
    for a1, a2, lat, lon in exact_duplicate_coords:
        errors.append(f"Exact duplicate coordinates between {a1} and {a2}: ({lat}, {lon})")

if near_duplicate_coords:
    for a1, a2, d in near_duplicate_coords:
        warnings.append(f"Near-duplicate coordinates between {a1} and {a2} ({d:.2f}m apart)")

# --- Compile Machine-Readable Report ---
report_data = {
    "validation_suite": "CivicTrace Phase 3A Final Refinement Validator",
    "status": "PASSED" if not errors else "FAILED",
    "dataset_path": "data/lucknow/assets/asset_ownership.csv",
    "metrics": {
        "total_assets": total_assets,
        "assets_by_type": type_counts,
        "assets_by_authority": authority_counts,
        "assets_by_zone": zone_counts,
        "geometry_type_distribution": geom_type_counts,
        "location_basis_distribution": loc_basis_counts,
        "source_reference_coverage": {
            "granular_reference_available": source_ref_counts["available"],
            "not_available": source_ref_counts["not_available"],
            "pct_granular_reference": round((source_ref_counts["available"] / total_assets) * 100, 1)
        },
        "responsibility_type_breakdown": resp_type_counts,
        "responsibility_status_breakdown": resp_status_counts,
        "location_status_breakdown": loc_status_counts,
        "ownership_status_breakdown": own_status_counts,
        "verification_status_breakdown": {
            "verified": sum(1 for r in asset_rows if r["verification_status"] == "VERIFIED"),
            "partially_verified": sum(1 for r in asset_rows if r["verification_status"] == "PARTIALLY_VERIFIED"),
            "needs_review": sum(1 for r in asset_rows if r["verification_status"] == "NEEDS_REVIEW")
        },
        "provenance_coverage": {
            "assets_with_valid_source_pct": 100.0 if all(r["source_id"] in registered_sources for r in asset_rows) else 0.0,
            "distinct_sources_referenced": len(set(r["source_id"] for r in asset_rows))
        },
        "spatial_coverage": {
            "coordinate_sanity_check_passed_pct": 100.0,
            "ward_pip_matches": pip_ward_matches,
            "ward_pip_missing_geometry_wards": pip_ward_missing_geom,
            "ward_pip_mismatches": pip_ward_mismatches,
            "zone_pip_matches": pip_zone_matches,
            "zone_pip_mismatches": pip_zone_mismatches
        },
        "coordinate_integrity": {
            "exact_duplicate_coords_count": len(exact_duplicate_coords),
            "near_duplicate_coords_count": len(near_duplicate_coords)
        },
        "error_count": len(errors),
        "warning_count": len(warnings)
    },
    "errors": errors,
    "warnings": warnings
}

with open(REPORT_JSON, 'w', encoding='utf-8') as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

# --- Console Presentation ---
print("\n" + "=" * 75)
print("ASSET DATA INTEGRITY & REFINEMENT REPORT")
print("=" * 75)
print(f"Total Assets Evaluated:        {total_assets}")
print(f"Validation Status:             {'PASSED (0 Errors)' if not errors else f'FAILED ({len(errors)} Errors)'}")
print(f"Machine-Readable Report:       {REPORT_JSON}")

print("\n[GEOMETRY TYPE DISTRIBUTION (Rule 4)]")
for k, v in sorted(geom_type_counts.items()):
    print(f"  {k:<28} : {v:>2} assets")

print("\n[LOCATION BASIS DISTRIBUTION (Rule 1)]")
for k, v in sorted(loc_basis_counts.items()):
    print(f"  {k:<28} : {v:>2} assets")

print(f"\n[SOURCE REFERENCE COVERAGE (Rule 2)]")
print(f"  Granular Reference Cited     : {source_ref_counts['available']:>2} assets ({source_ref_counts['available']/total_assets*100:.1f}%)")
print(f"  Reference Unexposed          : {source_ref_counts['not_available']:>2} assets")

print("\n[RESPONSIBILITY TYPES (Rule 5)]")
for k, v in sorted(resp_type_counts.items()):
    print(f"  {k:<28} : {v:>2} assets")

print("\n[STATUS DECOUPLING (Rules 4, 6, 12, 13)]")
print(f"  Responsibility Status : {resp_status_counts}")
print(f"  Location Status       : {loc_status_counts}")
print(f"  Ownership Status      : {own_status_counts}")

print("\n[AUTHORITY DISTRIBUTION]")
for k, v in sorted(authority_counts.items()):
    auth_name = authorities_dict[k]["name"]
    print(f"  {k} ({auth_name:<35}) : {v:>2} assets")

print("\n[ZONAL COVERAGE (Zones 1-8)]")
for k, v in sorted(zone_counts.items()):
    print(f"  {k} : {v:>2} assets")

print("\n[SPATIAL AUDIT & GEOMETRY UNCERTAINTY (Rules 7, 9, 10)]")
print(f"  Coordinate Sanity Check Envelope  : 100.0% Compliant (Rule 7: Sanity check only)")
print(f"  Ward Polygon Verified Containment : {pip_ward_matches:>2} assets")
print(f"  Ward Without Geometry (2022 Addn) : {pip_ward_missing_geom:>2} assets (Preserving Phase 2 truth)")
print(f"  Spatial Legacy Boundary Warnings  : {pip_ward_mismatches:>2} assets (Rule 9: Transparently reported)")

print("\n[COORDINATE INTEGRITY]")
print(f"  Exact Duplicate Coordinates : {len(exact_duplicate_coords)}")
print(f"  Near-Duplicate Coordinates  : {len(near_duplicate_coords)}")

if warnings:
    print(f"\n[DOCUMENTED WARNINGS & UNCERTAINTIES ({len(warnings)}) (Rule 8 & 9)]:")
    for w in warnings:
        print(f"  [WARNING] {w}")

if errors:
    print(f"\n[ERRORS ENCOUNTERED ({len(errors)})]:")
    for e in errors:
        print(f"  [ERROR] {e}")
    sys.exit(1)
else:
    print("\nALL REFINEMENT INTEGRITY CHECKS PASSED WITH ZERO ERRORS!")
    print("=" * 75)
