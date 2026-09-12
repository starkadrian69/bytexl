# CivicTrace Phase 3C: Lucknow Evidence Dataset

**Directory:** `data/lucknow/evidence/`  
**Dataset File:** `evidence.csv`  
**Validation Suite:** `scripts/validate_evidence.py`  
**Machine-Readable Report:** `evidence_validation_report.json`  
**Technical Documentation:** `docs/phase3c_evidence.md`  
**Status:** COMPLETE & FROZEN  

---

## 1. Purpose & Design Philosophy

The Phase 3C Evidence Layer provides a structured, provenance-aware observational foundation for the CivicTrace civic intelligence platform. It establishes the empirical and documentary record connected to grievances reported in Phase 3B (`data/lucknow/incidents/seed_incidents.csv`), answering two fundamental operational questions:

1. **"What evidence exists for this incident?"** (Intake proof, citizen photographs, field measurement logs, authority notices).
2. **"Does the available evidence support that the issue was resolved?"** (Post-repair verification, inspection reports, contradictory citizen follow-ups).

### Scope Guardrails
> [!IMPORTANT]
> This dataset is strictly for **DATA COLLECTION AND DATA VALIDATION**. It does NOT implement computer vision, image similarity, NLP, automated ticket closure, or AI classification algorithms. Duplicate complaint detection and ML inference are deferred to subsequent platform intelligence phases.

---

## 2. Core Architectural Principles

### Core Principle 1: Curated Ground Truth vs. Individual Evidence Scope
> "An AFTER-stage record does not automatically establish FULLY_RESOLVED. Resolution ground truth requires sufficient evidence that the reported condition was actually addressed. Authority closure statements may constitute resolution evidence but can be contradicted by subsequent citizen or field evidence. Such contradictions are preserved rather than automatically overwritten."

In CivicTrace, `resolution_label` represents the curated ground truth of the incident sequence across its full evidence chain. An individual evidence item represents an observation with a defined `evidence_scope` (`INCIDENT`, `LOCATION`, `CONDITION`, `RESOLUTION`, or `AUTHORITY_UPDATE`), but does not unilaterally dictate platform ground truth.

### Core Principle 2: Human/Data-Curation Confidence
> "confidence represents human/data-curation confidence, not AI confidence."

The `confidence` metric is a normalized decimal float between `0.0` and `1.0` assigned during human data curation. It reflects the defensibility and clarity of the record's provenance and observation, not a machine learning probability score.

### Core Principle 3: Zero-Fabrication Policy
No physical photographs, government reports, or citizen submissions are fabricated.
- For `REAL_DOCUMENTED` records, `file_path` remains empty when no local physical file exists. Provenance is anchored via `source_id` and `source_reference`. Internal identifiers may use `source://<source_id>/<section>`.
- For `SYNTHETIC_EVALUATION` records, transparent virtual URIs (`synthetic://<incident_id>/<scenario>`) are utilized, and the scenario ground-truth basis is explicitly documented.

---

## 3. 18-Column Schema

The dataset `evidence.csv` adheres strictly to the following 18 columns in order:

| Column | Data Type | Nullable | Description & Format |
| :--- | :--- | :--- | :--- |
| `evidence_id` | String | No | Unique evidence identifier (`CT-EVD-001` through `CT-EVD-013`). |
| `evidence_chain_id` | String | No | Sequence identifier grouping records for an incident (`CHAIN-001` through `CHAIN-008`). |
| `incident_id` | String | No | Foreign key referencing `data/lucknow/incidents/seed_incidents.csv`. |
| `evidence_type` | Enum | No | Type of empirical artifact (see Controlled Vocabularies). |
| `evidence_stage` | Enum | No | Chronological phase of evidence collection relative to repair lifecycle. |
| `evidence_scope` | Enum | No | Specific grievance attribute substantiated by this individual record. |
| `file_path` | URI / Path | Yes | Virtual URI (`synthetic://...`), internal reference, or empty string. |
| `latitude` | Float | Yes | Decimal latitude (WGS84). Permitted empty for non-spatial or unknown locations. |
| `longitude` | Float | Yes | Decimal longitude (WGS84). Permitted empty for non-spatial or unknown locations. |
| `capture_time` | ISO 8601 | No | UTC timestamp of observation capture (`YYYY-MM-DDTHH:MM:SSZ`). |
| `source_type` | Enum | No | Data origin classification (`REAL_DOCUMENTED`, `OWN_CONTROLLED`, `SYNTHETIC_EVALUATION`). |
| `resolution_label` | Enum | No | Curated ground truth state for the incident chain. |
| `evidence_quality` | Enum | No | Observational integrity rating (`HIGH`, `MEDIUM`, `LOW`, `UNUSABLE`). |
| `confidence` | Float (0.0–1.0)| No | Curation certainty score reflecting evidentiary strength. |
| `source_id` | String | No | Registered source identifier referencing Phase 1 / Phase 2 registries (`SRC-001`–`SRC-019`). |
| `source_reference` | String | No | Section, notification number, or synthetic evaluation scenario description. |
| `location_status` | Enum | No | Spatial validity classification (`VERIFIED`, `APPROXIMATE`, `UNKNOWN`, `CONFLICT`, `NOT_APPLICABLE`). |
| `notes` | String | No | Contextual curation notes, edge-case rationale, and operational commentary. |

---

## 4. Controlled Vocabularies (Enums)

### `evidence_type`
- `CITIZEN_PHOTO`: Mobile camera capture submitted by a citizen complainant or bystander.
- `CITIZEN_VIDEO`: Video recording frame or clip submitted by a citizen.
- `AUTHORITY_UPDATE`: Official administrative or portal grievance action update text.
- `BEFORE_PHOTO`: Dedicated pre-intervention baseline condition photograph.
- `AFTER_PHOTO`: Dedicated post-intervention rectification photograph.
- `FIELD_INSPECTION`: Formal on-site engineering or health inspection report/log.
- `DOCUMENTARY_EVIDENCE`: Official administrative schedule, register, or survey inventory.

### `evidence_stage`
- `BEFORE`: Captured prior to municipal or utility repair intervention.
- `DURING`: Captured during active physical excavation, desiltation, or construction.
- `AFTER`: Captured subsequent to reported departmental action.
- `UNKNOWN`: Timestamp or lifecycle sequence cannot be determined.

### `evidence_scope`
- `INCIDENT`: Substantiates the core occurrence of the grievance event.
- `LOCATION`: Substantiates the spatial position or landmark context.
- `CONDITION`: Substantiates the physical severity, defect depth, or environmental state.
- `RESOLUTION`: Substantiates the physical rectification or persistence of the defect.
- `AUTHORITY_UPDATE`: Substantiates administrative status logging without physical proof.

### `source_type`
- `REAL_DOCUMENTED`: Derived from verified public records, published schedules, or official gazettes.
- `OWN_CONTROLLED`: Physical evaluation photographs captured directly under controlled field tests.
- `SYNTHETIC_EVALUATION`: Methodologically engineered scenario used to benchmark platform logic.

### `resolution_label`
- `FULLY_RESOLVED`: Empirical evidence confirms complete rectification of the reported defect.
- `PARTIALLY_RESOLVED`: Intervention occurred, but secondary distress or partial defect persists.
- `NOT_RESOLVED`: No remedial intervention occurred, or post-closure evidence shows failure.
- `INSUFFICIENT_EVIDENCE`: Evidence is inadequate, blurry, unlocalized, or conflicting.

### `evidence_quality`
- `HIGH`: Sharp focus, discernible defect metrics, clear surrounding landmarks.
- `MEDIUM`: Identifiable defect, but minor lighting, distance, or framing limitations.
- `LOW`: Poor lighting, heavy pixelation, or ambiguous spatial context.
- `UNUSABLE`: Extreme motion blur, pitch-black underexposure, or completely corrupted media.

### `location_status`
- `VERIFIED`: Survey-grade or landmark-grounded spatial positioning.
- `APPROXIMATE`: Inherited from arterial centerline, colony landmark, or uncalibrated consumer GPS.
- `UNKNOWN`: No spatial coordinates or geographic metadata available.
- `CONFLICT`: Context-supported discordance between complaint narrative and EXIF coordinates.
- `NOT_APPLICABLE`: Non-spatial evidence records (such as centralized portal action logs).

---

## 5. Dataset Composition & Evidence Chains

The dataset comprises **13 evidence records** grouped into **8 evidence chains** across **8 Phase 3B seed incidents**:

```mermaid
flowchart TD
    subgraph CHAIN001["CHAIN-001 (CT-INC-001: Pothole)"]
        E1["CT-EVD-001 (BEFORE: Condition)<br/>REAL_DOCUMENTED"] --> E2["CT-EVD-002 (AFTER: Resolution)<br/>SYNTHETIC_EVALUATION"]
        E2 --> R1["FULLY_RESOLVED"]
    end
    subgraph CHAIN002["CHAIN-002 (CT-INC-004: Road & Waterlogging)"]
        E3["CT-EVD-003 (BEFORE: Incident)<br/>SYNTHETIC_EVALUATION"] --> E4["CT-EVD-004 (AFTER: Resolution)<br/>SYNTHETIC_EVALUATION"]
        E4 --> R2["PARTIALLY_RESOLVED"]
    end
    subgraph CHAIN006["CHAIN-006 (CT-INC-014: Sewer Surcharge)"]
        E8["CT-EVD-008 (BEFORE: Condition)<br/>CITIZEN_PHOTO"] --> E9["CT-EVD-009 (AFTER: Portal Update)<br/>AUTHORITY_UPDATE"]
        E9 --> E10["CT-EVD-010 (AFTER: Resolution Proof)<br/>CITIZEN_PHOTO (Persists)"]
        E10 --> R6["NOT_RESOLVED<br/>(Contradiction Warning)"]
    end
    subgraph CHAIN008["CHAIN-008 (CT-INC-008: Blocked Trunk Drain)"]
        E12["CT-EVD-012 (BEFORE: Condition)<br/>REAL_DOCUMENTED"] --> E13["CT-EVD-013 (AFTER: Resolution)<br/>FIELD_INSPECTION"]
        E13 --> R8["FULLY_RESOLVED"]
    end
```

### Complete Chains (4 Chains)
1. **`CHAIN-001` (`CT-INC-001`)**: PWD arterial road distress documented in official road schedule (`SRC-007`) followed by synthetic post-overlay inspection photo $\rightarrow$ `FULLY_RESOLVED`.
2. **`CHAIN-002` (`CT-INC-004`)**: Citizen complaint photo of damaged colony road followed by Junior Engineer field inspection report noting stone grit backfilling without drainage clearance $\rightarrow$ `PARTIALLY_RESOLVED`.
3. **`CHAIN-006` (`CT-INC-014`)**: Citizen photo of raw sewage surcharge followed by authority text update claiming closure, contradicted by citizen follow-up photo 2 hours later showing persistent overflow $\rightarrow$ `NOT_RESOLVED` (`CONTRADICTORY_RESOLUTION_EVIDENCE`).
4. **`CHAIN-008` (`CT-INC-008`)**: LMC pre-monsoon covered drain silt survey (`SRC-005`) followed by Assistant Engineer desiltation measurement log $\rightarrow$ `FULLY_RESOLVED`.

### Incomplete & Edge-Case Chains (4 Chains)
5. **`CHAIN-003` (`CT-INC-003`)**: Unlocalized pothole photo with stripped EXIF, unidentifiable background, and missing GPS (`location_status=UNKNOWN`) $\rightarrow$ `INSUFFICIENT_EVIDENCE`.
6. **`CHAIN-004` (`CT-INC-019`)**: Critical sparking distribution transformer video frame; no repair evidence exists $\rightarrow$ `NOT_RESOLVED`.
7. **`CHAIN-005` (`CT-INC-010`)**: Citizen photo where EXIF coordinates point to Hazratganj while intake narrative specifies Kapoorthala Aliganj (`location_status=CONFLICT`) $\rightarrow$ `INSUFFICIENT_EVIDENCE`.
8. **`CHAIN-007` (`CT-INC-016`)**: Nighttime streetlight outage photo completely underexposed and blurred (`evidence_quality=UNUSABLE`) $\rightarrow$ `INSUFFICIENT_EVIDENCE`.

---

## 6. Spatial Handling & Coordinate Policy

- **Coordinate Bounds**: Broad sanity envelope for Lucknow urban area ($26.60^\circ\text{N} \le \text{Lat} \le 27.15^\circ\text{N}$, $80.70^\circ\text{E} \le \text{Lon} \le 81.25^\circ\text{E}$). Out-of-bounds coordinates trigger validation review, not automatic invalidation.
- **Null Coordinates**: Empty latitude and longitude are explicitly permitted when `location_status` is `UNKNOWN` or `NOT_APPLICABLE`.
- **Coordinate Integrity**: Coordinates are never artificially altered, snapped, or synthesized to match incident or asset points.

---

## 7. Validation & Quality Metrics

The automated test suite `scripts/validate_evidence.py` enforces all structural and semantic integrity constraints:
- **Total Records:** 13
- **Total Incidents Represented:** 8
- **Evidence Chains:** 8
- **Complete BEFORE/AFTER Chains:** 4
- **Incomplete Chains:** 4
- **Contradictory Chains:** 1 (`CONTRADICTORY_RESOLUTION_EVIDENCE` warning)
- **Unsupported FULLY_RESOLVED Claims:** 0 (Hard constraint)
- **Provenance Completeness:** 100%
- **Validation Errors:** 0
- **Intentional Test Warnings:** 7

---

## 8. Dataset Limitations

1. **Static Demonstration Scope**: The dataset is intentionally compact (13 records across 8 chains) to rigorously exercise edge cases rather than volume.
2. **Virtual Media Referencing**: Physical image binaries are not bundled; virtual URI schemes (`synthetic://...`) prevent media fabrication.
3. **No Inference Engine**: Ground-truth labels reflect human curation, not output from an automated vision or NLP pipeline.
