import re
import os
from PIL import Image

# --- Constants ---
DPI = 300
INCH_TO_CM = 2.54

def cm_to_pixels(cm: float) -> int:
    """Converts a length in centimeters to pixels at a given DPI."""
    inches = cm / INCH_TO_CM
    pixels = inches * DPI
    return int(round(pixels))

def sanitize_filename(name: str) -> str:
    """Removes invalid characters from a string to make it a valid filename."""
    # Remove leading/trailing whitespace
    name = name.strip()
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    name = re.sub(r'[^\w-]', '', name)
    return name

def process_specs_file(filepath: str):
    """
    Reads a device specifications file and generates PNGs for each entry.
    """
    print(f"Reading data from: {filepath}\n")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: The file '{filepath}' was not found.")
        return
    except Exception as e:
        print(f"❌ ERROR: Could not read the file. Reason: {e}")
        return

    # Split the file content into blocks, one for each device.
    # UPDATED PATTERN: Looks for "Results for:" OR "Complete Specs for:"
    device_blocks = re.split(r'(?:Results for:|Complete Specs for:)', content)


    # The first split item is usually empty, so we skip it.
    if len(device_blocks) < 2:
        print("⚠️ No devices found in the specified format.")
        return

    created_count = 0
    for block in device_blocks[1:]: # Start from the first actual device
        if not block.strip(): # Skip empty blocks that can result from splitting
            continue

        device_name = None
        width_cm = None
        height_cm = None

        # --- Extract Data using Regular Expressions ---
        # 1. Device Name (the first line of the block)
        name_match = block.strip().split('\n', 1)[0]
        if name_match:
            device_name = name_match.strip()

        # 2. Physical Width
        width_match = re.search(r'Physical Width:\s*([\d.]+)\s*cm', block)
        if width_match:
            width_cm = float(width_match.group(1))

        # 3. Physical Height
        height_match = re.search(r'Physical Height:\s*([\d.]+)\s*cm', block)
        if height_match:
            height_cm = float(height_match.group(1))

        # --- Process and Create Image ---
        if device_name and width_cm is not None and height_cm is not None:
            print(f"Processing: {device_name}...")

            # Convert dimensions to pixels
            width_px = cm_to_pixels(width_cm)
            height_px = cm_to_pixels(height_cm)

            # Create a new blank image
            try:
                img = Image.new('RGB', (width_px, height_px), color='white')

                # Generate a sanitized filename
                filename = sanitize_filename(device_name) + '.png'

                # Save the image
                img.save(filename, 'PNG')
                print(f"  ✅ Successfully created '{filename}' ({width_px}x{height_px}px)\n")
                created_count += 1
            except Exception as e:
                print(f"  ❌ ERROR: Could not create image for {device_name}. Reason: {e}\n")

        else:
            # Handle cases where a block is malformed
            device_name_str = device_name if device_name else "Unknown Device"
            print(f"⚠️ Skipping block for '{device_name_str}' due to missing data.\n")

    print("-" * 40)
    print(f"🎉 Processing complete. Created {created_count} PNG file(s).")
    print("-" * 40)


# --- Main Execution ---
if __name__ == "__main__":
    print("--- Device Spec to PNG Generator ---")
    print("This script reads a text file and creates a PNG for each device")
    print("sized according to its physical dimensions at 300 DPI.\n")
    print("NOTE: You must have the Pillow library installed (`pip install Pillow`).\n")

    # Get the file path from the user
    try:
        file_to_read = input("Enter the path to your text file: ")
        process_specs_file(file_to_read)
    except KeyboardInterrupt:
        print("\n\nProcess cancelled by user. Goodbye!")
