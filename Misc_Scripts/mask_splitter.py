import os
import cv2
import numpy as np

def process_images(folder_path):
    # Ensure output folder exists
    output_folder = os.path.join(folder_path, "processed_masks")
    os.makedirs(output_folder, exist_ok=True)
    
    # Define thresholds for fuzziness
    black_threshold = 10  # Anything <= 10 is considered black
    white_threshold = 245  # Anything >= 245 is considered white
    
    # Iterate over PNG files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                print(f"Skipping {filename}, could not read file.")
                continue
            
            # Identify unique colors in the image
            has_mask1 = np.any(image >= white_threshold)  # White pixels
            has_mask2 = np.any(image <= black_threshold)  # Black pixels
            
            if has_mask1:
                mask1 = ((image >= white_threshold).astype(np.uint8)) * 255  # Convert near-white to mask
                mask1_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_mask1.png")
                cv2.imwrite(mask1_filename, mask1)
            
            if has_mask2:
                mask2 = ((image <= black_threshold).astype(np.uint8)) * 255  # Convert near-black to mask
                mask2_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_mask2.png")
                cv2.imwrite(mask2_filename, mask2)
            
            print(f"Processed {filename}: {'Mask 1' if has_mask1 else ''} {'Mask 2' if has_mask2 else ''}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PNG images: ")
    if os.path.isdir(folder_path):
        process_images(folder_path)
    else:
        print("Invalid folder path.")
