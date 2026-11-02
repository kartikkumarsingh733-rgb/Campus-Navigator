import json
import math

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

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

exact_positions = {
    "block_6": {
        "lat": 28.610590,
        "lon": 77.037850,
        "name": "Block 6 (COE / IT)",
        "desc": "Top academic building (North of fountain) housing Computer Engineering (COE) and Information Technology (IT)."
    },
    "block_4": {
        "lat": 28.609550,
        "lon": 77.037580,
        "name": "Block 4 (ECE)",
        "desc": "Bottom-left academic building (South-West of fountain) housing Electronics & Communication Engineering (ECE)."
    },
    "block_5": {
        "lat": 28.609740,
        "lon": 77.038520,
        "name": "Block 5 (ICE)",
        "desc": "Bottom-right academic building (South-East of fountain) housing Instrumentation & Control Engineering (ICE)."
    }
}

for lm_id, info in exact_positions.items():
    best_nid = None
    min_dist = float('inf')
    for nid, (nlat, nlon) in nodes.items():
        d = haversine(info["lat"], info["lon"], nlat, nlon)
        if d < min_dist:
            min_dist = d
            best_nid = nid
    print(f"Landmark {lm_id}: ({info['lat']}, {info['lon']}) -> nearest node {best_nid} at {min_dist:.1f} m")

    for lm in landmarks:
        if lm["id"] == lm_id:
            lm["lat"] = info["lat"]
            lm["lon"] = info["lon"]
            lm["coords"] = [info["lat"], info["lon"]]
            lm["nearest_node"] = best_nid
            lm["snap_distance_m"] = round(min_dist, 1)
            lm["name"] = info["name"]
            lm["description"] = info["desc"]

with open("landmarks_snapped.json", "w", encoding="utf-8") as f:
    json.dump(landmarks, f, indent=2)

print("\nSuccessfully calibrated Block 6, Block 4, and Block 5 in landmarks_snapped.json!")

