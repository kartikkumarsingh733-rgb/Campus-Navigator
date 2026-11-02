import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Searching for building ways near Admin / Central Fountain (lat 28.608 to 28.612, lon 77.036 to 77.040):")

buildings = []
for el in raw["elements"]:
    if el["type"] == "way" and "building" in el.get("tags", {}):
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if pts:
            avg_lat = sum(p[0] for p in pts) / len(pts)
            avg_lon = sum(p[1] for p in pts) / len(pts)
            if 28.6080 <= avg_lat <= 28.6120 and 77.0360 <= avg_lon <= 77.0400:
                tags = el.get("tags", {})
                buildings.append({
                    "id": el["id"],
                    "name": tags.get("name", "unnamed"),
                    "tags": tags,
                    "center": (avg_lat, avg_lon),
                    "pts_count": len(pts),
                    "pts": pts
                })

# Sort by center latitude descending (North to South)
buildings.sort(key=lambda b: b["center"][0], reverse=True)

for b in buildings:
    print(f"Way {b['id']}: '{b['name']}' @ center ({b['center'][0]:.6f}, {b['center'][1]:.6f}), pts: {b['pts_count']}")

