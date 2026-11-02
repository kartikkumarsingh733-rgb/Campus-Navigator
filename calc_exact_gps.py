from PIL import Image

img_path = r"C:/Users/kartik/.gemini/antigravity/brain/81552b74-4410-40ad-b2f1-670c05e95f56/.user_uploaded/media_1793631722620_bbe2e71f.jpg"
img = Image.open(img_path)

# Known anchor points:
# Admin: pixel (123.6, 311.4) -> GPS: lat 28.609847, lon 77.037082
# Fountain: pixel (331.3, 256.5) -> GPS: lat 28.610056, lon 77.037968

# dx = 331.3 - 123.6 = 207.7 pixels corresponds to dlon = 77.037968 - 77.037082 = 0.000886 deg lon
# dy = 256.5 - 311.4 = -54.9 pixels corresponds to dlat = 28.610056 - 28.609847 = +0.000209 deg lat
# (Note that on satellite imagery tiles: North is UP, so decreasing y means increasing lat)

px_to_dlon = 0.000886 / 207.7
# Let's verify pixel-to-meter or standard Web Mercator ratio:
# In Web Mercator at lat 28.6 deg: 1 deg lat is approx 110,800 m, 1 deg lon is approx 111,320 * cos(28.6 deg) = 97,700 m.
# 1 pixel lon in meters: px_to_dlon * 97700 = (0.000886 / 207.7) * 97700 = 0.4168 meters / pixel!
# Therefore 1 pixel lat: 0.4168 / 110800 = 0.000003762 deg lat / pixel.

fx, fy = 331.3, 256.5
flat, flon = 28.610056, 77.037968

def pixel_to_gps(px, py):
    d_x = px - fx
    d_y = py - fy
    lon = flon + d_x * (0.000886 / 207.7)
    lat = flat - d_y * (0.4168 / 110800)
    return lat, lon

print("Let's test pixel-to-gps on Admin pin (123.6, 311.4):")
alat_est, alon_est = pixel_to_gps(123.6, 311.4)
print(f"  Admin estimated: ({alat_est:.6f}, {alon_est:.6f}) vs actual (28.609847, 77.037082)")

# Now, let's find visual centers in the screenshot:
# Top building (Block 6):
# Looking at the image, top building spans roughly x from 190 to 420 (center ~305), y from 40 to 190 (center ~115)
top_x, top_y = 305.0, 115.0
b6_lat, b6_lon = pixel_to_gps(top_x, top_y)
print(f"\nBlock 6 (Top Building, pixel {top_x}, {top_y}):")
print(f"  GPS: ({b6_lat:.6f}, {b6_lon:.6f})")

# Bottom-left building (Block 4):
# Spans roughly x from 150 to 330 (center ~240), y from 320 to 460 (center ~390)
bl_x, bl_y = 240.0, 390.0
b4_lat, b4_lon = pixel_to_gps(bl_x, bl_y)
print(f"\nBlock 4 (Bottom-Left Building, pixel {bl_x}, {bl_y}):")
print(f"  GPS: ({b4_lat:.6f}, {b4_lon:.6f})")

# Bottom-right building (Block 5):
# Spans roughly x from 370 to 550 (center ~460), y from 270 to 410 (center ~340)
br_x, br_y = 460.0, 340.0
b5_lat, b5_lon = pixel_to_gps(br_x, br_y)
print(f"\nBlock 5 (Bottom-Right Building, pixel {br_x}, {br_y}):")
print(f"  GPS: ({b5_lat:.6f}, {b5_lon:.6f})")

