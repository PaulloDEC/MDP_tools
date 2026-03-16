import os
import imageio
import numpy as np
from PIL import Image

def process_tga_files(folder):
    # Define output folders
    output_folders = {
        "DIFFUSE": os.path.join(folder, "DIFFUSE"),
        "NORMAL X": os.path.join(folder, "NORMAL X"),
        "NORMAL Y": os.path.join(folder, "NORMAL Y"),
        "MASK": os.path.join(folder, "MASK"),
        "SPECULAR": os.path.join(folder, "SPECULAR"),
        "NORMAL": os.path.join(folder, "NORMAL")
    }
    
    # Create output directories if they don't exist
    for key in output_folders:
        os.makedirs(output_folders[key], exist_ok=True)
    
    normal_x_files = {}
    normal_y_files = {}
    
    # Process each TGA file in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".tga"):
            filepath = os.path.join(folder, filename)
            try:
                # Read image using imageio
                img = imageio.v3.imread(filepath)
                
                # Ensure the image is RGBA
                if img.shape[-1] != 4:
                    print(f"Skipping {filename}, not an RGBA image.")
                    continue
                
                # Extract channels
                rgb = img[:, :, :3]  # RGB channels
                alpha = img[:, :, 3]  # Alpha channel
                blue_channel = img[:, :, 2]  # Blue channel
                green_channel = img[:, :, 1]  # Green channel
                
                # Determine category based on filename
                base_name = filename.split("TEXSET")[0]
                if "NormX" in filename:
                    normal_x_files[base_name] = alpha
                    # Save Diffuse (RGB without alpha)
                    Image.fromarray(rgb).save(os.path.join(output_folders["DIFFUSE"], filename.replace(".tga", ".png")))
                    
                    # Save Normal X (alpha as grayscale)
                    Image.fromarray(alpha).convert("L").save(os.path.join(output_folders["NORMAL X"], filename.replace(".tga", ".png")))
                
                if "NormY" in filename:
                    normal_y_files[base_name] = alpha
                    # Save Normal Y (alpha as grayscale)
                    Image.fromarray(alpha).convert("L").save(os.path.join(output_folders["NORMAL Y"], filename.replace(".tga", ".png")))
                    
                    # Save Mask (blue channel)
                    Image.fromarray(blue_channel).convert("L").save(os.path.join(output_folders["MASK"], filename.replace(".tga", ".png")))
                    
                    # Save Specular (green channel)
                    Image.fromarray(green_channel).convert("L").save(os.path.join(output_folders["SPECULAR"], filename.replace(".tga", ".png")))
            
            except Exception as e:
                print(f"Skipping {filename}, unable to read. Error: {e}")
    
    # Combine Normal X and Normal Y into a complete normal map
    for base_name in normal_x_files.keys():
        if base_name in normal_y_files:
            normal_x = normal_x_files[base_name]
            normal_y = normal_y_files[base_name]
            
            # Create a new normal map with X in red, Y in green, and a filled blue channel
            height, width = normal_x.shape
            normal_map = np.zeros((height, width, 3), dtype=np.uint8)
            normal_map[:, :, 0] = normal_x  # Red channel (X)
            normal_map[:, :, 1] = normal_y  # Green channel (Y)
            normal_map[:, :, 2] = 255  # Blue channel filled to 255
            
            normal_filename = base_name + "TEXSET_Normal.png"
            Image.fromarray(normal_map).save(os.path.join(output_folders["NORMAL"], normal_filename))
    
    print("Processing complete!")

# Run the script
folder_path = input("Enter the folder containing TGA files: ")
process_tga_files(folder_path)
