import urllib.request

urls = {
    "leaflet.css": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
    "leaflet.js": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            with open(filename, "wb") as f:
                f.write(content)
        print(f"Saved {filename} ({len(content)} bytes)")
    except Exception as e:
        print(f"Failed {filename}: {e}")

