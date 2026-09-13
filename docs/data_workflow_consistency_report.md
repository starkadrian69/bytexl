# CivicTrace — Data & Workflow Consistency Audit Report

**Audit Target:** Phase 1–3D Data Foundation & Final Nigam Workflow Integration  
**Date:** September 2026  
**Final Status:** **`READY WITH DOCUMENTED LIMITATIONS`**  
**Document ID:** `DOC-CT-CONSISTENCY-REPORT-001`  

---

## 1. Final Workflow Inspected

The source of truth for the CivicTrace backend architecture and workflow is Nigam's finalized codebase (`apps/api/`) and associated architectural contracts (`docs/*-contract.md`, `docs/architecture.md`, `docs/decisions.md`).

Key architectural artifacts inspected:
- **Modular Monolith Gateway & Service Architecture**: [`docs/architecture.md`](file:///d:/CIVICTRACE/docs/architecture.md)
- **AI Perception Sensor Boundary**: [`docs/ai-contract.md`](file:///d:/CIVICTRACE/docs/ai-contract.md)
- **Deterministic GIS Containment**: [`docs/gis-contract.md`](file:///d:/CIVICTRACE/docs/gis-contract.md)
- **Algorithmic Incident Fusion**: [`docs/fusion-contract.md`](file:///d:/CIVICTRACE/docs/fusion-contract.md)
- **Holistic Priority Engine**: [`docs/priority-contract.md`](file:///d:/CIVICTRACE/docs/priority-contract.md)
- **Accountability & SLA Engine**: [`docs/sla-contract.md`](file:///d:/CIVICTRACE/docs/sla-contract.md)
- **Resolution Verification Engine**: [`docs/verification-contract.md`](file:///d:/CIVICTRACE/docs/verification-contract.md)
- **Controlled Domain Enums**: [`apps/api/app/models/enums.py`](file:///d:/CIVICTRACE/apps/api/app/models/enums.py)
- **End-to-End Pipeline Integration Tests**: [`apps/api/tests/test_e2e_pipeline.py`](file:///d:/CIVICTRACE/apps/api/tests/test_e2e_pipeline.py)

---

## 2. Data-to-Workflow Mapping

CivicTrace enforces an unbroken 10-hop conceptual chain from citizen report to resolution:

```
CITIZEN REPORT
    ↓
ISSUE (Controlled Taxonomy: 18 Categories in Data, 13 Enums in API)
    ↓
LOCATION / GPS (WGS-84 Point)
    ↓
WARD (110 Administrative Wards; 105 Spatial Polygons)
    ↓
ZONE (8 Administrative Zones)
    ↓
ASSET (39 Physical Assets across 6 Classes)
    ↓
AUTHORITY (6 Statutory Civic Bodies: LMC, PWD, LJS, MVVNL, UPJN, LDA)
    ↓
DEPARTMENT / RESPONSIBILITY (Ownership vs. Maintenance vs. Operation vs. Service)
    ↓
SERVICE (Zonal / Subdivisional Service Mandate)
    ↓
PRIORITY (CRITICAL / HIGH / MEDIUM / LOW via Severity + Safety + Persistence)
    ↓
SLA (21 Pilot Rules; Linear Progression: PENDING → DUE → OVERDUE → ESCALATION_ELIGIBLE)
    ↓
AUTHORITY WORKFLOW (Field Inspection / Jetting / Overlay)
    ↓
RESOLUTION EVIDENCE (BEFORE condition, AFTER photo, Field Report)
    ↓
EVIDENCE VERIFICATION (FULLY_RESOLVED / PARTIALLY_RESOLVED / NOT_RESOLVED / INSUFFICIENT_EVIDENCE / HUMAN_REVIEW)
    ↓
ADMINISTRATIVE CLOSURE (Statutory Closure by Custodial Officer)
    ↓
ACCOUNTABILITY / ESCALATION (L1 / L2 / L3 Escalation Trigger)
```

---

## 3. Changes Made

1. **Portable Repository-Relative Paths**:
   - Eliminated hardcoded `d:/CIVICTRACE` across all validation scripts (`scripts/validate_*.py`, `scripts/build_*.py`). Updated them to resolve root dynamically via `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`.
   - Updated machine-readable JSON reports in `data/lucknow/*/*_validation_report.json` to store clean, repository-relative `dataset_path` strings (`data/lucknow/...`).
2. **Spatial Semantics & `EXACT_OR_VERIFIED` Clarification**:
   - Audited every usage of `EXACT_OR_VERIFIED` in [`data/lucknow/incidents/README.md`](file:///d:/CIVICTRACE/data/lucknow/incidents/README.md) and [`docs/phase3b_seed_incidents.md`](file:///d:/CIVICTRACE/docs/phase3b_seed_incidents.md).
   - Embedded the required canonical disclaimer: *"EXACT_OR_VERIFIED does not mean official government verification or legal confirmation of the incident coordinates. It means that the supplied coordinates are consistent with the available CivicTrace reference data within the configured validation tolerance."*
3. **Phase 4 Data & Integration Contract**:
   - Created [`docs/phase4_data_contract.md`](file:///d:/CIVICTRACE/docs/phase4_data_contract.md) defining input data schemas, expected runtime outputs, strict truth vs. prediction separation (`cluster_id` vs `predicted_cluster_id`), uncertainty handling, and enum normalization.
4. **Golden Demo Cases Specification Polish**:
   - Updated [`docs/golden_demo_cases.md`](file:///d:/CIVICTRACE/docs/golden_demo_cases.md) to explicitly expose all 18 required attributes for all 10 Golden Demo Cases using canonical IDs (`CT-INC-*`, `CT-DUP-*`, `AST-*`, `AUTH-*`, `CHAIN-*`).
   - Clearly demarcated expected benchmark behavior from actual prototype output.
5. **README Documentation & Scope Distinction**:
   - Updated [`README.md`](file:///d:/CIVICTRACE/README.md) with data foundation architecture, freeze notice, synthetic vs. real warning, hackathon demo scope vs. full foundation scope, and validator execution instructions.
6. **Data Foundation Tooling Integration**:
   - Staged and validated all 7 data foundation validators in `scripts/`.

---

## 4. Changes Intentionally NOT Made

1. **No Dataset Expansion or Deletion**: The dataset remains strictly frozen at 39 assets, 20 incidents, 13 evidence records, 26 duplicate cases, 110 wards, 8 zones, and 21 SLA rules.
2. **No Fabrication of Missing Wards**: The 5 wards lacking public GIS vectors (`WARD-001`, `WARD-007`, `WARD-009`, `WARD-012`, `WARD-014`) remain explicitly documented as `NOT_AVAILABLE`.
3. **No Overwriting of Difficult Edge Cases**:
   - `CT-INC-003` retains incomplete location with `NEEDS_REVIEW`.
   - `CT-INC-010` retains text vs. GPS spatial conflict.
   - `CT-INC-014` retains contradictory authority closure vs. citizen photo.
   - `CT-INC-019` retains streetlight vs. transformer arcing edge case.
   - `CT-INC-020` retains LDA vs. LMC transitional boundary ambiguity.
4. **No Renaming of Historical Enums**: Existing dataset values (`NOT_RESOLVED`, uppercase `POTHOLE`, `DUPLICATE`) were preserved; a bidirectional mapping adapter was defined in the integration contract rather than corrupting historical ground truth.
5. **No Modifications to Nigam's Application Files**: `apps/api/` and related docker/configuration files were untouched.
6. **No Implementation of Phase 4 Logic**: No AI models, computer vision, vector databases, or production dispatchers were implemented.

---

## 5. Phase 1 — Authority Foundation Validation

- **Script**: `python scripts/validate_lexicon.py`
- **Result**: **PASS (0 Errors, 0 Warnings)**
- **Coverage**: 6 statutory civic authorities, 28 services, 4 documented inter-agency conflicts (`CONF-001` through `CONF-004`).
- **Controlled Vocabulary**: 18 controlled issue categories.
- **Routing Invariant**: Preserves `ISSUE + LOCATION + JURISDICTION + ASSET + RULE → AUTHORITY`. Disallows universal "POTHOLE → PWD".
- **Separation of Responsibilities**: Maintenance $\neq$ Operation $\neq$ Ownership $\neq$ Service Responsibility.

---

## 6. Phase 2 — GIS / Jurisdiction Validation

- **Script**: `python scripts/validate_gis.py`
- **Result**: **PASS (0 Errors, 0 Warnings)**
- **Coverage**: 110 administrative wards across 8 zones.
- **Geometries**: 105 legacy ward polygons, 8 synthesized zone polygons (`DERIVED_CIVICTRACE_GEOMETRY`).
- **Missing Geometries**: Exactly 5 wards (`WARD-001`, `007`, `009`, `012`, `014`) documented as `NOT_AVAILABLE`.
- **CRS Compliance**: 100% WGS-84 (`EPSG:4326`), 100% Shapely 2D topological validity.

---

## 7. Phase 3A — Asset Foundation Validation

- **Script**: `python scripts/validate_assets.py`
- **Result**: **PASS (0 Errors, 4 Documented Legacy Warnings)**
- **Asset Count**: Exactly 39 assets (11 Roads, 7 Drains, 6 Water Pipelines, 5 Sewers, 5 Streetlights, 5 Electrical Poles).
- **Coordinate Status**: 100% `APPROXIMATE` / source-traceable reference locations.
- **Documented Warnings**: 4 transparent legacy polygon containment warnings for `AST-ROAD-006` and `AST-DRN-004` (located in post-2022 developing sectors outside pre-2022 open GIS envelopes).

---

## 8. Phase 3B — Incident Foundation Validation

- **Script**: `python scripts/validate_incidents.py`
- **Result**: **PASS (0 Errors, 8 Intentional Test Warnings)**
- **Incident Count**: Exactly 20 records (`CT-INC-001` through `CT-INC-020`).
- **Grounding Breakdown**: 2 `REAL_DOCUMENTED`, 18 `SYNTHETIC_EVALUATION`.
- **Linguistic Distribution**: 8 English, 6 Hindi, 4 Hinglish, 2 Mixed.
- **Documented Warnings**: 8 intentional test warnings preserving edge cases (3 unlinked diffuse solid waste, 1 incomplete location `CT-INC-003`, 1 spatial conflict `CT-INC-010`, 1 jurisdictional transition `CT-INC-020`).

---

## 9. Phase 3C — Evidence Foundation Validation

- **Script**: `python scripts/validate_evidence.py`
- **Result**: **PASS (0 Errors, 7 Intentional Test Warnings)**
- **Evidence Count**: Exactly 13 evidence records across 8 chains.
- **Chains**: 4 complete before/after pairs, 4 intentional single-stage / incomplete chains.
- **Curated Ground Truth**: 4 `FULLY_RESOLVED`, 2 `PARTIALLY_RESOLVED`, 4 `NOT_RESOLVED`, 3 `INSUFFICIENT_EVIDENCE`.
- **Documented Warnings**: 7 intentional test warnings (1 spatial discordance `CT-EVD-007`, 1 unusable image `CT-EVD-011`, 1 contradictory closure `CHAIN-006` / `CT-INC-014`, 4 incomplete chains).

---

## 10. Phase 3D — Duplicate Benchmark Validation

- **Script**: `python scripts/validate_duplicates.py`
- **Result**: **PASS (0 Errors, 0 Warnings)**
- **Benchmark Count**: Exactly 26 synthetic evaluation cases across 7 candidate clusters (`CLUSTER-001` to `CLUSTER-007`).
- **Label Balance**: 9 `DUPLICATE`, 5 `LIKELY_DUPLICATE`, 5 `POSSIBLE_DUPLICATE`, 7 `UNRELATED` (hard negative controls in `CLUSTER-007`).
- **Integrity**: `cluster_id` and `curation_confidence` preserved strictly as human-curated benchmark ground truth.

---

## 11. SLA Configuration Validation

- **Script**: `python scripts/validate_sla.py`
- **Result**: **PASS (0 Errors, 0 Warnings)**
- **Rule Count**: Exactly 21 CivicTrace pilot rules covering all 18 Phase 1 categories across 6 authorities.
- **Rule Type**: 100% `CIVICTRACE_PILOT_RULE`. Zero invented statutory government SLAs.
- **Lifecycle Alignment**: SLA contract models continuous lifecycle monitoring (`PENDING → DUE → OVERDUE → ESCALATION_ELIGIBLE`).

---

## 12. Golden Demo Validation

- **Document**: [`docs/golden_demo_cases.md`](file:///d:/CIVICTRACE/docs/golden_demo_cases.md)
- **Status**: **100% Compliant**
- **Cases**: All 10 required Golden Demo Cases are fully specified with real repository IDs:
  1. Simple pothole → GIS/asset correct authority (`GD-CASE-01` / `CT-INC-002`)
  2. Hindi/multilingual intake (`GD-CASE-01`, `GD-CASE-02`, `GD-CASE-10`)
  3. Multilingual duplicate cluster (`GD-CASE-02` / `CLUSTER-001`)
  4. Non-duplicate negative controls (`GD-CASE-03` / `CLUSTER-007`)
  5. Text vs. GPS spatial conflict (`GD-CASE-04` / `CT-INC-010`)
  6. Contradictory resolution evidence (`GD-CASE-05` / `CT-INC-014`)
  7. Partial resolution audit (`GD-CASE-06` / `CT-INC-004`)
  8. Insufficient / unusable evidence gate (`GD-CASE-07` / `CT-INC-016`)
  9. Streetlight vs. electrical distribution hazard (`GD-CASE-08` / `CT-INC-019`)
  10. High-impact repeat grievance escalation (`GD-CASE-10` / `CT-INC-012`)

---

## 13. Cross-Phase Foreign Key & Referential Integrity

All cross-phase relationships were checked and verified:
- **Incident → Asset**: 16 valid linkages to `asset_ownership.csv`, 3 intentionally `UNKNOWN` (`UNLINKED_BUT_VALID` solid waste), 1 intentionally `UNKNOWN` (`CT-INC-003` incomplete location).
- **Incident → Ward / Zone**: 19 valid linkages to `jurisdiction_registry.csv`, 1 intentionally `UNKNOWN` (`CT-INC-003`).
- **Incident → Authority**: 18 valid linkages to `lucknow_authority_master.json`, 2 intentionally `NEEDS_REVIEW` (`CT-INC-003` and `CT-INC-020`).
- **Evidence → Incident**: 100% of 13 records reference valid `CT-INC-*` records.
- **Duplicate → Incident / Reference Record**: 100% of 26 records reference valid incident or benchmark record IDs.
- **All Datasets → Sources**: 100% of referenced `source_id` keys exist in `data/sources/source_registry.csv` or `data/gis/gis_source_registry.csv`.

---

## 14. Provenance Validation

- **Registered Sources**: 13 general civic sources in `data/sources/source_registry.csv` + 6 spatial sources in `data/gis/gis_source_registry.csv` (19 total).
- **Traceability**: 100% of records across Phases 1, 2, 3A, 3B, 3C, 3D, and SLA rules cite granular source IDs and specific document sections.
- **Zero Fake Citations**: No invented URLs, no fabricated gazettes, and no fake complaint tracking numbers.

---

## 15. Privacy & Security Scan

A comprehensive security scan was executed across the repository:
- **Credentials & API Keys**: Scanned for private API keys, tokens, service account credentials, and passwords. `.env.example` contains only empty placeholders (`GEMINI_API_KEY=""`); `.env.test` contains documented dummy test secrets (`test-secret-key-do-not-use-in-production`).
- **Personal Identifiable Information (PII)**: 0 citizen phone numbers, 0 private citizen names, 0 personal residential addresses in evaluation datasets. All listed contact numbers are public institutional nodal officer landlines or published helpline numbers.
- **Media / EXIF**: Synthetic URIs (`synthetic://...`) are used for synthetic evaluation cases; no private citizen photographs or unvetted EXIF records exist in the repository.

---

## 16. Synthetic Data Limitations

> [!WARNING]
> The CivicTrace dataset contains synthetic evaluation records created specifically for testing and benchmarking the intelligence pipeline during the hackathon.
> 
> - **Synthetic Incidents (`CT-INC-002` through `007`, `009` through `020`)**: Realistic problem statements constructed to test multilingual processing and edge-case routing. They do not represent actual grievances logged by citizens.
> - **Synthetic Duplicates (`CT-DUP-001` through `026`)**: Crafted to benchmark deduplication precision, recall, and cross-lingual similarity. They do not represent real duplicate submission volume.
> - **Synthetic Evidence (`CT-EVD-002` through `007`, `009` through `011`, `013`)**: Structured to test computer vision before/after comparison and contradiction handling.

---

## 17. GIS & Asset Coordinate Uncertainty

> [!NOTE]
> - **Asset Coordinates**: The latitude and longitude values in `data/lucknow/assets/asset_ownership.csv` are **approximate reference locations** derived from open street alignments and public facility addresses (`APPROXIMATE`). They are not legally surveyed cadastral boundaries.
> - **Legacy GIS Ward Boundaries**: The 105 ward polygons in `data/gis/lucknow_wards.geojson` represent secondary legacy open-source vectors (DataMeet pre-2022). They reflect municipal core alignments but do not capture peripheral revenue village expansions from the 2022 Delimitation.
> - **Missing Wards**: Wards 1, 7, 9, 12, and 14 have no published open-source GIS vectors and are explicitly recorded with `geometry_status = NOT_AVAILABLE`.

---

## 18. Phase 4 Integration Contract Summary

The contract [`docs/phase4_data_contract.md`](file:///d:/CIVICTRACE/docs/phase4_data_contract.md) governs Phase 4 integration:
- **Separation of Concerns**: AI handles perception/extraction; PostGIS and rules handle routing, priority, and SLA; humans handle unresolved ambiguity and final closure.
- **Strict Immutability**: Benchmark ground truth is read-only. Runtime predictions are stored in separate application fields (`predicted_*`, `runtime_*`).
- **Explicit Uncertainty**: Systems must output `UNKNOWN`, `NEEDS_REVIEW`, `CONFLICT`, or `INVALID_LOCATION` when data is missing or discordant.
- **Canonical Mapping**: Normalizes uppercase ground-truth strings (`POTHOLE`, `NOT_RESOLVED`) to application enums (`pothole`, `unresolved`).

---

## 19. Nigam Application File Protection Check

Verification via `git status` and `git diff` confirms that zero application, backend, or frontend files created by Nigam were modified:
- `apps/api/` : **UNTOUCHED (0 changes)**
- `docker-compose.yml` : **UNTOUCHED (0 changes)**
- `.env.example` : **UNTOUCHED (0 changes)**
- `docs/architecture.md`, `docs/*-contract.md` : **UNTOUCHED (0 changes)**

---

## 20. Final Readiness Status

### **`READY WITH DOCUMENTED LIMITATIONS`**

The CivicTrace Phase 1–3D Data Foundation is internally consistent, fully validated, and aligned with Nigam's finalized Phase 4 integration workflow. All seven validators pass with zero errors. All limitations regarding synthetic data, approximate coordinates, legacy boundaries, and pilot SLAs are rigorously documented.
