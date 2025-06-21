from PIL import Image
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
TARGET_SIZE = (300, 300)  # Resize to 300x300

def resize_and_compress(folder):
    path = os.path.join(BASE_DIR, folder)
    for filename in os.listdir(path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(path, filename)
            img = Image.open(filepath)
            img = img.convert('RGB')
            img.thumbnail(TARGET_SIZE)

            new_name = os.path.splitext(filename)[0] + ".webp"
            new_path = os.path.join(path, new_name)

            img.save(new_path, "WEBP", quality=80)
            print(f"✅ Compressed: {new_name}")

# Add your themes here
themes = ["drinks", "food", "fruits", "flowers", "bakery"]
for theme in themes:
    resize_and_compress(theme)
