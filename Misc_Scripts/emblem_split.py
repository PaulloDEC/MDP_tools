import os
from PIL import Image

# Function to determine if a pixel is 'close enough' to white
def is_close_to_white(r, g, b, threshold=240):
    return r > threshold and g > threshold and b > threshold

# Function to determine if a pixel is 'close enough' to grey (#3f3f3f)
def is_close_to_grey(r, g, b, threshold=10):
    return abs(r - g) < threshold and abs(g - b) < threshold and abs(r - 63) < threshold

# Ask for the path to the TGA file
tga_path = input("Enter the path to the TGA file: ")

# Load the TGA image
tga_image = Image.open(tga_path)

# Convert the image to RGBA to ensure it has an alpha channel
tga_image = tga_image.convert("RGBA")

# Get the directory of the TGA file
tga_dir = os.path.dirname(tga_path)

# Create an empty image for the first PNG (white areas kept, everything else black)
first_png = Image.new("RGBA", tga_image.size)

# Process for first PNG (white areas preserved)
for x in range(tga_image.width):
    for y in range(tga_image.height):
        r, g, b, a = tga_image.getpixel((x, y))
        if is_close_to_white(r, g, b):  # Close to white
            first_png.putpixel((x, y), (255, 255, 255, a))  # Keep white with original alpha
        else:
            first_png.putpixel((x, y), (0, 0, 0, a))  # Set other areas to black with original alpha

# Save the first PNG in the same location as the TGA file
first_png_path = os.path.join(tga_dir, 'output_first.png')
first_png.save(first_png_path)

# Create an empty image for the second PNG (grey areas (#3f3f3f) turned white)
second_png = Image.new("RGBA", tga_image.size)

# Process for second PNG (grey areas #3f3f3f turned white)
for x in range(tga_image.width):
    for y in range(tga_image.height):
        r, g, b, a = tga_image.getpixel((x, y))
        if is_close_to_grey(r, g, b):  # Close to grey color
            second_png.putpixel((x, y), (255, 255, 255, a))  # Turn grey to white with original alpha
        else:
            second_png.putpixel((x, y), (0, 0, 0, a))  # Set other areas to black with original alpha

# Save the second PNG in the same location as the TGA file
second_png_path = os.path.join(tga_dir, 'output_second.png')
second_png.save(second_png_path)

print(f"PNG files have been saved in {tga_dir}.")
