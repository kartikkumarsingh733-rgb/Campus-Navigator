from PIL import Image

img_path = r"C:/Users/kartik/.gemini/antigravity/brain/81552b74-4410-40ad-b2f1-670c05e95f56/.user_uploaded/media_1793631722620_bbe2e71f.jpg"
img = Image.open(img_path).convert("RGB")
w, h = img.size

# Let's find:
# 1. Red castle pin in Admin Block: look for pixels near red/pink
# 2. Blue fountain pin: look for blue circle
# Admin Block GPS: (28.609847, 77.037082)
# Central Fountain GPS: (28.610056, 77.037968)

fountain_pts = []
admin_pts = []

for x in range(w):
    for y in range(h):
        r, g, b = img.getpixel((x, y))
        # Blue circle for fountain: high blue, lower red/green
        if b > 200 and r < 80 and g < 150:
            if 300 < x < 360 and 230 < y < 290:
                fountain_pts.append((x, y))
        # Red/pink circle for admin: high red, lower green
        if r > 200 and g < 100 and b < 120:
            if 100 < x < 160 and 280 < y < 340:
                admin_pts.append((x, y))

if fountain_pts:
    fx = sum(p[0] for p in fountain_pts) / len(fountain_pts)
    fy = sum(p[1] for p in fountain_pts) / len(fountain_pts)
    print(f"Fountain pin at pixel ({fx:.1f}, {fy:.1f})")

if admin_pts:
    ax = sum(p[0] for p in admin_pts) / len(admin_pts)
    ay = sum(p[1] for p in admin_pts) / len(admin_pts)
    print(f"Admin pin at pixel ({ax:.1f}, {ay:.1f})")

