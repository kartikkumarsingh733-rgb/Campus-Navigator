from PIL import Image
import os

img_path = r"C:/Users/kartik/.gemini/antigravity/brain/81552b74-4410-40ad-b2f1-670c05e95f56/.user_uploaded/media_1793631722620_bbe2e71f.jpg"

if os.path.exists(img_path):
    img = Image.open(img_path)
    print(f"Image size: {img.size} (width, height)")
else:
    print("File not found")

