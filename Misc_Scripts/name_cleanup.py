import os

def rename_files(folder_path):
    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)  # Get current folder name
        
        for filename in files:
            old_path = os.path.join(root, filename)
            
            # Skip non-file items
            if not os.path.isfile(old_path):
                continue
            
            # Remove 'RB_' prefix if present
            new_name = filename.lstrip("RB_") if filename.startswith("RB_") else filename
            
            # Replace '_TEXSET' and everything after with folder name
            if "_TEXSET" in new_name:
                base_name = new_name.split("_TEXSET")[0]  # Keep only portion before '_TEXSET'
                extension = os.path.splitext(new_name)[1]  # Extract file extension
                new_name = f"{base_name}_{folder_name}{extension}"
            
            new_path = os.path.join(root, new_name)
            
            # Rename file only if the name has changed
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path to process: ")
    if os.path.isdir(folder_path):
        rename_files(folder_path)
        print("Renaming complete.")
    else:
        print("Invalid folder path.")
