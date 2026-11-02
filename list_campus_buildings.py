import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("All buildings with name or tag inside NSUT:")
for el in raw["elements"]:
    if el["type"] == "way" and ("building" in el.get("tags", {}) or "amenity" in el.get("tags", {})):
        tags = el.get("tags", {})
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if pts:
            clat = sum(p[0] for p in pts)/len(pts)
            clon = sum(p[1] for p in pts)/len(pts)
            if 28.604 <= clat <= 28.616 and 77.033 <= clon <= 77.043:
                name = tags.get("name")
                btype = tags.get("building") or tags.get("amenity")
                if name or btype not in ["yes", "shed", "service", "barn"]:
                    print(f"Way {el['id']:10} '{name or 'unnamed':35}' ({btype:15}) @ ({clat:.6f}, {clon:.6f})")

