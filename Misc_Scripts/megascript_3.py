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
        "EMISSIVE": os.path.join(folder, "EMISSIVE"),
        "NORMAL": os.path.join(folder, "NORMAL")
    }
    
    # Create output directories if they don't exist
    for key in output_folders:
        os.makedirs(output_folders[key], exist_ok=True)
    
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
                
                # Determine category based on filename
                if "NormX" in filename:
                    # Save Diffuse (RGB without alpha)
                    Image.fromarray(rgb).save(os.path.join(output_folders["DIFFUSE"], filename.replace(".tga", ".png")))
                    
                    # Save Normal X (alpha as grayscale)
                    Image.fromarray(alpha).convert("L").save(os.path.join(output_folders["NORMAL X"], filename.replace(".tga", ".png")))
                
                if "NormY" in filename:
                    # Save Normal Y (alpha as grayscale)
                    Image.fromarray(alpha).convert("L").save(os.path.join(output_folders["NORMAL Y"], filename.replace(".tga", ".png")))
                    
                    # Save Mask (blue channel)
                    blue_channel = img[:, :, 2]
                    Image.fromarray(blue_channel).convert("L").save(os.path.join(output_folders["MASK"], filename.replace(".tga", ".png")))
                    
                    # Save Specular (green channel)
                    green_channel = img[:, :, 1]
                    Image.fromarray(green_channel).convert("L").save(os.path.join(output_folders["SPECULAR"], filename.replace(".tga", ".png")))
                    
                    # Save Emissive (red channel)
                    red_channel = img[:, :, 0]
                    Image.fromarray(red_channel).convert("L").save(os.path.join(output_folders["EMISSIVE"], filename.replace(".tga", ".png")))
    
    # Combine Normal X and Normal Y into complete normal maps
    normal_x_files = {f.split("TEXSET")[0]: f for f in os.listdir(output_folders["NORMAL X"]) if f.endswith(".png")}
    normal_y_files = {f.split("TEXSET")[0]: f for f in os.listdir(output_folders["NORMAL Y"]) if f.endswith(".png")}
    
    for key in normal_x_files:
        if key in normal_y_files:
            x_img = Image.open(os.path.join(output_folders["NORMAL X"], normal_x_files[key]))
            y_img = Image.open(os.path.join(output_folders["NORMAL Y"], normal_y_files[key]))
            
            x_array = np.array(x_img)
            y_array = np.array(y_img)
            
            # Create a new normal map with X in red, Y in green, and blue filled with 255
            normal_map = np.stack((x_array, y_array, np.full_like(x_array, 255)), axis=-1)
            
            # Save the combined normal map
            Image.fromarray(normal_map).save(os.path.join(output_folders["NORMAL"], key + "_Normal.png"))
    
    print("Processing complete!")

# Run the script
folder_path = input("Enter the folder containing TGA files: ")
process_tga_files(folder_path)
