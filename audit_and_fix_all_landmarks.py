import json
import math

with open("graphData.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
match = re.search(r'nodes:\s*(\{.*?\})\s*,\s*edges:', content, re.DOTALL)
nodes = json.loads(match.group(1))

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# The authoritative ground-truth database of NSUT Dwarka landmarks
# derived directly from OpenStreetMap node/way features and online satellite mapping:
ground_truth_landmarks = [
    {
        "id": "main_gate",
        "name": "Main Gate",
        "aliases": ["Gate 1", "Dwarka Mor Gate", "Azad Hind Fauj Marg Entrance"],
        "category": "Gates",
        "lat": 28.608484,
        "lon": 77.035251,
        "description": "Primary university entrance along Azad Hind Fauj Marg with security guardhouse and DTC bus stop."
    },
    {
        "id": "north_gate",
        "name": "North Gate",
        "aliases": ["Gate 2", "North Entrance", "Suraj Vihar Gate"],
        "category": "Gates",
        "lat": 28.613175,
        "lon": 77.033627,
        "description": "Northern campus entrance near J.C. Bose boys hostel and Suraj Vihar."
    },
    {
        "id": "mandir",
        "name": "Campus Mandir (Sulahkul Mandir)",
        "aliases": ["Sulahkul Mandir", "Temple", "Campus Temple"],
        "category": "Landmarks",
        "lat": 28.607087,
        "lon": 77.034684,
        "description": "Serene campus temple sanctuary located near Sulahkul Bridge and water body in the south-west."
    },
    {
        "id": "boys_hostels",
        "name": "Boys' Hostels Complex (North)",
        "aliases": ["BH Complex", "Ramanujan Hostel", "J.C. Bose Hostel", "Aryabhatta Hostel", "BH-1", "BH-2", "BH-3", "BH-4"],
        "category": "Hostels",
        "lat": 28.613635,
        "lon": 77.034314,
        "description": "Main residential complex for male undergraduate students with mess dining halls and courtyards."
    },
    {
        "id": "boys_hostel_south",
        "name": "Boys' Hostel (South Block)",
        "aliases": ["South Boys Hostel", "Senior Boys Hostel"],
        "category": "Hostels",
        "lat": 28.606208,
        "lon": 77.039025,
        "description": "Southern residential block for male senior and postgraduate students near sports facilities."
    },
    {
        "id": "design_block",
        "name": "Design Block (DoD / Fashion Tech)",
        "aliases": ["Department of Design", "DoD", "Fashion Technology Block", "MPC"],
        "category": "Academic",
        "lat": 28.611371,
        "lon": 77.039070,
        "description": "Department of Design studios, Fashion Design labs, prototyping facilities, and exhibition galleries."
    },
    {
        "id": "admin_block",
        "name": "Admin Block",
        "aliases": ["Administrative Building", "VC Office", "Main Auditorium"],
        "category": "Admin",
        "lat": 28.609847,
        "lon": 77.037082,
        "description": "Hub of university administration, Vice-Chancellor's office, registrar, accounts, and Main Auditorium on 2nd floor."
    },
    {
        "id": "central_fountain",
        "name": "Central Fountain",
        "aliases": ["Fountain Circle", "Admin Roundabout"],
        "category": "Landmarks",
        "lat": 28.610056,
        "lon": 77.037968,
        "description": "Ornamental central fountain circle connecting Admin Block, Block 6, Block 4, Block 5, and Library."
    },
    {
        "id": "block_6",
        "name": "Block 6 (COE / IT)",
        "aliases": ["Academic Block 6", "Computer Engineering", "IT Block"],
        "category": "Academic",
        "lat": 28.610590,
        "lon": 77.037850,
        "description": "Top academic building (North of fountain) housing Computer Engineering and Information Technology."
    },
    {
        "id": "block_4",
        "name": "Block 4 (ECE)",
        "aliases": ["Academic Block 4", "ECE Block", "Biotechnology"],
        "category": "Academic",
        "lat": 28.609550,
        "lon": 77.037580,
        "description": "Bottom-left academic building (South-West of fountain) housing Electronics & Communication Engineering."
    },
    {
        "id": "block_5",
        "name": "Block 5 (ICE)",
        "aliases": ["Academic Block 5", "ICE Block", "Automation"],
        "category": "Academic",
        "lat": 28.609740,
        "lon": 77.038520,
        "description": "Bottom-right academic building (South-East of fountain) housing Instrumentation & Control Engineering."
    },
    {
        "id": "mini_audi",
        "name": "Mini Auditorium",
        "aliases": ["Mini Audi", "Academic Auditorium"],
        "category": "Academic",
        "lat": 28.609595,
        "lon": 77.038066,
        "description": "Auditorium hall situated between the academic blocks hosting guest lectures and society events."
    },
    {
        "id": "central_library",
        "name": "Central Library",
        "aliases": ["Library", "Central Reading Room"],
        "category": "Academic",
        "lat": 28.610395,
        "lon": 77.038969,
        "description": "Three-storey university library with IEEE digital repository, book dispensary, and reading halls."
    },
    {
        "id": "sac",
        "name": "Student Activity Centre (SAC)",
        "aliases": ["SAC", "Clubs Hub", "Gymnasium"],
        "category": "Hangouts",
        "lat": 28.610386,
        "lon": 77.039310,
        "description": "Student societies headquarters, cultural rehearsal rooms, sports gym, and indoor recreation games."
    },
    {
        "id": "apj_complex",
        "name": "APJ Abdul Kalam Complex",
        "aliases": ["APJ Complex", "Lecture Theatres", "LT 1-12"],
        "category": "Academic",
        "lat": 28.611974,
        "lon": 77.037063,
        "description": "Multi-tier modern Lecture Theatre Complex where core undergraduate lectures are conducted."
    },
    {
        "id": "student_center",
        "name": "Student Center & Canteen",
        "aliases": ["Canteen", "Cafeteria", "Student Centre"],
        "category": "Food & Hangouts",
        "lat": 28.611663,
        "lon": 77.036911,
        "description": "Main campus cafeteria, multi-cuisine food court, and vibrant student socializing lounge."
    },
    {
        "id": "amul_ground",
        "name": "Amul Ground & Kiosk",
        "aliases": ["Amul Parlour", "Amul Lawn"],
        "category": "Food & Hangouts",
        "lat": 28.611500,
        "lon": 77.036500,
        "description": "Popular outdoor student hangout lawn with an official Amul ice cream and dairy booth."
    },
    {
        "id": "smart_block",
        "name": "Smart Block",
        "aliases": ["Smart Classrooms", "Smart Class"],
        "category": "Academic",
        "lat": 28.612011,
        "lon": 77.037664,
        "description": "Modern smart classroom complex equipped with interactive digital podiums and audiovisual gear."
    },
    {
        "id": "stationery",
        "name": "Stationery & Shopping Complex",
        "aliases": ["Shopping Complex", "Photocopy Shop", "Book Depot"],
        "category": "Utility",
        "lat": 28.612321,
        "lon": 77.037526,
        "description": "Stationery supplies, printing, blueprint scanning, xerox, and project binding stores."
    },
    {
        "id": "clinic",
        "name": "Campus Clinic & Health Centre",
        "aliases": ["Medical Centre", "Dispensary", "Health Centre"],
        "category": "Utility",
        "lat": 28.611698,
        "lon": 77.038589,
        "description": "University 24/7 health center providing primary healthcare, first-aid, and medical observation."
    },
    {
        "id": "kaveri_hostel",
        "name": "Kaveri Girls' Hostel",
        "aliases": ["Kaveri Hostel", "GH 2"],
        "category": "Hostels",
        "lat": 28.613742,
        "lon": 77.038450,
        "description": "Northern girls' hostel with attached dining mess, garden lawns, and quiet study rooms."
    },
    {
        "id": "girls_hostels",
        "name": "Girls' Hostels Complex (South)",
        "aliases": ["Alaknanda Hostel", "GH-1", "GH-3"],
        "category": "Hostels",
        "lat": 28.608039,
        "lon": 77.039571,
        "description": "Gated residential hostel complex for female students with security and badminton court."
    },
    {
        "id": "tnp_building",
        "name": "Training & Placement Cell (TnP)",
        "aliases": ["T&P Cell", "Placement Office"],
        "category": "Admin",
        "lat": 28.608570,
        "lon": 77.039573,
        "description": "Campus placements headquarters with corporate interview cabins and auditorium."
    },
    {
        "id": "sports_grounds",
        "name": "Sports Complex & Stadium",
        "aliases": ["Stadium", "Athletic Track", "Cricket Ground", "Football Ground"],
        "category": "Sports",
        "lat": 28.610394,
        "lon": 77.041365,
        "description": "Grand athletic stadium, standard 400m running track, cricket pitch, football field, and tennis courts."
    },
    {
        "id": "parking_west",
        "name": "West Campus Parking",
        "aliases": ["Faculty Parking", "Student Parking"],
        "category": "Utility",
        "lat": 28.610609,
        "lon": 77.035970,
        "description": "Primary vehicle parking lot for faculty, staff, and students along western perimeter road."
    },
    {
        "id": "nescii_lawns",
        "name": "Nescii Lawns (Shaheed Vatika)",
        "aliases": ["Shaheed Vatika", "Front Lawns"],
        "category": "Hangouts",
        "lat": 28.608856,
        "lon": 77.035895,
        "description": "Iconic green lawns in front of Admin Block where college festival gatherings and acoustic jams occur."
    },
    {
        "id": "moksha_ground",
        "name": "Moksha Ground",
        "aliases": ["Festival Ground", "Open Stage Ground"],
        "category": "Hangouts",
        "lat": 28.610800,
        "lon": 77.037100,
        "description": "Vast open ground hosting Moksha annual cultural festival concerts and student competitions."
    },
    {
        "id": "mgmt_block",
        "name": "Management Block (DMS)",
        "aliases": ["DMS", "Department of Management Studies"],
        "category": "Academic",
        "lat": 28.610200,
        "lon": 77.040200,
        "description": "Department of Management Studies (MBA/BBA programs) seminar halls and executive lecture rooms."
    }
]

print(f"Auditing and snapping {len(ground_truth_landmarks)} ground-truth landmarks to walking graph...")

for lm in ground_truth_landmarks:
    best_nid = None
    min_dist = float('inf')
    for nid, (nlat, nlon) in nodes.items():
        d = haversine(lm["lat"], lm["lon"], nlat, nlon)
        if d < min_dist:
            min_dist = d
            best_nid = nid
    
    lm["nearest_node"] = str(best_nid)
    lm["snap_distance_m"] = round(min_dist, 1)
    lm["coords"] = [lm["lat"], lm["lon"]]
    print(f"  {lm['name']:38} @ ({lm['lat']:.6f}, {lm['lon']:.6f}) -> Node {best_nid} ({min_dist:.1f} m)")

with open("landmarks_snapped.json", "w", encoding="utf-8") as f:
    json.dump(ground_truth_landmarks, f, indent=2)

print("\nSuccessfully updated landmarks_snapped.json with complete online ground-truth!")

