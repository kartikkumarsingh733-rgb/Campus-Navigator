import json
import math

# Real-world GPS coordinates for the key styled zones from the Alliance Map:
# 1. Campus Boundary Polygon (surrounds NSUT Dwarka)
campus_boundary = [
    [28.6145, 77.0325],
    [28.6155, 77.0380],
    [28.6145, 77.0425],
    [28.6110, 77.0435],
    [28.6075, 77.0440],
    [28.6045, 77.0425],
    [28.6042, 77.0360],
    [28.6055, 77.0335],
    [28.6080, 77.0330],
    [28.6115, 77.0325]
]

# 2. Moksha Ground (Central festival ground north of Block 6, south of Student Center)
# Real GPS: ~28.6100 to 28.6112 N, 77.0365 to 77.0378 E
moksha_ground_coords = [
    [28.6101, 77.0365],
    [28.6111, 77.0364],
    [28.6112, 77.0373],
    [28.6108, 77.0378],
    [28.6102, 77.0377],
    [28.6099, 77.0371]
]

# 3. Nescii Lawns (Lush lawns between western road and Admin Block)
# Real GPS: ~28.6080 to 28.6095 N, 77.0354 to 77.0366 E
nescii_lawns_coords = [
    [28.6080, 77.0355],
    [28.6094, 77.0353],
    [28.6096, 77.0362],
    [28.6089, 77.0366],
    [28.6081, 77.0364]
]

# 4. Amul Ground (Opposite Student Center, south of Boys Hostels)
amul_ground_coords = [
    [28.6113, 77.0352],
    [28.6122, 77.0350],
    [28.6123, 77.0361],
    [28.6115, 77.0362]
]

# 5. Sports Grounds & Stadium (South-East athletic stadium & fields)
sports_ground_coords = [
    [28.6085, 77.0405],
    [28.6108, 77.0408],
    [28.6110, 77.0425],
    [28.6085, 77.0425],
    [28.6075, 77.0418]
]

# 6. North Greenery (Behind Kaveri Hostel / Mandir)
north_greenery_coords = [
    [28.6138, 77.0390],
    [28.6148, 77.0392],
    [28.6146, 77.0415],
    [28.6135, 77.0410]
]

# 7. South Lawn (South of Blocks 4 and 5)
south_lawn_coords = [
    [28.6058, 77.0365],
    [28.6070, 77.0366],
    [28.6069, 77.0390],
    [28.6057, 77.0388]
]

zones = [
    {
        "id": "moksha_ground",
        "name": "Moksha Ground",
        "style": "pink_textured",
        "coords": moksha_ground_coords
    },
    {
        "id": "nescii_lawns",
        "name": "Nescii Lawns",
        "style": "mint_green",
        "coords": nescii_lawns_coords
    },
    {
        "id": "amul_ground",
        "name": "Amul Ground",
        "style": "pink_textured",
        "coords": amul_ground_coords
    },
    {
        "id": "sports_grounds",
        "name": "Sports Grounds & Stadium",
        "style": "pink_textured",
        "coords": sports_ground_coords
    },
    {
        "id": "north_greenery",
        "name": "North Woods",
        "style": "mint_green",
        "coords": north_greenery_coords
    },
    {
        "id": "south_lawn",
        "name": "Academic South Lawns",
        "style": "pink_textured",
        "coords": south_lawn_coords
    }
]

# Decorative trees scattered across campus matching the Alliance illustration
decorative_trees = [
    {"coords": [28.6088, 77.0351], "color": "#f472b6"},
    {"coords": [28.6092, 77.0350], "color": "#38bdf8"},
    {"coords": [28.6085, 77.0352], "color": "#fbbf24"},
    {"coords": [28.6078, 77.0358], "color": "#34d399"},
    {"coords": [28.6072, 77.0360], "color": "#f472b6"},
    {"coords": [28.6068, 77.0362], "color": "#38bdf8"},
    {"coords": [28.6065, 77.0365], "color": "#fbbf24"},
    {"coords": [28.6082, 77.0371], "color": "#34d399"},
    {"coords": [28.6083, 77.0378], "color": "#38bdf8"},
    {"coords": [28.6082, 77.0388], "color": "#f472b6"},
    {"coords": [28.6095, 77.0392], "color": "#fbbf24"},
    {"coords": [28.6105, 77.0398], "color": "#38bdf8"},
    {"coords": [28.6115, 77.0396], "color": "#f472b6"},
    {"coords": [28.6125, 77.0396], "color": "#34d399"},
    {"coords": [28.6132, 77.0402], "color": "#fbbf24"},
    {"coords": [28.6140, 77.0398], "color": "#38bdf8"},
    {"coords": [28.6142, 77.0405], "color": "#f472b6"},
    {"coords": [28.6128, 77.0345], "color": "#34d399"},
    {"coords": [28.6122, 77.0348], "color": "#fbbf24"},
    {"coords": [28.6052, 77.0415], "color": "#38bdf8"},
    {"coords": [28.6048, 77.0418], "color": "#f472b6"},
    {"coords": [28.6045, 77.0422], "color": "#34d399"}
]

with open("campus_zones.json", "w", encoding="utf-8") as f:
    json.dump({
        "campus_boundary": campus_boundary,
        "zones": zones,
        "decorative_trees": decorative_trees
    }, f, indent=2)

print("Generated campus_zones.json successfully!")

