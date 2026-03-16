import os
import rawpy
from PIL import Image

# --- Paths ---
SRC_FOLDER = r"X:\ONe life centre\2025\OCT content\card"
DEST_FOLDER = r"X:\ONe life centre\2025\OCT content\card\JPEG lowres"

# --- Ensure output directory exists ---
os.makedirs(DEST_FOLDER, exist_ok=True)

# --- Conversion loop ---
for filename in os.listdir(SRC_FOLDER):
    if not filename.lower().endswith(".cr3"):
        continue

    src_path = os.path.join(SRC_FOLDER, filename)
    base_name = os.path.splitext(filename)[0]
    dest_path = os.path.join(DEST_FOLDER, f"{base_name}.jpg")

    print(f"Processing {filename}...")

    try:
        # Read RAW image
        with rawpy.imread(src_path) as raw:
            rgb = raw.postprocess(use_auto_wb=True, no_auto_bright=True)

        # Convert to PIL image
        img = Image.fromarray(rgb)

        # Resize to 33% of original size
        new_size = (int(img.width * 0.33), int(img.height * 0.33))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Save as JPEG (80% quality)
        img.save(dest_path, "JPEG", quality=80, optimize=True)
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

print("✅ All done!")
