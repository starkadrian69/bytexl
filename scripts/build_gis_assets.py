import os
import sys
import json
import csv
import shutil
import requests
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_GIS_DIR = os.path.join(BASE_DIR, "data/gis")
RAW_DIR = os.path.join(DATA_GIS_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_GIS_DIR, "processed")
VERIFIED_DIR = os.path.join(DATA_GIS_DIR, "verified")
SOURCES_DIR = os.path.join(DATA_GIS_DIR, "sources")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VERIFIED_DIR, exist_ok=True)
os.makedirs(SOURCES_DIR, exist_ok=True)

print("=" * 65)
print("CIVICTRACE PHASE 2: GIS JURISDICTION ASSET GENERATOR")
print("=" * 65)

# --- 1. DOWNLOAD & SAVE RAW DATASETS ---
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
raw_files = {
    "datameet_lucknow_ward_boundary_raw.geojson": "https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Lucknow/Lucknow_ward_boundary.geojson",
    "datameet_lucknow_zone_boundary_raw.geojson": "https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Lucknow/Lucknow_zone_boundary.geojson",
    "datameet_lucknow_city_boundary_raw.geojson": "https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Lucknow/Lucknow_city_boundary.geojson",
}

for fname, url in raw_files.items():
    dest = os.path.join(RAW_DIR, fname)
    if not os.path.exists(dest):
        print(f"Downloading {fname}...")
        r = requests.get(url, headers=headers)
        with open(dest, 'wb') as f:
            f.write(r.content)
        print(f"  Saved {fname} ({len(r.content)} bytes)")
    else:
        print(f"  Found existing {fname}")

scratch_microplan = r'C:\Users\Akshat\.gemini\antigravity\brain\7679ce2b-93fe-4a3d-ad2d-9a6ee7f578c8\scratch\microplan.pdf'
dest_microplan = os.path.join(RAW_DIR, "lmc_microplan_september_2024.pdf")
if os.path.exists(scratch_microplan) and not os.path.exists(dest_microplan):
    shutil.copyfile(scratch_microplan, dest_microplan)
    print(f"Copied microplan to {dest_microplan}")

# --- 2. GENERATE GIS SOURCE REGISTRY ---
GIS_SOURCES = [
    {
        "source_id": "SRC-GIS-001",
        "source_name": "DataMeet Lucknow Municipal Spatial Data",
        "source_type": "SECONDARY_OPEN_VECTOR",
        "organization": "DataMeet Community",
        "url": "https://github.com/datameet/Municipal_Spatial_Data/tree/master/Lucknow",
        "document_title": "Lucknow Municipal Ward and Zone Boundary GeoJSON",
        "publication_date": "2017-05-18",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "2012-2017 (Pre-2022 Delimitation)",
        "spatial_vintage": "PRE_2022",
        "administrative_authority": "NOT_AUTHORITATIVE_FOR_CURRENT_DELIMITATION",
        "geometry_status": "SECONDARY_LEGACY",
        "data_extracted": "Historical vector polygons for 110 municipal wards and 6 zones, plus Airport and Cantonment enclosures.",
        "verification_status": "PARTIALLY_VERIFIED",
        "notes": "Useful as a secondary reference polygon geometry baseline for the urban core; reflects the legacy 6-zone regime and pre-2022 ward numbering. Does NOT establish current legal ward identity or 8-zone structure."
    },
    {
        "source_id": "SRC-GIS-002",
        "source_name": "Uttar Pradesh Gazette Final Delimitation Notification 2022",
        "source_type": "OFFICIAL_GAZETTE",
        "organization": "Department of Urban Development, Government of Uttar Pradesh",
        "url": "https://lmc.up.nic.in/pdf/DelimiationfinalNotification31_10_2022HINDI.pdf",
        "document_title": "Uttar Pradesh Gazette Notification No. 1774/9-1-2022",
        "publication_date": "2022-10-31",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "2022-Present (Effective 2022-10-31)",
        "spatial_vintage": "CURRENT_LEGAL_STATUTE",
        "administrative_authority": "AUTHORITATIVE_LEGAL_GROUND_TRUTH",
        "geometry_status": "NOT_AVAILABLE",
        "data_extracted": "Statutory delimitation of Lucknow Nagar Nigam establishing 110 municipal wards and 8 zones following inclusion of 88 peripheral revenue villages.",
        "verification_status": "VERIFIED",
        "notes": "Primary statutory enactment governing current territorial boundaries and legal ward structure. Published as text gazette notification without downloadable GIS vector polygons."
    },
    {
        "source_id": "SRC-GIS-003",
        "source_name": "Lucknow Municipal Corporation Sworn Corporators List 2023-2027",
        "source_type": "OFFICIAL_DOCUMENT",
        "organization": "Lucknow Municipal Corporation",
        "url": "https://lmc.up.nic.in/pdf/Corporator_2023_2027_sapath_date_26_05_2023_Main_List.pdf",
        "document_title": "Sworn Corporators List 2023-2027 (Nagar Nigam Lucknow Nav Nirvachit Parshad List)",
        "publication_date": "2023-05-26",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "2023-2027 Municipal Tenure",
        "spatial_vintage": "CURRENT_ELECTED_COUNCIL",
        "administrative_authority": "AUTHORITATIVE_MUNICIPAL_RECORD",
        "geometry_status": "NOT_AVAILABLE",
        "data_extracted": "Complete enumeration of 110 municipal wards (Ward 1 to Ward 110) with exact Hindi ward names and elected corporators.",
        "verification_status": "VERIFIED",
        "notes": "Primary administrative reference establishing current ward numbering and official nomenclature under the 2022 delimitation."
    },
    {
        "source_id": "SRC-GIS-004",
        "source_name": "Lucknow Municipal Corporation Official Telephone Directory (Doorbhas Suchi)",
        "source_type": "OFFICIAL_DIRECTORY",
        "organization": "Lucknow Municipal Corporation",
        "url": "https://lmc.up.nic.in/pdf/DoorbhasSuchi.pdf",
        "document_title": "LMC Doorbhas Suchi (Telephone Directory of Officials)",
        "publication_date": "2024-08-01",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "2024-Present",
        "spatial_vintage": "CURRENT_ZONAL_ADMINISTRATION",
        "administrative_authority": "AUTHORITATIVE_MUNICIPAL_RECORD",
        "geometry_status": "NOT_AVAILABLE",
        "data_extracted": "Executive directory verifying 8 operational municipal zones (Zone 1 to Zone 8) with CUG contacts for Zonal Officers and Executive Engineers.",
        "verification_status": "VERIFIED",
        "notes": "Corroborates active 8-zone municipal administration."
    },
    {
        "source_id": "SRC-GIS-005",
        "source_name": "Lucknow Municipal Corporation Sanchari Rog Niyantran Micro-Plan September 2024",
        "source_type": "OFFICIAL_OPERATIONAL_PLAN",
        "organization": "Lucknow Municipal Corporation (Health & Sanitation Department)",
        "url": "https://lmc.up.nic.in/pdf/microplanallzonesseptember.pdf",
        "document_title": "Sanchari Rog Niyantran Karyayojana (Micro-Plan Across All Zones)",
        "publication_date": "2024-09-01",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "September 2024",
        "spatial_vintage": "CURRENT_OPERATIONAL_FIELD_MAPPING",
        "administrative_authority": "AUTHORITATIVE_MUNICIPAL_RECORD",
        "geometry_status": "NOT_AVAILABLE",
        "data_extracted": "Operational roster mapping all municipal wards and localities to their respective Zones 1 through 8 for daily sanitation and fogging operations.",
        "verification_status": "VERIFIED",
        "notes": "Primary field evidence establishing operational ward-to-zone allocations across all 8 zones."
    },
    {
        "source_id": "SRC-GIS-006",
        "source_name": "Uttar Pradesh Urban Roads Infrastructure Development Agency (URIDA) Geo-Portal",
        "source_type": "GOVERNMENT_INFRASTRUCTURE_PORTAL",
        "organization": "Urban Development Department, Government of Uttar Pradesh",
        "url": "https://github.com/webgisprojects-creator/urida-geo-portal",
        "document_title": "URIDA GIS-based Urban Infrastructure Management System",
        "publication_date": "2024-10-01",
        "accessed_date": "2026-09-12",
        "temporal_coverage": "2024",
        "spatial_vintage": "STATE_ENTERPRISE_INTERNAL",
        "administrative_authority": "STATE_TECHNICAL_AGENCY",
        "geometry_status": "NOT_AVAILABLE",
        "data_extracted": "Technical schema and layer registry referencing internal PostGIS tables lucknow.lucknow_ward_boundary and lko_analysis.zone_development_summary_lnn.",
        "verification_status": "PARTIALLY_VERIFIED",
        "notes": "Confirms state-level GIS modeling of Lucknow wards and zones on internal enterprise servers; vector layers are not publicly downloadable."
    }
]

source_headers = [
    "source_id", "source_name", "source_type", "organization", "url",
    "document_title", "publication_date", "accessed_date", "temporal_coverage",
    "spatial_vintage", "administrative_authority", "geometry_status",
    "data_extracted", "verification_status", "notes"
]

for out_path in [os.path.join(DATA_GIS_DIR, "gis_source_registry.csv"), os.path.join(SOURCES_DIR, "gis_source_registry.csv")]:
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=source_headers)
        writer.writeheader()
        writer.writerows(GIS_SOURCES)
    print(f"Wrote {out_path}")

# --- 3. DEFINITIVE 110-WARD DATASET (LKO-JUR-2023-01) ---
# Format: (ward_number, hindi_name, english_name, zone_number, legacy_ward_num, legacy_ward_name, alignment_status, notes)
WARDS_DEFINITION = [
    (1, "श्रद्धेय अटल बिहारी वाजपेयी वार्ड", "Shraddheya Atal Bihari Vajpayee Ward", 8, None, None, "NEEDS_REVIEW", "Newly created ward under 2022 delimitation incorporating peripheral revenue villages in southern sector; no dedicated pre-2022 legacy polygon."),
    (2, "शारदा नगर द्वितीय वार्ड", "Sharda Nagar Second Ward", 8, 21, "Sharda Nagar", "PARTIALLY_VERIFIED", "Bifurcated from legacy Sharda Nagar ward (legacy Ward 21); covers southern residential sector."),
    (3, "इब्राहिमपुर द्वितीय वार्ड", "Ibrahimpur Second Ward", 8, 1, "Ibrahimpur", "PARTIALLY_VERIFIED", "Bifurcated from legacy Ibrahimpur ward (legacy Ward 1); covers eastern/Vrindavan colony sectors."),
    (4, "इब्राहिमपुर प्रथम वार्ड", "Ibrahimpur First Ward", 8, 1, "Ibrahimpur", "PARTIALLY_VERIFIED", "Bifurcated from legacy Ibrahimpur ward (legacy Ward 1); covers core village and Rajani Khand."),
    (5, "राजा बिजली पासी द्वितीय वार्ड", "Raja Bijli Pasi Second Ward", 8, 2, "Raja Bijli Pasi", "PARTIALLY_VERIFIED", "Bifurcated from legacy Raja Bijli Pasi ward (legacy Ward 2); covers southern sector."),
    (6, "राजा बिजली पासी प्रथम वार्ड", "Raja Bijli Pasi First Ward", 8, 2, "Raja Bijli Pasi", "PARTIALLY_VERIFIED", "Bifurcated from legacy Raja Bijli Pasi ward (legacy Ward 2); covers northern sector."),
    (7, "माननीय लालजी टंडन वार्ड", "Mananiya Lalji Tandon Ward", 6, None, None, "NEEDS_REVIEW", "Newly created ward under 2022 delimitation incorporating Barauna Khand/Hayatnagar peripheral villages."),
    (8, "अम्बेडकर नगर वार्ड", "Ambedkar Nagar Ward", 2, 14, "Ambedkar Nagar 1st", "PARTIALLY_VERIFIED", "Re-aligned from legacy Ambedkar Nagar 1st/2nd into unified ward in Zone 2."),
    (9, "माननीय कल्याण सिंह वार्ड", "Mananiya Kalyan Singh Ward", 6, None, None, "NEEDS_REVIEW", "Newly created ward under 2022 delimitation in western Lucknow; named after former CM Kalyan Singh."),
    (10, "सरोजनी नगर प्रथम वार्ड", "Sarojini Nagar First Ward", 5, 4, "Sarojni Nagar Part 1", "PARTIALLY_VERIFIED", "Bifurcated from legacy Sarojini Nagar Part 1 (legacy Ward 4); northern industrial/residential corridor."),
    (11, "शहीद भगत सिंह द्वितीय वार्ड", "Shaheed Bhagat Singh Second Ward", 4, 6, "Shaheed Bhagat Singh", "PARTIALLY_VERIFIED", "Bifurcated from legacy Shaheed Bhagat Singh ward (legacy Ward 6); covers Matiyari/BKT corridor."),
    (12, "खरगापुर सरसवां वार्ड", "Khargapur Saraswan Ward", 4, None, None, "NEEDS_REVIEW", "Newly created ward under 2022 delimitation incorporating Khargapur, Saraswan, and Gomti Nagar Extension."),
    (13, "शहीद भगत सिंह प्रथम वार्ड", "Shaheed Bhagat Singh First Ward", 4, 6, "Shaheed Bhagat Singh", "PARTIALLY_VERIFIED", "Bifurcated from legacy Shaheed Bhagat Singh ward (legacy Ward 6); covers Kanchana Pur/Matiyari."),
    (14, "भरवारा मल्हौर वार्ड", "Bharwara Malhaur Ward", 4, None, None, "NEEDS_REVIEW", "Newly created ward under 2022 delimitation incorporating Bharwara, Malhaur, and Amity University zone."),
    (15, "लाल बहादुर शास्त्री प्रथम वार्ड", "Lal Bahadur Shastri First Ward", 7, 8, "Lal Bahadur Shastri 1st", "PARTIALLY_VERIFIED", "Bifurcated from legacy Lal Bahadur Shastri ward (legacy Ward 8); northern Indira Nagar sector."),
    (16, "फैजुल्लागंज चतुर्थ वार्ड", "Faizullaganj Fourth Ward", 3, 12, "Faizullah Ganj 2nd", "PARTIALLY_VERIFIED", "Reorganized from legacy Faizullah Ganj complex; covers Daud Nagar and IIM Road corridor."),
    (17, "विक्रमादित्य महात्मा गांधी वार्ड", "Vikramaditya Mahatma Gandhi Ward", 1, 107, "Vikramaditya Ward", "VERIFIED", "Core historical central municipal ward comprising Vikramaditya Marg, Raj Bhavan, and Gautampalli."),
    (18, "सरोजनी नगर द्वितीय वार्ड", "Sarojini Nagar Second Ward", 5, 15, "Sarojni Nagar Part 2", "PARTIALLY_VERIFIED", "Bifurcated from legacy Sarojini Nagar Part 2 (legacy Ward 15); covers southern airport link corridor."),
    (19, "शारदा नगर प्रथम वार्ड", "Sharda Nagar First Ward", 8, 21, "Sharda Nagar", "PARTIALLY_VERIFIED", "Bifurcated from legacy Sharda Nagar ward (legacy Ward 21); covers Sector G/Ruchi Khand."),
    (20, "न्यू हैदरगंज तृतीय वार्ड", "New Haiderganj Third Ward", 6, 83, "Haidar Ganj 3rd", "PARTIALLY_VERIFIED", "Bifurcated from legacy Haidar Ganj 3rd (legacy Ward 83); covers Campbell Road and Para sectors."),
    (21, "मालवीय नगर वार्ड", "Malviya Nagar Ward", 2, 7, "Malviya Nagar", "VERIFIED", "Stable historical ward in Aishbagh / Old City South."),
    (22, "जानकीपुरम तृतीय वार्ड", "Jankipuram Third Ward", 3, 75, "Jankipuram", "PARTIALLY_VERIFIED", "Expanded from legacy Jankipuram ward; covers Sector J and extension colonies."),
    (23, "गुरु नानक नगर वार्ड", "Guru Nanak Nagar Ward", 5, 87, "Guru Nanak Nagar", "VERIFIED", "Stable historical ward in Alambagh commercial center."),
    (24, "साआदतगंज वार्ड", "Saadatganj Ward", 6, 91, "Saadat Ganj", "VERIFIED", "Stable historical Old City ward with heritage fabric."),
    (25, "बाबू कुंज बिहारी ओम नगर वार्ड", "Babu Kunj Bihari Om Nagar Ward", 5, 18, "Om Nagar", "PARTIALLY_VERIFIED", "Expanded from legacy Om Nagar ward (legacy Ward 18) incorporating Babu Kunj Bihari Nagar."),
    (26, "ऐशबाग वार्ड", "Aishbagh Ward", 2, 60, "Aishbagh", "VERIFIED", "Stable historical industrial and residential municipal ward."),
    (27, "बालागंज प्रथम वार्ड", "Balaganj First Ward", 6, 103, "Balaganj", "PARTIALLY_VERIFIED", "Demarcated from legacy Balaganj ward (legacy Ward 103)."),
    (28, "राम मोहन राय वार्ड", "Ram Mohan Roy Ward", 1, 89, "Raja Ram Mohan Rai", "VERIFIED", "Core historical central ward along Shahnajaf and Hazratganj arterial corridors."),
    (29, "खरिका द्वितीय वार्ड", "Kharika Second Ward", 8, 10, "Kharika", "PARTIALLY_VERIFIED", "Bifurcated from legacy Kharika ward (legacy Ward 10); southern Telibagh residential corridor."),
    (30, "खरिका प्रथम वार्ड", "Kharika First Ward", 8, 10, "Kharika", "PARTIALLY_VERIFIED", "Bifurcated from legacy Kharika ward (legacy Ward 10); northern Telibagh / LDA colony sector."),
    (31, "जानकीपुरम प्रथम वार्ड", "Jankipuram First Ward", 3, 75, "Jankipuram", "PARTIALLY_VERIFIED", "Core Jankipuram residential sectors along Engineering College corridor."),
    (32, "आलमनगर वार्ड", "Alamnagar Ward", 6, 68, "Alam Nagar", "VERIFIED", "Stable historical railway and residential ward in western Lucknow."),
    (33, "लालकुआं वार्ड", "Lalkuan Ward", 1, 13, "Lal Kuan", "VERIFIED", "Stable central municipal ward comprising Chitwapur and Lalkuan."),
    (34, "हजरतगंज रामतीर्थ वार्ड", "Hazratganj Ramtirth Ward", 1, 17, "Hazarat Ganj", "VERIFIED", "Definitive central commercial and administrative core of Lucknow."),
    (35, "हिन्द नगर वार्ड", "Hind Nagar Ward", 8, 66, "Hind Nagar", "VERIFIED", "Established residential ward along Kanpur Road opposite transport depot."),
    (36, "केसरी खेड़ा वार्ड", "Kesri Kheda Ward", 5, 19, "Kesri Kheda", "VERIFIED", "Stable residential ward in Alambagh peripheral area."),
    (37, "गोमती नगर वार्ड", "Gomti Nagar Ward", 4, 80, "Gomti Nagar", "VERIFIED", "Core planned development ward along Vipin Khand and Sanjay Gandhi Puram."),
    (38, "कन्हैया माधवपुर द्वितीय वार्ड", "Kanhaiya Madhopur Second Ward", 6, 9, "Kanhaiya Madhopur", "PARTIALLY_VERIFIED", "Bifurcated from legacy Kanhaiya Madhopur ward (legacy Ward 9)."),
    (39, "न्यू हैदरगंज द्वितीय वार्ड", "New Haiderganj Second Ward", 6, 16, "Haidar Ganj 2nd", "PARTIALLY_VERIFIED", "Bifurcated from legacy Haidar Ganj 2nd (legacy Ward 16)."),
    (40, "इन्दिर प्रियदर्शिनी वार्ड", "Indira Priyadarshini Ward", 7, 72, "Indira Priyadarshini", "VERIFIED", "Stable residential ward in Indira Nagar Sector 11/14 corridor."),
    (41, "रामजी लाल सरदार पटेल नगर वार्ड", "Ramji Lal Sardar Patel Nagar Ward", 5, 96, "Sardar Patel Nagar", "PARTIALLY_VERIFIED", "Expanded from legacy Sardar Patel Nagar incorporating Ramji Lal Nagar."),
    (42, "शंकरपुरवा द्वितीय वार्ड", "Shankarpurwa Second Ward", 7, 78, "Shanker Purwa 2nd", "VERIFIED", "Established residential ward along Ring Road / Kalyanpur corridor."),
    (43, "इस्माइलगंज द्वितीय वार्ड", "Ismailganj Second Ward", 7, 41, "Ismail Ganj 2nd", "PARTIALLY_VERIFIED", "Bifurcated from legacy Ismailganj complex along Faizabad Road."),
    (44, "फैजुल्लागंज द्वितीय वार्ड", "Faizullaganj Second Ward", 3, 12, "Faizullah Ganj 2nd", "PARTIALLY_VERIFIED", "Established ward in northern Sitapur Road suburban belt."),
    (45, "गुरु गोविंद सिंह वार्ड", "Guru Govind Singh Ward", 5, 20, "Guru Govind Singh Ward", "VERIFIED", "Stable historical ward in Charbagh / Alambagh corridor."),
    (46, "कुंवर ज्योति प्रसाद वार्ड", "Kunwar Jyoti Prasad Ward", 2, 64, "Kunwar Jyoti Prasad 1st", "PARTIALLY_VERIFIED", "Re-aligned from legacy Kunwar Jyoti Prasad 1st/2nd in Rajajipuram sector."),
    (47, "डालीगंज निराला नगर वार्ड", "Daliganj Nirala Nagar Ward", 3, 76, "Nirala Nagar", "PARTIALLY_VERIFIED", "Core northern ward uniting historical Daliganj riverfront and Nirala Nagar."),
    (48, "फैजुल्लागंज प्रथम वार्ड", "Faizullaganj First Ward", 3, 12, "Faizullah Ganj 2nd", "PARTIALLY_VERIFIED", "Covers Indrapuri, Aziz Nagar, and inner Sitapur road settlements."),
    (49, "महाकवि जय शंकर प्रसाद वार्ड", "Mahakavi Jai Shankar Prasad Ward", 3, 90, "Jai Shankar Prasad", "VERIFIED", "Stable northern municipal ward around Purania and Sector D Aliganj."),
    (50, "चिनहट प्रथम वार्ड", "Chinhat First Ward", 4, 11, "Chinhat", "PARTIALLY_VERIFIED", "Bifurcated from legacy Chinhat ward (legacy Ward 11); western Chinhat core."),
    (51, "इस्माइलगंज प्रथम वार्ड", "Ismailganj First Ward", 7, 37, "Ismail Ganj 1st", "PARTIALLY_VERIFIED", "Bifurcated from legacy Ismailganj complex; covers Patel Nagar / Harihar Nagar."),
    (52, "कन्हैया माधवपुर प्रथम वार्ड", "Kanhaiya Madhopur First Ward", 6, 9, "Kanhaiya Madhopur", "PARTIALLY_VERIFIED", "Bifurcated from legacy Kanhaiya Madhopur ward (legacy Ward 9); eastern sector."),
    (53, "महानगर वार्ड", "Mahanagar Ward", 3, 44, "Mahanagar", "VERIFIED", "Established residential planned layout in north-central Lucknow."),
    (54, "गीता पल्ली वार्ड", "Geeta Palli Ward", 5, 59, "Geeta Palli", "VERIFIED", "Stable historical ward along VIP road / Alambagh corridor."),
    (55, "रानी लक्ष्मी बाई वार्ड", "Rani Laxmi Bai Ward", 1, 99, "Rani Laxmi Bai", "VERIFIED", "Historical central ward in Lalbagh / Naka Hindola area."),
    (56, "विद्यावती द्वितीय वार्ड", "Vidyavati Second Ward", 8, 73, "Vidyavati 2nd", "PARTIALLY_VERIFIED", "Bifurcated from legacy Vidyavati complex (legacy Ward 73) in LDA colony."),
    (57, "बाबू बनारसी दास वार्ड", "Babu Banarsi Das Ward", 1, 94, "Babu Banarsi Das", "VERIFIED", "Central ward comprising Qila, Husainganj, and old cantonment interface."),
    (58, "मोती लाल नेहरू चंद्र भानु गुप्त वार्ड", "Moti Lal Nehru Chandra Bhanu Gupt Ward", 2, 45, "Moti Lal Nehru", "PARTIALLY_VERIFIED", "Unified ward joining historical Moti Lal Nehru and CB Gupta municipal sectors."),
    (59, "काल्विन कालेज निशातगंज वार्ड", "Colvin College Nishatganj Ward", 4, 22, "Nishat Ganj", "PARTIALLY_VERIFIED", "Historic riverfront ward around Colvin Taluqdars College and Nishatganj."),
    (60, "विद्यावती तृतीय वार्ड", "Vidyavati Third Ward", 8, 73, "Vidyavati 2nd", "PARTIALLY_VERIFIED", "Bifurcated from legacy Vidyavati complex; covers Sector I/K Kanpur Road scheme."),
    (61, "तिलक नगर कुंदरी रकाबगंज वार्ड", "Tilak Nagar Kundari Rakabganj Ward", 2, 3, "Tilak Nagar", "PARTIALLY_VERIFIED", "Unified ward uniting Tilak Nagar and Kundari Rakabganj."),
    (62, "रफी अहमद किदवई वार्ड", "Rafi Ahmed Kidwai Ward", 4, 85, "Rafi Ahmad Kidwai", "VERIFIED", "Established ward in Vikas Khand / Gomti Nagar sector."),
    (63, "अयोध्यादास द्वितीय वार्ड", "Ayodhyadas Second Ward", 3, 29, "Ayodhya Das 2nd", "VERIFIED", "Established northern ward along Khadra and Sitapur road."),
    (64, "विद्यावती प्रथम वार्ड", "Vidyavati First Ward", 8, 88, "Vidyavati 1st", "PARTIALLY_VERIFIED", "Core LDA colony sector around Sector E/G."),
    (65, "चित्रगुप्त नगर वार्ड", "Chitragupta Nagar Ward", 5, 93, "Chitragupta Nagar", "VERIFIED", "Stable residential municipal ward in Alambagh."),
    (66, "चिनहट द्वितीय वार्ड", "Chinhat Second Ward", 4, 11, "Chinhat", "PARTIALLY_VERIFIED", "Bifurcated from legacy Chinhat ward; covers eastern extension / Uttardhona."),
    (67, "लाला लाजपत राय वार्ड", "Lala Lajpat Rai Ward", 3, 71, "Lala Lajpat Rai", "VERIFIED", "Stable planned residential ward in Aliganj Sector M/N."),
    (68, "बाबू जगजीवन राम वार्ड", "Babu Jagjivan Ram Ward", 7, 74, "Babu Jagjiwan Ram", "VERIFIED", "Planned housing board ward in Indira Nagar Sector 16/17."),
    (69, "जे.सी. बोस वार्ड", "J.C. Bose Ward", 1, 98, "Acharya Jagdish Chandra Bose", "VERIFIED", "Historical central ward around Ghasiyari Mandi and Kalibari."),
    (70, "पेपर मिल कालोनी वार्ड", "Paper Mill Colony Ward", 4, 48, "Paper Mill Colony", "VERIFIED", "Historic municipal colony ward along Nishatganj riverbend."),
    (71, "मनकामेश्वर मंदिर वार्ड", "Mankameshwar Mandir Ward", 3, 30, "Mankameshwar Mandir", "VERIFIED", "Historical religious and cultural ward along northern Gomti bank."),
    (72, "शंकरपुरवा तृतीय वार्ड", "Shankarpurwa Third Ward", 7, 78, "Shanker Purwa 2nd", "PARTIALLY_VERIFIED", "Covers Sector 7/8/12 Indira Nagar and outer Kalyanpur."),
    (73, "फैजुल्लागंज तृतीय वार्ड", "Faizullaganj Third Ward", 3, 12, "Faizullah Ganj 2nd", "PARTIALLY_VERIFIED", "Covers Bharat Nagar, Agrasen Nagar, and Preeti Nagar."),
    (74, "जानकीपुरम द्वितीय वार्ड", "Jankipuram Second Ward", 3, 75, "Jankipuram", "PARTIALLY_VERIFIED", "Covers Sector G/H, Sahara State, and Jankipuram Garden."),
    (75, "भारतेन्दु हरिश्चंद्र वार्ड", "Bhartendu Harishchandra Ward", 3, 70, "Bhartendu Harishchandra", "VERIFIED", "Stable planned municipal ward in Aliganj Sector A/E."),
    (76, "राजीव गांधी प्रथम वार्ड", "Rajiv Gandhi First Ward", 4, 84, "Rajeev Gandhi 1st", "VERIFIED", "Planned development ward in Gomti Nagar Vinay Khand / Virat Khand."),
    (77, "मैथिलीशरण गुप्त वार्ड", "Maithilisharan Gupt Ward", 7, 69, "Maithili Sharan Gupt", "VERIFIED", "Stable housing sector in Indira Nagar Sector B/C."),
    (78, "लेबर कालोनी वार्ड", "Labour Colony Ward", 2, 40, "Labour Colony", "VERIFIED", "Historic workers colony ward in Talkatora industrial area."),
    (79, "राजाजीपुरम वार्ड", "Rajajipuram Ward", 2, 38, "Rajaji Puram", "VERIFIED", "Flagship planned residential scheme in western Lucknow."),
    (80, "इन्दिर नगर वार्ड", "Indira Nagar Ward", 7, 77, "Indira Nagar", "VERIFIED", "Central commercial and residential core of Indira Nagar housing board."),
    (81, "मल्लाही टोला द्वितीय वार्ड", "Mallahi Tola Second Ward", 6, 92, "Mallahi Tola 2nd", "VERIFIED", "Historical Gomti riverfront ward in Old City."),
    (82, "त्रिवेणी नगर वार्ड", "Triveni Nagar Ward", 3, 67, "Triveni Nagar", "VERIFIED", "Established residential colony in Sitapur road corridor."),
    (83, "न्यू हैदरगंज प्रथम वार्ड", "New Haiderganj First Ward", 6, 25, "Haidar Ganj 1st", "PARTIALLY_VERIFIED", "Bifurcated from legacy Haidar Ganj 1st (legacy Ward 25)."),
    (84, "कदम रसूल वार्ड", "Kadam Rasool Ward", 3, 31, "Kadam Rasool", "VERIFIED", "Historic heritage ward on northern bank of Gomti around Shia College."),
    (85, "मल्लाही टोला प्रथम वार्ड", "Mallahi Tola First Ward", 6, 82, "Mallahi Tola 1st", "VERIFIED", "Gomti riverfront heritage settlement near Generalganj."),
    (86, "लोहिया नगर वार्ड", "Lohia Nagar Ward", 7, 79, "Lohia Nagar", "VERIFIED", "Planned municipal ward in Indira Nagar Sector 1/2/3."),
    (87, "गोलागंज वार्ड", "Golaganj Ward", 1, 102, "Gola Ganj", "VERIFIED", "Historic core municipal ward around Christian College and Kaiserbagh."),
    (88, "बशीरगंज गणेशगंज वार्ड", "Bashirganj Ganeshganj Ward", 1, 100, "Ganesh Ganj", "PARTIALLY_VERIFIED", "Unified historic commercial ward uniting Bashirganj and Ganeshganj."),
    (89, "शीतला देवी वार्ड", "Sheetla Devi Ward", 6, 81, "Sheetla Devi", "VERIFIED", "Historic Old City ward around Naubasta temple complex."),
    (90, "राजेन्द्र नगर वार्ड", "Rajendra Nagar Ward", 2, 57, "Rajendra Nagar", "VERIFIED", "Historic planned layout adjacent to Motinagar and Aishbagh."),
    (91, "विवेकानन्दपुरी वार्ड", "Vivekanandapuri Ward", 3, 49, "Vivekanand Puri", "VERIFIED", "Established residential enclave adjacent to IT College and Mahanagar."),
    (92, "शंकरपुरवा प्रथम वार्ड", "Shankarpurwa First Ward", 7, 50, "Shanker Purwa 1st", "VERIFIED", "Established residential sector in northern Indira Nagar / Ring Road."),
    (93, "हुसैनाबाद वार्ड", "Husainabad Ward", 6, 52, "Husainabad", "VERIFIED", "Definitive historic core containing Bara and Chhota Imambaras."),
    (94, "दौलतगंज वार्ड", "Daulatganj Ward", 6, 51, "Daulat Ganj", "VERIFIED", "Historic municipal ward along Hardoi road / Gaughat."),
    (95, "मौलवीगंज वार्ड", "Maulviganj Ward", 1, 105, "Maulvi Ganj", "VERIFIED", "Historical commercial and publishing quarter of old Lucknow."),
    (96, "लाल बहादुर शास्त्री द्वितीय वार्ड", "Lal Bahadur Shastri Second Ward", 7, 43, "Lal Bahadur Shastri 2nd", "VERIFIED", "Planned housing board ward in Indira Nagar Sector 18/20."),
    (97, "गढी पीर खां वार्ड", "Gadhi Peer Khan Ward", 6, 42, "Garhi Peer Khan", "VERIFIED", "Historic settlement ward in Chowk vicinity."),
    (98, "यदुनाथ सान्याल नजरबाग वार्ड", "Yadunath Sanyal Nazarbagh Ward", 1, 95, "Yadunath Sanyal", "PARTIALLY_VERIFIED", "Historic residential ward uniting Nazarbagh and Phoolbagh."),
    (99, "आचार्य नरेन्द्र देव वार्ड", "Acharya Narendra Dev Ward", 6, 97, "Acharya Narendra Dev", "VERIFIED", "Historic Old City ward around Chaupatiyan."),
    (100, "राजीव गांधी द्वितीय वार्ड", "Rajiv Gandhi Second Ward", 4, 86, "Rajeev Gandhi 2nd", "VERIFIED", "Planned development ward in Gomti Nagar Viram Khand / Vishwas Khand."),
    (101, "अम्बरगंज वार्ड", "Ambarganj Ward", 6, 47, "Ambar Ganj", "VERIFIED", "Historic Old City ward along Campbell Road."),
    (102, "मौलाना कल्बे आबिद वार्ड", "Maulana Kalbe Abid Ward", 6, 108, "Maulana Kalbe Abid", "VERIFIED", "Historic cultural ward around Victoria Street and Mufeed-e-Aam."),
    (103, "मशकगंज वजीरगंज वार्ड", "Mashakganj Wazirganj Ward", 1, 101, "Wazir Ganj", "PARTIALLY_VERIFIED", "Unified central commercial and residential ward along Wazirganj."),
    (104, "यहियागंज नेताजी सुभाष चन्द्र बोस वार्ड", "Yahiyaganj Netaji Subhash Chandra Bose Ward", 2, 104, "Subhash Chandra Bose", "PARTIALLY_VERIFIED", "Historical trading market quarter of old Lucknow."),
    (105, "कश्मीरी मोहल्ला वार्ड", "Kashmiri Mohalla Ward", 6, 61, "Kashmiri Mohalla", "VERIFIED", "Historic cultural enclave in Chowk / Old City West."),
    (106, "चौक बाजार काली जी वार्ड", "Chowk Bazar Kali Ji Ward", 6, 106, "Chowk", "PARTIALLY_VERIFIED", "Definitive ancient bazaar and heritage quarter of Lucknow."),
    (107, "राजा बाजार वार्ड", "Raja Bazar Ward", 2, 62, "Raja Bazar", "VERIFIED", "Historical market ward adjacent to Medical College / Victoria Street."),
    (108, "भवानीगंज वार्ड", "Bhawaniganj Ward", 6, 63, "Bhawani Ganj", "VERIFIED", "Historic settlement ward near Old Tikaitganj."),
    (109, "अलीगंज वार्ड", "Aliganj Ward", 3, 34, "Aliganj", "VERIFIED", "Definitive core of historic and planned Aliganj around Hanuman Temple."),
    (110, "अयोध्यादास प्रथम वार्ड", "Ayodhyadas First Ward", 3, 28, "Ayodhya Das 1st", "VERIFIED", "Historic northern settlement on Gomti bank near Deen Dayal Nagar Khadra.")
]

print(f"Loaded {len(WARDS_DEFINITION)} definitive ward specifications.")

# Zone metadata lookup
ZONE_METADATA = {
    1: {"name": "Zone 1 (Hazratganj / Central)", "code": "ZONE-01", "office": "Zone 1 Office, Lalbagh, Lucknow-226001", "phone": "8874241500"},
    2: {"name": "Zone 2 (Aishbagh / Old City South)", "code": "ZONE-02", "office": "Zone 2 Office, Aishbagh, Lucknow", "phone": "8318813463"},
    3: {"name": "Zone 3 (Aliganj / North)", "code": "ZONE-03", "office": "Zone 3 Office, Sector E Aliganj, Lucknow", "phone": "8528907375"},
    4: {"name": "Zone 4 (Gomti Nagar / East)", "code": "ZONE-04", "office": "Zone 4 Office, Gomti Nagar, Lucknow", "phone": "8810721513"},
    5: {"name": "Zone 5 (Alambagh / South-West)", "code": "ZONE-05", "office": "Zone 5 Office, Alambagh, Lucknow", "phone": "8810724965"},
    6: {"name": "Zone 6 (Chowk / West)", "code": "ZONE-06", "office": "Zone 6 Office, Chowk, Lucknow", "phone": "8874704500"},
    7: {"name": "Zone 7 (Chinhat / Indira Nagar)", "code": "ZONE-07", "office": "Zone 7 Office, Chinhat / Indira Nagar, Lucknow", "phone": "8810724166"},
    8: {"name": "Zone 8 (Sarojini Nagar / South)", "code": "ZONE-08", "office": "Zone 8 Office, Kanpur Road / Sarojini Nagar, Lucknow", "phone": "8808866500"},
}

# Write jurisdiction_registry.csv
registry_headers = [
    "jurisdiction_version", "version_type", "zone_id", "zone_number", "zone_name",
    "ward_id", "ward_number", "ward_name_hindi", "ward_name_en", "administrative_status",
    "geometry_source_id", "geometry_status", "alignment_status", "legacy_ward_num",
    "legacy_ward_name", "legal_basis_source_id", "effective_from", "effective_to",
    "derivation_method", "notes"
]

registry_rows = []
for w in WARDS_DEFINITION:
    wnum, hname, ename, znum, lnum, lname, astat, nts = w
    zinfo = ZONE_METADATA[znum]
    geom_status = "SECONDARY_LEGACY" if lnum is not None else "NOT_AVAILABLE"
    geom_source = "SRC-GIS-001" if lnum is not None else "NOT_AVAILABLE"
    
    row = {
        "jurisdiction_version": "LKO-JUR-2023-01",
        "version_type": "CIVICTRACE_INTERNAL",
        "zone_id": zinfo["code"],
        "zone_number": znum,
        "zone_name": zinfo["name"],
        "ward_id": f"WARD-{wnum:03d}",
        "ward_number": wnum,
        "ward_name_hindi": hname,
        "ward_name_en": ename,
        "administrative_status": "VERIFIED",
        "geometry_source_id": geom_source,
        "geometry_status": geom_status,
        "alignment_status": astat,
        "legacy_ward_num": lnum if lnum is not None else "",
        "legacy_ward_name": lname if lname is not None else "",
        "legal_basis_source_id": "SRC-GIS-002",
        "effective_from": "2022-10-31",
        "effective_to": "",
        "derivation_method": "PRIMARY_ADMINISTRATIVE_RECORD",
        "notes": nts
    }
    registry_rows.append(row)

for rpath in [os.path.join(DATA_GIS_DIR, "jurisdiction_registry.csv"), os.path.join(VERIFIED_DIR, "jurisdiction_registry.csv")]:
    with open(rpath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=registry_headers)
        writer.writeheader()
        writer.writerows(registry_rows)
    print(f"Wrote {rpath}")

# --- 4. PROCESS RAW GEOMETRY & PRODUCE LUCKNOW_WARDS.GEOJSON ---
raw_ward_path = os.path.join(RAW_DIR, "datameet_lucknow_ward_boundary_raw.geojson")
with open(raw_ward_path, 'r', encoding='utf-8') as f:
    dm_raw = json.load(f)

# Index DataMeet features by legacy Ward Num
dm_features_by_num = {}
for feat in dm_raw['features']:
    p = feat['properties']
    wn = p.get('Ward Num')
    # Filter out Airport and Cantonment (wn == 0)
    if wn is not None and wn > 0:
        dm_features_by_num[wn] = feat

print(f"Indexed {len(dm_features_by_num)} positive legacy DataMeet polygons.")

# Build ward GeoJSON features
ward_geojson_features = []
unmatched_wards = []

for w in WARDS_DEFINITION:
    wnum, hname, ename, znum, lnum, lname, astat, nts = w
    zinfo = ZONE_METADATA[znum]
    
    # If legacy polygon exists, attach geometry
    if lnum is not None and lnum in dm_features_by_num:
        raw_feat = dm_features_by_num[lnum]
        geom = raw_feat['geometry']
        geom_status = "SECONDARY_LEGACY"
        geom_source = "SRC-GIS-001"
    else:
        geom = None
        geom_status = "NOT_AVAILABLE"
        geom_source = "NOT_AVAILABLE"
        unmatched_wards.append(wnum)

    if geom is not None:
        # Construct cleansed RFC 7946 feature
        feat_dict = {
            "type": "Feature",
            "id": f"WARD-{wnum:03d}",
            "properties": {
                "ward_id": f"WARD-{wnum:03d}",
                "ward_number": wnum,
                "ward_name": f"{hname} ({ename})",
                "ward_name_hindi": hname,
                "ward_name_en": ename,
                "zone_id": zinfo["code"],
                "zone_number": znum,
                "zone_name": zinfo["name"],
                "administrative_status": "VERIFIED",
                "geometry_source_id": geom_source,
                "geometry_status": geom_status,
                "alignment_status": astat,
                "legacy_ward_num": lnum,
                "legacy_ward_name": lname,
                "jurisdiction_version": "LKO-JUR-2023-01",
                "version_type": "CIVICTRACE_INTERNAL",
                "legal_basis_source_id": "SRC-GIS-002",
                "notes": nts
            },
            "geometry": geom
        }
        ward_geojson_features.append(feat_dict)

wards_geojson_output = {
    "type": "FeatureCollection",
    "name": "lucknow_wards",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": ward_geojson_features
}

for wpath in [os.path.join(DATA_GIS_DIR, "lucknow_wards.geojson"), 
              os.path.join(PROCESSED_DIR, "lucknow_wards_cleaned.geojson"),
              os.path.join(VERIFIED_DIR, "lucknow_wards_verified.geojson")]:
    with open(wpath, 'w', encoding='utf-8') as f:
        json.dump(wards_geojson_output, f, ensure_ascii=False, indent=2)
    print(f"Wrote {wpath} ({len(ward_geojson_features)} features)")

print(f"Unmatched modern wards without legacy polygon (missing geometry): {unmatched_wards}")

# --- 5. SYNTHESIZE 8 ZONES (DERIVED_CIVICTRACE_GEOMETRY) ---
print("\nSynthesizing 8 modern municipal zones via spatial union of constituent wards...")
zone_features = []

for znum in range(1, 9):
    zinfo = ZONE_METADATA[znum]
    constituent_geoms = []
    constituent_wards = []
    
    for f in ward_geojson_features:
        if f['properties']['zone_number'] == znum:
            s_geom = shape(f['geometry'])
            if s_geom.is_valid:
                constituent_geoms.append(s_geom)
                constituent_wards.append(f['properties']['ward_number'])
            else:
                s_clean = s_geom.buffer(0)
                constituent_geoms.append(s_clean)
                constituent_wards.append(f['properties']['ward_number'])

    if constituent_geoms:
        dissolved = unary_union(constituent_geoms)
        if not dissolved.is_valid:
            dissolved = dissolved.buffer(0)
            
        z_feat = {
            "type": "Feature",
            "id": zinfo["code"],
            "properties": {
                "zone_id": zinfo["code"],
                "zone_number": znum,
                "zone_name": zinfo["name"],
                "administrative_status": "VERIFIED",
                "geometry_source_id": "SRC-GIS-001",
                "geometry_status": "DERIVED_CIVICTRACE_GEOMETRY",
                "alignment_status": "PARTIALLY_VERIFIED",
                "ward_count": len(constituent_wards),
                "constituent_wards": constituent_wards,
                "zonal_office_location": zinfo["office"],
                "zonal_officer_phone": zinfo["phone"],
                "jurisdiction_version": "LKO-JUR-2023-01",
                "version_type": "CIVICTRACE_INTERNAL",
                "legal_basis_source_id": "SRC-GIS-004",
                "derivation_method": "SPATIAL_DISSOLVE_OF_CONSTITUENT_WARDS",
                "notes": f"Computational polygon synthesized by CivicTrace by dissolving {len(constituent_wards)} constituent ward polygons from SRC-GIS-001. Inherits legacy baseline uncertainty; does not capture 88 peripheral revenue villages awaiting municipal GIS vector release."
            },
            "geometry": mapping(dissolved)
        }
        zone_features.append(z_feat)
        print(f"  Synthesized {zinfo['code']} ({zinfo['name']}) from {len(constituent_wards)} wards. Geometry type: {dissolved.geom_type}")

zones_geojson_output = {
    "type": "FeatureCollection",
    "name": "lucknow_zones",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": zone_features
}

for zpath in [os.path.join(DATA_GIS_DIR, "lucknow_zones.geojson"),
              os.path.join(PROCESSED_DIR, "lucknow_zones_synthesized.geojson"),
              os.path.join(VERIFIED_DIR, "lucknow_zones_verified.geojson")]:
    with open(zpath, 'w', encoding='utf-8') as f:
        json.dump(zones_geojson_output, f, ensure_ascii=False, indent=2)
    print(f"Wrote {zpath} ({len(zone_features)} features)")

# --- 6. HIERARCHICAL JURISDICTION MASTER JSON ---
master_json = {
    "jurisdiction_version": "LKO-JUR-2023-01",
    "version_type": "CIVICTRACE_INTERNAL",
    "state": "Uttar Pradesh",
    "city": "Lucknow",
    "legal_basis": {
        "source_id": "SRC-GIS-002",
        "title": "Uttar Pradesh Gazette Delimitation Notification No. 1774/9-1-2022",
        "effective_from": "2022-10-31",
        "effective_to": None,
        "verification_status": "VERIFIED",
        "authority": "Department of Urban Development, Government of Uttar Pradesh"
    },
    "summary": {
        "total_administrative_zones": 8,
        "total_administrative_wards": 110,
        "total_geometry_features_wards": len(ward_geojson_features),
        "total_geometry_features_zones": len(zone_features),
        "official_geometry_count": 0,
        "secondary_legacy_geometry_count": len(ward_geojson_features),
        "derived_geometry_count": len(zone_features),
        "missing_geometry_count": len(unmatched_wards)
    },
    "zones": []
}

for znum in range(1, 9):
    zinfo = ZONE_METADATA[znum]
    zone_entry = {
        "zone_id": zinfo["code"],
        "zone_number": znum,
        "zone_name": zinfo["name"],
        "administrative_status": "VERIFIED",
        "geometry_status": "DERIVED_CIVICTRACE_GEOMETRY",
        "alignment_status": "PARTIALLY_VERIFIED",
        "office_location": zinfo["office"],
        "contact_phone": zinfo["phone"],
        "wards": []
    }
    
    for w in WARDS_DEFINITION:
        wnum, hname, ename, wznum, lnum, lname, astat, nts = w
        if wznum == znum:
            zone_entry["wards"].append({
                "ward_id": f"WARD-{wnum:03d}",
                "ward_number": wnum,
                "ward_name_hindi": hname,
                "ward_name_en": ename,
                "administrative_status": "VERIFIED",
                "geometry_source_id": "SRC-GIS-001" if lnum is not None else "NOT_AVAILABLE",
                "geometry_status": "SECONDARY_LEGACY" if lnum is not None else "NOT_AVAILABLE",
                "alignment_status": astat,
                "legacy_ward_num": lnum,
                "legacy_ward_name": lname,
                "notes": nts
            })
    master_json["zones"].append(zone_entry)

master_json_path = os.path.join(VERIFIED_DIR, "lucknow_jurisdiction_master.json")
with open(master_json_path, 'w', encoding='utf-8') as f:
    json.dump(master_json, f, ensure_ascii=False, indent=2)
print(f"Wrote {master_json_path}")

print("=" * 65)
print("PHASE 2 GIS ASSET BUILD COMPLETED SUCCESSFULLY")
print("=" * 65)
