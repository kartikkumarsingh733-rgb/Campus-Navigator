import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Checking relations:")
for el in raw["elements"]:
    if el["type"] == "relation":
        tags = el.get("tags", {})
        print(f"Relation {el['id']}: tags={tags}")

# Check any ways with many nodes in the range lat 28.6085-28.6115, lon 77.0370-77.0395
print("\nChecking all ways with >= 8 nodes in quad:")
for el in raw["elements"]:
    if el["type"] == "way":
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if len(pts) >= 8:
            avg_lat = sum(p[0] for p in pts) / len(pts)
            avg_lon = sum(p[1] for p in pts) / len(pts)
            if 28.6088 <= avg_lat <= 28.6115 and 77.0370 <= avg_lon <= 77.0392:
                tags = el.get("tags", {})
                print(f"Way {el['id']}: tags={tags}, center=({avg_lat:.6f}, {avg_lon:.6f}), pts={len(pts)}")

