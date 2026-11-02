import json
import math

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract nodes
nodes = {}
for el in data.get("elements", []):
    if el.get("type") == "node":
        nodes[el["id"]] = {
            "id": el["id"],
            "lat": el["lat"],
            "lon": el["lon"],
            "tags": el.get("tags", {})
        }

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Campus bounds for NSUT Dwarka
MIN_LAT, MAX_LAT = 28.6040, 28.6160
MIN_LON, MAX_LON = 77.0315, 77.0440

walkable_types = {
    "footway", "path", "pedestrian", "service", "residential",
    "unclassified", "track", "steps", "living_street", "secondary", "tertiary", "road"
}

graph = {}  # node_id -> list of {to, distance, way_id, way_type, name}
edges = []
included_node_ids = set()

for el in data.get("elements", []):
    if el.get("type") == "way":
        tags = el.get("tags", {})
        hw = tags.get("highway")
        if hw in walkable_types:
            way_nodes = el.get("nodes", [])
            # Filter to campus
            campus_nodes = [nid for nid in way_nodes if nid in nodes and MIN_LAT <= nodes[nid]["lat"] <= MAX_LAT and MIN_LON <= nodes[nid]["lon"] <= MAX_LON]
            if len(campus_nodes) >= 2:
                for i in range(len(campus_nodes) - 1):
                    u = campus_nodes[i]
                    v = campus_nodes[i+1]
                    dist = haversine(nodes[u]["lat"], nodes[u]["lon"], nodes[v]["lat"], nodes[v]["lon"])
                    if u not in graph: graph[u] = []
                    if v not in graph: graph[v] = []
                    
                    graph[u].append({"to": v, "dist": round(dist, 2), "way_id": el["id"], "type": hw, "name": tags.get("name", "")})
                    graph[v].append({"to": u, "dist": round(dist, 2), "way_id": el["id"], "type": hw, "name": tags.get("name", "")})
                    included_node_ids.add(u)
                    included_node_ids.add(v)
                    edges.append({
                        "u": u,
                        "v": v,
                        "dist": round(dist, 2),
                        "type": hw,
                        "coords": [[nodes[u]["lat"], nodes[u]["lon"]], [nodes[v]["lat"], nodes[v]["lon"]]]
                    })

print(f"Graph nodes: {len(graph)}")
print(f"Graph edges: {len(edges)}")

# Find connected components
visited = set()
components = []
for node in graph:
    if node not in visited:
        comp = []
        q = [node]
        visited.add(node)
        for cur in q:
            comp.append(cur)
            for neighbor in graph.get(cur, []):
                nxt = neighbor["to"]
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        components.append(comp)

components.sort(key=len, reverse=True)
print(f"Connected components: {len(components)}")
for i, c in enumerate(components[:5]):
    print(f"  Component {i+1}: {len(c)} nodes")

