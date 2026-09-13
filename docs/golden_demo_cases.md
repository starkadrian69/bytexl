# CivicTrace Golden Demo Data Contract
**Phase 3D Final Verification & Prototype Specification**  
**Target Environment:** byteBuilt 1.0 Hackathon (Lucknow Focus)  
**Dataset Freeze Status:** FROZEN FOUNDATION (Phases 1, 2, 3A, 3B, 3C, 3D)  
**Document Status:** OFFICIAL CONTRACT FOR PHASE 4 DEVELOPMENT  

---

## Executive Overview & Architectural Purpose

This document defines the **10 Golden Demo Cases** for CivicTrace v1.0. These cases represent the curated ground truth against which future application pipelines (intake NLP, geocoding, jurisdictional routing, duplicate detection, computer vision resolution auditing, and escalation) will be evaluated.

### Ground Truth vs Prototype Output Distinction
> [!IMPORTANT]
> - **Synthetic Benchmark Distinction**: All `CT-DUP` records and duplicate clusters (e.g., `CLUSTER-001`) represent **human-curated synthetic evaluation scenarios**, designed specifically to test algorithmic capabilities. They are **NOT** evidence of real citizen submissions or real-world duplicate complaints.
> - **Evaluation Role**: Each case defines **Ground Truth** and **Expected Prototype Behavior**. During Phase 4, the engineering team will benchmark prototype outputs against these exact expected states (`Ground Truth → Expected Result → Actual Prototype Output`).
> - **Pilot Rules vs Government Policy**: All resolution timeframes and escalation thresholds reference `CIVICTRACE_PILOT_RULE` configurations from `data/authority/sla_rules.csv`, reflecting hackathon demonstration targets rather than official statutory government commitments.
> - **Prototype Output Distinction**: The expected behavior defined in this contract describes what the prototype SHOULD produce when executing correctly; it does not claim that the prototype already produces these results.

---

## Golden Demo Lineage & Verification Matrix

| Case ID | Incident ID | Issue Category | Language | Ward | Zone | Asset ID | Authority ID | Priority | SLA Rule | Resolution Status | Duplicate Scenario | Data Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GD-CASE-01** | `CT-INC-002` | `POTHOLE` | `HINDI` | `WARD-034` | `ZONE-01` | `AST-ROAD-002` | `AUTH-LMC` | `MEDIUM` | `SLA-RULE-001` | `PENDING_INTAKE` | Standalone Municipal Lane | `SYNTHETIC_EVALUATION` |
| **GD-CASE-02** | `CT-INC-001` | `POTHOLE` | `ENGLISH` | `WARD-034` | `ZONE-01` | `AST-ROAD-001` | `AUTH-UPPWD` | `HIGH` | `SLA-RULE-002` | `FULLY_RESOLVED` | `CLUSTER-001` (Multilingual Duplicates) | `REAL_DOCUMENTED` / `SYNTHETIC_EVALUATION` |
| **GD-CASE-03** | `CT-DUP-020`, `CT-DUP-021` | `STREETLIGHT_FAILURE`, `BLOCKED_DRAIN` | `ENGLISH` | Multiple | Multiple | `AST-STL-001`, `AST-DRN-004` | `AUTH-LMC` | `MEDIUM` / `HIGH` | `SLA-RULE-010`, `012` | `UNRELATED` | `CLUSTER-007` (Negative Controls) | `SYNTHETIC_EVALUATION` |
| **GD-CASE-04** | `CT-INC-010` | `WATERLOGGING` | `HINGLISH` | `WARD-109` | `ZONE-03` | `AST-DRN-003` | `AUTH-LMC` | `HIGH` | `SLA-RULE-013` | `INSUFFICIENT_EVIDENCE` | `CLUSTER-004` (Spatial Conflict) | `SYNTHETIC_EVALUATION` |
| **GD-CASE-05** | `CT-INC-014` | `SEWER_OVERFLOW` | `ENGLISH` | `WARD-034` | `ZONE-01` | `AST-SWR-001` | `AUTH-LKO-JALSANSTHAN` | `HIGH` | `SLA-RULE-016` | `NOT_RESOLVED` | `CT-DUP-025` (Contradictory Evidence) | `SYNTHETIC_EVALUATION` |
| **GD-CASE-06** | `CT-INC-004` | `ROAD_DAMAGE` | `MIXED` | `WARD-109` | `ZONE-03` | `AST-ROAD-004` | `AUTH-LMC` | `HIGH` | `SLA-RULE-003` | `PARTIALLY_RESOLVED` | Standalone Multi-Issue | `SYNTHETIC_EVALUATION` |
| **GD-CASE-07** | `CT-INC-016` | `STREETLIGHT_FAILURE` | `ENGLISH` | `WARD-080` | `ZONE-07` | `AST-STL-004` | `AUTH-LMC` | `LOW` | `SLA-RULE-010` | `INSUFFICIENT_EVIDENCE` | Standalone Poor Evidence | `SYNTHETIC_EVALUATION` |
| **GD-CASE-08** | `CT-INC-019` | `ELECTRICAL_INFRASTRUCTURE` | `MIXED` | `WARD-109` | `ZONE-03` | `AST-ELE-003` | `AUTH-MVVNL` | `CRITICAL` | `SLA-RULE-018` | `NOT_RESOLVED` | High Voltage Hazard (CONF-003) | `SYNTHETIC_EVALUATION` |
| **GD-CASE-09** | `CT-INC-003` | `POTHOLE` | `HINGLISH` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `NEEDS_REVIEW` | `MEDIUM` | `SLA-RULE-001` | `INSUFFICIENT_EVIDENCE` | Incomplete Location Intake | `SYNTHETIC_EVALUATION` |
| **GD-CASE-10** | `CT-INC-012` | `BROKEN_PIPELINE` | `HINDI` | `WARD-026` | `ZONE-02` | `AST-WTR-001` | `AUTH-LKO-JALSANSTHAN` | `CRITICAL` | `SLA-RULE-015` | `NOT_RESOLVED` | `CLUSTER-005` (High Impact Repeat) | `SYNTHETIC_EVALUATION` |

---

## Detailed Golden Demo Specifications

```
================================================================================
CASE ID: GD-CASE-01
TITLE: Simple Municipal Road Pothole -> Correct Local Authority
================================================================================
INPUT COMPLAINT:
  "हज़रतगंज मार्केट की आंतरिक सड़क पर बहुत बड़ा गड्ढा हो गया है, गाड़ियाँ टकरा रही हैं।"
LANGUAGE:
  HINDI (Devanagari script)

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-002
  issue_category:           POTHOLE (Subcategory: Internal Colony / Market Road Pothole)
  location_status:          APPROXIMATE (Latitude: 26.85242, Longitude: 80.94513)
  ward_id:                  WARD-034 (Hazratganj)
  zone_id:                  ZONE-01
  asset_id:                 AST-ROAD-002 (Hazratganj Market Internal Commercial Road)
  authority_id:             AUTH-LMC (Lucknow Municipal Corporation)
  responsibility_type:      MAINTENANCE (Civil Engineering Department Zone 1)
  priority:                 MEDIUM
  sla_rule_id:              SLA-RULE-001 (Target: 48h, Escalation: 72h)
  duplicate_status:         STANDALONE
  cluster_id:               NONE (Standalone municipal lane incident)
  evidence_chain_id:        NONE
  evidence_status:          NOT_EVALUATED
  resolution_status:        PENDING_INTAKE
  human_review_required:    FALSE
  provenance:               SRC-005 (UP Municipal Corporations Act 1959 Ch 12)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Intake NLP parses Hindi text and accurately extracts issue category 'POTHOLE'.
  2. Preserves original Devanagari complaint text without lossy translation artifacts.
  3. Reverse-geocodes coordinate (26.85242, 80.94513) to WARD-034, ZONE-01 via PostGIS containment.
  4. Distinguishes internal municipal lane (AST-ROAD-002) from arterial highway;
     routes deterministically to Lucknow Municipal Corporation (AUTH-LMC Civil Wing),
     avoiding incorrect assignment to UP PWD.
  5. Assigns CivicTrace Pilot Rule SLA-RULE-001 (48h resolution target).
```

```
================================================================================
CASE ID: GD-CASE-02
TITLE: Arterial PWD Corridor Pothole & Multilingual Duplicate Cluster (Cluster-001)
================================================================================
INPUT COMPLAINT:
  Primary:     "Large deep pothole and bituminous disintegration on Hazratganj arterial corridor near GPO causing vehicle damage." [ENGLISH]
  Duplicate A: "Massive crater-like pothole on Mahatma Gandhi Marg near GPO Hazratganj, damaging two-wheelers and disrupting traffic." [ENGLISH - CT-DUP-001]
  Duplicate B: "हजरतगंज में जीपीओ के सामने मुख्य सड़क पर बहुत गहरा गड्ढा है, जिससे गाड़ियाँ दुर्घटनाग्रस्त हो रही हैं।" [HINDI - CT-DUP-002]
  Duplicate C: "GPO Hazratganj ke paas main road par bohot bada pothole bana hua hai, accidents ho rahe hain." [HINGLISH - CT-DUP-003]
LANGUAGE:
  ENGLISH (Primary Anchor), HINDI (Devanagari), HINGLISH (Romanized Hindi)

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-001
  issue_category:           POTHOLE (Subcategory: Major Arterial Road Pothole)
  location_status:          APPROXIMATE (Latitude: 26.85028, Longitude: 80.94382)
  ward_id:                  WARD-034 (Hazratganj)
  zone_id:                  ZONE-01
  asset_id:                 AST-ROAD-001 (Mahatma Gandhi Marg Arterial Corridor - PWD Section)
  authority_id:             AUTH-UPPWD (Public Works Department, UP - Lucknow Circle)
  responsibility_type:      MAINTENANCE (Provincial Division Lucknow)
  priority:                 HIGH
  sla_rule_id:              SLA-RULE-002 (Target: 48h, Escalation: 72h)
  duplicate_status:         DUPLICATE_ANCHOR
  cluster_id:               CLUSTER-001 (Curated labels: CT-DUP-001, 002, 003 DUPLICATE)
  evidence_chain_id:        CHAIN-001 (CT-EVD-001 BEFORE condition, CT-EVD-002 AFTER resolution)
  evidence_status:          VERIFIED
  resolution_status:        FULLY_RESOLVED (Supported by verified after-repair photo)
  human_review_required:    FALSE
  provenance:               SRC-007 (PWD Citizen Charter & Lucknow Circle Schedule)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Identifies Mahatma Gandhi Marg as a State PWD Highway/Arterial Corridor;
     routes to AUTH-UPPWD (NOT LMC), demonstrating inter-agency jurisdictional boundary.
  2. Duplicate Engine recognizes that English, Hindi, and Hinglish inputs describe the
     exact same spatial crater on AST-ROAD-001 and clusters them into CLUSTER-001.
  3. Resolution Verifier ingests BEFORE (CT-EVD-001) and AFTER (CT-EVD-002) evidence;
     validates surface leveling and transitions incident status to FULLY_RESOLVED.
```

```
================================================================================
CASE ID: GD-CASE-03
TITLE: Similar Wording / Proximate Locality -> Hard Non-Duplicate Negative Controls
================================================================================
INPUT COMPLAINT:
  Scenario A (CT-DUP-020): "Streetlight fixture mounted on median pole opposite GPO Hazratganj is not working, road pitch dark at night." [ENGLISH]
  Reference A (CT-DUP-001): GPO Hazratganj Pothole Complaint (Distance: ~30 meters)
  Scenario B (CT-DUP-021): "Stormwater drain heavily choked and overflowing with dirty runoff along sector road in Gomti Nagar near Vibhuti Khand." [ENGLISH]
  Reference B (CT-DUP-006): Trilokinath Road Drain Choke Complaint (Distance: ~4.2 kilometers)
LANGUAGE:
  ENGLISH

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              UNKNOWN (Evaluates control records CT-DUP-020, CT-DUP-021)
  issue_category:           Scenario A: STREETLIGHT_FAILURE vs POTHOLE; Scenario B: BLOCKED_DRAIN (Distant)
  location_status:          APPROXIMATE (Scenario A: 26.85035, 80.94390; Scenario B: 26.85100, 80.98500)
  ward_id:                  Scenario A: WARD-034 (Zone 1); Scenario B: WARD-037 (Zone 4)
  zone_id:                  Scenario A: ZONE-01; Scenario B: ZONE-04
  asset_id:                 Scenario A: AST-STL-001 vs AST-ROAD-001; Scenario B: AST-DRN-004 vs AST-DRN-001
  authority_id:             Scenario A: AUTH-LMC (E/M Wing) vs AUTH-UPPWD; Scenario B: AUTH-LMC Zone 4 vs Zone 1
  responsibility_type:      MAINTENANCE
  priority:                 Scenario A: MEDIUM; Scenario B: HIGH
  sla_rule_id:              Scenario A: SLA-RULE-010 (48h); Scenario B: SLA-RULE-012 (24h)
  duplicate_status:         UNRELATED
  cluster_id:               CLUSTER-007 (Curated Ground Truth: UNRELATED Negative Controls)
  evidence_chain_id:        NONE
  evidence_status:          NOT_EVALUATED
  resolution_status:        INDEPENDENT_INTAKE
  human_review_required:    FALSE
  provenance:               SRC-005, SRC-013

EXPECTED PROTOTYPE BEHAVIOR:
  1. Precision Guardrail: Refuses to merge complaints purely on geographic proximity
     (<40m) when issue domains and physical assets differ (Streetlight vs Pothole).
  2. Anti-Hallucination Guardrail: Refuses to merge complaints purely on semantic text
     similarity ('stormwater drain choked and overflowing') when coordinates and ward
     boundaries are separated by >4 km.
  3. Accurately flags both comparisons as UNRELATED in duplicate scoring benchmark.
```

```
================================================================================
CASE ID: GD-CASE-04
TITLE: Text vs GPS Spatial Conflict (Difficult Case D)
================================================================================
INPUT COMPLAINT:
  "Kapoorthala Aliganj crossing par drain block hone se sadak par 2 feet paani bhar gaya hai, traffic jammed."
LANGUAGE:
  HINGLISH

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-010
  issue_category:           WATERLOGGING (Subcategory: Commercial Intersection Waterlogging)
  location_status:          CONFLICT / NEEDS_REVIEW (Text: Kapoorthala Aliganj; GPS: 26.85025, 80.94380 -> Hazratganj ~1.4 km distant)
  ward_id:                  WARD-109 (Intake narrative ward) / WARD-034 (GPS containment ward)
  zone_id:                  ZONE-03 (Narrative zone) / ZONE-01 (GPS zone)
  asset_id:                 AST-DRN-003 (Kapoorthala Roadside Stormwater Drain)
  authority_id:             AUTH-LMC (Civil Engineering Department Zone 3)
  responsibility_type:      OPERATION (Dewatering & Pumping)
  priority:                 HIGH
  sla_rule_id:              SLA-RULE-013 (Emergency Pumping: Target 6h, Escalation 12h)
  duplicate_status:         DUPLICATE_ANCHOR (Primary anchor for CLUSTER-004)
  cluster_id:               CLUSTER-004 (CT-DUP-013, 014, 015)
  evidence_chain_id:        CHAIN-005 (CT-EVD-007: Geotagged photo with text vs EXIF discordance)
  evidence_status:          CONFLICT
  resolution_status:        INSUFFICIENT_EVIDENCE (Location unresolved)
  human_review_required:    TRUE (Spatial Text vs GPS Discrepancy)
  provenance:               SRC-005 (UP Municipal Corporations Act 1959 Ch 10 Section 114)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Geocoding anomaly detector compares text named-entity ('Kapoorthala Aliganj')
     against submitted GPS point (Hazratganj); detects 1.4 km spatial discrepancy.
  2. Does NOT mutate GPS coordinates or silently overwrite text locality.
  3. Emits warning: 'SPATIAL_REVIEW_REQUIRED' with 'LOCATION_STATUS = CONFLICT'.
  4. Routes complaint to human intake triage queue for citizen re-verification.
```

```
================================================================================
CASE ID: GD-CASE-05
TITLE: Contradictory Resolution Evidence (Authority Closure vs Citizen Follow-up)
================================================================================
INPUT COMPLAINT:
  "Sewage line backed up and surcharging through manhole cover on Hazratganj lane causing foul odor."
LANGUAGE:
  ENGLISH

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-014
  issue_category:           SEWER_OVERFLOW (Subcategory: Surging Sewer Manhole / Conduit Blockage)
  location_status:          APPROXIMATE (Latitude: 26.85304, Longitude: 80.94423)
  ward_id:                  WARD-034 (Hazratganj)
  zone_id:                  ZONE-01
  asset_id:                 AST-SWR-001 (Hazratganj Commercial District Lateral Sewer Line)
  authority_id:             AUTH-LKO-JALSANSTHAN (Lucknow Jal Sansthan - Sewerage Wing)
  responsibility_type:      OPERATION (Desilting & Jetting)
  priority:                 HIGH
  sla_rule_id:              SLA-RULE-016 (Target: 24h, Escalation: 48h)
  duplicate_status:         DUPLICATE_ANCHOR (Linked with repeat grievance CT-DUP-025)
  cluster_id:               CLUSTER-007 (Negative control) / Repeat Grievance
  evidence_chain_id:        CHAIN-006 (Contradictory Resolution Audit: CT-EVD-008, 009, 010)
  evidence_status:          CONTRADICTORY_RESOLUTION_EVIDENCE
  resolution_status:        NOT_RESOLVED (Authority closure rejected by evidence)
  human_review_required:    TRUE (Contradictory closure text vs citizen photo)
  provenance:               SRC-011 (UP Act 43 of 1975 Section 18 & 24), SRC-006 (Jansunwai)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Evidence Verification Module compares unverified authority text closure (CT-EVD-009)
     against subsequent citizen follow-up imagery (CT-EVD-010).
  2. Perception layer detects ongoing sewage overflow in the 'after' timeframe.
  3. Rejects premature administrative closure; flags 'CONTRADICTORY_RESOLUTION_EVIDENCE'.
  4. Maintains incident state as NOT_RESOLVED and triggers automatic L2 supervisor escalation.
```

```
================================================================================
CASE ID: GD-CASE-06
TITLE: Partial Resolution Audit (Compound Road Damage & Drainage Choke)
================================================================================
INPUT COMPLAINT:
  "Colony road poori tarah damage ho chuki hai aur side mein waterlogging ho rahi hai after slight rain."
LANGUAGE:
  MIXED (Hinglish / English)

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-004
  issue_category:           ROAD_DAMAGE (Compound issue: Pavement depression + stormwater choke)
  location_status:          APPROXIMATE (Latitude: 26.85115, Longitude: 80.92992)
  ward_id:                  WARD-109 (Aliganj)
  zone_id:                  ZONE-03
  asset_id:                 AST-ROAD-004 (Aliganj Sector B Internal Residential Colony Road)
  authority_id:             AUTH-LMC (Civil Engineering Department Zone 3)
  responsibility_type:      MAINTENANCE (Pavement Repair)
  priority:                 HIGH
  sla_rule_id:              SLA-RULE-003 (Target: 72h, Escalation: 120h)
  duplicate_status:         STANDALONE
  cluster_id:               NONE (Standalone compound complaint)
  evidence_chain_id:        CHAIN-002 (CT-EVD-003 BEFORE photo, CT-EVD-004 AFTER JE inspection report)
  evidence_status:          PARTIALLY_RESOLVED
  resolution_status:        PARTIALLY_RESOLVED (Road backfilled, drainage berm choked)
  human_review_required:    FALSE
  provenance:               SRC-002 (LMC Doorbhas Suchi Item 30 - EE Zone 3)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Classifies compound distress (road damage accompanied by drainage ponding).
  2. Ingests inspection record CT-EVD-004; detects road leveling completed but drainage incomplete.
  3. Transitions incident status to PARTIALLY_RESOLVED (not closed).
  4. Keeps residual drainage remediation open on the zonal maintenance taskboard.
```

```
================================================================================
CASE ID: GD-CASE-07
TITLE: Insufficient / Unusable Image Evidence Gate
================================================================================
INPUT COMPLAINT:
  "Streetlight LED luminaire fixture on Sector 14 municipal pole not illuminating for the past 4 days."
LANGUAGE:
  ENGLISH

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-016
  issue_category:           STREETLIGHT_FAILURE (Subcategory: Dark Streetlight / Luminaire Failure)
  location_status:          APPROXIMATE (Latitude: 26.90653, Longitude: 80.94424)
  ward_id:                  WARD-080 (Indira Nagar)
  zone_id:                  ZONE-07
  asset_id:                 AST-STL-004 (Indira Nagar Sector 14 Public Lighting Line)
  authority_id:             AUTH-LMC (Electrical & Mechanical Department / EESL Concessionaire)
  responsibility_type:      MAINTENANCE (Luminaire Replacement)
  priority:                 LOW
  sla_rule_id:              SLA-RULE-010 (Target: 48h, Escalation: 72h)
  duplicate_status:         STANDALONE
  cluster_id:               NONE (Standalone residential lighting complaint)
  evidence_chain_id:        CHAIN-007 (CT-EVD-011: Severely blurred, pitch-black underexposure)
  evidence_status:          UNUSABLE (Confidence: 0.20)
  resolution_status:        INSUFFICIENT_EVIDENCE
  human_review_required:    TRUE (Unusable / degraded evidence gate)
  provenance:               SRC-013 (EESL SLNP Municipal LED Concession Framework)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Ingestion quality filter assesses CT-EVD-011 for sharpness, exposure, and landmark features.
  2. Categorizes image quality as UNUSABLE.
  3. Refuses automated processing based on degraded imagery; marks INSUFFICIENT_EVIDENCE.
  4. Requests user upload daytime photograph or routes for physical field verification.
```

```
================================================================================
CASE ID: GD-CASE-08
TITLE: Streetlight Failure vs Electrical Distribution Hazard (CONF-003)
================================================================================
INPUT COMPLAINT:
  "Sector Q crossing par streetlight nahi chal rahi aur distribution transformer pole se sparking ho rahi hai."
LANGUAGE:
  MIXED (Hindi / English)

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-019
  issue_category:           ELECTRICAL_INFRASTRUCTURE (Primary hazard: Arcing transformer / distribution safety)
  location_status:          APPROXIMATE (Latitude: 26.85184, Longitude: 80.92804)
  ward_id:                  WARD-109 (Aliganj)
  zone_id:                  ZONE-03
  asset_id:                 AST-ELE-003 (Aliganj Sector Q 11kV Distribution Transformer & Substation Feeder)
  authority_id:             AUTH-MVVNL (Madhyanchal Vidyut Vitran Nigam Limited - LESA)
  responsibility_type:      MAINTENANCE (Distribution Line & Transformer Maintenance)
  priority:                 CRITICAL
  sla_rule_id:              SLA-RULE-018 (Emergency Isolation: Target 4h, Escalation 8h)
  duplicate_status:         STANDALONE
  cluster_id:               NONE (Jurisdictional disambiguation anchor)
  evidence_chain_id:        CHAIN-004 (CT-EVD-006: Video frame of active arcing at transformer)
  evidence_status:          OPEN_HAZARD
  resolution_status:        NOT_RESOLVED (Open critical life-safety hazard)
  human_review_required:    FALSE (Deterministically routed to MVVNL via CONF-003)
  provenance:               SRC-008 (MVVNL / LESA Urban Distribution Division Directory)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Hazard Classifier detects compound mention of 'streetlight' and 'sparking transformer'.
  2. Applies Jurisdictional Conflict Rule CONF-003: Electrical distribution arcing supersedes
     routine luminaire repair.
  3. Overrides municipal lighting assignment; routes strictly to AUTH-MVVNL (LESA).
  4. Sets Priority to CRITICAL with 4h emergency pilot target (SLA-RULE-018).
```

```
================================================================================
CASE ID: GD-CASE-09
TITLE: Incomplete Location Intake & Jurisdictional Uncertainty (Difficult Case C)
================================================================================
INPUT COMPLAINT:
  "Market ke paas main road par bada gaddha hai, please jaldi repair karwayein."
LANGUAGE:
  HINGLISH

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-003
  issue_category:           POTHOLE (Subcategory: Pothole Repair / Unspecified Road Distress)
  location_status:          NEEDS_REVIEW (No GPS coordinates, no ward, no landmark, no colony named)
  ward_id:                  UNKNOWN
  zone_id:                  UNKNOWN
  asset_id:                 UNKNOWN
  authority_id:             NEEDS_REVIEW (Presumptive SRV-LMC-POTHOLE pending spatial localization)
  responsibility_type:      UNKNOWN
  priority:                 MEDIUM
  sla_rule_id:              SLA-RULE-001 (Presumptive)
  duplicate_status:         STANDALONE
  cluster_id:               NONE (Standalone unlocalized intake)
  evidence_chain_id:        CHAIN-003 (CT-EVD-005: Macro photo of asphalt hole; EXIF stripped)
  evidence_status:          INSUFFICIENT_EVIDENCE
  resolution_status:        INSUFFICIENT_EVIDENCE
  human_review_required:    TRUE (Missing coordinates, ward, and landmarks)
  provenance:               SRC-001 (LMC Central Helpline 1533 Directory)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Intake Parser detects complete absence of spatial landmarks and GPS coordinates.
  2. Refuses to guess or hallucinate an administrative ward or physical asset.
  3. Sets Ward, Zone, and Asset to 'UNKNOWN'.
  4. Flags Authority as 'NEEDS_REVIEW'.
  5. Places incident in intake triage queue with automated prompt for citizen location details.
```

```
================================================================================
CASE ID: GD-CASE-10
TITLE: High-Impact Repeat Grievance Escalation (Burst Potable Trunk Main)
================================================================================
INPUT COMPLAINT:
  Primary:  "ऐशबाग वाटर वर्क्स के पास मुख्य पेयजल पाइपलाइन फट गई है और सड़क पर हजारों लीटर पानी बर्बाद हो रहा है।" [HINDI - CT-INC-012]
  Repeat A: "ऐशबाग जलकल संस्थान के पास मुख्य पेयजल पाइपलाइन फट गई है और सड़क पर हजारों लीटर पानी बह रहा है।" [HINDI - CT-DUP-016]
  Repeat B: "Massive potable water trunk pipeline burst near Aishbagh Water Works pumping compound, clean drinking water gushing onto Mill Road." [ENGLISH - CT-DUP-017]
  Repeat C: "Aishbagh water works wali main pipeline se lagataar drinking water leak ho raha hai, sadak par paani bhara hai." [MIXED - CT-DUP-018]
LANGUAGE:
  HINDI (Primary & Repeat A), ENGLISH (Repeat B), MIXED (Repeat C)

BENCHMARK GROUND-TRUTH FIELDS:
  incident_id:              CT-INC-012
  issue_category:           BROKEN_PIPELINE (Subcategory: Burst Potable Water Trunk Main)
  location_status:          APPROXIMATE (Latitude: 26.84506, Longitude: 80.88655)
  ward_id:                  WARD-026 (Aishbagh)
  zone_id:                  ZONE-02
  asset_id:                 AST-WTR-001 (Aishbagh Water Works Primary Potable Trunk Main)
  authority_id:             AUTH-LKO-JALSANSTHAN (Lucknow Jal Sansthan - Water Supply Wing)
  responsibility_type:      OPERATION (Emergency Main Isolation & Repair)
  priority:                 CRITICAL
  sla_rule_id:              SLA-RULE-015 (Emergency Pipeline Burst: Target 6h, Escalation 12h)
  duplicate_status:         DUPLICATE_ANCHOR
  cluster_id:               CLUSTER-005 (Curated repeat duplicates: CT-DUP-016, 017, 018)
  evidence_chain_id:        NONE
  evidence_status:          EMERGENCY_PENDING
  resolution_status:        NOT_RESOLVED (Open critical utility disruption)
  human_review_required:    FALSE (High-velocity critical escalation)
  provenance:               SRC-011 (UP Act 43 of 1975 Section 18 & 24)

EXPECTED PROTOTYPE BEHAVIOR:
  1. Identifies critical potable trunk transmission infrastructure (AST-WTR-001).
  2. Aggregates multi-channel repeat complaints across languages into CLUSTER-005.
  3. Escalation Engine recognizes volume threshold on high-criticality water asset;
     compresses escalation timeframe and dispatches emergency alert to Jal Sansthan GM.
```

---

## Technical Handoff Notes for Phase 4 Implementation

1. **Intake API Contract**: The application intake must preserve original complaint text, original language encoding (`language`), and coordinate metadata without premature forced normalization.
2. **Deterministic Spatial Pipeline**: Spatial mapping must first evaluate point containment against `lucknow_wards.geojson` and `lucknow_zones.geojson`. If coordinates are missing or conflict with named text entities, the system must emit `NEEDS_REVIEW` rather than predicting an arbitrary ward.
3. **Lexicon Compliance**: All routed authorities must be validated against `data/authority/lucknow_authority_master.json`. If ambiguous (such as un-transferred LDA layouts), authority must be stored as `NEEDS_REVIEW`.
4. **Duplicate Scoring Benchmark**: Phase 4 deduplication models must evaluate against `data/lucknow/duplicates/duplicate_cases.csv`, ensuring that positive clusters (e.g., `CLUSTER-001`) are grouped while negative controls (`CLUSTER-007`) are cleanly segregated.
5. **Resolution Verification**: Prototype computer vision verification must evaluate BEFORE/AFTER evidence chains from `data/lucknow/evidence/evidence.csv`, verifying that unbacked closures (e.g., `CT-INC-014`) are rejected when contradictory visual evidence exists.
