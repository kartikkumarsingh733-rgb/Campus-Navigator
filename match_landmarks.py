import json
import math

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = {}
for el in data.get("elements", []):
    if el.get("type") == "node":
        nodes[el["id"]] = {"id": el["id"], "lat": el["lat"], "lon": el["lon"]}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Build main component
MIN_LAT, MAX_LAT = 28.6040, 28.6160
MIN_LON, MAX_LON = 77.0315, 77.0440

walkable_types = {
    "footway", "path", "pedestrian", "service", "residential",
    "unclassified", "track", "steps", "living_street", "secondary", "tertiary", "road"
}

graph = {}
for el in data.get("elements", []):
    if el.get("type") == "way":
        tags = el.get("tags", {})
        if tags.get("highway") in walkable_types:
            way_nodes = [nid for nid in el.get("nodes", []) if nid in nodes and MIN_LAT <= nodes[nid]["lat"] <= MAX_LAT and MIN_LON <= nodes[nid]["lon"] <= MAX_LON]
            for i in range(len(way_nodes) - 1):
                u, v = way_nodes[i], way_nodes[i+1]
                d = haversine(nodes[u]["lat"], nodes[u]["lon"], nodes[v]["lat"], nodes[v]["lon"])
                graph.setdefault(u, []).append((v, d))
                graph.setdefault(v, []).append((u, d))

# Find largest component
visited = set()
components = []
for node in graph:
    if node not in visited:
        comp = []
        q = [node]
        visited.add(node)
        for cur in q:
            comp.append(cur)
            for nxt, _ in graph.get(cur, []):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        components.append(comp)

main_comp_nodes = set(max(components, key=len))
print(f"Main component has {len(main_comp_nodes)} nodes")

# Known landmarks from OSM and Alliance Map
landmarks_defs = [
    {
        "id": "main_gate",
        "name": "Main Gate",
        "aliases": ["Gate 1", "Dwarka Mor Gate", "South Gate"],
        "category": "Gates",
        "lat": 28.608484,
        "lon": 77.035251,
        "description": "Primary campus entrance on Azad Hind Fauj Marg with guard posts and bus stop."
    },
    {
        "id": "north_gate",
        "name": "North Gate",
        "aliases": ["Gate 2", "Dwarka Sector 3 North Gate"],
        "category": "Gates",
        "lat": 28.613175,
        "lon": 77.033627,
        "description": "Northern entry point close to Design Block, J.C. Bose hostel, and shopping stalls."
    },
    {
        "id": "design_block",
        "name": "Design Block",
        "aliases": ["DoD", "Department of Design"],
        "category": "Academic",
        "lat": 28.614200,
        "lon": 77.034100,
        "description": "Department of Design studios, workshop labs, and design exhibition halls."
    },
    {
        "id": "boys_hostels",
        "name": "Boys' Hostels Complex",
        "aliases": ["BH Complex", "Ramanujan Hostel", "Aryabhatta Hostel", "J.C. Bose Hostel"],
        "category": "Hostels",
        "lat": 28.613635,
        "lon": 77.034314,
        "description": "Hostels for male students with dining halls, courtyards, and common rooms."
    },
    {
        "id": "parking_west",
        "name": "West Campus Parking",
        "aliases": ["Main Parking", "Vehicles Parking"],
        "category": "Utility",
        "lat": 28.610608,
        "lon": 77.035970,
        "description": "Designated parking area for students, faculty, and visitor vehicles."
    },
    {
        "id": "amul_ground",
        "name": "Amul Ground & Kiosk",
        "aliases": ["Amul Booth", "Amul Lawn"],
        "category": "Food & Hangouts",
        "lat": 28.611400,
        "lon": 77.035800,
        "description": "Popular student hangout lawn with an official Amul dairy and snacks parlour."
    },
    {
        "id": "nescii_lawns",
        "name": "Nescii Lawns",
        "aliases": ["Shaheed Vatika", "Front Lawns"],
        "category": "Hangouts",
        "lat": 28.608856,
        "lon": 77.035895,
        "description": "Iconic expansive green lawn where college fests, society jams, and gatherings occur."
    },
    {
        "id": "admin_block",
        "name": "Admin Block",
        "aliases": ["Administrative Building", "VC Office", "Main Auditorium"],
        "category": "Admin",
        "lat": 28.609847,
        "lon": 77.037082,
        "description": "Hub of university administration, VC office, registrar, accounts, and main auditorium on 2nd floor."
    },
    {
        "id": "central_fountain",
        "name": "Central Fountain",
        "aliases": ["Admin Circle", "Fountain Roundabout"],
        "category": "Landmarks",
        "lat": 28.610056,
        "lon": 77.037968,
        "description": "Ornamental central fountain circle connecting Admin, Library, and Academic blocks."
    },
    {
        "id": "block_6",
        "name": "Block 6",
        "aliases": ["Academic Block 6", "Computer Engineering", "IT Block"],
        "category": "Academic",
        "lat": 28.609300,
        "lon": 77.038100,
        "description": "Academic block housing Computer Engineering, Information Technology, and advanced compute labs."
    },
    {
        "id": "block_4",
        "name": "Block 4",
        "aliases": ["Academic Block 4", "ECE Block"],
        "category": "Academic",
        "lat": 28.608700,
        "lon": 77.037500,
        "description": "Electronics & Communication Engineering department, labs, and faculty rooms."
    },
    {
        "id": "block_5",
        "name": "Block 5",
        "aliases": ["Academic Block 5", "ICE Block"],
        "category": "Academic",
        "lat": 28.608600,
        "lon": 77.038300,
        "description": "Instrumentation & Control Engineering block and specialized research laboratories."
    },
    {
        "id": "moksha_ground",
        "name": "Moksha Ground",
        "aliases": ["Festival Ground", "Open Stage Ground"],
        "category": "Hangouts",
        "lat": 28.610800,
        "lon": 77.037100,
        "description": "Massive central campus ground hosting the annual cultural fest Moksha and large concerts."
    },
    {
        "id": "student_center",
        "name": "Student Center & Canteen",
        "aliases": ["Canteen", "Student Activity Canteen", "Zomato Point"],
        "category": "Food & Hangouts",
        "lat": 28.611663,
        "lon": 77.036911,
        "description": "Central multi-cuisine student cafeteria, refreshment counters, and hangout lounge."
    },
    {
        "id": "apj_complex",
        "name": "APJ Abdul Kalam Complex",
        "aliases": ["APJ Complex", "Lecture Theatres", "LT 1-12"],
        "category": "Academic",
        "lat": 28.611974,
        "lon": 77.037063,
        "description": "Modern multi-tiered Lecture Theatre Complex where core engineering lectures and orientations take place."
    },
    {
        "id": "stationery",
        "name": "Stationery & Utility Complex",
        "aliases": ["Shopping Complex", "Book Depot", "Photocopy Shop"],
        "category": "Utility",
        "lat": 28.612321,
        "lon": 77.037526,
        "description": "On-campus stationery, textbook dispensary, high-speed xerox, and project binding shop."
    },
    {
        "id": "smart_block",
        "name": "Smart Block",
        "aliases": ["Smart Classrooms", "New Academic Complex"],
        "category": "Academic",
        "lat": 28.612011,
        "lon": 77.037664,
        "description": "Hi-tech air-conditioned smart classrooms equipped with digital interactive podiums."
    },
    {
        "id": "clinic",
        "name": "Campus Clinic",
        "aliases": ["Medical Centre", "Health Centre", "Dispensary"],
        "category": "Utility",
        "lat": 28.611698,
        "lon": 77.038589,
        "description": "24/7 campus medical aid unit, duty physicians, first-aid, and emergency ambulance dispatch."
    },
    {
        "id": "kaveri_hostel",
        "name": "Kaveri Hostel",
        "aliases": ["Kaveri Girls Hostel", "GH Kaveri"],
        "category": "Hostels",
        "lat": 28.613742,
        "lon": 77.038450,
        "description": "Northern girls' hostel with attached mess, lawn garden, and study reading rooms."
    },
    {
        "id": "mandir",
        "name": "Campus Mandir",
        "aliases": ["Temple", "Sulahkul Mandir"],
        "category": "Landmarks",
        "lat": 28.612800,
        "lon": 77.039200,
        "description": "Serene campus temple sanctuary set amongst verdant trees for meditation and prayers."
    },
    {
        "id": "f_tech_block",
        "name": "Faculty of Technology (MPC)",
        "aliases": ["F. Tech Block", "Multi-Purpose Complex", "Fashion Tech"],
        "category": "Academic",
        "lat": 28.611371,
        "lon": 77.039070,
        "description": "State-of-the-art multi-purpose academic complex housing emerging tech departments and workshops."
    },
    {
        "id": "central_library",
        "name": "Central Library",
        "aliases": ["Library", "Digital Reading Room"],
        "category": "Academic",
        "lat": 28.610395,
        "lon": 77.038969,
        "description": "Three-storey central library boasting over 100,000 volumes, IEEE digital archives, and quiet study zones."
    },
    {
        "id": "sac",
        "name": "Student Activity Centre (SAC)",
        "aliases": ["SAC", "Clubs Hub", "Gymnasium"],
        "category": "Hangouts",
        "lat": 28.610386,
        "lon": 77.039310,
        "description": "Headquarters of technical and cultural student societies, dance/music rooms, indoor games, and gym."
    },
    {
        "id": "mgmt_block",
        "name": "Management Block",
        "aliases": ["DMS", "Department of Management Studies"],
        "category": "Academic",
        "lat": 28.610200,
        "lon": 77.040500,
        "description": "Department of Management Studies (MBA/BBA programs) seminar halls and executive conference rooms."
    },
    {
        "id": "tnp_building",
        "name": "Training & Placement Cell (TnP)",
        "aliases": ["T&P Cell", "Placement Office"],
        "category": "Admin",
        "lat": 28.608570,
        "lon": 77.039573,
        "description": "Campus recruitment hub featuring corporate interview suites, group discussion rooms, and presentation halls."
    },
    {
        "id": "girls_hostels",
        "name": "Girls' Hostels Complex (GH)",
        "aliases": ["Alaknanda Hostel", "GH-1", "GH-2", "GH-3"],
        "category": "Hostels",
        "lat": 28.607500,
        "lon": 77.039600,
        "description": "South-campus residential complex for female students, gated with 24/7 security and sports badminton court."
    },
    {
        "id": "sports_grounds",
        "name": "Sports Complex & Stadium",
        "aliases": ["Cricket Ground", "Football Ground", "Running Track", "Stadium"],
        "category": "Sports",
        "lat": 28.609533,
        "lon": 77.041012,
        "description": "Grand sports arena featuring Olympic-size athletic running track, cricket pitch, football turf, and tennis courts."
    }
]

print(f"\nMatching {len(landmarks_defs)} landmarks to nearest node in main component...")
for lm in landmarks_defs:
    best_nid = None
    min_dist = float('inf')
    for nid in main_comp_nodes:
        d = haversine(lm["lat"], lm["lon"], nodes[nid]["lat"], nodes[nid]["lon"])
        if d < min_dist:
            min_dist = d
            best_nid = nid
    lm["nearest_node"] = best_nid
    lm["snap_distance_m"] = round(min_dist, 1)
    print(f"  {lm['name']}: node {best_nid} ({min_dist:.1f} m)")

with open("landmarks_snapped.json", "w", encoding="utf-8") as f:
    json.dump(landmarks_defs, f, indent=2)

