import json
import math

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

with open("campus_zones.json", "r", encoding="utf-8") as f:
    campus_zones = json.load(f)

# Collect all nodes
raw_nodes = {}
for el in raw_data.get("elements", []):
    if el.get("type") == "node":
        raw_nodes[el["id"]] = (el["lat"], el["lon"])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

MIN_LAT, MAX_LAT = 28.6040, 28.6160
MIN_LON, MAX_LON = 77.0315, 77.0440

walkable_types = {
    "footway", "path", "pedestrian", "service", "residential",
    "unclassified", "track", "steps", "living_street", "secondary", "tertiary", "road"
}

temp_graph = {}
for el in raw_data.get("elements", []):
    if el.get("type") == "way":
        tags = el.get("tags", {})
        hw = tags.get("highway")
        if hw in walkable_types:
            way_nodes = [nid for nid in el.get("nodes", []) if nid in raw_nodes and MIN_LAT <= raw_nodes[nid][0] <= MAX_LAT and MIN_LON <= raw_nodes[nid][1] <= MAX_LON]
            if len(way_nodes) >= 2:
                for i in range(len(way_nodes) - 1):
                    u, v = way_nodes[i], way_nodes[i+1]
                    d = haversine(raw_nodes[u][0], raw_nodes[u][1], raw_nodes[v][0], raw_nodes[v][1])
                    temp_graph.setdefault(u, []).append((v, d, hw, el["id"]))
                    temp_graph.setdefault(v, []).append((u, d, hw, el["id"]))

visited = set()
components = []
for n in temp_graph:
    if n not in visited:
        comp = []
        q = [n]
        visited.add(n)
        for cur in q:
            comp.append(cur)
            for nxt, _, _, _ in temp_graph.get(cur, []):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        components.append(comp)

main_comp = set(max(components, key=len))

buildings_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for el in raw_data.get("elements", []):
    if el.get("type") == "way" and "building" in el.get("tags", {}):
        way_nodes = el.get("nodes", [])
        coords = []
        in_bounds = False
        for nid in way_nodes:
            if nid in raw_nodes:
                lat, lon = raw_nodes[nid]
                if MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON:
                    in_bounds = True
                coords.append([lon, lat])
        if in_bounds and len(coords) >= 3:
            tags = el.get("tags", {})
            name = tags.get("name", "")
            b_type = tags.get("building", "yes")
            buildings_geojson["features"].append({
                "type": "Feature",
                "properties": {
                    "id": el["id"],
                    "name": name,
                    "building": b_type,
                    "amenity": tags.get("amenity", "")
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            })

nodes_dict = {}
for nid in main_comp:
    nodes_dict[str(nid)] = [round(raw_nodes[nid][0], 6), round(raw_nodes[nid][1], 6)]

clean_edges = []
adj_list = {}
edge_set = set()

for u in main_comp:
    adj_list[str(u)] = []
    for v, d, hw, way_id in temp_graph.get(u, []):
        if v in main_comp:
            adj_list[str(u)].append({
                "to": str(v),
                "dist": round(d, 2),
                "type": hw,
                "edgeId": f"e_{min(u,v)}_{max(u,v)}"
            })
            pair = tuple(sorted([u, v]))
            if pair not in edge_set:
                edge_set.add(pair)
                clean_edges.append({
                    "id": f"e_{min(u,v)}_{max(u,v)}",
                    "u": str(min(u, v)),
                    "v": str(max(u, v)),
                    "dist": round(d, 2),
                    "type": hw,
                    "coords": [
                        [round(raw_nodes[min(u, v)][0], 6), round(raw_nodes[min(u, v)][1], 6)],
                        [round(raw_nodes[max(u, v)][0], 6), round(raw_nodes[max(u, v)][1], 6)]
                    ],
                    "blocked": False,
                    "isAccessible": (hw != "steps")
                })

for lm in landmarks:
    nid = lm["nearest_node"]
    lm["nearest_node"] = str(nid)
    lm["coords"] = [lm["lat"], lm["lon"]]

js_content = f"""// NSUT Dwarka Smart Campus Navigation & Resource Optimizer
// Graph Dataset generated from OpenStreetMap & The Alliance Official Campus Map

window.CAMPUS_DATA = {{
  campusCenter: [28.6100, 77.0375],
  bounds: [
    [28.6040, 77.0315],
    [28.6160, 77.0440]
  ],
  campusBoundary: {json.dumps(campus_zones['campus_boundary'])},
  zones: {json.dumps(campus_zones['zones'], indent=2)},
  decorativeTrees: {json.dumps(campus_zones['decorative_trees'])},
  landmarks: {json.dumps(landmarks, indent=2)},
  nodes: {json.dumps(nodes_dict)},
  edges: {json.dumps(clean_edges)},
  adjacency: {json.dumps(adj_list)},
  buildingsGeoJSON: {json.dumps(buildings_geojson)}
}};
"""

with open("graphData.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Updated graphData.js with Alliance Campus Zones and Trees!")
