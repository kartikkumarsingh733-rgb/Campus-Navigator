import json

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

print("Current Landmark Positions:")
for lm in landmarks:
    print(f"{lm['id']:20} : lat={lm['lat']:.6f}, lon={lm['lon']:.6f} -> {lm['name']}")

