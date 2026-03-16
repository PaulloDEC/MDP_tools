import os
from PIL import Image

# Function to calculate the brightness of a pixel (luminance)
def calculate_brightness(r, g, b):
    return (r * 0.2989 + g * 0.5870 + b * 0.1140) / 255.0

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

# Process for first PNG (white areas preserved, black becomes transparent)
for x in range(tga_image.width):
    for y in range(tga_image.height):
        r, g, b, a = tga_image.getpixel((x, y))
        brightness = calculate_brightness(r, g, b)
        
        # Map the brightness to an alpha value (blacker pixels become more transparent)
        alpha = int(brightness * 255)  # Black pixels get more transparent (alpha=0), white gets opaque (alpha=255)
        
        if r == 255 and g == 255 and b == 255:  # White areas
            first_png.putpixel((x, y), (255, 255, 255, 255))  # Keep white fully opaque
        else:
            first_png.putpixel((x, y), (0, 0, 0, alpha))  # Set the pixel to black with the calculated transparency

# Save the first PNG in the same location as the TGA file
first_png_path = os.path.join(tga_dir, 'output_first.png')
first_png.save(first_png_path)

# Create an empty image for the second PNG (grey areas (#3f3f3f) turned white)
second_png = Image.new("RGBA", tga_image.size)

# Process for second PNG (grey areas #3f3f3f turned white, black becomes transparent)
for x in range(tga_image.width):
    for y in range(tga_image.height):
        r, g, b, a = tga_image.getpixel((x, y))
        brightness = calculate_brightness(r, g, b)
        
        # Map the brightness to an alpha value (blacker pixels become more transparent)
        alpha = int(brightness * 255)  # Black pixels get more transparent (alpha=0), white gets opaque (alpha=255)
        
        if (r, g, b) == (63, 63, 63):  # Grey color close to #3f3f3f
            second_png.putpixel((x, y), (255, 255, 255, 255))  # Turn grey to white with full opacity
        else:
            second_png.putpixel((x, y), (0, 0, 0, alpha))  # Set the pixel to black with the calculated transparency

# Save the second PNG in the same location as the TGA file
second_png_path = os.path.join(tga_dir, 'output_second.png')
second_png.save(second_png_path)

print(f"PNG files have been saved in {tga_dir}.")
