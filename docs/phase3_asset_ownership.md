# Lucknow Asset Ownership Data Foundation Report

**Project:** CivicTrace — Evidence-First Civic Grievance Intelligence Platform  
**Phase:** Phase 3A — Final Refinement Pass  
**Author:** Lead Backend & Civic Data Architect  
**Geographic Scope:** Lucknow District & Municipal Corporation, Uttar Pradesh, India  
**Integrity Standard:** 14 Critical Data Integrity Rules  
**Date:** September 2026  
**Document Version:** 2.1 (Final Refinement Baseline)

---

## Executive Summary

Phase 1 established the **Lucknow Authority Master, Departments, and Service Lexicon** (`data/authority/lucknow_authority_master.json`).  
Phase 2 established the **Lucknow Ward and Zone Administrative Baseline & GIS Reference Layer** (`data/gis/jurisdiction_registry.csv`, `lucknow_wards.geojson`, `lucknow_zones.geojson`).

**Phase 3A establishes the Lucknow Asset Ownership Data Foundation.**  
Its purpose is to bridge the fundamental operational traversal chain:

$$\text{Civic Issue} \longrightarrow \text{GPS Location} \longrightarrow \text{Ward} \longrightarrow \text{Zone} \longrightarrow \textbf{Physical Asset} \longrightarrow \textbf{Responsible Authority / Department}$$

Citizen grievances do not occur in an abstract administrative vacuum; they attach to physical infrastructure located in geographic space. This data foundation establishes a representative, quality-controlled, and strictly traceable baseline of **39 infrastructure assets** across **all 8 municipal zones** and **all 6 target infrastructure categories** adhering to 14 strict anti-fabrication and evidentiary integrity rules.

> [!NOTE]
> **Asset Terminology & Evidentiary Scope**:
> Asset records correspond to identified physical infrastructure entities or infrastructure classes supported by cited sources; exact asset-level identity and location remain subject to the recorded verification status. CivicTrace strictly decouples the existence of infrastructure, its approximate representation, exact asset-level identity, legal ownership, operational responsibility, and maintenance responsibility.

---

## 1. Compliance with the 14 Critical Data Integrity Rules

| # | Integrity Rule | Implementation in CivicTrace Phase 3A |
| :---: | :--- | :--- |
| **1** | **No Fabrication** | Zero invented assets, coordinates, fake asset tags (e.g. `#CK-11-204` was eradicated), or invented specs (e.g. pipe diameters like "600mm", kVA ratings like "250kVA", or wattages like "70W" were eradicated). |
| **2** | **Coverage Target vs. Invention** | The target of ~37 assets is treated as a coverage benchmark, not a requirement to invent records. 39 genuine, source-backed assets were established. |
| **3** | **Uncertainty Assignment** | Proposed assets lacking definitive title or cadastral survey are explicitly tagged `INFERRED`, `APPROXIMATE`, or `NEEDS_REVIEW`. |
| **4** | **Statutory Duty $\neq$ Ownership** | General statutory responsibility under UP Municipal Corporations Act 1959 is never treated as legal property deed ownership of physical roads or drains. |
| **5** | **Functional Mandate Types** | Explicitly distinguishes `OWNERSHIP` (legal capital vesting), `OPERATION` (daily service/pumping), `MAINTENANCE` (patching/desilting), and `SERVICE_RESPONSIBILITY` (capital scheme execution). |
| **6** | **Decoupled Status Tracking** | Schema explicitly separates `responsibility_status` (is authority duty verified?), `location_status` (is coordinate exact or approximate?), and `ownership_status` (is legal title verified?). |
| **7** | **Sanity Envelope Only** | The bounding box `[26.60..27.15, 80.70..81.25]` is treated strictly as a coordinate sanity check, never claimed as an authoritative municipal boundary. |
| **8** | **3-Tier Reporting** | Validation explicitly distinguishes `PASS`, `WARNING`, and `ERROR`. |
| **9** | **Preserve Legitimate Uncertainty** | Geospatial limitations (e.g. DataMeet pre-2022 spatial extents) are surfaced as warnings in validation reports, never converted into fake passes. |
| **10** | **Truthful GIS Classification** | Phase 2 GIS is acknowledged as `SECONDARY_LEGACY` (pre-2022 DataMeet open data) and `DERIVED_CIVICTRACE_GEOMETRY`, never claimed as official current government geometry. |
| **11** | **Complete Provenance** | Every factual claim preserves complete `source_id` provenance and granular `source_reference` pointers. |
| **12** | **No False Location Verification** | If a source supports authority responsibility but does not publish cadastral GPS points, `location_status` is marked `APPROXIMATE`, never `VERIFIED`. |
| **13** | **No False Ownership Verification** | If a source supports physical existence/location but not legal property deeds, `ownership_status` is marked `INFERRED` or `UNKNOWN`, never `VERIFIED`. |
| **14** | **Immutability of Prior Baselines** | Zero modifications or regenerations of Phase 1 or Phase 2 verified reference files. |

---

## 2. Refined Asset Schema (21 Columns)

The dataset `asset_ownership.csv` implements the 21-attribute schema:

```
asset_id,asset_type,asset_name,geometry_type,latitude,longitude,location_status,location_basis,ward_id,zone_id,authority_id,department,service,responsibility_type,responsibility_status,ownership_status,source_id,source_reference,verification_status,confidence,notes
```

### Schema Attributes & Controlled Vocabularies

| Column | Data Type | Description & Controlled Vocabulary |
| :--- | :--- | :--- |
| `asset_id` | String | Unique CivicTrace asset identifier (`AST-ROAD-###`, `AST-DRN-###`, `AST-WTR-###`, `AST-SWR-###`, `AST-STL-###`, `AST-ELE-###`). |
| `asset_type` | Enum | `ROAD`, `DRAIN`, `WATER_PIPELINE`, `SEWER`, `STREETLIGHT`, `ELECTRICAL_INFRASTRUCTURE`. |
| `asset_name` | String | Plaintext description without invented serial tags or unevidenced specifications. |
| `geometry_type` | Enum | Controlled geometry type: `POINT`, `LINESTRING`, `POLYGON`, `APPROXIMATE_POINT`, `UNKNOWN`. |
| `latitude` | Float (WGS 84) | Decimal latitude within coordinate sanity envelope (`[26.60, 27.15]`). |
| `longitude` | Float (WGS 84) | Decimal longitude within coordinate sanity envelope (`[80.70, 81.25]`). |
| `location_status` | Enum | Spatial precision standing: `VERIFIED`, `APPROXIMATE`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `location_basis` | Enum | Coordinate derivation method: `OFFICIAL_COORDINATE`, `SOURCE_DERIVED`, `MAP_DERIVED`, `MANUALLY_ESTIMATED`, `UNKNOWN`. |
| `ward_id` | String | CivicTrace ward identifier from `data/gis/jurisdiction_registry.csv` (`WARD-001` to `WARD-110`). |
| `zone_id` | String | CivicTrace zone identifier from `data/gis/jurisdiction_registry.csv` (`ZONE-01` to `ZONE-08`). |
| `authority_id` | String | CivicTrace authority from `data/authority/lucknow_authority_master.json`. |
| `department` | String | Custodial department / division from Phase 1 master. |
| `service` | String | Relevant civic service from Phase 1 master. |
| `responsibility_type` | Enum | Mandate type: `OWNERSHIP`, `OPERATION`, `MAINTENANCE`, `SERVICE_RESPONSIBILITY`, `UNKNOWN`. |
| `responsibility_status`| Enum | Evidentiary standing of authority mandate: `VERIFIED`, `INFERRED`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `ownership_status` | Enum | Legal property vesting standing: `VERIFIED`, `INFERRED`, `UNKNOWN`. |
| `source_id` | String | Authoritative provenance pointer from registered sources. |
| `source_reference` | String | Specific section, chapter, schedule, or item supporting the claim. |
| `verification_status` | Enum | Composite standing: `VERIFIED`, `PARTIALLY_VERIFIED`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `confidence` | Enum | Assessment confidence: `HIGH`, `MEDIUM`, `LOW`. |
| `notes` | String | Detailed explanation of statutory basis, operational delegation, and spatial uncertainty. |

---

## 3. Controlled Definitions for Refinement Fields

### A. `location_basis`
- `OFFICIAL_COORDINATE`: Coordinate published in an official government gazette, map, or GIS register. (None in current dataset; zero false claims).
- `SOURCE_DERIVED`: Extracted directly from textual location descriptions or survey tables in cited official source.
- `MAP_DERIVED`: Derived by referencing the named landmark/corridor on open spatial baselines (DataMeet/OSM/satellite) corresponding to the cited official locality.
- `MANUALLY_ESTIMATED`: Centroid or representative interior estimation within the verified ward/sector.
- `UNKNOWN`: Insufficient evidence to establish the derivation basis.

### B. `geometry_type`
- `APPROXIMATE_POINT`: A point coordinate representing an approximate location along a linear infrastructure asset (road, drain, pipeline, sewer conduit, overhead circuit). (34 assets in Phase 3A).
- `POINT`: A point coordinate representing a standalone physical facility node (e.g. substation compound, plinth transformer installation, high-mast lighting tower). (5 assets in Phase 3A).
- `LINESTRING`: Continuous polyline vector (reserved for future Phase 3B expansion; zero fake geometries generated).
- `POLYGON`: Enclosed polygon boundary (reserved for future Phase 3B facility footprint expansion).
- `UNKNOWN`: Unspecified geometry.

### C. `source_reference`
Identifies the exact evidence location supporting the asset claim whenever such information is available:
- `Chapter 12 (Streets and Public Roads)` (UP Municipal Corporations Act 1959 `SRC-005`)
- `Chapter 10 (Drains and Drainage)` (UP Municipal Corporations Act 1959 `SRC-005`)
- `Section 18 & Section 24` (UP Water Supply and Sewerage Act 1975 `SRC-011`)
- `Section 24 (Sewerage Services)` (UP Water Supply and Sewerage Act 1975 `SRC-011`)
- `Section 15 & Engineering Division Directory` (UP Urban Planning & Development Act 1973 `SRC-012`)
- `Lucknow Circle / Provincial Division Road Schedule` (UP PWD Charter `SRC-007`)
- `LESA Urban Distribution Division Directory` (MVVNL Portal `SRC-008`)
- `AMRUT & Capital Works Project Portfolio` (UP Jal Nigam Urban `SRC-009`)
- `Item 10 (Chief Engineer Electrical/Mechanical)` (LMC Doorbhas Suchi `SRC-002`)
- `Item 28 to 34 (Executive Engineers Civil Zones 1-8)` (LMC Doorbhas Suchi `SRC-002`)
- `SLNP Municipal LED Concession Framework` (EESL Records `SRC-013`)

---

## 4. Ambiguous Authority Evaluation Test (Acceptance Case)

To demonstrate why infrastructure type and failure mode determine authority routing rather than generic assumptions, the following standardized evaluation scenario is established:

```
========================================================================================
AMBIGUOUS JURISDICTION ACCEPTANCE TEST: STREETLIGHTING VS POWER INFRASTRUCTURE
========================================================================================
Location: Victoria Street, Chowk Ward (WARD-106, ZONE-06)
Shared Physical Asset Node: Roadside Utility Infrastructure

SCENARIO A: Luminaire / Light Fixture Breakdown (Dark Street)
  1. Citizen Grievance : "Streetlights are completely dark at night on Victoria Street"
  2. Issue Category    : STREETLIGHT_FAILURE
  3. Failure Mode      : Defective LED luminaire / broken bulb / optical diffuser fault
  4. Physical Asset    : AST-STL-005 (Chowk Chauraha Historical Roundabout High-Mast Luminaire)
  5. Asset Type        : STREETLIGHT (geometry_type: POINT, location_status: APPROXIMATE)
  6. Custodial Dept    : DEPT-LMC-ELEC (Electrical & Mechanical Department, LMC)
  7. Service Routed    : SRV-LMC-STREETLIGHT-REPAIR (Streetlight Luminaire & Fixture Repair)
  8. Authority Routed  : AUTH-LMC (Lucknow Municipal Corporation)
  9. Source Citation   : SRC-002 (Doorbhas Suchi Item 10) & SRC-013 (EESL Concession)
 10. Evidentiary Status: PARTIALLY_VERIFIED (Responsibility: VERIFIED, Location: APPROXIMATE)

SCENARIO B: Leaning Utility Pole / Snapped High-Tension Conductor
  1. Citizen Grievance : "Utility pole leaning dangerously with snapped live electric wire"
  2. Issue Category    : ELECTRICAL_INFRASTRUCTURE
  3. Failure Mode      : Structural pole failure / distribution transformer trip / snapped 11kV line
  4. Physical Asset    : AST-ELE-005 (Chowk Victoria Street Overhead Feeder & Utility Pole)
  5. Asset Type        : ELECTRICAL_INFRASTRUCTURE (geometry_type: APPROXIMATE_POINT)
  6. Custodial Dept    : DEPT-MVVNL-LESA (Lucknow Electricity Supply Administration)
  7. Service Routed    : SRV-MVVNL-LINE-MAINTENANCE (Overhead Line & Pole Maintenance)
  8. Authority Routed  : AUTH-MVVNL (Madhyanchal Vidyut Vitran Nigam Limited)
  9. Source Citation   : SRC-008 (MVVNL Mandate & Safety Manual) & CONF-003
 10. Evidentiary Status: PARTIALLY_VERIFIED (Responsibility: VERIFIED, Location: APPROXIMATE)
========================================================================================
```

**Resolution Rationale (`CONF-003`)**:  
Even though a municipal streetlighting fixture is mounted directly upon a utility pole, the civic grievance routing engine separates the **luminaire appliance** (governed by LMC / EESL under `SRC-013`) from the **structural power distribution pole** (governed by MVVNL / LESA under `SRC-008`). Routing is deterministically bound to failure mode and asset classification.

---

## 5. Current Point-Based Limitations vs. Future Phase 3B Architecture

### Current Phase 3A Baseline:
- **Discreet Point Coordinates**: Linear infrastructure (roads, drains, pipelines, sewers, and overhead lines) is indexed via representative junction or facility points (`APPROXIMATE_POINT`).
- **No Fictitious Centerlines**: CivicTrace strictly avoids drawing arbitrary polylines without authoritative CAD/GIS survey vectors.

### Future Phase 3B+ Roadmap:
- **LineString Vector Support**: Integrating official GIS vector centerlines for road corridors and trunk pipelines as official departmental GIS layers are published.
- **Buffer-Based Spatial Snapping**: Implementing automated 15-meter spatial buffers around road vectors to allow citizen GPS incident reports to snap cleanly to confirmed corridors.
- **Multi-Polygon Facility Enclosures**: Mapping detailed cadastral property boundaries for major installations (e.g. Aishbagh Water Works compound, Bharwara STP plant perimeter).

---

## 6. Validation Results & Quality Metrics

Validation was executed via `scripts/validate_assets.py`.

### Summary of Audit Output:
- **Total Assets Evaluated:** 39
- **Validation Status:** **PASSED (0 Errors)**
- **Documented Warnings:** **4 Warnings** (transparently surfacing DataMeet pre-2022 spatial baseline extents for trans-Gomti wards, preserving legitimate uncertainty per Rule 8 & 9).
- **Machine-Readable Report:** `data/lucknow/assets/asset_validation_report.json`

### Detailed Metric Breakdown:

| Metric Group | Metric | Value | Compliance Note |
| :--- | :--- | :---: | :--- |
| **Dataset Size** | Total Assets | 39 | Coverage benchmark met (30–50) |
| **Geometry Types** | `APPROXIMATE_POINT` | 34 | Linear infrastructure corridors |
| | `POINT` | 5 | Standalone physical facilities |
| | `LINESTRING` / `POLYGON` | 0 | Zero fabricated vectors |
| **Location Basis** | `MAP_DERIVED` | 31 | Verified against named landmark |
| | `MANUALLY_ESTIMATED` | 8 | Interior representative estimation |
| | `OFFICIAL_COORDINATE` | 0 | Zero false official coordinate claims |
| **Source References**| Granular Citation Available | 39 (100.0%) | Section, chapter, or directory item cited |
| | Unexposed Citation | 0 (0.0%) | Traceability complete |
| **Responsibility Mandates** | `MAINTENANCE` | 29 | Routine upkeep / patching / desilting |
| | `OPERATION` | 5 | Pumping stations / water boosting |
| | `OWNERSHIP` | 3 | Dedicated utility installations |
| | `SERVICE_RESPONSIBILITY`| 2 | Capital project execution |
| **Status Decoupling** | `responsibility_status` | VERIFIED: 20, INFERRED: 19 | Separated from location |
| | `location_status` | APPROXIMATE: 39 | Zero false location claims |
| | `ownership_status` | UNKNOWN: 3, INFERRED: 29, VERIFIED: 7 | Zero false title deed claims |
| **Authorities Represented** | LMC (`AUTH-LMC`) | 19 | Municipal streets, drains, lighting |
| | Jal Sansthan (`AUTH-LKO-JALSANSTHAN`) | 9 | Drinking water & sewerage O&M |
| | MVVNL / LESA (`AUTH-MVVNL`) | 5 | Power distribution & poles |
| | UP PWD (`AUTH-UPPWD`) | 3 | Arterial highways & MDRs |
| | UP Jal Nigam (`AUTH-UPJN-URBAN`) | 2 | Capital water/sewer works |
| | LDA (`AUTH-LDA`) | 1 | Un-transferred housing layout |
| **Zonal Coverage** | Zones Represented | 8 of 8 | Zones 1 through 8 covered |
| **Coordinate Collisions** | Exact Duplicates | 0 | Zero coordinate collisions |
| | Near-Duplicates (< 5m) | 0 | Clean physical spacing |

---

## 7. Regression Test Verification

All three validation suites pass cleanly:
1. `python scripts/validate_lexicon.py` $\rightarrow$ **PASS (0 Errors, 28 verified records, 6 authorities)**
2. `python scripts/validate_gis.py` $\rightarrow$ **PASS (0 Errors, 110 wards, 8 zones, 100% Shapely validity)**
3. `python scripts/validate_assets.py` $\rightarrow$ **PASS (0 Errors, 39 assets, 4 transparent warnings, 100% provenance)**
