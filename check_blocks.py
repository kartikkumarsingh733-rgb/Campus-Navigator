import json

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

for lm in landmarks:
    if lm["id"] in ["admin_block", "central_fountain", "block_6", "block_4", "block_5"]:
        print(f"{lm['id']}: ({lm['lat']}, {lm['lon']}) -> {lm['name']}")

