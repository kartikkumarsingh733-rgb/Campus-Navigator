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

authoritative_landmarks = [
    {
        "id": "main_gate",
        "name": "Main Gate (Gate 1)",
        "aliases": ["Gate 1", "Dwarka Mor Gate", "Azad Hind Fauj Marg Entrance"],
        "category": "Gates",
        "lat": 28.608484,
        "lon": 77.035251,
        "description": "Primary university entrance along Azad Hind Fauj Marg with security checkpoint and DTC transit stop."
    },
    {
        "id": "north_gate",
        "name": "North Gate (Gate 2)",
        "aliases": ["Gate 2", "North Entrance", "Suraj Vihar Gate"],
        "category": "Gates",
        "lat": 28.613175,
        "lon": 77.033627,
        "description": "Northern campus entrance near Suraj Vihar, Design Block, and Boys' Hostels."
    },
    {
        "id": "mandir",
        "name": "Campus Mandir (Temple)",
        "aliases": ["Campus Temple", "Mandir", "Shiv Mandir", "Temple"],
        "category": "Landmarks",
        "lat": 28.612706,
        "lon": 77.038519,
        "description": "Revered campus temple sanctuary located in the northeast near Kaveri Girls' Hostel and lotus pond garden."
    },
    {
        "id": "boys_hostels",
        "name": "Boys' Hostels Complex (BH 1-4)",
        "aliases": ["BH Complex", "Ramanujan Hostel", "J.C. Bose Hostel", "Aryabhatta Hostel", "Raman Hostel", "BH-1", "BH-2", "BH-3", "BH-4", "Boys Mess"],
        "category": "Hostels",
        "lat": 28.613400,
        "lon": 77.034350,
        "description": "Northwest residential quadrangle housing BH-1 (Ramanujan freshers), BH-2 (Aryabhatta), BH-3 (J.C. Bose), BH-4 (Raman), dining mess halls, and sports courts."
    },
    {
        "id": "design_block",
        "name": "Design Block (Department of Design)",
        "aliases": ["Department of Design", "DoD", "Design Building", "B.Des Block"],
        "category": "Academic",
        "lat": 28.613522,
        "lon": 77.033963,
        "description": "Modern Department of Design facility near North Gate featuring design studios, prototyping labs, UI/UX suites, and exhibition spaces."
    },
    {
        "id": "admin_block",
        "name": "Admin Block & Main Audi",
        "aliases": ["Administrative Building", "VC Office", "Main Auditorium", "Administration"],
        "category": "Admin",
        "lat": 28.609847,
        "lon": 77.037082,
        "description": "Hub of university administration, Vice-Chancellor's Secretariat, Registrar, Examination Cell, and Main Auditorium on the 2nd floor."
    },
    {
        "id": "central_fountain",
        "name": "Central Fountain Circle",
        "aliases": ["Fountain Circle", "Admin Roundabout", "Central Circle"],
        "category": "Landmarks",
        "lat": 28.610056,
        "lon": 77.037968,
        "description": "Iconic central circular fountain connecting Admin Block, Block 6, Block 4, Block 5, and Central Library."
    },
    {
        "id": "block_6",
        "name": "Block 6 (COE / IT / MPAE)",
        "aliases": ["Academic Block 6", "Computer Engineering", "IT Block", "Top Academic Block"],
        "category": "Academic",
        "lat": 28.610590,
        "lon": 77.037850,
        "description": "Top academic building north of the central fountain housing Computer Science & Engineering, IT, and software labs."
    },
    {
        "id": "block_4",
        "name": "Block 4 (ECE / Biotech)",
        "aliases": ["Academic Block 4", "ECE Block", "Biotechnology", "Bottom Left Academic Block"],
        "category": "Academic",
        "lat": 28.609550,
        "lon": 77.037580,
        "description": "Bottom-left academic building southwest of fountain housing Electronics & Communication Engineering and Biotech labs."
    },
    {
        "id": "block_5",
        "name": "Block 5 (ICE / Automation)",
        "aliases": ["Academic Block 5", "ICE Block", "Instrumentation", "Bottom Right Academic Block"],
        "category": "Academic",
        "lat": 28.609740,
        "lon": 77.038520,
        "description": "Bottom-right academic building southeast of fountain housing Instrumentation & Control Engineering."
    },
    {
        "id": "mini_audi",
        "name": "Mini Auditorium",
        "aliases": ["Mini Audi", "Academic Auditorium", "Block 4-5 Audi"],
        "category": "Academic",
        "lat": 28.609595,
        "lon": 77.038066,
        "description": "Auditorium hall situated centrally between Block 4 and Block 5 hosting guest lectures, orientations, and technical society summits."
    },
    {
        "id": "central_library",
        "name": "Central Library",
        "aliases": ["Library", "Central Reading Room", "Digital Library"],
        "category": "Academic",
        "lat": 28.610395,
        "lon": 77.038969,
        "description": "Three-storey university library with IEEE digital resource access, book lending division, and silent study halls."
    },
    {
        "id": "sac",
        "name": "Student Activity Centre (SAC)",
        "aliases": ["SAC", "Clubs Hub", "Gymnasium", "Indoor Sports"],
        "category": "Hangouts",
        "lat": 28.610386,
        "lon": 77.039310,
        "description": "Student societies headquarters, dance and music rehearsal rooms, badminton hall, fitness gym, and indoor games room."
    },
    {
        "id": "apj_complex",
        "name": "APJ Abdul Kalam Complex",
        "aliases": ["APJ Complex", "Lecture Theatres", "LT 1-12"],
        "category": "Academic",
        "lat": 28.611974,
        "lon": 77.037063,
        "description": "Multi-tier modern Lecture Theatre Complex (LT 1 to LT 12) where core undergraduate lectures are conducted."
    },
    {
        "id": "student_center",
        "name": "Student Center & Canteen",
        "aliases": ["Canteen", "Cafeteria", "Student Centre", "Food Court"],
        "category": "Food & Hangouts",
        "lat": 28.611663,
        "lon": 77.036911,
        "description": "Main campus cafeteria, multi-cuisine food court, outdoor shaded tables, and vibrant student socializing lounge."
    },
    {
        "id": "amul_ground",
        "name": "Amul Ground & Kiosk",
        "aliases": ["Amul Parlour", "Amul Lawn", "Amul"],
        "category": "Food & Hangouts",
        "lat": 28.611500,
        "lon": 77.036300,
        "description": "Popular outdoor student hangout lawn with an official Amul ice cream, shakes, and dairy booth."
    },
    {
        "id": "smart_block",
        "name": "Smart Block (S-Block)",
        "aliases": ["Smart Classrooms", "Smart Class", "S Block"],
        "category": "Academic",
        "lat": 28.612011,
        "lon": 77.037664,
        "description": "Modern smart classroom complex equipped with interactive digital podiums, projectors, and seminar facilities."
    },
    {
        "id": "stationery",
        "name": "Stationery & Shopping Complex",
        "aliases": ["Shopping Complex", "Photocopy Shop", "Book Depot", "Printing"],
        "category": "Utility",
        "lat": 28.612321,
        "lon": 77.037526,
        "description": "Stationery supplies, blueprint scanning, xerox, spiral binding, and daily convenience essentials."
    },
    {
        "id": "clinic",
        "name": "Campus Clinic & Health Centre",
        "aliases": ["Medical Centre", "Dispensary", "Health Centre"],
        "category": "Utility",
        "lat": 28.611698,
        "lon": 77.038589,
        "description": "University 24/7 health center providing primary healthcare, doctor consultation, first-aid, and medical observation."
    },
    {
        "id": "kaveri_hostel",
        "name": "Kaveri Girls' Hostel (GH-2)",
        "aliases": ["Kaveri Hostel", "GH 2", "Girls Hostel North"],
        "category": "Hostels",
        "lat": 28.613742,
        "lon": 77.038450,
        "description": "Northern girls' hostel with attached dining mess, garden lawns, security, and quiet study rooms."
    },
    {
        "id": "girls_hostels",
        "name": "Girls' Hostels Complex (Alaknanda / GH-1)",
        "aliases": ["Alaknanda Hostel", "GH-1", "GH-3", "Girls Hostels South"],
        "category": "Hostels",
        "lat": 28.608039,
        "lon": 77.039571,
        "description": "Gated residential hostel complex for female students in the southeast with security, mess, and badminton court."
    },
    {
        "id": "tnp_building",
        "name": "Training & Placement Cell (TnP)",
        "aliases": ["T&P Cell", "Placement Office", "Corporate Relations"],
        "category": "Admin",
        "lat": 28.608570,
        "lon": 77.039573,
        "description": "Campus placements headquarters with corporate interview cabins, recruitment presentation halls, and GD rooms."
    },
    {
        "id": "sports_grounds",
        "name": "Sports Complex & Stadium",
        "aliases": ["Stadium", "Athletic Track", "Cricket Ground", "Football Ground", "Running Track"],
        "category": "Sports",
        "lat": 28.610394,
        "lon": 77.041365,
        "description": "Grand athletic stadium, standard 400m running track, cricket pitch, football turf, tennis courts, and basketball arena."
    },
    {
        "id": "parking_west",
        "name": "West Campus Parking",
        "aliases": ["Faculty Parking", "Student Parking", "Main Parking"],
        "category": "Utility",
        "lat": 28.610609,
        "lon": 77.035970,
        "description": "Primary vehicle parking lot for faculty, staff, and students along western perimeter avenue."
    },
    {
        "id": "nescii_lawns",
        "name": "Nescii Lawns (Shaheed Vatika)",
        "aliases": ["Shaheed Vatika", "Front Lawns", "Nescii"],
        "category": "Hangouts",
        "lat": 28.608856,
        "lon": 77.035895,
        "description": "Iconic green lawns in front of Admin Block where college festival gatherings, acoustic sessions, and student circles take place."
    },
    {
        "id": "moksha_ground",
        "name": "Moksha Ground",
        "aliases": ["Festival Ground", "Open Stage Ground", "Moksha Arena"],
        "category": "Hangouts",
        "lat": 28.610800,
        "lon": 77.037100,
        "description": "Vast open arena hosting the annual Moksha cultural festival concerts, pro-nights, and university-wide sports festivals."
    },
    {
        "id": "mgmt_block",
        "name": "Management Block (DMS)",
        "aliases": ["DMS", "Department of Management Studies", "MBA Block"],
        "category": "Academic",
        "lat": 28.610200,
        "lon": 77.040200,
        "description": "Department of Management Studies (MBA/BBA programs) seminar halls, computer lab, and executive lecture rooms."
    }
]

print(f"Auditing and snapping {len(authoritative_landmarks)} ground-truth landmarks to walking graph...")
for lm in authoritative_landmarks:
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
    print(f"  {lm['name'][:35]:35} @ ({lm['lat']:.6f}, {lm['lon']:.6f}) -> Node {best_nid} ({min_dist:.1f} m)")

with open("landmarks_snapped.json", "w", encoding="utf-8") as f:
    json.dump(authoritative_landmarks, f, indent=2)

print("\nSaved updated landmarks_snapped.json!")

