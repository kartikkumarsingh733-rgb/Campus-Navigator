import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

elements = data.get("elements", [])
print(f"Total elements: {len(elements)}")

nodes_by_id = {}
for el in elements:
    if el.get("type") == "node":
        nodes_by_id[el["id"]] = (el.get("lat"), el.get("lon"))

named_items = []
highways = []
buildings = []

for el in elements:
    tags = el.get("tags", {})
    name = tags.get("name")
    el_type = el.get("type")
    
    # Calculate center coordinate if way
    center = None
    if el_type == "node":
        center = (el.get("lat"), el.get("lon"))
    elif el_type == "way":
        way_nodes = el.get("nodes", [])
        pts = [nodes_by_id[nid] for nid in way_nodes if nid in nodes_by_id]
        if pts:
            center = (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))

    if name:
        category = tags.get("amenity") or tags.get("building") or tags.get("highway") or tags.get("leisure") or tags.get("shop") or "other"
        named_items.append({
            "type": el_type,
            "id": el.get("id"),
            "name": name,
            "category": category,
            "tags": tags,
            "coord": center
        })
    if "highway" in tags:
        highways.append(el)
    if "building" in tags:
        buildings.append(el)

with open("named_items.json", "w", encoding="utf-8") as f:
    json.dump(named_items, f, indent=2, ensure_ascii=False)

print(f"Named items saved: {len(named_items)}")
print(f"Highways count: {len(highways)}")
print(f"Buildings count: {len(buildings)}")

# Filter specifically inside NSUT Campus bounds
campus_items = []
for item in named_items:
    if item["coord"]:
        lat, lon = item["coord"]
        if 28.604 <= lat <= 28.616 and 77.032 <= lon <= 77.044:
            campus_items.append(item)

print(f"\nItems inside NSUT Campus bounds: {len(campus_items)}")
for it in campus_items:
    safe_name = it['name'].encode('ascii', 'replace').decode('ascii')
    print(f"  [{it['type']} {it['id']}] {safe_name} ({it['category']}) @ {it['coord']}")
