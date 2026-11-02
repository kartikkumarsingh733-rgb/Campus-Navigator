import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

for el in raw["elements"]:
    if el.get("id") == 370682386:
        pts = [nodes[nid] for nid in el.get("nodes", []) if nid in nodes]
        print(f"Way 370682386 has {len(pts)} points:")
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        print(f"  Lat range: {min(lats):.6f} to {max(lats):.6f}")
        print(f"  Lon range: {min(lons):.6f} to {max(lons):.6f}")
        print(f"  Center: ({sum(lats)/len(lats):.6f}, {sum(lons)/len(lons):.6f})")

