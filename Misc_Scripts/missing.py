import os
import sys

def get_basenames(folder):
    basenames = set()

    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            base, _ = os.path.splitext(name)
            basenames.add(base)

    return basenames


def compare_folders(folder1, folder2):
    set1 = get_basenames(folder1)
    set2 = get_basenames(folder2)

    missing_in_2 = sorted(set1 - set2)
    missing_in_1 = sorted(set2 - set1)

    return missing_in_1, missing_in_2


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_folders.py <folder1> <folder2>")
        sys.exit(1)

    folder1, folder2 = sys.argv[1], sys.argv[2]

    missing_in_1, missing_in_2 = compare_folders(folder1, folder2)

    print(f"\nFiles present in {folder2} but missing in {folder1}:")
    for name in missing_in_1:
        print("  ", name)

    print(f"\nFiles present in {folder1} but missing in {folder2}:")
    for name in missing_in_2:
        print("  ", name)

    if not missing_in_1 and not missing_in_2:
        print("\n✔ The folders match (ignoring extensions).")
