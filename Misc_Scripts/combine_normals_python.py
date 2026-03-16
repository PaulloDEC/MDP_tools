import cv2
import numpy as np
import os

# Set input folder paths
folder_x = r"D:\PAUL\Misc Transformers Bullshit\Transformers Rise of the Dark Spark\2nd Attempt\TR_OptimusG1_ROBO_p\Texture2D\X\Normal X"  # Replace with the actual path
folder_y = r"D:\PAUL\Misc Transformers Bullshit\Transformers Rise of the Dark Spark\2nd Attempt\TR_OptimusG1_ROBO_p\Texture2D\Y\Normal Y"  # Replace with the actual path
output_folder = r"D:\PAUL\Misc Transformers Bullshit\Transformers Rise of the Dark Spark\2nd Attempt\TR_OptimusG1_ROBO_p\Texture2D\Normal Maps"  # Replace with the actual path

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Get sorted list of files (assumes files are named in corresponding order)
files_x = sorted([f for f in os.listdir(folder_x) if f.lower().endswith(".png")])
files_y = sorted([f for f in os.listdir(folder_y) if f.lower().endswith(".png")])

if len(files_x) != len(files_y):
    print("Error: The number of X and Y images does not match.")
    exit()

# Process each pair of images
for i, (file_x, file_y) in enumerate(zip(files_x, files_y)):
    path_x = os.path.join(folder_x, file_x)
    path_y = os.path.join(folder_y, file_y)

    # Load grayscale images
    img_x = cv2.imread(path_x, cv2.IMREAD_GRAYSCALE)
    img_y = cv2.imread(path_y, cv2.IMREAD_GRAYSCALE)

    if img_x is None or img_y is None:
        print(f"Skipping {file_x} or {file_y} due to load failure.")
        continue

    # Ensure images have the same dimensions
    if img_x.shape != img_y.shape:
        print(f"Skipping {file_x} and {file_y} due to size mismatch.")
        continue

    # Create empty BGR image
    height, width = img_x.shape
    normal_map = np.zeros((height, width, 3), dtype=np.uint8)

    # Assign X to Red channel, Y to Green channel, set Blue to 255 (default depth)
    normal_map[:, :, 0] = img_x  # Red channel
    normal_map[:, :, 1] = img_y  # Green channel
    normal_map[:, :, 2] = 255    # Blue channel set to neutral

    # Save the result
    output_path = os.path.join(output_folder, f"NormalMap_{i}.png")
    cv2.imwrite(output_path, normal_map)

    print(f"Saved {output_path}")

print("Processing complete!")
