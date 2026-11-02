import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("app.js", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "alliance" in line.lower() or "poster" in line.lower():
            print(f"Line {idx+1}: {line.strip()[:80]}")
