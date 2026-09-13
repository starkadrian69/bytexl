# CivicTrace Phase 4 Data & Integration Contract

**Specification Version:** 1.0.0  
**Status:** FROZEN REFERENCE & INTEGRATION SPECIFICATION  
**Target Consumer:** CivicTrace Phase 4 Application, Backend Pipelines, and AI Perception Services  
**Effective Date:** September 2026  

---

## 1. Architectural Boundary & Data Foundation Status

The CivicTrace Data Foundation (Phases 1 through 3D) provides the authoritative, frozen baseline for system evaluation, routing rules, spatial jurisdiction, and ground truth.

```
+---------------------------------------------------------------------------------------+
|                             CIVICTRACE DATA FOUNDATION                                |
|   Phase 1 (Authority)  -> Phase 2 (GIS) -> Phase 3A (Assets) -> Phase 3B (Incidents) |
|   -> Phase 3C (Evidence) -> Phase 3D (Duplicate Benchmark) -> SLA Configuration        |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                             PHASE 4 RUNTIME PIPELINE                                  |
|   Evidence Intake -> AI Perception -> Deterministic GIS/Asset -> Fusion & Priority    |
|   -> Accountability / SLA Poller -> Resolution Verifier -> Human Triage / Closure     |
+---------------------------------------------------------------------------------------+
```

### Core Immutability Principles
1. **Zero Ground-Truth Mutation**: Phase 4 runtime services MUST NOT overwrite, modify, or delete any record in `data/authority/`, `data/gis/`, `data/lucknow/`, or `data/sources/`.
2. **Strict Separation of Truth vs. Prediction**: Curated benchmark values (`cluster_id`, `duplicate_label`, `resolution_label`, `severity`, curated `authority_id`) are immutable ground truth. Runtime outputs MUST be persisted in distinct application columns, schemas, or tables using the established naming convention.
3. **No Fabricated Certainty**: If location, jurisdiction, asset, or evidence is missing or conflicting, the system MUST return explicit uncertainty states (`UNKNOWN`, `NEEDS_REVIEW`, `CONFLICT`, `NOT_EVALUATED`, `INVALID_LOCATION`) rather than guessing or manufacturing values.
4. **Synthetic vs. Real Grounding**: Real documented records (`CT-INC-001`, `CT-INC-008`, `CT-EVD-001`, `CT-EVD-012`) are grounded in actual Lucknow municipal/PWD schedules. All other records are synthetic evaluation scenarios. Runtime services and UI representations must never display synthetic benchmark scenarios as actual citizen grievances.
5. **Pilot Rules vs. Statutory Guarantees**: All SLA rules in `data/authority/sla_rules.csv` are `CIVICTRACE_PILOT_RULE` hackathon targets, not official statutory government guarantees.

---

## 2. Division of System Responsibilities

CivicTrace strictly demarcates responsibilities across three discrete layers:

| Layer | Subsystem / Actor | Permitted Responsibilities | Strictly Prohibited Actions |
| :--- | :--- | :--- | :--- |
| **AI / Perception** | Gemini API / Multimodal Models | - Image attribute extraction & classification<br/>- Unstructured complaint text parsing<br/>- Multilingual transcription (Hindi/Hinglish/English)<br/>- Visual surface distress assessment<br/>- Quality / blurriness / ambiguity detection | - Determining civic authority responsibility<br/>- Inferring or altering GIS boundaries<br/>- Setting SLA deadlines or due dates<br/>- Overriding deterministic spatial containment<br/>- Administrative incident closure |
| **Deterministic** | FastAPI Services / PostGIS Engine | - PostGIS point-in-polygon containment (`ST_Contains`)<br/>- Exact/approximate asset attribution (`asset_ownership.csv`)<br/>- Multi-agency conflict routing (`CONF-001` - `CONF-004`)<br/>- Proximity-based fusion scoring (radius $\le 50\text{m}$, time $\le 14\text{d}$)<br/>- Mathematical priority scoring: $(0.5\cdot\text{Sev}) + (0.3\cdot\text{Safe}) + (0.2\cdot\text{Pers})$<br/>- SLA clock tracking & escalation state machine | - Guessing boundaries when coordinates are outside known polygons<br/>- Forcing multi-issue complaints into single rigid categories<br/>- Overwriting citizen-reported location discrepancies |
| **Human / Operator** | Zonal Executive / Control Room Admin | - Resolving ambiguous cross-agency boundaries (`NEEDS_REVIEW`)<br/>- Investigating spatial text vs. GPS conflicts (`CONFLICT`)<br/>- Auditing contradictory resolution evidence (`CHAIN-006`)<br/>- Evaluating unlocalized intake reports (`CT-INC-003`)<br/>- Final administrative closure of legal grievance records | - Silently bypassing documented field inspection evidence<br/>- Arbitrarily altering SLA due dates without reason codes |

---

## 3. Data Schema & Integration Contracts

### A. Input Data Schemas (Frozen Data Foundation)

| Dataset | Master File | Total Records | Key Primary Fields | Intended Role |
| :--- | :--- | :--- | :--- | :--- |
| **Authority Master** | `data/authority/lucknow_authority_master.json` | 6 Authorities | `authority_id`, `short_code`, `name`, `sla_tiers` | Authoritative agency registry |
| **Authority Lexicon** | `data/authority/lucknow_authority_lexicon_master.csv` | 28 Services | `record_id`, `authority_id`, `issue_category`, `service_id`, `escalation_level_*` | Service mapping & escalation paths |
| **SLA Rules** | `data/authority/sla_rules.csv` | 21 Pilot Rules | `rule_id`, `issue_category`, `authority_id`, `priority`, `target_hours`, `escalation_threshold_hours` | Target SLA hours per domain/authority |
| **Jurisdictions** | `data/gis/verified/jurisdiction_registry.csv` | 110 Wards | `ward_id`, `ward_number`, `zone_id`, `geometry_status` | Administrative ward/zone hierarchy |
| **Ward Polygons** | `data/gis/lucknow_wards.geojson` | 105 Polygons | `geometry` (EPSG:4326), `ward_id`, `geometry_status` | PostGIS spatial containment layer |
| **Zone Polygons** | `data/gis/lucknow_zones.geojson` | 8 Polygons | `geometry` (EPSG:4326), `zone_id`, `geometry_status` | PostGIS zonal containment layer |
| **Assets** | `data/lucknow/assets/asset_ownership.csv` | 39 Assets | `asset_id`, `asset_type`, `latitude`, `longitude`, `ward_id`, `authority_id`, `responsibility_type` | Physical infrastructure attribution |
| **Seed Incidents** | `data/lucknow/incidents/seed_incidents.csv` | 20 Incidents | `incident_id`, `issue_category`, `severity`, `latitude`, `longitude`, `ward_id`, `asset_id`, `authority_id` | Baseline evaluation complaints |
| **Evidence** | `data/lucknow/evidence/evidence.csv` | 13 Evidence (8 chains) | `evidence_id`, `evidence_chain_id`, `incident_id`, `evidence_stage`, `resolution_label`, `confidence` | Ground-truth verification evidence |
| **Duplicates** | `data/lucknow/duplicates/duplicate_cases.csv` | 26 Cases (7 clusters) | `duplicate_record_id`, `cluster_id`, `reference_record_id`, `duplicate_label`, `curation_confidence` | Ground-truth deduplication benchmark |

---

### B. Expected Runtime Output & State Machines

Phase 4 runtime services must generate outputs corresponding to the following domain state machines:

#### 1. GIS Spatial Resolution Output (`JurisdictionResult`)
```json
{
  "status": "JURISDICTION_FOUND | NO_JURISDICTION | JURISDICTION_CONFLICT | INVALID_LOCATION",
  "ward_id": "WARD-034 | null",
  "zone_id": "ZONE-01 | null",
  "authority_id": "AUTH-LMC | AUTH-UPPWD | NEEDS_REVIEW | null",
  "explanation": "Human-readable provenance trace of the spatial lookup."
}
```
*Rules:*
- If coordinates fall within a verified ward polygon, return `JURISDICTION_FOUND`.
- If coordinates fall in a ward with `geometry_status = NOT_AVAILABLE` (Wards 1, 7, 9, 12, 14), return `NO_JURISDICTION` or `NEEDS_REVIEW`.
- If text conflicts with coordinates (e.g., `CT-INC-010`), flag `JURISDICTION_CONFLICT`.
- If latitude/longitude are absent or out-of-bounds, return `INVALID_LOCATION`.

#### 2. Authority Routing Resolution Contract
In Lucknow's multi-agency environment, authority is NEVER determined by issue category alone:
$$\textbf{ISSUE} + \textbf{LOCATION} + \textbf{JURISDICTION} + \textbf{ASSET} + \textbf{RESPONSIBILITY RULE} \longrightarrow \textbf{RESPONSIBLE AUTHORITY}$$
*Anti-Patterns Forbidden:*
- `POTHOLE -> AUTH-UPPWD` (Violates LMC internal colony road mandate)
- `POTHOLE -> AUTH-LMC` (Violates PWD arterial corridor mandate)
- `STREETLIGHT -> AUTH-MVVNL` (Violates LMC luminaire concession mandate)
- `WARD-034 -> AUTH-LMC` (Ignores PWD, Jal Sansthan, and MVVNL assets in Ward 34)

#### 3. Deterministic Incident Fusion Output
When processing new evidence, the `FusionService` computes a weighted match score against open incidents within $\le 50\text{ meters}$ and $\le 14\text{ days}$:
$$\text{Score} = (0.5 \cdot \text{LocScore}) + (0.4 \cdot \text{CatScore}) + (0.1 \cdot \text{TimeScore})$$
- If $\max(\text{Score}) \ge 0.85$ and `ai_ambiguity_flag == False`: Fuse into existing `Incident` (`INCIDENT_FUSED`).
- If score $< 0.85$: Create new `Incident` in `DRAFT` status (`INCIDENT_CREATED`).
- If `ai_ambiguity_flag == True`: Create new `Incident` in `UNDER_REVIEW` status; bypass automated fusion.

#### 4. Priority Scoring Contract
The `PriorityService` deterministically aggregates evidence-level observations into a mathematical score:
$$\text{Total Score} = (0.5 \cdot \text{HighestSeverity}) + (0.3 \cdot \text{SafetyRisk}) + (0.2 \cdot \text{Persistence})$$
Where:
- $\text{HighestSeverity} \in \{1.0\,(\text{CRITICAL}),\, 0.75\,(\text{HIGH}),\, 0.5\,(\text{MEDIUM}),\, 0.25\,(\text{LOW})\}$
- $\text{SafetyRisk} = 1.0$ if any linked evidence detected hazard, else $0.0$.
- $\text{Persistence} = \min(1.0, (\text{evidence\_count} \cdot 0.1) + (\text{days\_active} / 30.0))$.
- Final Priority Mapping:
  - $\ge 0.75 \implies \textbf{CRITICAL}$
  - $\ge 0.50 \implies \textbf{HIGH}$
  - $\ge 0.25 \implies \textbf{MEDIUM}$
  - $< 0.25 \implies \textbf{LOW}$

#### 5. Accountability & SLA Lifecycle Contract
SLA tracking operates across the entire active incident lifecycle:
$$\textbf{INCIDENT CREATED} \longrightarrow \textbf{SLA CLOCK START} \longrightarrow \textbf{IN PROGRESS} \longrightarrow \textbf{RESOLUTION EVIDENCE} \longrightarrow \textbf{VERIFICATION} \longrightarrow \textbf{FINAL CLOSURE}$$
- State Transitions:
  - `PENDING`: Started, within target window.
  - `DUE`: Remaining time $\le 24\text{ hours}$ (`DUE_WARNING_HOURS`).
  - `OVERDUE`: Current time $\ge \text{due\_at}$.
  - `ESCALATION_ELIGIBLE`: Overdue by $\ge 72\text{ hours}$ (`ESCALATION_DELAY_HOURS`).
  - `RESOLVED`: Set when verification confirms `FULLY_RESOLVED`.

#### 6. Resolution Verification Contract
Verification strictly evaluates submitted "after" evidence against baseline condition:
$$\textbf{AUTHORITY STATUS UPDATE} \neq \textbf{CIVICTRACE EVIDENCE VERIFICATION} \neq \textbf{ADMINISTRATIVE CLOSURE}$$
- Outcomes:
  - `FULLY_RESOLVED`: All verified after-evidence confirms defect remediated and severity eliminated.
  - `PARTIALLY_RESOLVED`: After-evidence shows measurable improvement, but residual distress persists.
  - `UNRESOLVED`: After-evidence indicates defect persists at or above original severity.
  - `INSUFFICIENT_EVIDENCE`: No after-evidence submitted, or all after-evidence is flagged as ambiguous/unusable.
  - `HUMAN_REVIEW`: Triggered when authority claims completion but citizen follow-up evidence shows issue persists (e.g., `CT-INC-014` / `CHAIN-006`).

---

## 4. Ground Truth vs. Runtime Prediction Separation

To preserve historical ground-truth benchmarks while allowing runtime models to predict outcomes, the following field naming convention is enforced across all Phase 4 integration components:

| Domain | Curated Ground-Truth Field (Frozen Foundation) | Runtime Prediction Field (Phase 4 Application) |
| :--- | :--- | :--- |
| **Deduplication** | `cluster_id` (e.g., `CLUSTER-001`)<br/>`duplicate_label` (`DUPLICATE`, `UNRELATED`) | `predicted_cluster_id`<br/>`runtime_duplicate_score` |
| **Authority** | `authority_id` (Curated assignment in Phase 3B) | `predicted_authority_id`<br/>`runtime_routing_explanation` |
| **Jurisdiction** | `ward_id`, `zone_id` (Curated ground truth) | `predicted_ward_id`, `predicted_zone_id`<br/>`gis_resolution_status` |
| **Issue Category** | `issue_category` (Uppercase controlled taxonomy) | `ai_category` (Perception string / `IssueType`) |
| **Severity / Priority** | `severity` (Curated baseline severity) | `ai_severity_raw`, `computed_priority` |
| **Resolution Verification** | `resolution_label` (Curated chain ground truth) | `verification_result` (`VerificationResult`)<br/>`verification_confidence` |
| **Confidence** | `confidence`, `curation_confidence` (Human curation) | `ai_confidence`, `model_confidence` |

---

## 5. Bidirectional Taxonomy & Enum Normalization

Phase 1–3D ground-truth datasets use uppercase controlled strings, while the backend application models (`apps/api/app/models/enums.py`) use lowercase string enums. The integration adapter must perform the following canonical mapping:

### A. Issue Taxonomy Normalization
| Ground-Truth Dataset (`issue_category`) | Application Enum (`IssueType`) | Mapping Category |
| :--- | :--- | :--- |
| `POTHOLE` | `pothole` | Exact 1:1 |
| `ROAD_DAMAGE`, `ROAD_COLLAPSE` | `road_damage` | Normalized |
| `DAMAGED_FOOTPATH` | `road_damage` (or `other`) | Mapped |
| `WATERLOGGING`, `BLOCKED_DRAIN`, `DRAIN_DAMAGE` | `flooding` | Domain group |
| `GARBAGE_ACCUMULATION`, `ILLEGAL_DUMPING`, `OVERFLOWING_BIN` | `illegal_dumping` | Domain group |
| `STREETLIGHT_FAILURE`, `STREETLIGHT_DAMAGE` | `broken_streetlight` | Exact 1:1 |
| `WATER_LEAKAGE`, `BROKEN_PIPELINE`, `LOW_WATER_SUPPLY` | `water_leak` | Domain group |
| `SEWER_OVERFLOW`, `SEWER_INFRASTRUCTURE` | `sewage_overflow` | Exact 1:1 |
| `ELECTRICAL_INFRASTRUCTURE`, `POWER_OUTAGE` | `other` (or extended) | Infrastructure |
| `ANIMAL_NUISANCE`, `GENERAL_CIVIC` | `other` | General |

### B. Verification Result Normalization
| Dataset Ground Truth (`resolution_label`) | Application Enum (`VerificationResult`) |
| :--- | :--- |
| `FULLY_RESOLVED` | `fully_resolved` |
| `PARTIALLY_RESOLVED` | `partially_resolved` |
| `NOT_RESOLVED` | `unresolved` |
| `INSUFFICIENT_EVIDENCE` | `insufficient_evidence` |
| *(Contradictory / Review Trigger)* | `UNDER_REVIEW` (Incident Status) + `human_review` |

---

## 6. Golden Demo Test Harness Integration

All automated test suites and benchmark evaluations in Phase 4 must bind directly to the 10 Golden Demo Cases defined in `docs/golden_demo_cases.md`:

```python
# Conceptual Phase 4 Test Assertion Harness
def test_evaluate_golden_demo_case(case_id, prototype_engine):
    benchmark = load_golden_demo_case(case_id)
    result = prototype_engine.process_incident(benchmark.incident_id)
    
    # Assert deterministic routing matches ground truth
    assert result.predicted_authority_id == benchmark.expected_authority_id
    assert result.predicted_ward_id == benchmark.expected_ward_id
    
    # Assert uncertainty preserved
    if benchmark.human_review_required:
        assert result.human_review_flag is True
        assert result.status in ["under_review", "draft"]
```

---

## 7. Verification & Compliance Checklist for Integrators

- [ ] Ground-truth datasets in `data/` are treated as read-only.
- [ ] No hardcoded machine paths (`d:/`, `c:/`, `file:///`) exist in runtime configurations.
- [ ] GIS containment logic properly handles the 5 wards without legacy geometry.
- [ ] Multi-agency routing adheres to `CONF-001` through `CONF-004` conflict rules.
- [ ] AI Perception never overrides deterministic PostGIS jurisdiction assignment.
- [ ] Duplicate detection benchmark scores against `data/lucknow/duplicates/duplicate_cases.csv`.
- [ ] Resolution verification evaluates before/after imagery rather than relying on authority status text.
- [ ] All 7 data validation scripts pass with 0 errors prior to deployment.
