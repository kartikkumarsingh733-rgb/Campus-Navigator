import json

with open("named_items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

for it in items:
    name = it["name"]
    if any(k in name.lower() for k in ["block", "ece", "coe", "ice", "fountain", "audi", "admin", "library", "central"]):
        print(f"[{it['type']} {it['id']}] '{name}' ({it['category']}) @ {it['coord']}")

