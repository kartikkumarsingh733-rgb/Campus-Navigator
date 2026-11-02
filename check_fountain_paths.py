import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Nodes along footways going North and South from Fountain (lat 28.609 to 28.612, lon 77.0375 to 77.0385):")
for el in raw["elements"]:
    if el["type"] == "way" and el.get("tags", {}).get("highway") in ["footway", "path", "service"]:
        way_nodes = el.get("nodes", [])
        pts = [(nid, nodes[nid][0], nodes[nid][1]) for nid in way_nodes if nid in nodes]
        for nid, lat, lon in pts:
            if 28.6090 <= lat <= 28.6115 and 77.0375 <= lon <= 77.0385:
                # print nodes near central line
                if abs(lon - 77.0379) < 0.0006:
                    print(f"Node {nid}: lat={lat:.6f}, lon={lon:.6f}")

