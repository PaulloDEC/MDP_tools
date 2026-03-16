import os
import tkinter as tk
from tkinter import filedialog
from psd_tools import PSDImage
from PIL import Image

def convert_psd_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".psd"):
            psd_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
            
            try:
                psd = PSDImage.open(psd_path)
                image = psd.composite()
                image = image.convert("RGBA")  # Ensure alpha is preserved
                image.save(png_path, "PNG")
                print(f"Converted: {filename} -> {png_path}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    input_folder = filedialog.askdirectory(title="Select Folder Containing PSD Files")
    if not input_folder:
        print("No folder selected. Exiting...")
        exit()
    
    output_folder = os.path.join(input_folder, "converted_pngs")
    convert_psd_to_png(input_folder, output_folder)
    print(f"Conversion complete. PNG files saved in: {output_folder}")
