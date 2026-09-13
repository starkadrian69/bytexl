import csv
import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.makedirs(os.path.join(BASE_DIR, "data/sources"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data/conflicts"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data/authority"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "scripts"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "docs"), exist_ok=True)

# ==============================================================================
# 1. SOURCE REGISTRY (data/sources/source_registry.csv)
# ==============================================================================
source_headers = [
    "source_id", "source_name", "source_type", "organization", "url",
    "document_title", "publication_date", "accessed_date", "relevant_topic",
    "authority_supported", "data_extracted", "verification_status", "notes"
]

sources_data = [
    [
        "SRC-001",
        "Lucknow Municipal Corporation Official Helpline & Contact Directory",
        "OFFICIAL_WEBSITE",
        "Lucknow Municipal Corporation",
        "https://lmc.up.nic.in/helpline.aspx",
        "LMC Official Contact and Helpline Directory",
        "NOT_PUBLICLY_AVAILABLE",
        "2026-09-11",
        "Municipal contact numbers, address, toll-free helpline, social handles",
        "AUTH-LMC",
        "Control Room Toll Free No. 1533; WhatsApp Nos 9219902911-14; Address Trilokinath Road Lalbagh Lucknow-226001; Email nnlko@nic.in",
        "VERIFIED",
        "Primary contact portal for LMC headquarters and central control room."
    ],
    [
        "SRC-002",
        "Lucknow Municipal Corporation Official Telephone Directory (Doorbhas Suchi)",
        "OFFICIAL_DOCUMENT",
        "Lucknow Municipal Corporation",
        "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf",
        "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "2024-08-01",
        "2026-09-11",
        "Executive leadership, department heads, zonal officers, executive engineers",
        "AUTH-LMC",
        "Designations and official CUG mobile numbers: Mayor, Municipal Commissioner, Addl Municipal Commissioners, Chief Engineers (Civil and E/M), Municipal Health Officer, Environment Engineer, 8 Zonal Officers, 8 Zonal Executive Engineers",
        "VERIFIED",
        "Official internal telephone directory hosted on LMC server."
    ],
    [
        "SRC-003",
        "Lucknow Municipal Corporation Sworn Corporators List 2023-2027",
        "OFFICIAL_DOCUMENT",
        "Lucknow Municipal Corporation",
        "https://lmc.up.nic.in/pdf/Corporator_2023_2027_sapath_date_26_05_2023_Main_List.pdf",
        "Sworn Corporators List 2023-2027 (Nagar Nigam Lucknow Nav Nirvachit Parshad List)",
        "2023-05-26",
        "2026-09-11",
        "Ward names, ward numbers, corporator details across 110 municipal wards",
        "AUTH-LMC",
        "Complete enumeration of 110 municipal wards (Ward 1 to Ward 110) with ward names, elected corporators, and residential contacts for 2023-2027 tenure",
        "VERIFIED",
        "Statutory list published pursuant to oath taken on 26-05-2023 following municipal general elections."
    ],
    [
        "SRC-004",
        "Lucknow Municipal Corporation Final Delimitation Notification 2022",
        "OFFICIAL_NOTIFICATION",
        "Department of Urban Development, Government of Uttar Pradesh",
        "https://lmc.up.nic.in/pdf/DelimiationfinalNotification31_10_2022HINDI.pdf",
        "Uttar Pradesh Gazette Delimitation Notification No. 1774/9-1-2022",
        "2022-10-31",
        "2026-09-11",
        "Municipal boundary delimitation, ward demarcation, zone allocation",
        "AUTH-LMC",
        "Statutory delimitation of Lucknow Nagar Nigam into 110 wards and 8 zones following inclusion of 88 peripheral revenue villages",
        "VERIFIED",
        "Definitive legal gazette establishing the 110-ward structure for the current municipal period (effective 31-Oct-2022)."
    ],
    [
        "SRC-005",
        "Uttar Pradesh Municipal Corporations Act, 1959",
        "OFFICIAL_DOCUMENT",
        "Legislative Department, Government of Uttar Pradesh",
        "https://lmc.up.nic.in/acts.aspx",
        "The Uttar Pradesh Municipal Corporations Act, 1959 (U.P. Act No. 2 of 1959)",
        "1959-01-01",
        "2026-09-11",
        "Statutory obligatory and discretionary duties of municipal corporations",
        "AUTH-LMC",
        "Chapter 5 (Powers and Duties of Authorities), Chapter 10 (Drains and Drainage), Chapter 11 (Water Supply), Chapter 12 (Streets and Public Roads), Chapter 15 (Scavenging and Cleansing / Solid Waste)",
        "VERIFIED",
        "Primary legislative enactment governing municipal duties, road maintenance, drainage, and sanitation."
    ],
    [
        "SRC-006",
        "Government of Uttar Pradesh Integrated Grievance Redressal System (Jansunwai-Samadhan)",
        "GOVERNMENT_PORTAL",
        "Lok Shikayat Vibhag, Chief Minister Office, Government of Uttar Pradesh",
        "https://jansunwai.up.nic.in",
        "Jansunwai - Integrated Grievance Redressal System Portal & Governance Manual",
        "2016-01-25",
        "2026-09-11",
        "Statewide citizen grievance registration, tracking, departmental routing, L1-L3 escalation hierarchy",
        "AUTH-LMC,AUTH-UPPWD,AUTH-MVVNL,AUTH-LKO-JALSANSTHAN,AUTH-UPJN-URBAN,AUTH-LDA",
        "Standard operating procedure for civic complaints, CM Helpline 1076, 3-tier grievance escalation hierarchy (L1 Field Officer, L2 Department Head / Municipal Commissioner, L3 District Magistrate / Secretary)",
        "VERIFIED",
        "Statewide overarching grievance redressal framework."
    ],
    [
        "SRC-007",
        "Public Works Department, Uttar Pradesh Official Web Portal & Organization Mandate",
        "OFFICIAL_WEBSITE",
        "Public Works Department, Government of Uttar Pradesh",
        "https://uppwd.gov.in",
        "UP PWD Citizen Charter, Role, Functions & Directory",
        "2024-09-05",
        "2026-09-11",
        "State highways, major district roads, arterial road construction and maintenance, Lucknow Circle",
        "AUTH-UPPWD",
        "UPPWD role, functions, organizational hierarchy (E-in-C, Chief Engineer Lucknow Zone, Superintending Engineer Lucknow Circle, Provincial Division Lucknow), road classification jurisdiction",
        "VERIFIED",
        "Official portal establishing PWD jurisdiction over non-municipal highways and major district roads."
    ],
    [
        "SRC-008",
        "Madhyanchal Vidyut Vitran Nigam Limited (MVVNL) Official Web Portal",
        "OFFICIAL_WEBSITE",
        "Madhyanchal Vidyut Vitran Nigam Limited / UPPCL",
        "https://www.mvvnl.in",
        "MVVNL Corporate Overview, Contact Directory & Consumer Services",
        "2024-07-13",
        "2026-09-11",
        "Electricity distribution, Lucknow Electricity Supply Administration (LESA), substation management, power outages, electrical poles",
        "AUTH-MVVNL",
        "Corporate office 4-A Gokhale Marg Lucknow; 1912 toll-free helpline; LESA urban electricity supply mandate; demarcation between power supply infrastructure and lighting fixtures",
        "VERIFIED",
        "Official portal for power distribution in Lucknow district."
    ],
    [
        "SRC-009",
        "Uttar Pradesh Jal Nigam (Urban) Official Web Portal",
        "OFFICIAL_WEBSITE",
        "Uttar Pradesh Jal Nigam (Urban), Department of Urban Development",
        "http://jn.upsdc.gov.in",
        "UP Jal Nigam (Urban) Organization Mandate & Project Portfolio",
        "2026-08-31",
        "2026-09-11",
        "Capital infrastructure for urban water supply, sewerage treatment plants (STPs), trunk sewers under AMRUT / Namami Gange",
        "AUTH-UPJN-URBAN",
        "Capital scheme execution, sewage treatment plant construction, major trunk lines; operational relief and transfer of maintenance to urban local bodies",
        "VERIFIED",
        "Official portal for state urban water/sewerage capital engineering."
    ],
    [
        "SRC-010",
        "District Administration Lucknow Official Portal (National Informatics Centre)",
        "GOVERNMENT_PORTAL",
        "District Administration Lucknow, Government of Uttar Pradesh",
        "https://lucknow.nic.in/who-is-who/",
        "District Administration Lucknow - Who is Who & Public Utilities Directory",
        "2024-08-01",
        "2026-09-11",
        "District leadership, administrative setup, inter-agency coordination, utility listings",
        "AUTH-LMC,AUTH-LDA,AUTH-UPPWD,AUTH-MVVNL",
        "Key administrative contacts: District Magistrate Lucknow (dmluc@nic.in, 9415005000), Vice Chairman LDA (0522-2307868), Municipal Commissioner Lucknow (8189077822), CDO Lucknow (9454465461)",
        "VERIFIED",
        "Official district government portal."
    ],
    [
        "SRC-011",
        "Uttar Pradesh Water Supply and Sewerage Act, 1975 & LMC Operational Records",
        "OFFICIAL_DOCUMENT",
        "Lucknow Jal Sansthan / Department of Urban Development, GoUP",
        "https://lmc.up.nic.in/procedure.aspx",
        "The Uttar Pradesh Water Supply and Sewerage Act, 1975 (U.P. Act No. 43 of 1975)",
        "1975-08-23",
        "2026-09-11",
        "Statutory constitution, functions and duties of Lucknow Jal Sansthan for water supply and sewerage operation & maintenance",
        "AUTH-LKO-JALSANSTHAN",
        "Section 18 & 20 establishing Jal Sansthan for Lucknow local area; Mayor as ex-officio Chairman; General Manager as executive head; operational responsibility for water distribution pipe leakages, potable supply, and sewer line clearance",
        "VERIFIED",
        "Authoritative statutory enactment and LMC operational procedure documentation."
    ],
    [
        "SRC-012",
        "Lucknow Development Authority Mandate & UP Urban Planning and Development Act, 1973",
        "OFFICIAL_DOCUMENT",
        "Lucknow Development Authority / Housing & Urban Planning Department, GoUP",
        "https://lucknow.nic.in/who-is-who/",
        "The Uttar Pradesh Urban Planning and Development Act, 1973 (U.P. Act No. 30 of 1973) & LDA Administrative Setup",
        "1973-09-02",
        "2026-09-11",
        "Urban development, colony infrastructure execution, road and civic maintenance in developing and un-transferred housing sectors",
        "AUTH-LDA",
        "Office of Vice Chairman LDA Lucknow (Phone 0522-2307868, Vipin Khand Gomti Nagar); infrastructure maintenance in planned schemes prior to formal municipal handover to LMC",
        "VERIFIED",
        "Statutory act and official district administration leadership listing."
    ],
    [
        "SRC-013",
        "Energy Efficiency Services Limited (EESL) / LMC Street Lighting National Programme Records",
        "OFFICIAL_DOCUMENT",
        "Energy Efficiency Services Limited / Lucknow Municipal Corporation",
        "https://eeslindia.org",
        "National Street Lighting Programme (SLNP) Implementation & Municipal Concession Framework",
        "2020-01-01",
        "2026-09-11",
        "Public street lighting retrofit, LED luminaire deployment, Centralized Control & Monitoring System (CCMS), operational maintenance concession",
        "AUTH-LMC",
        "Concessionaire operational framework supporting LMC Electrical & Mechanical Department for fixture repair and timer control, operating under LMC supervision (1533 helpline)",
        "VERIFIED",
        "Official national programme documentation and municipal partnership records."
    ]
]

with open(os.path.join(BASE_DIR, "data/sources/source_registry.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(source_headers)
    writer.writerows(sources_data)

print("Created data/sources/source_registry.csv successfully.")


# ==============================================================================
# 2. CONFLICT REGISTRY (data/conflicts/authority_conflicts.csv)
# ==============================================================================
conflict_headers = [
    "conflict_id", "field_name", "entity", "source_1", "value_1",
    "source_2", "value_2", "preferred_value", "reason", "resolution_status", "notes"
]

conflicts_data = [
    [
        "CONF-001",
        "ward_count",
        "Lucknow Municipal Corporation",
        "SRC-004",
        "110 Wards across 8 Zones",
        "SRC-010",
        "120 Wards (pre-delimitation public proposal following 88 village expansion in 2019-2020)",
        "110 Wards (current verified reference)",
        "UP Gazette Notification No. 1774/9-1-2022 dated 31-Oct-2022 definitively fixed the ward count at 110 for the 2023-2027 term. Draft proposals of 120 wards were not enacted.",
        "RESOLVED_WITH_CURRENT_SOURCE",
        "The current reference dataset reflects 110 wards; schema supports dynamic versioning for future delimitation changes."
    ],
    [
        "CONF-002",
        "water_sewer_operations_responsibility",
        "Water Supply & Sewerage Operations in Lucknow",
        "SRC-005",
        "Obligatory municipal duty under UP Municipal Corporations Act 1959 Ch 10 & 11",
        "SRC-011",
        "Special statutory utility responsibility under UP Water Supply and Sewerage Act 1975",
        "Lucknow Jal Sansthan for O&M; UP Jal Nigam for Capital infrastructure; LMC for municipal policy oversight",
        "The 1975 Act enacted specialized water/sewerage utilities in KAVAL cities. Lucknow Jal Sansthan handles daily water leakages and sewer chokes, chaired ex-officio by the Mayor of Lucknow.",
        "FUNCTIONAL_DECOMPOSITION_APPLIED",
        "Distinguishes operational water/sewer grievances from long-term capital construction."
    ],
    [
        "CONF-003",
        "streetlight_failure_responsibility",
        "Public Lighting vs Electrical Power Supply",
        "SRC-002",
        "LMC Electrical & Mechanical Department (supported by EESL concession)",
        "SRC-008",
        "Madhyanchal Vidyut Vitran Nigam Limited (MVVNL / LESA)",
        "Tiered infrastructure routing: LMC for luminaire/fixture/switching; MVVNL for power supply, feeder, transformer, pole damage",
        "A citizen report of dark streetlights can be caused by a defective bulb/fixture (LMC) or a dead power distribution phase/pole damage (MVVNL).",
        "INFRASTRUCTURE_DECOMPOSITION_APPLIED",
        "CivicTrace AI and rules engine must separate luminaire faults from upstream power outages."
    ],
    [
        "CONF-004",
        "road_maintenance_responsibility",
        "Road Infrastructure in Lucknow District",
        "SRC-005",
        "LMC Civil Engineering Department for municipal roads and streets",
        "SRC-007",
        "UP PWD Lucknow Circle for State Highways and Major District Roads; LDA (SRC-012) for un-transferred sectors",
        "Jurisdiction-aware routing: LMC for municipal colony roads; UP PWD for State Highways & MDRs; LDA for developing un-transferred layouts",
        "Road responsibility is legally fragmented across urban tiers. Routing depends deterministically on road hierarchy and GIS spatial layer.",
        "JURISDICTION_AWARE_ROUTING_APPLIED",
        "POTHOLE cannot route universally to a single authority without road classification context."
    ]
]

with open(os.path.join(BASE_DIR, "data/conflicts/authority_conflicts.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(conflict_headers)
    writer.writerows(conflicts_data)

print("Created data/conflicts/authority_conflicts.csv successfully.")


# ==============================================================================
# 3. PRIMARY CSV MASTER (data/authority/lucknow_authority_lexicon_master.csv)
# ==============================================================================
master_headers = [
    "record_id", "authority_id", "authority_name", "authority_type",
    "parent_authority_id", "parent_authority_name", "administrative_level",
    "city", "district", "state", "department_id", "department_name",
    "department_type", "service_id", "service_name", "service_description",
    "issue_category_id", "issue_category", "issue_subcategory",
    "jurisdiction_type", "zone", "ward", "local_jurisdiction",
    "responsibility_scope", "responsibility_status", "contact_name",
    "contact_designation", "contact_phone", "contact_email", "office_address",
    "official_portal", "grievance_portal", "escalation_level_1",
    "escalation_level_2", "escalation_level_3", "operating_hours",
    "source_id", "source_url", "source_title", "source_page_or_section",
    "source_date", "source_type", "source_confidence", "verification_status",
    "last_verified", "notes"
]

master_records = [
    # 1. LMC General Civic Services
    [
        "AUTH-001", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "CITY",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-ADMIN", "Central Municipal Administration",
        "OTHER", "SRV-LMC-GENERAL", "General Civic Inquiries & Service Coordination",
        "Central administration and helpline dispatch for municipal civic grievances.",
        "GENERAL_CIVIC", "General Civic", "General Municipal Assistance",
        "CITY", "ALL", "ALL", "Municipal Corporation Limits",
        "Overall municipal governance, citizen grievance reception, and inter-departmental routing.",
        "VERIFIED", "Shri Gaurav Kumar", "Nagar Ayukt (Municipal Commissioner)", "8189077822",
        "nnlko@nic.in", "Lucknow Nagar Nigam Headquarters, Trilokinath Road, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Zonal Officer", "Additional Municipal Commissioner", "Municipal Commissioner",
        "24x7 Control Room; Office Hours 10:00 - 17:00",
        "SRC-001", "https://lmc.up.nic.in/helpline.aspx", "LMC Official Contact and Helpline Directory",
        "Control Room & Office Directory", "2024-08-01", "OFFICIAL_WEBSITE", "HIGH",
        "VERIFIED", "2026-09-11", "Central gateway for municipal complaints via 1533 helpline."
    ],
    # 2. LMC Road Maintenance - Pothole
    [
        "AUTH-002", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL", "Civil Engineering Department",
        "ROADS", "SRV-LMC-POTHOLE", "Municipal Road Pothole Filling & Patchwork",
        "Repair and filling of potholes on internal colony streets, link roads, and municipal sector roads.",
        "POTHOLE", "Road", "Pothole Repair",
        "ROAD", "ALL", "ALL", "Municipal Roads and Colony Streets",
        "Maintenance, pothole filling, and bituminous patching on roads vested in Lucknow Municipal Corporation.",
        "VERIFIED", "Shri Mahesh Chandra Verma", "Chief Engineer (Civil/General)", "8810721504",
        "nnlko@nic.in", "Civil Engineering Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Civil) / Assistant Engineer (Civil)", "Executive Engineer (Civil) of Zone", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 9 (Chief Engineer Civil)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Statutory duty under UP Municipal Corporations Act 1959 Ch 12; covers roads under LMC jurisdiction only."
    ],
    # 3. LMC Road Maintenance - Road Damage
    [
        "AUTH-003", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL", "Civil Engineering Department",
        "ROADS", "SRV-LMC-ROAD-REPAIR", "Municipal Road Surface Reconstruction & Damage Repair",
        "Resurfacing, reconstruction, and structural repair of damaged municipal roads and caved-in surfaces.",
        "ROAD_DAMAGE", "Road", "Road Damage / Road Collapse",
        "ROAD", "ALL", "ALL", "Municipal Roads and Colony Streets",
        "Structural repair, leveling, and reconstruction of eroded or collapsed municipal asphalt and concrete roads.",
        "VERIFIED", "Shri Mahesh Chandra Verma", "Chief Engineer (Civil/General)", "8810721504",
        "nnlko@nic.in", "Civil Engineering Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Civil) / Assistant Engineer (Civil)", "Executive Engineer (Civil) of Zone", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-005", "https://lmc.up.nic.in/acts.aspx", "The Uttar Pradesh Municipal Corporations Act, 1959",
        "Chapter 12 (Streets and Public Roads)", "1959-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Obligatory duty under Section 114(29) of UP Municipal Corporations Act 1959."
    ],
    # 4. LMC Road Maintenance - Damaged Footpath
    [
        "AUTH-004", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL", "Civil Engineering Department",
        "ROADS", "SRV-LMC-FOOTPATH", "Municipal Footpath & Pedestrian Walkway Maintenance",
        "Repair and maintenance of pedestrian footpaths, interlocking pavers, and kerbstones.",
        "DAMAGED_FOOTPATH", "Road", "Damaged Footpath / Broken Pavement",
        "ROAD", "ALL", "ALL", "Pedestrian Footpaths along Municipal Roads",
        "Repair of broken pavement tiles, missing kerbstones, and pedestrian walkway hazards along LMC roads.",
        "VERIFIED", "Shri Mahesh Chandra Verma", "Chief Engineer (Civil/General)", "8810721504",
        "nnlko@nic.in", "Civil Engineering Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Civil) / Assistant Engineer (Civil)", "Executive Engineer (Civil) of Zone", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-005", "https://lmc.up.nic.in/acts.aspx", "The Uttar Pradesh Municipal Corporations Act, 1959",
        "Chapter 12 Section 114", "1959-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Ensures barrier-free pedestrian infrastructure along public streets."
    ],
    # 5. LMC Sanitation - Garbage Accumulation
    [
        "AUTH-005", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-SWM", "Health & Sanitation Department",
        "SANITATION", "SRV-LMC-GARBAGE-COLLECTION", "Municipal Solid Waste Collection & Street Sweeping",
        "Daily street sweeping, residential waste collection, and clearance of accumulated roadside garbage.",
        "GARBAGE_ACCUMULATION", "Sanitation", "Unattended Garbage Accumulation",
        "WARD", "ALL", "ALL", "All Wards and Public Spaces",
        "Door-to-door solid waste collection, street sweeping, and primary transportation to secondary collection points.",
        "VERIFIED", "Shri Nand Kishore", "Municipal Health Officer (Nagar Swasthya Adhikari)", "8810721509",
        "nnlko@nic.in", "Health & Sanitation Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Sanitary Inspector (Ward Level)", "Zonal Sanitary Officer / Zonal Officer", "Municipal Health Officer",
        "Morning Operations 06:00 - 14:00; Control Room 24x7",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 7 (Nagar Swasthya Adhikari)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Supported by Environment Engineer Shri Sanjeev Pradhan (8726796666)."
    ],
    # 6. LMC Sanitation - Illegal Dumping
    [
        "AUTH-006", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-SWM", "Health & Sanitation Department",
        "SANITATION", "SRV-LMC-ILLEGAL-DUMPING", "Illegal Garbage Dumping Removal & Enforcement",
        "Removal of unauthorized garbage dumping from vacant plots, roadside berms, and public spaces.",
        "ILLEGAL_DUMPING", "Sanitation", "Open Waste Dumping on Public Land",
        "LOCALITY", "ALL", "ALL", "Public Spaces, Berms and Open Plots",
        "Clearing unauthorized open refuse mounds, deploying mobile lifting teams, and imposing municipal fines.",
        "VERIFIED", "Shri Sanjeev Pradhan", "Environment Engineer (Paryavaran Abhiyanta)", "8726796666",
        "nnlko@nic.in", "Solid Waste Management Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Sanitary Inspector / Zonal Sanitary Officer", "Environment Engineer", "Municipal Health Officer",
        "Operating Hours 06:00 - 18:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 27 (Paryavaran Abhiyanta)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Includes spot challaning under SWM Rules 2016 and LMC bylaws."
    ],
    # 7. LMC Sanitation - Overflowing Garbage Bin
    [
        "AUTH-007", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-SWM", "Health & Sanitation Department",
        "SANITATION", "SRV-LMC-BIN-CLEARANCE", "Community Garbage Bin & Compactor Clearance",
        "Emptying, clearing, and sanitizing overflowing community bins, dumper placers, and dhalao ghars.",
        "OVERFLOWING_BIN", "Sanitation", "Overflowing Garbage Bin / Dhalao Ghar",
        "LOCALITY", "ALL", "ALL", "Community Bin Locations and Transfer Stations",
        "Timely mechanised lifting and transfer of secondary waste containers to prevent overflow and litter.",
        "VERIFIED", "Shri Nand Kishore", "Municipal Health Officer (Nagar Swasthya Adhikari)", "8810721509",
        "nnlko@nic.in", "Health & Sanitation Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Sanitary Inspector / RR Workshop Dispatcher", "Zonal Sanitary Officer", "Municipal Health Officer",
        "Daily Shifts 06:00 - 22:00",
        "SRC-005", "https://lmc.up.nic.in/acts.aspx", "The Uttar Pradesh Municipal Corporations Act, 1959",
        "Chapter 15 (Scavenging and Cleansing)", "1959-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Transport fleet coordinated via LMC RR Workshop (Chief Engineer E/M)."
    ],
    # 8. LMC Street Lighting - Streetlight Failure
    [
        "AUTH-008", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-ELEC", "Electrical & Mechanical Department",
        "ELECTRICAL", "SRV-LMC-STREETLIGHT-REPAIR", "Streetlight Luminaire & Fixture Repair",
        "Restoring non-functional streetlights, replacing burned LED luminaires, and repairing lamp fixtures.",
        "STREETLIGHT_FAILURE", "Streetlight", "Streetlight Not Glowing / Dark Street",
        "WARD", "ALL", "ALL", "Public Streets and Municipal Road Lighting",
        "Maintenance, repair, and replacement of defective municipal streetlights and LED fittings.",
        "VERIFIED", "Shri Manoj Prabhat", "Chief Engineer (Electrical/Mechanical)", "8860311555",
        "nnlko@nic.in", "Electrical & Mechanical Wing, RR Workshop, LMC, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Electrical) / EESL Field Team", "Assistant Engineer (Electrical)", "Chief Engineer (Electrical/Mechanical)",
        "24x7 Monitoring via CCMS; Field Repairs 09:00 - 18:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 10 (Chief Engineer Electrical/Mechanical)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Supported by concessionaire EESL (SRC-013) for LED fixtures. Excludes upstream power outages."
    ],
    # 9. LMC Street Lighting - Streetlight Damage
    [
        "AUTH-009", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-ELEC", "Electrical & Mechanical Department",
        "ELECTRICAL", "SRV-LMC-STREETLIGHT-HARDWARE", "Streetlight Bracket, Fitting & Hardware Maintenance",
        "Repair and replacement of damaged streetlight brackets, broken diffusers, hanging fixtures, and timer switches.",
        "STREETLIGHT_DAMAGE", "Streetlight", "Damaged Streetlight Fixture / Broken Bracket",
        "LOCALITY", "ALL", "ALL", "Streetlight Poles and Municipal Fixtures",
        "Rectification of physically damaged municipal streetlight fixtures, brackets, arm mountings, and local timer panels.",
        "VERIFIED", "Shri Manoj Prabhat", "Chief Engineer (Electrical/Mechanical)", "8860311555",
        "nnlko@nic.in", "Electrical & Mechanical Wing, RR Workshop, LMC, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Electrical) / EESL Field Technician", "Assistant Engineer (Electrical)", "Chief Engineer (Electrical/Mechanical)",
        "Field Operations 09:00 - 18:00",
        "SRC-013", "https://eeslindia.org", "National Street Lighting Programme (SLNP) Implementation Framework",
        "Hardware Maintenance Clause", "2020-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Applies to municipal lighting fixtures. If the entire utility pole has collapsed, MVVNL (SRC-008) is responsible."
    ],
    # 10. LMC Drainage - Blocked Drain
    [
        "AUTH-010", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL", "Civil Engineering Department",
        "DRAINAGE", "SRV-LMC-DRAIN-CLEANING", "Stormwater Drain Desilting & Unblocking",
        "Desilting, unclogging, and clearing choke points in roadside stormwater drains and open channels.",
        "BLOCKED_DRAIN", "Drainage", "Clogged Stormwater Drain / Silted Nala",
        "LOCALITY", "ALL", "ALL", "Roadside Stormwater Drains and Municipal Nalas",
        "Cleaning, desilting, and unblocking surface stormwater drains and secondary drains to maintain gravity flow.",
        "VERIFIED", "Shri Mahesh Chandra Verma", "Chief Engineer (Civil/General)", "8810721504",
        "nnlko@nic.in", "Civil Engineering Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Junior Engineer (Civil) / Sanitary Inspector", "Executive Engineer (Civil) of Zone", "Chief Engineer (Civil)",
        "Daily Shifts 08:00 - 16:00",
        "SRC-005", "https://lmc.up.nic.in/acts.aspx", "The Uttar Pradesh Municipal Corporations Act, 1959",
        "Chapter 10 (Drains and Drainage)", "1959-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Executed jointly by Civil Wing (structural maintenance) and Sanitation Wing (silt clearance)."
    ],
    # 11. LMC Drainage - Waterlogging
    [
        "AUTH-011", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL", "Civil Engineering Department",
        "DRAINAGE", "SRV-LMC-WATERLOGGING-PUMPING", "Waterlogging Mitigation & Emergency Dewatering",
        "Emergency pumping, drain outfall clearance, and relief operations for rainwater accumulation on streets.",
        "WATERLOGGING", "Drainage", "Waterlogging on Public Street",
        "LOCALITY", "ALL", "ALL", "Low-lying Roads, Intersections, and Settlements",
        "Deployment of mobile dewatering pumps, clearing choked outfalls, and relieving inundation on public roads.",
        "VERIFIED", "Shri Mahesh Chandra Verma", "Chief Engineer (Civil/General)", "8810721504",
        "nnlko@nic.in", "Civil Engineering Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Zonal Executive Engineer (Civil)", "Zonal Officer", "Chief Engineer (Civil)",
        "24x7 Emergency Response during Monsoon",
        "SRC-005", "https://lmc.up.nic.in/acts.aspx", "The Uttar Pradesh Municipal Corporations Act, 1959",
        "Chapter 10 Section 114", "1959-01-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Coordinated with Lucknow Smart City ICCC Control Room during heavy rainfall."
    ],
    # 12. Lucknow Jal Sansthan - Water Leakage
    [
        "AUTH-012", "AUTH-LKO-JALSANSTHAN", "Lucknow Jal Sansthan", "PUBLIC_UTILITY",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "CITY",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-JS-WATER", "Water Distribution & Maintenance Wing",
        "WATER", "SRV-JS-LEAK-REPAIR", "Potable Water Distribution Pipeline Leakage Repair",
        "Repair and sealing of leaks in underground and surface municipal drinking water distribution pipelines.",
        "WATER_LEAKAGE", "Water", "Water Distribution Pipe Leakage",
        "CITY", "ALL", "ALL", "Lucknow Urban Water Supply Network",
        "Operation, maintenance, and leak rectifications on municipal drinking water supply feeder mains and distribution pipelines.",
        "VERIFIED", "Shri Ram Kumar", "General Manager (Mahaprabandhak)", "0522-2622617",
        "nnlko@nic.in", "Jal Sansthan Head Office, Lalbagh / Aishbagh Water Works, Lucknow-226004",
        "https://lmc.up.nic.in/procedure.aspx", "https://jansunwai.up.nic.in",
        "Junior Engineer (Water) / Assistant Engineer (Water)", "Executive Engineer (Jal Sansthan) of Zone", "General Manager (Jal Sansthan)",
        "24x7 Jal Sansthan Control Room (0522-2622617 / 1533)",
        "SRC-011", "https://lmc.up.nic.in/procedure.aspx", "The Uttar Pradesh Water Supply and Sewerage Act, 1975",
        "Section 18 & 24 (Water Supply Functions)", "1975-08-23", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Mayor of Lucknow serves as ex-officio Chairman; complaints also accepted through LMC 1533."
    ],
    # 13. Lucknow Jal Sansthan - Broken Pipeline
    [
        "AUTH-013", "AUTH-LKO-JALSANSTHAN", "Lucknow Jal Sansthan", "PUBLIC_UTILITY",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "CITY",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-JS-WATER", "Water Distribution & Maintenance Wing",
        "WATER", "SRV-JS-BURST-PIPE", "Drinking Water Main / Service Pipe Burst Repair",
        "Emergency replacement and heavy joint welding for major ruptured water mains and broken distribution lines.",
        "BROKEN_PIPELINE", "Water", "Burst Water Main / Severed Distribution Pipe",
        "LOCALITY", "ALL", "ALL", "Lucknow Urban Potable Pipeline Network",
        "Emergency excavation, pipeline isolation, replacement, and restoration of burst drinking water pipes.",
        "VERIFIED", "Shri Ram Kumar", "General Manager (Mahaprabandhak)", "0522-2622617",
        "nnlko@nic.in", "Jal Sansthan Head Office, Lalbagh / Aishbagh Water Works, Lucknow-226004",
        "https://lmc.up.nic.in/procedure.aspx", "https://jansunwai.up.nic.in",
        "Assistant Engineer (Water)", "Executive Engineer (Jal Sansthan) of Zone", "General Manager (Jal Sansthan)",
        "24x7 Emergency Pipeline Squad",
        "SRC-011", "https://lmc.up.nic.in/procedure.aspx", "The Uttar Pradesh Water Supply and Sewerage Act, 1975",
        "Section 24 (Maintenance & Operations)", "1975-08-23", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Requires coordination with LMC Civil Wing for road cutting and reinstatement."
    ],
    # 14. Lucknow Jal Sansthan - Sewer Overflow
    [
        "AUTH-014", "AUTH-LKO-JALSANSTHAN", "Lucknow Jal Sansthan", "PUBLIC_UTILITY",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "CITY",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-JS-SEWER", "Sewerage Operations & Maintenance Wing",
        "SEWER", "SRV-JS-SEWER-CLEARANCE", "Sewer Line Clearance & Manhole Overflow Redressal",
        "Clearing choked sewer lines, unblocking underground sewage conduits, and abating manhole overflow.",
        "SEWER_OVERFLOW", "Sewer", "Overflowing Sewer Line / Surging Manhole",
        "LOCALITY", "ALL", "ALL", "Municipal Underground Sewerage Network",
        "Operation and routine maintenance of municipal sewer reticulation, suction jetting, and clearing sewer surcharges.",
        "VERIFIED", "Shri Ram Kumar", "General Manager (Mahaprabandhak)", "0522-2622617",
        "nnlko@nic.in", "Jal Sansthan Head Office, Lalbagh / Aishbagh Water Works, Lucknow-226004",
        "https://lmc.up.nic.in/procedure.aspx", "https://jansunwai.up.nic.in",
        "Junior Engineer (Sewer) / Jetting Machine Operator", "Executive Engineer (Jal Sansthan) of Zone", "General Manager (Jal Sansthan)",
        "Daily Operations 07:00 - 19:00; Emergency 24x7",
        "SRC-011", "https://lmc.up.nic.in/procedure.aspx", "The Uttar Pradesh Water Supply and Sewerage Act, 1975",
        "Section 24 (Sewerage Services)", "1975-08-23", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Super sucker and high-pressure jetting machines deployed across zones."
    ],
    # 15. UP PWD - Major Road Damage
    [
        "AUTH-015", "AUTH-UPPWD", "Public Works Department, Uttar Pradesh", "STATE_DEPARTMENT",
        "AUTH-GOUP", "Government of Uttar Pradesh", "DISTRICT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-PWD-LKO-CIRCLE", "Lucknow Circle (Provincial Division)",
        "ROADS", "SRV-PWD-ROAD-REPAIR", "State Highway & Major District Road Maintenance",
        "Repairing potholes, structural failures, and bitumen deterioration on PWD State Highways and Major District Roads.",
        "ROAD_DAMAGE", "Road", "Major Road Damage / PWD Arterial Road Potholes",
        "ROAD", "DISTRICT", "NOT_APPLICABLE", "Designated PWD Corridors, State Highways and MDRs",
        "Maintenance and capital reconstruction of arterial state highways, major district roads (MDRs), and other district roads (ODRs) in Lucknow.",
        "VERIFIED", "Shri Anil Kumar Dubey", "Chief Engineer (HQ-1) / Web Info Manager", "0522-2236496",
        "cehq1-pwd-up@nic.in", "UP PWD Headquarters, 96 Mahatma Gandhi Marg, Hazratganj, Lucknow-226001",
        "https://uppwd.gov.in", "https://jansunwai.up.nic.in",
        "Assistant Engineer (PWD Provincial Division)", "Executive Engineer (Provincial Division PWD Lucknow)", "Superintending Engineer (Lucknow Circle PWD)",
        "Office Hours 10:00 - 17:00",
        "SRC-007", "https://uppwd.gov.in", "UP PWD Citizen Charter, Role, Functions & Directory",
        "Role, Functions and Organization Structure", "2024-09-05", "OFFICIAL_WEBSITE", "HIGH",
        "VERIFIED", "2026-09-11", "LMC has no maintenance authority on PWD roads; GIS spatial layer routes these issues to UP PWD."
    ],
    # 16. MVVNL - Electrical Infrastructure & Power Supply
    [
        "AUTH-016", "AUTH-MVVNL", "Madhyanchal Vidyut Vitran Nigam Limited", "PUBLIC_UTILITY",
        "AUTH-UPPCL", "Uttar Pradesh Power Corporation Limited", "DISTRICT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-MVVNL-LESA", "Lucknow Electricity Supply Administration (LESA)",
        "ELECTRICAL", "SRV-MVVNL-POWER-SUPPLY", "Electricity Distribution & Streetlight Power Circuit Maintenance",
        "Restoring electricity supply to public lighting circuits, repairing distribution transformers, and fixing tripped power lines.",
        "POWER_OUTAGE", "Electrical", "Area Power Supply Failure / Streetlight Circuit Tripped",
        "LOCALITY", "ALL", "ALL", "33/11kV Distribution Network and Substation Feeders",
        "Distribution and retail supply of electricity in Lucknow urban and rural supply zones, including power feeding streetlighting control panels.",
        "VERIFIED", "Managing Director MVVNL", "Managing Director", "0522-2208737",
        "1912@mvvnl.org", "MVVNL Head Office, 4-A Gokhale Marg, Lucknow-226001",
        "https://www.mvvnl.in", "https://1912.uppcl.org",
        "Junior Engineer (LESA Substation)", "Sub-Divisional Officer (SDO LESA)", "Executive Engineer (Distribution Division LESA)",
        "24x7 Consumer Call Centre (1912)",
        "SRC-008", "https://www.mvvnl.in", "MVVNL Corporate Overview, Contact Directory & Consumer Services",
        "Contact Directory & About MVVNL", "2024-07-13", "OFFICIAL_WEBSITE", "HIGH",
        "VERIFIED", "2026-09-11", "Responsible for power delivery up to the meter/pole. Excludes luminaire bulb maintenance."
    ],
    # 17. MVVNL - Damaged Electrical Pole / Dangerous Snapped Conductor
    [
        "AUTH-017", "AUTH-MVVNL", "Madhyanchal Vidyut Vitran Nigam Limited", "PUBLIC_UTILITY",
        "AUTH-UPPCL", "Uttar Pradesh Power Corporation Limited", "DISTRICT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-MVVNL-LESA", "Lucknow Electricity Supply Administration (LESA)",
        "ELECTRICAL", "SRV-MVVNL-LINE-MAINTENANCE", "Overhead Distribution Line & Electrical Pole Maintenance",
        "Replacement of leaning/damaged utility poles, restringing snapped LT/HT conductors, and eliminating public electrical hazards.",
        "ELECTRICAL_INFRASTRUCTURE", "Electrical", "Damaged Electrical Pole / Dangerous Snapped Wire",
        "LOCALITY", "ALL", "ALL", "Distribution Lines and Poles across Lucknow",
        "Ensuring structural safety of electricity distribution poles, stays, overhead lines, and distribution transformer substations.",
        "VERIFIED", "Managing Director MVVNL", "Managing Director", "0522-2208737",
        "1912@mvvnl.org", "MVVNL Head Office, 4-A Gokhale Marg, Lucknow-226001",
        "https://www.mvvnl.in", "https://1912.uppcl.org",
        "Junior Engineer (LESA Line Maintenance)", "Sub-Divisional Officer (SDO LESA)", "Executive Engineer (Distribution Division LESA)",
        "24x7 Emergency Breakdown Service (1912)",
        "SRC-008", "https://www.mvvnl.in", "MVVNL Corporate Overview, Contact Directory & Consumer Services",
        "Consumer Safety & Breakdown Guidelines", "2024-07-13", "OFFICIAL_WEBSITE", "HIGH",
        "VERIFIED", "2026-09-11", "Critical public safety issue. Even if streetlight is mounted on pole, pole replacement belongs to MVVNL."
    ],
    # 18. UP Jal Nigam (Urban) - Capital Water & Sewerage Infrastructure
    [
        "AUTH-018", "AUTH-UPJN-URBAN", "Uttar Pradesh Jal Nigam (Urban)", "PUBLIC_UTILITY",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "STATE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-UPJN-CONSTR", "Capital Projects & Construction Wing",
        "WATER", "SRV-UPJN-CAPITAL-WORKS", "Major Trunk Sewer & Water Augmentation Scheme Construction",
        "Planning, designing, and constructing Sewage Treatment Plants (STPs), Water Treatment Plants (WTPs), and trunk mains.",
        "SEWER_INFRASTRUCTURE", "Sewer", "Major Trunk Sewer Construction / STP Defect",
        "CITY", "ALL", "ALL", "Capital Water & Sewer Infrastructure Schemes",
        "Capital scheme execution under AMRUT, SBM 2.0, and Namami Gange. Does not handle routine consumer pipe leaks.",
        "VERIFIED", "Managing Director UP Jal Nigam", "Managing Director (Urban)", "0522-2626395",
        "md@upjn.org", "UP Jal Nigam Head Office, 6 Rana Pratap Marg, Hazratganj, Lucknow-226001",
        "http://jn.upsdc.gov.in", "https://jansunwai.up.nic.in",
        "Executive Engineer (Construction Division UPJN)", "Superintending Engineer (UP Jal Nigam)", "Chief Engineer (UP Jal Nigam Urban)",
        "Office Hours 10:00 - 17:00",
        "SRC-009", "http://jn.upsdc.gov.in", "UP Jal Nigam (Urban) Organization Mandate & Project Portfolio",
        "Role, Functions & Responsibilities", "2026-08-31", "OFFICIAL_WEBSITE", "HIGH",
        "VERIFIED", "2026-09-11", "Once schemes are completed, O&M is handed over to Lucknow Jal Sansthan."
    ],
    # 19. Lucknow Development Authority - Un-transferred Scheme Road Damage
    [
        "AUTH-019", "AUTH-LDA", "Lucknow Development Authority", "DEVELOPMENT_AUTHORITY",
        "AUTH-GOUP-HUPD", "Housing and Urban Planning Department, Government of Uttar Pradesh", "CITY",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LDA-ENG", "Engineering Division",
        "ROADS", "SRV-LDA-SECTOR-MAINT", "Civic Infrastructure Maintenance in Un-transferred Sectors",
        "Road maintenance, drainage repairs, and civic upkeep in planned LDA layouts prior to formal municipal handover to LMC.",
        "ROAD_DAMAGE", "Road", "Road Damage in Un-transferred LDA Sector",
        "LOCALITY", "NOT_APPLICABLE", "NOT_APPLICABLE", "LDA Schemes (e.g., Basant Kunj, CG City, Gomti Nagar Extension Sectors)",
        "Construction and interim maintenance of roads, stormwater drains, and streetlights in LDA developed sectors before gazetted municipal transfer.",
        "PARTIALLY_VERIFIED", "Shri Prathmesh Kumar", "Vice Chairman LDA", "0522-2307868",
        "vc@ldaonline.in", "Lucknow Development Authority Headquarters, Vipin Khand, Gomti Nagar, Lucknow-226010",
        "https://ldaonline.co.in", "https://jansunwai.up.nic.in",
        "Assistant Engineer (LDA Engineering Division)", "Executive Engineer (LDA Zone)", "Chief Engineer (LDA)",
        "Office Hours 10:00 - 17:00",
        "SRC-012", "https://lucknow.nic.in/who-is-who/", "The Uttar Pradesh Urban Planning and Development Act, 1973",
        "Section 15 & LDA Leadership Setup", "1973-09-02", "OFFICIAL_DOCUMENT", "MEDIUM",
        "VERIFIED", "2026-09-11", "Jurisdiction applies to development sectors where final municipal maintenance handover resolution has not yet been passed by LMC."
    ],
    # 20. LMC Animal Welfare - Stray Cattle / Dead Animal Carcass
    [
        "AUTH-020", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "DEPARTMENT",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-VET", "Animal Welfare Department",
        "OTHER", "SRV-LMC-ANIMAL-CONTROL", "Stray Cattle Impounding & Animal Carcass Removal",
        "Catching and impounding stray cattle from roads, managing Kanha Upwan cowshed, and lifting dead animal carcasses.",
        "ANIMAL_NUISANCE", "Sanitation", "Stray Cattle Traffic Hazard / Dead Animal Carcass",
        "CITY", "ALL", "ALL", "Public Streets and Municipal Thoroughfares",
        "Control of stray cattle causing road hazards, impounding in municipal cattle pounds, and rapid removal of dead animal carcasses.",
        "VERIFIED", "Dr. Abhinav Verma", "Veterinary Welfare Officer (Pashu Chikitsa Kalyan Adhikari)", "8810729191",
        "nnlko@nic.in", "Animal Welfare Wing, LMC Headquarters, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Veterinary Inspector / Cattle Catching Squad Leader", "Veterinary Welfare Officer", "Additional Municipal Commissioner",
        "24x7 Carcass Lifting Helpline via 1533",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 16 (Pashu Chikitsa Kalyan Adhikari)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Key road safety factor preventing stray cattle traffic accidents."
    ],
    # 21-28. LMC Zonal Executive Engineers (Civil) - Zone 1 to Zone 8
    [
        "AUTH-021", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z1", "Civil Engineering Division (Zone 1)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z1", "Zonal Municipal Road and Drain Maintenance (Zone 1)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 1.",
        "POTHOLE", "Road", "Pothole in Zone 1",
        "ZONE", "Zone-1", "ALL", "Zone 1 Wards (Hazratganj, Raj Bhavan, Narhi, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 1.",
        "VERIFIED", "Shri Atul Mishra", "Executive Engineer (Zone-1 & Zone-4)", "8810721522",
        "nnlko@nic.in", "Zone 1 Office, Lalbagh, Lucknow-226001",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 1)", "Executive Engineer (Zone 1)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 28 (Executive Engineer Zone 1 & 4)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-1 is Shri Om Prakash Singh (8874241500)."
    ],
    [
        "AUTH-022", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z2", "Civil Engineering Division (Zone 2)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z2", "Zonal Municipal Road and Drain Maintenance (Zone 2)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 2.",
        "POTHOLE", "Road", "Pothole in Zone 2",
        "ZONE", "Zone-2", "ALL", "Zone 2 Wards (Aishbagh, Kundari Rakabganj, Motinagar, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 2.",
        "VERIFIED", "Shri Devendra Dhiman", "Executive Engineer (Zone-2)", "8004626599",
        "nnlko@nic.in", "Zone 2 Office, Aishbagh, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 2)", "Executive Engineer (Zone 2)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 29 (Executive Engineer Zone 2)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-2 is Shri Manoj Yadav (8318813463)."
    ],
    [
        "AUTH-023", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z3", "Civil Engineering Division (Zone 3)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z3", "Zonal Municipal Road and Drain Maintenance (Zone 3)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 3.",
        "POTHOLE", "Road", "Pothole in Zone 3",
        "ZONE", "Zone-3", "ALL", "Zone 3 Wards (Aliganj, Mahanagar, Nishatganj, Vikas Nagar, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 3.",
        "VERIFIED", "Shri Najmi Muzaffar", "Executive Engineer (Zone-3)", "8960958949",
        "nnlko@nic.in", "Zone 3 Office, Sector E Aliganj, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 3)", "Executive Engineer (Zone 3)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 30 (Executive Engineer Zone 3)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-3 is Shri Ajit Rai (8528907375)."
    ],
    [
        "AUTH-024", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z4", "Civil Engineering Division (Zone 4)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z4", "Zonal Municipal Road and Drain Maintenance (Zone 4)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 4.",
        "POTHOLE", "Road", "Pothole in Zone 4",
        "ZONE", "Zone-4", "ALL", "Zone 4 Wards (Gomti Nagar, Indira Nagar, Vibhuti Khand, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 4.",
        "VERIFIED", "Shri Atul Mishra", "Executive Engineer (Zone-1 & Zone-4)", "8810721522",
        "nnlko@nic.in", "Zone 4 Office, Gomti Nagar, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 4)", "Executive Engineer (Zone 4)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 28 (Executive Engineer Zone 1 & 4)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-4 is Sushri Shilpa Kumari (8810721513)."
    ],
    [
        "AUTH-025", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z5", "Civil Engineering Division (Zone 5)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z5", "Zonal Municipal Road and Drain Maintenance (Zone 5)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 5.",
        "POTHOLE", "Road", "Pothole in Zone 5",
        "ZONE", "Zone-5", "ALL", "Zone 5 Wards (Alambagh, Singar Nagar, Sardarnagar, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 5.",
        "VERIFIED", "Shri Rajiv Sharma", "Executive Engineer in Charge (Zone-5)", "8810721544",
        "nnlko@nic.in", "Zone 5 Office, Alambagh, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 5)", "Executive Engineer (Zone 5)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 31 (Executive Engineer Zone 5)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-5 is Shri Vineet Kumar (8810724965)."
    ],
    [
        "AUTH-026", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z6", "Civil Engineering Division (Zone 6)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z6", "Zonal Municipal Road and Drain Maintenance (Zone 6)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 6.",
        "POTHOLE", "Road", "Pothole in Zone 6",
        "ZONE", "Zone-6", "ALL", "Zone 6 Wards (Chowk, Saadatganj, Kashmiri Mohalla, Daulatganj, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 6.",
        "VERIFIED", "Shri Ashok Yadav", "Executive Engineer in Charge (Zone-6)", "8810721552",
        "nnlko@nic.in", "Zone 6 Office, Chowk, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 6)", "Executive Engineer (Zone 6)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 32 (Executive Engineer Zone 6)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-6 is Shri Amarjit Yadav (8874704500)."
    ],
    [
        "AUTH-027", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z7", "Civil Engineering Division (Zone 7)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z7", "Zonal Municipal Road and Drain Maintenance (Zone 7)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 7.",
        "POTHOLE", "Road", "Pothole in Zone 7",
        "ZONE", "Zone-7", "ALL", "Zone 7 Wards (Chinhat, Ismailganj, Indira Nagar Extension, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 7.",
        "VERIFIED", "Shri Sanjay Kumar Pandey", "Executive Engineer in Charge (Zone-7)", "8810721556",
        "nnlko@nic.in", "Zone 7 Office, Chinhat, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 7)", "Executive Engineer (Zone 7)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 33 (Executive Engineer Zone 7)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-7 is Shri Vikas Singh (8810724166)."
    ],
    [
        "AUTH-028", "AUTH-LMC", "Lucknow Municipal Corporation", "MUNICIPAL_CORPORATION",
        "AUTH-GOUP-UDD", "Department of Urban Development, Government of Uttar Pradesh", "ZONE",
        "Lucknow", "Lucknow", "Uttar Pradesh", "DEPT-LMC-CIVIL-Z8", "Civil Engineering Division (Zone 8)",
        "ROADS", "SRV-LMC-ZONAL-ROADS-Z8", "Zonal Municipal Road and Drain Maintenance (Zone 8)",
        "Field execution of pothole filling, patch repairs, and stormwater drain clearing in Zone 8.",
        "POTHOLE", "Road", "Pothole in Zone 8",
        "ZONE", "Zone-8", "ALL", "Zone 8 Wards (Sarojini Nagar, Hind Nagar, Transport Nagar, etc.)",
        "Supervision and execution of civil engineering repairs on municipal streets within Zone 8.",
        "VERIFIED", "Shri Sheel Kumar Srivastava", "Executive Engineer in Charge (Zone-8)", "8810721526",
        "nnlko@nic.in", "Zone 8 Office, Kanpur Road / Sarojini Nagar, Lucknow",
        "https://lmc.up.nic.in", "https://lucknow.everythingcivic.com/citizen/createissue",
        "Assistant Engineer (Zone 8)", "Executive Engineer (Zone 8)", "Chief Engineer (Civil)",
        "Office Hours 10:00 - 17:00",
        "SRC-002", "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf", "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "Item 34 (Executive Engineer Zone 8)", "2024-08-01", "OFFICIAL_DOCUMENT", "HIGH",
        "VERIFIED", "2026-09-11", "Zonal Officer Zone-8 is Dr. Ashish Singh (8808866500)."
    ]
]

with open(os.path.join(BASE_DIR, "data/authority/lucknow_authority_lexicon_master.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(master_headers)
    writer.writerows(master_records)

print(f"Created data/authority/lucknow_authority_lexicon_master.csv with {len(master_records)} records successfully.")


# ==============================================================================
# 4. JSON HIERARCHY (data/authority/lucknow_authority_master.json)
# ==============================================================================
authority_json_data = {
    "geographic_context": {
        "state": "Uttar Pradesh",
        "city": "Lucknow",
        "current_jurisdiction_reference": {
            "zones_count": 8,
            "wards_count": 110,
            "jurisdiction_version": "2023-DELIM-01",
            "effective_from": "2022-10-31",
            "effective_to": None,
            "source_id": "SRC-004",
            "verification_status": "VERIFIED",
            "notes": "Current reference data reflects 8 zones and 110 wards per UP Gazette 31-Oct-2022. Not an immutable architectural constant; future delimitations will update jurisdiction_version."
        }
    },
    "authorities": [
        {
            "authority_id": "AUTH-LMC",
            "authority_name": "Lucknow Municipal Corporation",
            "authority_type": "MUNICIPAL_CORPORATION",
            "parent_authority_id": "AUTH-GOUP-UDD",
            "parent_authority_name": "Department of Urban Development, Government of Uttar Pradesh",
            "official_portal": "https://lmc.up.nic.in",
            "grievance_portal": "https://lucknow.everythingcivic.com/citizen/createissue",
            "toll_free_helpline": "1533",
            "departments": [
                {
                    "department_id": "DEPT-LMC-ADMIN",
                    "department_name": "Central Municipal Administration",
                    "department_type": "OTHER",
                    "services": [
                        {
                            "service_id": "SRV-LMC-GENERAL",
                            "service_name": "General Civic Inquiries & Service Coordination",
                            "issue_categories": ["GENERAL_CIVIC"]
                        }
                    ]
                },
                {
                    "department_id": "DEPT-LMC-CIVIL",
                    "department_name": "Civil Engineering Department",
                    "department_type": "ROADS",
                    "services": [
                        {
                            "service_id": "SRV-LMC-POTHOLE",
                            "service_name": "Municipal Road Pothole Filling & Patchwork",
                            "issue_categories": ["POTHOLE"]
                        },
                        {
                            "service_id": "SRV-LMC-ROAD-REPAIR",
                            "service_name": "Municipal Road Surface Reconstruction & Damage Repair",
                            "issue_categories": ["ROAD_DAMAGE", "ROAD_COLLAPSE"]
                        },
                        {
                            "service_id": "SRV-LMC-FOOTPATH",
                            "service_name": "Municipal Footpath & Pedestrian Walkway Maintenance",
                            "issue_categories": ["DAMAGED_FOOTPATH"]
                        },
                        {
                            "service_id": "SRV-LMC-DRAIN-CLEANING",
                            "service_name": "Stormwater Drain Desilting & Unblocking",
                            "issue_categories": ["BLOCKED_DRAIN"]
                        },
                        {
                            "service_id": "SRV-LMC-WATERLOGGING-PUMPING",
                            "service_name": "Waterlogging Mitigation & Emergency Dewatering",
                            "issue_categories": ["WATERLOGGING"]
                        }
                    ]
                },
                {
                    "department_id": "DEPT-LMC-SWM",
                    "department_name": "Health & Sanitation Department",
                    "department_type": "SANITATION",
                    "services": [
                        {
                            "service_id": "SRV-LMC-GARBAGE-COLLECTION",
                            "service_name": "Municipal Solid Waste Collection & Street Sweeping",
                            "issue_categories": ["GARBAGE_ACCUMULATION"]
                        },
                        {
                            "service_id": "SRV-LMC-ILLEGAL-DUMPING",
                            "service_name": "Illegal Garbage Dumping Removal & Enforcement",
                            "issue_categories": ["ILLEGAL_DUMPING"]
                        },
                        {
                            "service_id": "SRV-LMC-BIN-CLEARANCE",
                            "service_name": "Community Garbage Bin & Compactor Clearance",
                            "issue_categories": ["OVERFLOWING_BIN"]
                        }
                    ]
                },
                {
                    "department_id": "DEPT-LMC-ELEC",
                    "department_name": "Electrical & Mechanical Department",
                    "department_type": "ELECTRICAL",
                    "services": [
                        {
                            "service_id": "SRV-LMC-STREETLIGHT-REPAIR",
                            "service_name": "Streetlight Luminaire & Fixture Repair",
                            "issue_categories": ["STREETLIGHT_FAILURE"]
                        },
                        {
                            "service_id": "SRV-LMC-STREETLIGHT-HARDWARE",
                            "service_name": "Streetlight Bracket, Fitting & Hardware Maintenance",
                            "issue_categories": ["STREETLIGHT_DAMAGE"]
                        }
                    ]
                },
                {
                    "department_id": "DEPT-LMC-VET",
                    "department_name": "Animal Welfare Department",
                    "department_type": "OTHER",
                    "services": [
                        {
                            "service_id": "SRV-LMC-ANIMAL-CONTROL",
                            "service_name": "Stray Cattle Impounding & Animal Carcass Removal",
                            "issue_categories": ["ANIMAL_NUISANCE"]
                        }
                    ]
                }
            ]
        },
        {
            "authority_id": "AUTH-LKO-JALSANSTHAN",
            "authority_name": "Lucknow Jal Sansthan",
            "authority_type": "PUBLIC_UTILITY",
            "parent_authority_id": "AUTH-GOUP-UDD",
            "parent_authority_name": "Department of Urban Development, Government of Uttar Pradesh",
            "official_portal": "https://lmc.up.nic.in/procedure.aspx",
            "grievance_portal": "https://jansunwai.up.nic.in",
            "toll_free_helpline": "1533 / 0522-2622617",
            "departments": [
                {
                    "department_id": "DEPT-JS-WATER",
                    "department_name": "Water Distribution & Maintenance Wing",
                    "department_type": "WATER",
                    "services": [
                        {
                            "service_id": "SRV-JS-LEAK-REPAIR",
                            "service_name": "Potable Water Distribution Pipeline Leakage Repair",
                            "issue_categories": ["WATER_LEAKAGE"]
                        },
                        {
                            "service_id": "SRV-JS-BURST-PIPE",
                            "service_name": "Drinking Water Main / Service Pipe Burst Repair",
                            "issue_categories": ["BROKEN_PIPELINE"]
                        }
                    ]
                },
                {
                    "department_id": "DEPT-JS-SEWER",
                    "department_name": "Sewerage Operations & Maintenance Wing",
                    "department_type": "SEWER",
                    "services": [
                        {
                            "service_id": "SRV-JS-SEWER-CLEARANCE",
                            "service_name": "Sewer Line Clearance & Manhole Overflow Redressal",
                            "issue_categories": ["SEWER_OVERFLOW", "SEWER_BLOCKAGE"]
                        }
                    ]
                }
            ]
        },
        {
            "authority_id": "AUTH-UPPWD",
            "authority_name": "Public Works Department, Uttar Pradesh",
            "authority_type": "STATE_DEPARTMENT",
            "parent_authority_id": "AUTH-GOUP",
            "parent_authority_name": "Government of Uttar Pradesh",
            "official_portal": "https://uppwd.gov.in",
            "grievance_portal": "https://jansunwai.up.nic.in",
            "toll_free_helpline": "1076 (CM Helpline)",
            "departments": [
                {
                    "department_id": "DEPT-PWD-LKO-CIRCLE",
                    "department_name": "Lucknow Circle (Provincial Division)",
                    "department_type": "ROADS",
                    "services": [
                        {
                            "service_id": "SRV-PWD-ROAD-REPAIR",
                            "service_name": "State Highway & Major District Road Maintenance",
                            "issue_categories": ["ROAD_DAMAGE", "POTHOLE"]
                        }
                    ]
                }
            ]
        },
        {
            "authority_id": "AUTH-MVVNL",
            "authority_name": "Madhyanchal Vidyut Vitran Nigam Limited",
            "authority_type": "PUBLIC_UTILITY",
            "parent_authority_id": "AUTH-UPPCL",
            "parent_authority_name": "Uttar Pradesh Power Corporation Limited",
            "official_portal": "https://www.mvvnl.in",
            "grievance_portal": "https://1912.uppcl.org",
            "toll_free_helpline": "1912",
            "departments": [
                {
                    "department_id": "DEPT-MVVNL-LESA",
                    "department_name": "Lucknow Electricity Supply Administration (LESA)",
                    "department_type": "ELECTRICAL",
                    "services": [
                        {
                            "service_id": "SRV-MVVNL-POWER-SUPPLY",
                            "service_name": "Electricity Distribution & Streetlight Power Circuit Maintenance",
                            "issue_categories": ["POWER_OUTAGE"]
                        },
                        {
                            "service_id": "SRV-MVVNL-LINE-MAINTENANCE",
                            "service_name": "Overhead Distribution Line & Electrical Pole Maintenance",
                            "issue_categories": ["ELECTRICAL_INFRASTRUCTURE"]
                        }
                    ]
                }
            ]
        },
        {
            "authority_id": "AUTH-UPJN-URBAN",
            "authority_name": "Uttar Pradesh Jal Nigam (Urban)",
            "authority_type": "PUBLIC_UTILITY",
            "parent_authority_id": "AUTH-GOUP-UDD",
            "parent_authority_name": "Department of Urban Development, Government of Uttar Pradesh",
            "official_portal": "http://jn.upsdc.gov.in",
            "grievance_portal": "https://jansunwai.up.nic.in",
            "toll_free_helpline": "0522-2626395",
            "departments": [
                {
                    "department_id": "DEPT-UPJN-CONSTR",
                    "department_name": "Capital Projects & Construction Wing",
                    "department_type": "WATER",
                    "services": [
                        {
                            "service_id": "SRV-UPJN-CAPITAL-WORKS",
                            "service_name": "Major Trunk Sewer & Water Augmentation Scheme Construction",
                            "issue_categories": ["SEWER_INFRASTRUCTURE", "WATER_INFRASTRUCTURE"]
                        }
                    ]
                }
            ]
        },
        {
            "authority_id": "AUTH-LDA",
            "authority_name": "Lucknow Development Authority",
            "authority_type": "DEVELOPMENT_AUTHORITY",
            "parent_authority_id": "AUTH-GOUP-HUPD",
            "parent_authority_name": "Housing and Urban Planning Department, Government of Uttar Pradesh",
            "official_portal": "https://ldaonline.co.in",
            "grievance_portal": "https://jansunwai.up.nic.in",
            "toll_free_helpline": "0522-2307868",
            "departments": [
                {
                    "department_id": "DEPT-LDA-ENG",
                    "department_name": "Engineering Division",
                    "department_type": "ROADS",
                    "services": [
                        {
                            "service_id": "SRV-LDA-SECTOR-MAINT",
                            "service_name": "Civic Infrastructure Maintenance in Un-transferred Sectors",
                            "issue_categories": ["ROAD_DAMAGE", "DRAINAGE", "STREETLIGHT_FAILURE"]
                        }
                    ]
                }
            ]
        }
    ]
}

with open(os.path.join(BASE_DIR, "data/authority/lucknow_authority_master.json"), "w", encoding="utf-8") as f:
    json.dump(authority_json_data, f, indent=2, ensure_ascii=False)

print("Created data/authority/lucknow_authority_master.json successfully.")
