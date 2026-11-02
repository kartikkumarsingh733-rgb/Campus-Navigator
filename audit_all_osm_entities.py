import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

campus_elements = []

for el in raw["elements"]:
    tags = el.get("tags", {})
    name = tags.get("name")
    if not name:
        continue
    
    el_type = el["type"]
    center = None
    if el_type == "node":
        center = (el["lat"], el["lon"])
    elif el_type == "way":
        way_nodes = el.get("nodes", [])
        pts = [nodes[nid] for nid in way_nodes if nid in nodes]
        if pts:
            center = (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))
            
    # Filter strictly to NSUT inside campus gates (lon >= 77.0335)
    if center and 28.6040 <= center[0] <= 28.6160 and 77.0335 <= center[1] <= 77.0435:
        campus_elements.append({
            "type": el_type,
            "id": el["id"],
            "name": name,
            "tags": tags,
            "coord": center
        })

with open("nsut_internal_osm.json", "w", encoding="utf-8") as f:
    json.dump(campus_elements, f, indent=2, ensure_ascii=False)

print(f"Internal NSUT Elements: {len(campus_elements)}")
for item in sorted(campus_elements, key=lambda x: x["name"]):
    safe_name = item['name'].encode('ascii', 'replace').decode('ascii')
    tag_info = item['tags'].get('building') or item['tags'].get('amenity') or item['tags'].get('highway') or item['tags'].get('leisure')
    print(f"[{item['type']:4} {item['id']:11}] '{safe_name}' -> ({item['coord'][0]:.6f}, {item['coord'][1]:.6f}) | {tag_info}")
