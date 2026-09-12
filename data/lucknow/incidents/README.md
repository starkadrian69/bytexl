# Lucknow Seed Incident Dataset (`data/lucknow/incidents/`)

**Phase:** Phase 3B — Lucknow Seed Incident Dataset  
**Project:** CivicTrace — Evidence-First Civic Grievance Intelligence Platform  
**Spatial Baseline:** Lucknow GIS Jurisdiction Reference Layer (`data/gis/jurisdiction_registry.csv`)  
**Authority Master:** Lucknow Authority Reference Master (`data/authority/lucknow_authority_master.json`)  
**Asset Baseline:** Lucknow Civic Asset Ownership Layer (`data/lucknow/assets/asset_ownership.csv`)  
**Integrity Standard:** CivicTrace Phase 3B Data Integrity Standard & Refinement Pass  
**Date:** September 2026  
**Status:** Frozen Representative Evaluation Dataset (20 Incidents)

---

## 1. Explicit Disclaimer & Scope Statement

> [!IMPORTANT]
> **Data Foundation & Scope Boundaries**:
> "This dataset is a representative evaluation/data-foundation layer, not a complete record of all civic complaints in Lucknow."  
> "Phase 2 jurisdiction data is the authoritative internal reference for CivicTrace ward and zone IDs." (CivicTrace does not claim its internal registry is a legal government cadastral boundary.)  
> Phase 3B strictly establishes the data foundation and evaluation ground truth. **Phase 3B does not implement AI, NLP, computer vision, duplicate detection, or the production routing engine.**

---

## 2. Purpose & Architectural Context

The objective of Phase 3B is to establish a small, defensible, Lucknow-specific incident dataset that exercises the existing CivicTrace reference layers across the entire traversal chain:

$$\text{CIVIC INCIDENT} \longrightarrow \text{ISSUE} \longrightarrow \text{GPS / LOCATION} \longrightarrow \text{WARD} \longrightarrow \text{ZONE} \longrightarrow \text{ASSET} \longrightarrow \text{AUTHORITY} \longrightarrow \text{DEPARTMENT} \longrightarrow \text{SERVICE} \longrightarrow \text{PROVENANCE}$$

In municipal civic workflows, citizen reports are often linguistically diverse, unstructured, and contain varying levels of spatial and administrative ambiguity. Phase 3B constructs a benchmark of 20 representative incidents that stress-test how these reports map to physical assets, administrative wards, and jurisdictional mandates without fabricating facts or forcing artificial certainty.

---

## 3. Real Documented vs. Synthetic Evaluation Records

CivicTrace strictly enforces anti-fabrication standards:
1. **Never Fabricate Official IDs**: All incidents bear CivicTrace internal identifiers (`CT-INC-001` through `CT-INC-020`). No records mimic real government complaint numbers.
2. **`REAL_DOCUMENTED` Records**: Used only where public official documentation or published civic schedules attest to the occurrence and location of civic distress (e.g., arterial road surface distress on Mahatma Gandhi Marg or trunk drain siltation along Kaiserbagh).
   > *Integrity Rule*: Every `REAL_DOCUMENTED` record must have source evidence supporting both the incident and its location. If this cannot be established, it is classified as `SYNTHETIC_EVALUATION`.
3. **`SYNTHETIC_EVALUATION` Records**: Realistic citizen complaints authored for benchmarking and evaluation purposes. Synthetic evaluation coordinates attach to known Phase 3A asset coordinates or realistic local corridors but are explicitly flagged as synthetic.

---

## 4. Incident Schema (22 Attributes)

The dataset `seed_incidents.csv` implements a structured 22-attribute schema:

| Column | Data Type | Description & Controlled Enums |
| :--- | :--- | :--- |
| `incident_id` | String | Unique CivicTrace internal ID (`CT-INC-###`). |
| `record_type` | Enum | Controlled classification: `REAL_DOCUMENTED`, `SYNTHETIC_EVALUATION`. |
| `created_at` | ISO 8601 | Reference timestamp for evaluation reproducibility. |
| `description` | String | Citizen-style complaint text reflecting natural phrasing. |
| `language` | Enum | Controlled linguistic tag: `ENGLISH`, `HINDI`, `HINGLISH`, `MIXED`. |
| `issue_category` | Enum | Controlled taxonomy from Phase 1 (`POTHOLE`, `ROAD_DAMAGE`, `GARBAGE_ACCUMULATION`, `ILLEGAL_DUMPING`, `OVERFLOWING_BIN`, `BLOCKED_DRAIN`, `WATERLOGGING`, `WATER_LEAKAGE`, `BROKEN_PIPELINE`, `SEWER_OVERFLOW`, `STREETLIGHT_FAILURE`, `ELECTRICAL_INFRASTRUCTURE`). |
| `issue_subcategory`| String | Granular issue subcategory aligned with municipal service catalogues. |
| `severity` | Enum | Controlled scale: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`, `UNKNOWN`. |
| `latitude` | Float (WGS 84) | Decimal latitude within Lucknow bounding envelope (`[26.60, 27.15]`), or empty if unlocated. |
| `longitude` | Float (WGS 84) | Decimal longitude within Lucknow bounding envelope (`[80.70, 81.25]`), or empty if unlocated. |
| `location_status` | Enum | Spatial confidence standing: `VERIFIED`, `APPROXIMATE`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `ward_id` | String | Foreign key to `jurisdiction_registry.csv` (`WARD-001` to `WARD-110`), or `UNKNOWN`. |
| `zone_id` | String | Foreign key to `jurisdiction_registry.csv` (`ZONE-01` to `ZONE-08`), or `UNKNOWN`. |
| `asset_id` | String | Foreign key to Phase 3A `asset_ownership.csv` (`AST-###`), or `UNKNOWN`. |
| `authority_id` | String | Foreign key to Phase 1 authority master (`AUTH-###`), or `NEEDS_REVIEW`. |
| `department` | String | Responsible department from Phase 1 master, or `UNKNOWN`. |
| `service` | String | Relevant municipal service from Phase 1 master, or `UNKNOWN`. |
| `responsibility_status`| Enum | Evidentiary standing: `VERIFIED`, `INFERRED`, `NEEDS_REVIEW`, `UNKNOWN`. |
| `confidence` | Enum | Routing confidence level: `HIGH`, `MEDIUM`, `LOW`. |
| `source_id` | String | Provenance pointer to registered sources (`SRC-001` to `SRC-013`). |
| `source_reference` | String | Granular citation within the source (chapter, section, schedule). |
| `notes` | String | Contextual rationale, uncertainty preservation, and test case documentation. |

---

## 5. Domain Taxonomy & Language Coverage

### 7 Civic Domains + 1 Cross-Domain Edge Category (20 Incidents)
1. **Roads / Pavement** (4 cases): Arterial highways (`CT-INC-001`), internal market lanes (`CT-INC-002`), unlocated potholes (`CT-INC-003`), composite multi-issue distress (`CT-INC-004`).
2. **Solid Waste Management** (3 cases): Roadside garbage mounds (`CT-INC-005`), vacant plot dumping (`CT-INC-006`), overflowing secondary bins (`CT-INC-007`).
3. **Drainage & Stormwater** (3 cases): Covered trunk drains (`CT-INC-008`), masonry stormwater nalas (`CT-INC-009`), commercial junction waterlogging with spatial discrepancy (`CT-INC-010`).
4. **Water Supply Reticulation** (3 cases): Commercial distribution line leaks (`CT-INC-011`), burst transmission trunk mains (`CT-INC-012`), residential sector leaks (`CT-INC-013`).
5. **Sewerage Network** (2 cases): Commercial trunk surcharge (`CT-INC-014`), heritage masonry sewer conduit blockages (`CT-INC-015`).
6. **Street Lighting** (2 cases): Residential LED luminaire failure (`CT-INC-016`), heritage high-mast junction outage (`CT-INC-017`).
7. **Electrical Infrastructure** (2 cases): Leaning utility distribution pole (`CT-INC-018`), sparking transformer structure with dark streetlight (`CT-INC-019`).
8. **Cross-Domain Jurisdictional Edge** (1 case): Transition development sector road collapse on LDA/LMC boundary (`CT-INC-020`).

### Linguistic Diversity
- **ENGLISH** (8 incidents): Formal and semi-formal reports across commercial and institutional areas.
- **HINDI** (6 incidents): Vernacular reports written in Devanagari script (`"सड़क पर बड़ा गड्ढा हो गया है..."`).
- **HINGLISH** (4 incidents): Romanized Hindi expressions commonly used by citizens in mobile grievance apps (`"Kuda dan overflow ho raha hai..."`).
- **MIXED** (2 incidents): Code-switched sentences combining English technical terms with Hindi syntax (`"Sector Q crossing par streetlight nahi chal rahi aur distribution transformer pole se sparking ho rahi hai"`).

---

## 6. Location & Spatial Uncertainty Methodology

### Dynamic Phase 2 Jurisdiction Source of Truth
Rather than relying on hard-coded ID ranges, Phase 3B ingests `data/gis/jurisdiction_registry.csv` dynamically. CivicTrace strictly decouples **administrative ward existence** from **spatial geometry availability**:
- Wards created under the 2022 municipal delimitation that lack pre-2022 legacy GIS boundary polygons (e.g. `WARD-001`, `WARD-007`, `WARD-009`, `WARD-012`, `WARD-014`) remain fully valid administrative entities.
- If an incident maps to a ward with `geometry_status = NOT_AVAILABLE`, CivicTrace validates the administrative ward-zone relationship without raising an integrity failure.

### Decoupled Incident-to-Asset Spatial Consistency
Phase 3A physical asset coordinates represent approximate reference points derived from open GIS layers and road schedules. Therefore, CivicTrace does not require mathematical coordinate equality between incidents and assets:
- **`EXACT_OR_VERIFIED`**: Incident coordinate within $\le 10\text{ m}$ of the asset reference point.
- **`APPROXIMATE_CONSISTENT`**: Incident coordinate within reasonable corridor proximity ($\le 500\text{ m}$) within the same ward.
- **`SPATIAL_REVIEW_REQUIRED`**: Greater spatial separation requiring intake verification.
- **`CONFLICT`**: Deliberate or identified spatial discrepancies (e.g., text cites Kapoorthala Aliganj in Zone 3 while GPS indicates Hazratganj in Zone 1).
- **`NOT_EVALUATED`**: Incidents without coordinates or without a static asset link.

Coordinates are never silently altered or forced into false precision.

---

## 7. Asset Linkage & Unlinked Solid Waste Rationale

CivicTrace links 16 of the 20 incidents (80%) to physical infrastructure assets in Phase 3A:
- **`LINKED_ASSET` (16 incidents)**: Roads, drains, water lines, sewers, streetlights, and electrical poles.
- **`UNLINKED_BUT_VALID` (3 incidents)**: `CT-INC-005`, `CT-INC-006`, and `CT-INC-007` concern diffuse/accumulated solid waste. Phase 3A models static physical infrastructure, not dynamic waste piles or moveable trash containers. These records are intentionally assigned `asset_id = UNKNOWN` with clear explanatory notes. They represent valid civic incidents and are classified as `UNLINKED_BUT_VALID` (warning/not evaluated), not integrity errors.
- **`ASSET_REVIEW_REQUIRED` (1 incident)**: `CT-INC-003` has an incomplete location and cannot be assigned an asset until citizen intake clarifies the location.
- **`INVALID_ASSET_REFERENCE` (0 incidents)**: No incidents reference non-existent asset IDs.

---

## 8. Authority Linkage & Preserving Jurisdictional Ambiguity

Incidents are mapped to responsible authorities (`AUTH-LMC`, `AUTH-UPPWD`, `AUTH-MVVNL`, `AUTH-LKO-JALSANSTHAN`) using the Phase 1 Authority Master.

> [!IMPORTANT]
> **Preserving Intake Ambiguity**:
> Asset-level authority information must not automatically overwrite incident-level `NEEDS_REVIEW` jurisdiction status. For example, in `CT-INC-020`, an asphalt cave-in occurs on a sector road in an LDA scheme adjacent to municipal boundaries. While the underlying road asset `AST-ROAD-006` carries maintenance history, the actual administrative jurisdiction between `AUTH-LDA` and `AUTH-LMC` is legally disputed (`CONF-004`). CivicTrace preserves `authority_id = NEEDS_REVIEW` and `responsibility_status = NEEDS_REVIEW` at the incident level.

---

## 9. Difficult Case Coverage (5 Stress-Test Cases)

The dataset incorporates 5 deliberate edge cases:
1. **Case A (Multi-Issue Complaint - `CT-INC-004`)**: Citizen reports both road destruction and post-rain waterlogging. Tests composite grievance routing where a single-issue schema cannot capture the secondary distress.
2. **Case B (Streetlight vs Electrical Distinction - `CT-INC-019`)**: Citizen reports a dark streetlight together with transformer sparking. Tests demarcation between LMC luminaire maintenance and MVVNL high-voltage power distribution per `CONF-003`.
3. **Case C (Incomplete Location - `CT-INC-003`)**: Citizen reports a pothole "near the market" with no GPS or ward. Evaluates intake validation rules requiring `location_status = NEEDS_REVIEW`.
4. **Case D (Spatial Discrepancy / Text vs GPS - `CT-INC-010`)**: Text explicitly mentions Kapoorthala Aliganj (Ward 109, Zone 3), but the submitted GPS points to Hazratganj (Ward 34, Zone 1) 1.3 km away. Evaluates conflict detection.
5. **Case E (Authority Ambiguity - `CT-INC-020`)**: Pavement collapse in an un-transferred LDA development sector where municipal handover is unevidenced (`CONF-004`). Preserves intake-level uncertainty.

---

## 10. Validation & Machine-Readable Report

The dataset is audited using `scripts/validate_incidents.py`, which produces `seed_incidents_validation_report.json`.

```bash
python scripts/validate_incidents.py
```

### Validation Summary:
- **Total Incidents Evaluated**: 20
- **Integrity Errors**: 0
- **Intentional Test Warnings**: 8 (3 unlinked solid waste, 1 incomplete location, 1 spatial text-GPS conflict, 2 authority ambiguity reviews, 1 unassigned asset)
- **Status**: PASSED

---

## 11. Known Limitations & Roadmap to Phase 3C/3D

- **Sample Size**: 20 incidents provide an evaluation foundation, not an operational city-wide grievance stream.
- **Dynamic Assets**: Moveable waste bins, temporary street vendor obstructions, and seasonal fogging routes are not modeled as static physical assets.
- **Next Steps**:
  - **Phase 3C**: Ground-truth evidence pairing, photographic evidence schemas, and duplicate incident clustering.
  - **Phase 3D / AI Phase**: AI-based NLP classification, image validation, and multi-agency routing engine.
