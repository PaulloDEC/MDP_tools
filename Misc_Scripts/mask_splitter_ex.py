import os
import cv2
import numpy as np

def process_images(folder_path):
    # Ensure output folder exists
    output_folder = os.path.join(folder_path, "processed_masks")
    os.makedirs(output_folder, exist_ok=True)
    
    # Define thresholds for fuzziness
    black_threshold = 50  # Expanded range for black
    white_threshold = 205  # Expanded range for white
    
    # Iterate over PNG files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                print(f"Skipping {filename}, could not read file.")
                continue
            
            # Normalize grayscale values for anti-aliasing preservation
            mask1 = np.zeros_like(image)
            mask2 = np.zeros_like(image)
            
            # Mask 1: Extract white shades, remap to 0-255
            mask1_indices = image >= white_threshold
            mask1[mask1_indices] = ((image[mask1_indices] - white_threshold) / (255 - white_threshold) * 255).astype(np.uint8)
            
            # Mask 2: Extract black shades, remap to 0-255
            mask2_indices = image <= black_threshold
            mask2[mask2_indices] = ((black_threshold - image[mask2_indices]) / black_threshold * 255).astype(np.uint8)
            
            has_mask1 = np.any(mask1 > 0)
            has_mask2 = np.any(mask2 > 0)
            
            if has_mask1:
                mask1_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_mask1.png")
                cv2.imwrite(mask1_filename, mask1)
            
            if has_mask2:
                mask2_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_mask2.png")
                cv2.imwrite(mask2_filename, mask2)
            
            print(f"Processed {filename}: {'Mask 1' if has_mask1 else ''} {'Mask 2' if has_mask2 else ''}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PNG images: ")
    if os.path.isdir(folder_path):
        process_images(folder_path)
    else:
        print("Invalid folder path.")
