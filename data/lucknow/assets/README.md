# Lucknow Civic Asset Ownership Data Foundation (`data/lucknow/assets/`)

**Phase:** Phase 3A — Final Refinement Pass  
**Project:** CivicTrace — Evidence-First Civic Grievance Intelligence Platform  
**Spatial Baseline:** Lucknow GIS Jurisdiction Reference Layer (`LKO-JUR-2023-01`)  
**Authority Master:** Lucknow Authority Reference Master (`data/authority/lucknow_authority_master.json`)  
**Integrity Standard:** 14 Critical Data Integrity Rules  
**Date:** September 2026  
**Status:** Defensible Representative Data Foundation (39 Infrastructure Assets)

---

## 1. Purpose & Architectural Context

The purpose of the Lucknow Asset Ownership Data Foundation is to bridge the fundamental civic routing chain:

$$\text{Issue / Complaint} \longrightarrow \text{GPS Location} \longrightarrow \text{Ward} \longrightarrow \text{Zone} \longrightarrow \textbf{Asset} \longrightarrow \textbf{Responsible Authority / Dept}$$

In municipal civic operations, citizen complaints do not refer to abstract jurisdictions; they attach to physical infrastructure located in space. 

> [!NOTE]
> **Asset Terminology & Evidentiary Scope**:
> Asset records correspond to identified physical infrastructure entities or infrastructure classes supported by cited sources; exact asset-level identity and location remain subject to the recorded verification status. CivicTrace strictly decouples the existence of infrastructure, its approximate representation, exact asset-level identity, legal ownership, operational responsibility, and maintenance responsibility.

---

## 2. Granular Provenance Chain

To ensure 100% evidentiary defensibility without fabricating claims, CivicTrace implements a four-tier provenance chain:

$$\textbf{Asset Record} \longrightarrow \textbf{Source ID} \longrightarrow \textbf{Source Reference} \longrightarrow \textbf{Specific Evidence Cited}$$

- `source_id`: References the official document or gazette registered in `source_registry.csv` or `gis_source_registry.csv`.
- `source_reference`: References the specific section, chapter, schedule, or directory item within that source (e.g. `Chapter 12 (Streets and Public Roads)`, `Section 18 & Section 24`, `Item 10 (Chief Engineer Electrical/Mechanical)`, `Lucknow Circle / Provincial Division Road Schedule`). If an official document does not expose a granular sub-section, it is explicitly set to `NOT_AVAILABLE`.

---

## 3. Asset Schema (21 Columns)

The dataset `asset_ownership.csv` implements the refined 21-attribute schema:

| Column | Data Type | Description & Controlled Vocabulary |
| :--- | :--- | :--- |
| `asset_id` | String | Unique CivicTrace asset identifier (`AST-ROAD-###`, `AST-DRN-###`, `AST-WTR-###`, `AST-SWR-###`, `AST-STL-###`, `AST-ELE-###`). |
| `asset_type` | Enum | Controlled physical asset class: `ROAD`, `DRAIN`, `WATER_PIPELINE`, `SEWER`, `STREETLIGHT`, `ELECTRICAL_INFRASTRUCTURE`. |
| `asset_name` | String | Plaintext description without invented serial tags or unevidenced specifications. |
| `geometry_type` | Enum | Controlled geometry type: `POINT`, `LINESTRING`, `POLYGON`, `APPROXIMATE_POINT`, `UNKNOWN`. |
| `latitude` | Float (WGS 84) | Decimal latitude within coordinate sanity envelope (`[26.60, 27.15]`). |
| `longitude` | Float (WGS 84) | Decimal longitude within coordinate sanity envelope (`[80.70, 81.25]`). |
| `location_status` | Enum | Spatial precision standing: `VERIFIED`, `APPROXIMATE`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `location_basis` | Enum | Methodological basis of coordinate: `OFFICIAL_COORDINATE`, `SOURCE_DERIVED`, `MAP_DERIVED`, `MANUALLY_ESTIMATED`, `UNKNOWN`. |
| `ward_id` | String | Foreign key to `data/gis/jurisdiction_registry.csv` (`WARD-001` to `WARD-110`). |
| `zone_id` | String | Foreign key to `data/gis/jurisdiction_registry.csv` (`ZONE-01` to `ZONE-08`). |
| `authority_id` | String | Foreign key to `data/authority/lucknow_authority_master.json`. |
| `department` | String | Custodial department / division from Phase 1 master. |
| `service` | String | Relevant civic service from Phase 1 master. |
| `responsibility_type` | Enum | Nature of administrative mandate: `OWNERSHIP`, `OPERATION`, `MAINTENANCE`, `SERVICE_RESPONSIBILITY`, `UNKNOWN`. |
| `responsibility_status`| Enum | Evidentiary standing of authority mandate: `VERIFIED`, `INFERRED`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `ownership_status` | Enum | Legal property vesting standing: `VERIFIED`, `INFERRED`, `UNKNOWN`. |
| `source_id` | String | Authoritative provenance pointer from registered sources. |
| `source_reference` | String | Specific section, chapter, schedule, or item supporting the claim. |
| `verification_status` | Enum | Composite standing: `VERIFIED`, `PARTIALLY_VERIFIED`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `confidence` | Enum | Assessment confidence: `HIGH`, `MEDIUM`, `LOW`. |
| `notes` | String | Detailed explanation of statutory basis, operational delegation, and spatial uncertainty. |

---

## 4. Controlled Definitions

### `location_basis`
- `OFFICIAL_COORDINATE`: Coordinate published in an official government gazette, map, or GIS register. (None in current dataset; zero false claims).
- `SOURCE_DERIVED`: Extracted directly from textual location descriptions or survey tables in cited official source.
- `MAP_DERIVED`: Derived by referencing the named landmark/corridor on open spatial baselines (DataMeet/OSM/satellite) corresponding to the cited official locality.
- `MANUALLY_ESTIMATED`: Centroid or representative interior estimation within the verified ward/sector.
- `UNKNOWN`: Insufficient evidence to establish the derivation basis.

### `geometry_type`
- `APPROXIMATE_POINT`: A point coordinate representing an approximate location along a linear infrastructure asset (road, drain, pipeline, sewer conduit, overhead circuit).
- `POINT`: A point coordinate representing a standalone physical facility node (e.g. substation compound, plinth transformer installation, high-mast lighting tower).
- `LINESTRING`: Continuous polyline vector (reserved for future Phase 3B expansion).
- `POLYGON`: Enclosed polygon boundary (reserved for future Phase 3B facility footprint expansion).
- `UNKNOWN`: Unspecified geometry.

---

## 5. Ambiguous Authority Evaluation Scenario

To evaluate how CivicTrace resolves jurisdictional ambiguity between overlapping utilities, the platform defines the following standard acceptance case:

```
[SCENARIO]: Dark Street / Utility Failure at Victoria Street, Chowk (Ward 106, Zone 6)

CASE A: Non-Glowing Streetlight Fixture
  Issue Description : Streetlight luminaire not glowing on Victoria Street
  Issue Category    : STREETLIGHT_FAILURE
  Asset Evaluated   : AST-STL-005 (Chowk Chauraha Roundabout High-Mast Luminaire)
  Asset Type        : STREETLIGHT
  Custodial Dept    : DEPT-LMC-ELEC (Electrical & Mechanical Department, LMC)
  Service Routed    : SRV-LMC-STREETLIGHT-REPAIR (Streetlight Luminaire & Fixture Repair)
  Authority Routed  : AUTH-LMC (Lucknow Municipal Corporation)
  Source Evidence   : SRC-002 (Doorbhas Suchi Item 10) & SRC-013 (EESL Concession)
  Status            : PARTIALLY_VERIFIED (Confidence: HIGH)

CASE B: Leaning Utility Pole / Snapped Overhead Conductor
  Issue Description : Utility pole leaning dangerously and snapped power conductor on Victoria Street
  Issue Category    : ELECTRICAL_INFRASTRUCTURE
  Asset Evaluated   : AST-ELE-005 (Chowk Victoria Street Overhead Feeder & Utility Pole)
  Asset Type        : ELECTRICAL_INFRASTRUCTURE
  Custodial Dept    : DEPT-MVVNL-LESA (Lucknow Electricity Supply Administration)
  Service Routed    : SRV-MVVNL-LINE-MAINTENANCE (Overhead Line & Pole Maintenance)
  Authority Routed  : AUTH-MVVNL (Madhyanchal Vidyut Vitran Nigam Limited)
  Source Evidence   : SRC-008 (MVVNL Consumer Safety Mandate) & CONF-003
  Status            : PARTIALLY_VERIFIED (Confidence: HIGH)
```

**Resolution Principle (`CONF-003`)**: Even if a municipal luminaire is physically mounted on a utility pole, fixture failure routes to **LMC**, while structural pole damage or upstream electrical power failure routes to **MVVNL/LESA**.

---

## 6. Current Limitations & Roadmap

### Current Phase 3A:
- **Point-Based Representation**: All linear infrastructure assets are represented as `APPROXIMATE_POINT` coordinates marking key junction nodes or facility entrances.
- **Geographic Extent**: Derived from open pre-2022 spatial baselines (`SRC-GIS-001`); peri-urban wards lack vector polygons.

### Future Phase 3B+:
- **LineString Vector Support**: Digitizing centerline vectors for roads, pipelines, and drainage conduits.
- **Spatial Snapping Engine**: Automated 15-meter buffer snapping for citizen GPS reports.
- **Official Cadastral Integration**: Integrating official LMC CAD vector releases as they become publicly available.
