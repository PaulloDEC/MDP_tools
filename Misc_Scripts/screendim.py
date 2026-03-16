import math

def get_positive_int(prompt: str) -> int:
    """Gets a positive integer from the user."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Error: Please enter a positive whole number.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")

def get_positive_float(prompt: str) -> float:
    """Gets a positive float from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Error: Please enter a positive number.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

# --- Main Script ---
print("--- Screen Dimension Calculator 📐 ---\n")

# Part 1: Get all user inputs
device_name = input("Enter the device name: ")
width_px = get_positive_int("Enter the screen width in pixels: ")
height_px = get_positive_int("Enter the screen height in pixels: ")
diagonal_in = get_positive_float("Enter the screen diagonal in inches: ")

# Part 2: Perform all calculations
# Aspect Ratio
common_divisor = math.gcd(width_px, height_px)
aspect_w = width_px // common_divisor
aspect_h = height_px // common_divisor

# Physical width and height
# Use Pythagoras' theorem: (aspect_w * x)^2 + (aspect_h * x)^2 = diagonal_in^2
ratio_hypotenuse = math.sqrt(aspect_w**2 + aspect_h**2)
multiplier = diagonal_in / ratio_hypotenuse
width_in = aspect_w * multiplier
height_in = aspect_h * multiplier

# Convert inches to centimeters
INCH_TO_CM = 2.54
width_cm = width_in * INCH_TO_CM
height_cm = height_in * INCH_TO_CM

# Part 3: Display the final, consolidated results
print("\n" + "="*40)
print(f"📊 Complete Specs for: {device_name}")
print("="*40)
print(f"Resolution:      {width_px} x {height_px} pixels")
print(f"Aspect Ratio:    {aspect_w}:{aspect_h}")
print(f"Diagonal:        {diagonal_in:.2f}\"")
print("-" * 40)
print(f"Physical Width:  {width_cm:.2f} cm")
print(f"Physical Height: {height_cm:.2f} cm")
print("="*40)