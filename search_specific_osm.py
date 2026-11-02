import json

with open("nsut_osm_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

nodes = {}
for el in raw["elements"]:
    if el["type"] == "node":
        nodes[el["id"]] = (el["lat"], el["lon"])

print("Searching all elements with 'hostel' or 'bh' or 'gh' or 'ramanujan' or 'bose' or 'design' or 'mandir' or 'temple' in tags:")
for el in raw["elements"]:
    tags = el.get("tags", {})
    name = tags.get("name", "")
    all_text = " ".join([f"{k}={v}" for k, v in tags.items()]).lower()
    
    matches = ["hostel", "ramanujan", "aryabhatt", "bose", "design", "mandir", "temple", "sulahkul", "kaveri", "alaknanda"]
    if any(m in all_text for m in matches):
        el_type = el["type"]
        coord = None
        if el_type == "node":
            coord = (el["lat"], el["lon"])
        elif el_type == "way":
            way_nodes = el.get("nodes", [])
            pts = [nodes[nid] for nid in way_nodes if nid in nodes]
            if pts:
                coord = (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))
        safe_name = name.encode('ascii', 'replace').decode('ascii')
        tag_str = str(tags).encode('ascii', 'replace').decode('ascii')
        print(f"[{el_type:4} {el.get('id'):11}] '{safe_name}' -> coord={coord} | {tag_str}")
