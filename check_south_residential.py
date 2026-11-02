import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Checking buildings and nodes in South Residential area (lat 28.605 to 28.608, lon 77.037 to 77.041):")

for el in raw["elements"]:
    tags = el.get("tags", {})
    el_type = el["type"]
    coord = None
    if el_type == "node":
        coord = (el["lat"], el["lon"])
    elif el_type == "way":
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if pts:
            coord = (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))
    
    if coord and 28.6050 <= coord[0] <= 28.6085 and 77.0370 <= coord[1] <= 77.0410:
        if "building" in tags or "name" in tags or "tourism" in tags:
            print(f"[{el_type} {el['id']}] '{tags.get('name', 'unnamed')}' coord={coord} | {tags}")

