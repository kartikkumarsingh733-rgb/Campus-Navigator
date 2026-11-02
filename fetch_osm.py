import urllib.request
import urllib.parse
import json
import sys

query = """
[out:json][timeout:60];
(
  way["highway"](28.6040, 77.0310, 28.6180, 77.0450);
  way["building"](28.6040, 77.0310, 28.6180, 77.0450);
  way["amenity"](28.6040, 77.0310, 28.6180, 77.0450);
  way["leisure"](28.6040, 77.0310, 28.6180, 77.0450);
  node["amenity"](28.6040, 77.0310, 28.6180, 77.0450);
  node["shop"](28.6040, 77.0310, 28.6180, 77.0450);
  node["name"](28.6040, 77.0310, 28.6180, 77.0450);
);
out body;
>;
out skel qt;
"""

url = "https://overpass-api.de/api/interpreter"
data = urllib.parse.urlencode({"data": query}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"User-Agent": "NSUTCampusNavigator/1.0"})

print("Fetching data from Overpass API...")
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        with open("nsut_osm_raw.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Success! Elements fetched: {len(result.get('elements', []))}")
except Exception as e:
    print(f"Error fetching OSM: {e}", file=sys.stderr)
    sys.exit(1)

