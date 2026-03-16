# Smart Pixel Art Downscaler

A Python tool that intelligently recovers pristine pixel-perfect images from interpolated/blurred upscales of pixel art.

## The Problem

When pixel art is upscaled using interpolation methods (bilinear, bicubic, Lanczos, etc.), each original pixel becomes a block of slightly different colors due to blending. Simply downscaling back with standard methods produces muddy, imprecise results with colors that never existed in the original.

## The Solution

This tool:
1. **Detects the pixel grid** - Calculates exactly where each original pixel's block starts and ends
2. **Intelligently samples** - Uses statistical methods to determine the "true" color from each blurred block
3. **Handles any scale factor** - Works with both integer scales (2×, 3×, etc.) and fractional scales (5.4×, etc.)
4. **Optional palette snapping** - Can constrain output to a specific color palette

## Installation

Requires Python 3.6+ and PIL/Pillow:

```bash
pip install Pillow numpy
```

## Usage

### Basic Usage

```bash
# Downscale a 1728×1080 image back to 320×200
python pixel_art_downscaler.py input.png 320 200
```

### Sampling Methods

Different methods work better for different types of upscales:

```bash
# Mode: Most common color (DEFAULT - best for most cases)
python pixel_art_downscaler.py input.png 320 200 --method mode

# Median: Median color (good for reducing artifacts)
python pixel_art_downscaler.py input.png 320 200 --method median

# Center: Just the center pixel (fast, works if upscale was well-centered)
python pixel_art_downscaler.py input.png 320 200 --method center

# Mean: Average color (can help with slight variations)
python pixel_art_downscaler.py input.png 320 200 --method mean
```

### Palette Snapping

If you have the original image or a palette, you can snap colors to ensure perfect accuracy:

```bash
# Use a palette image
python pixel_art_downscaler.py input.png 320 200 --palette original.png

# Auto-extract palette from the input
python pixel_art_downscaler.py input.png 320 200 --auto-palette
```

### Custom Output Path

```bash
python pixel_art_downscaler.py input.png 320 200 -o my_output.png
```

## How Each Sampling Method Works

### Mode (Recommended)
Finds the **most common color** in each pixel block. Best for upscales where the interpolation created halos or gradients around solid colors. The original solid color will still be most prevalent.

**Best for:** Most upscales, especially bicubic/bilinear

### Median
Finds the **median color** by channel. Good for reducing outliers and interpolation artifacts. Less affected by extreme values at edges.

**Best for:** Upscales with strong edge artifacts or halos

### Center
Simply samples the **center pixel** of each block. Fast and works well if the upscale algorithm properly centered pixels.

**Best for:** Well-centered upscales, or when you need speed

### Mean
Averages all colors and rounds. Can produce colors that weren't in the block if interpolation was heavy.

**Best for:** Slight variations, experimental recovery

## Understanding Scale Factors

The script automatically calculates scale factors:

```
1728×1080 → 320×200
X scale: 1728 ÷ 320 = 5.4×
Y scale: 1080 ÷ 200 = 5.4×
```

Each original pixel was expanded to approximately a 5.4×5.4 block (some blocks will be 5×5, some 6×6 to maintain alignment).

## Examples

### Example 1: Your Case
```bash
python pixel_art_downscaler.py upscaled_1728x1080.png 320 200
```

### Example 2: With Palette Reference
If you have the original 320×200 image:
```bash
python pixel_art_downscaler.py upscaled.png 320 200 --palette original.png
```

### Example 3: Try Multiple Methods
```bash
# Generate multiple versions to compare
python pixel_art_downscaler.py input.png 320 200 --method mode -o output_mode.png
python pixel_art_downscaler.py input.png 320 200 --method median -o output_median.png
python pixel_art_downscaler.py input.png 320 200 --method center -o output_center.png
```

## Technical Details

### Block Sampling Algorithm

For each target pixel at position (x, y):

1. Calculate source block bounds:
   ```
   x_start = x × x_scale
   y_start = y × y_scale
   x_end = (x + 1) × x_scale
   y_end = (y + 1) × y_scale
   ```

2. Extract the block from source image

3. Apply sampling method:
   - **Mode**: Count color frequencies, pick most common
   - **Median**: Calculate median value per RGB channel
   - **Center**: Pick pixel at block center
   - **Mean**: Average all pixels, round to integers

4. (Optional) Snap to nearest palette color

### Why Not Just Use PIL.resize()?

PIL's resize methods are optimized for photographic images and assume you want smooth results. They don't understand that you're trying to recover discrete pixel data from interpolated blocks.

Standard downscaling averages or resamples based on continuous assumptions, while this tool uses discrete sampling that understands the pixel grid structure.

## Limitations

- **Memory**: Loads entire image into memory. Very large images may require significant RAM.
- **Speed**: Processes pixel-by-pixel for accuracy. Large downscales may take time.
- **Palette Detection**: Auto-palette extraction uses all unique colors in input. For better results, provide original palette.

## Testing

Run the included test to see it in action:

```bash
python test_downscaler.py
```

This creates a simple 16×16 pixel art image, upscales it to 160×160 with bicubic interpolation (introducing blur), then recovers it using different methods. Compare the recovered images to the original to see the quality.

## When to Use Which Method

- **Unknown upscale type?** Start with `mode`
- **Heavy blur/interpolation?** Try `median`
- **Clean, well-centered upscale?** `center` will be fastest
- **Have original palette?** Always use `--palette`
- **Not sure?** Generate multiple versions and compare

## Output

The script saves a PNG file with recovered pixel art. Default filename is `{input}_downscaled.png` unless you specify `--output`.

## Tips for Best Results

1. **Verify dimensions**: Make sure you know the exact original resolution
2. **Check scale factors**: Non-integer scales work but integer scales (2×, 3×, etc.) are cleaner
3. **Use palette when possible**: If you have the original or a reference, palette snapping ensures 100% accuracy
4. **Try multiple methods**: Each sampling method may produce slightly different results
5. **Visual comparison**: Always compare output to original if available

## License

Free to use for any purpose. Created to help preserve pixel art in its original form.
