import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Buildings in the North-West / North sector (lat 28.612 to 28.616, lon 77.033 to 77.037):")

for el in raw["elements"]:
    if el["type"] == "way" and "building" in el.get("tags", {}):
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if pts:
            avg_lat = sum(p[0] for p in pts) / len(pts)
            avg_lon = sum(p[1] for p in pts) / len(pts)
            if 28.6120 <= avg_lat <= 28.6160 and 77.0330 <= avg_lon <= 77.0375:
                tags = el.get("tags", {})
                name = tags.get("name", "unnamed")
                print(f"Way {el['id']}: '{name}' ({tags.get('building')}) center=({avg_lat:.6f}, {avg_lon:.6f}), pts={len(pts)}")

