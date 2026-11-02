import json
import math

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

with open("graphData.js", "r", encoding="utf-8") as f:
    content = f.read()

# Load nodes from graphData.js
import re
match = re.search(r'nodes:\s*(\{.*?\})\s*,\s*edges:', content, re.DOTALL)
if match:
    nodes = json.loads(match.group(1))
    print(f"Loaded {len(nodes)} nodes from graphData.js")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Exact centers specified by user:
# Block 6: Top building
# Block 4: Bottom left building
# Block 5: Bottom right building
new_coords = {
    "block_6": (28.610950, 77.037800),
    "block_4": (28.609400, 77.037550),
    "block_5": (28.609350, 77.038450)
}

for lm_id, (lat, lon) in new_coords.items():
    best_nid = None
    min_dist = float('inf')
    for nid, (nlat, nlon) in nodes.items():
        d = haversine(lat, lon, nlat, nlon)
        if d < min_dist:
            min_dist = d
            best_nid = nid
    print(f"Target {lm_id}: ({lat}, {lon}) -> nearest node {best_nid} at {min_dist:.1f} m")
    
    # Update landmark
    for lm in landmarks:
        if lm["id"] == lm_id:
            lm["lat"] = lat
            lm["lon"] = lon
            lm["coords"] = [lat, lon]
            lm["nearest_node"] = best_nid
            lm["snap_distance_m"] = round(min_dist, 1)

with open("landmarks_snapped.json", "w", encoding="utf-8") as f:
    json.dump(landmarks, f, indent=2)

print("\nUpdated landmarks_snapped.json successfully!")

