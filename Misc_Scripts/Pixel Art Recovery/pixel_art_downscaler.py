#!/usr/bin/env python3
"""
Smart Pixel Art Downscaler
===========================
Intelligently downscales interpolated/blurred upscales of pixel art back to
their original pristine pixel-perfect form.

Handles the challenge of recovering clean pixels from soft upscales where
interpolation has created gradients and color bleeding.
"""

import numpy as np
from PIL import Image
import argparse
from pathlib import Path
from collections import Counter


def calculate_scale_factors(input_size, target_size):
    """
    Calculate the scale factors between input and target dimensions.
    
    Args:
        input_size: (width, height) of input image
        target_size: (width, height) of target image
    
    Returns:
        (x_scale, y_scale) as floats
    """
    x_scale = input_size[0] / target_size[0]
    y_scale = input_size[1] / target_size[1]
    return x_scale, y_scale


def get_pixel_block_bounds(x, y, x_scale, y_scale):
    """
    Calculate the bounds of the upscaled pixel block in the source image.
    
    Args:
        x, y: Target pixel coordinates
        x_scale, y_scale: Scaling factors
    
    Returns:
        (x_start, y_start, x_end, y_end) in source image coordinates
    """
    x_start = int(x * x_scale)
    y_start = int(y * y_scale)
    x_end = int((x + 1) * x_scale)
    y_end = int((y + 1) * y_scale)
    
    return x_start, y_start, x_end, y_end


def sample_mode(block):
    """
    Find the most common color in a block (mode).
    Best for blocks with clear dominant colors.
    
    Args:
        block: numpy array of shape (height, width, channels)
    
    Returns:
        RGB tuple of the most common color
    """
    # Reshape to list of pixels
    pixels = block.reshape(-1, block.shape[2])
    
    # Convert to tuples for counting
    pixel_tuples = [tuple(p) for p in pixels]
    
    # Find most common
    counter = Counter(pixel_tuples)
    most_common = counter.most_common(1)[0][0]
    
    return most_common


def sample_median(block):
    """
    Find the median color in a block.
    Good for reducing interpolation artifacts.
    
    Args:
        block: numpy array of shape (height, width, channels)
    
    Returns:
        RGB tuple of median color
    """
    median_color = np.median(block, axis=(0, 1)).astype(np.uint8)
    return tuple(median_color)


def sample_center(block):
    """
    Sample the center pixel of a block.
    Simple and fast, works well if upscale was centered properly.
    
    Args:
        block: numpy array of shape (height, width, channels)
    
    Returns:
        RGB tuple of center pixel
    """
    center_y = block.shape[0] // 2
    center_x = block.shape[1] // 2
    return tuple(block[center_y, center_x])


def sample_mean_rounded(block):
    """
    Calculate mean color and round to nearest integer.
    Can help with slight color variations.
    
    Args:
        block: numpy array of shape (height, width, channels)
    
    Returns:
        RGB tuple of mean color (rounded)
    """
    mean_color = np.mean(block, axis=(0, 1)).astype(np.uint8)
    return tuple(mean_color)


def find_nearest_palette_color(color, palette):
    """
    Snap a color to the nearest color in a palette.
    
    Args:
        color: RGB tuple
        palette: list of RGB tuples
    
    Returns:
        RGB tuple from palette
    """
    color = np.array(color)
    palette_array = np.array(palette)
    
    # Calculate Euclidean distance to all palette colors
    distances = np.sqrt(np.sum((palette_array - color) ** 2, axis=1))
    
    # Return closest
    nearest_idx = np.argmin(distances)
    return tuple(palette_array[nearest_idx])


def extract_palette_from_image(img_array, max_colors=256):
    """
    Extract unique colors from an image to use as a palette.
    
    Args:
        img_array: numpy array of image
        max_colors: maximum number of colors to extract
    
    Returns:
        list of RGB tuples
    """
    pixels = img_array.reshape(-1, img_array.shape[2])
    unique_colors = np.unique(pixels, axis=0)
    
    if len(unique_colors) > max_colors:
        print(f"Warning: Image has {len(unique_colors)} unique colors, limiting to {max_colors}")
        unique_colors = unique_colors[:max_colors]
    
    return [tuple(c) for c in unique_colors]


def count_colors_in_image(img_array):
    """
    Count the frequency of each color in an image.
    
    Args:
        img_array: numpy array of image
    
    Returns:
        Counter object mapping RGB tuples to pixel counts
    """
    pixels = img_array.reshape(-1, img_array.shape[2])
    # Convert to native Python int to avoid numpy scalar type issues
    pixel_tuples = [tuple(int(v) for v in p) for p in pixels]
    return Counter(pixel_tuples)


def reduce_palette_kmeans(img_array, target_colors):
    """
    Reduce image palette using k-means clustering.
    This preserves color diversity better than frequency-based reduction.
    
    Args:
        img_array: numpy array of image
        target_colors: target number of colors
    
    Returns:
        dict mapping original colors to reduced palette colors
    """
    from sklearn.cluster import MiniBatchKMeans
    
    # Get all unique colors and their counts
    color_counts = count_colors_in_image(img_array)
    
    if len(color_counts) <= target_colors:
        print(f"Image already has {len(color_counts)} colors (target: {target_colors})")
        return {color: color for color in color_counts.keys()}
    
    print(f"Reducing from {len(color_counts)} colors to {target_colors} using k-means clustering...")
    
    # Create array of all unique colors
    unique_colors = np.array(list(color_counts.keys()), dtype=np.float32)
    
    # Use k-means to find cluster centers
    print(f"  Running k-means clustering...")
    kmeans = MiniBatchKMeans(
        n_clusters=target_colors,
        random_state=42,
        batch_size=1000,
        n_init=10
    )
    kmeans.fit(unique_colors)
    
    # Cluster centers are our new palette
    palette_colors = kmeans.cluster_centers_.astype(np.uint8)
    
    print(f"  Found {len(palette_colors)} palette colors")
    
    # Map each original color to its nearest cluster center
    color_mapping = {}
    
    for color in color_counts.keys():
        color_array = np.array(color, dtype=np.float32).reshape(1, -1)
        cluster_idx = kmeans.predict(color_array)[0]
        mapped_color = tuple(int(v) for v in palette_colors[cluster_idx])
        color_mapping[color] = mapped_color
    
    # Show some statistics
    clusters_used = len(set(color_mapping.values()))
    print(f"  Mapped {len(color_counts)} colors to {clusters_used} palette colors")
    
    return color_mapping


def reduce_palette_hybrid(img_array, target_colors, preserve_ratio=0.3):
    """
    Hybrid approach: keep most common colors + use k-means for the rest.
    This balances frequency importance with color diversity.
    
    Args:
        img_array: numpy array of image
        target_colors: target number of colors
        preserve_ratio: ratio of slots to reserve for most common colors (default 0.3)
    
    Returns:
        dict mapping original colors to reduced palette colors
    """
    from sklearn.cluster import MiniBatchKMeans
    
    # Get all unique colors and their counts
    color_counts = count_colors_in_image(img_array)
    
    if len(color_counts) <= target_colors:
        print(f"Image already has {len(color_counts)} colors (target: {target_colors})")
        return {color: color for color in color_counts.keys()}
    
    print(f"Reducing from {len(color_counts)} colors to {target_colors} using hybrid method...")
    
    # Sort by frequency
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Keep top N most common colors
    n_preserved = int(target_colors * preserve_ratio)
    n_clustered = target_colors - n_preserved
    
    print(f"  Preserving {n_preserved} most common colors")
    print(f"  Clustering remaining into {n_clustered} colors")
    
    preserved_colors = [color for color, count in sorted_colors[:n_preserved]]
    
    # Get remaining colors for clustering
    remaining_colors = [color for color, count in sorted_colors[n_preserved:]]
    
    if n_clustered > 0 and len(remaining_colors) > 0:
        # Cluster the remaining colors
        remaining_array = np.array(remaining_colors, dtype=np.float32)
        
        actual_clusters = min(n_clustered, len(remaining_colors))
        print(f"  Running k-means on {len(remaining_colors)} colors...")
        
        kmeans = MiniBatchKMeans(
            n_clusters=actual_clusters,
            random_state=42,
            batch_size=1000,
            n_init=10
        )
        kmeans.fit(remaining_array)
        
        clustered_colors = kmeans.cluster_centers_.astype(np.uint8)
    else:
        clustered_colors = np.array([])
    
    # Combine preserved and clustered colors
    if len(clustered_colors) > 0:
        palette_array = np.vstack([
            np.array(preserved_colors, dtype=np.int32),
            clustered_colors.astype(np.int32)
        ])
    else:
        palette_array = np.array(preserved_colors, dtype=np.int32)
    
    print(f"  Final palette has {len(palette_array)} colors")
    
    # Map all colors to nearest palette color
    color_mapping = {}
    
    for color, count in sorted_colors:
        if color in preserved_colors:
            color_mapping[color] = color
        else:
            # Find nearest palette color
            color_array = np.array(color, dtype=np.int32)
            distances = np.sqrt(np.sum((palette_array - color_array) ** 2, axis=1))
            nearest_idx = np.argmin(distances)
            nearest_color = tuple(int(v) for v in palette_array[nearest_idx])
            color_mapping[color] = nearest_color
    
    return color_mapping


def reduce_palette_smart(img_array, target_colors):
    """
    Reduce image palette to target number of colors by merging similar colors.
    Uses frequency-weighted clustering - rare colors get merged into common ones.
    
    Args:
        img_array: numpy array of image
        target_colors: target number of colors
    
    Returns:
        dict mapping original colors to reduced palette colors
    """
    # Count color frequencies
    color_counts = count_colors_in_image(img_array)
    
    # If already at or below target, no reduction needed
    if len(color_counts) <= target_colors:
        print(f"Image already has {len(color_counts)} colors (target: {target_colors})")
        return {color: color for color in color_counts.keys()}
    
    print(f"Reducing from {len(color_counts)} colors to {target_colors}...")
    
    # Sort colors by frequency (most common first)
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Keep the N most common colors as the base palette (as plain tuples)
    palette_colors = [color for color, count in sorted_colors[:target_colors]]
    palette_array = np.array(palette_colors, dtype=np.int32)
    
    print(f"Base palette: {target_colors} most common colors")
    print(f"  Most common: {sorted_colors[0][0]} ({sorted_colors[0][1]} pixels)")
    print(f"  Least common in palette: {sorted_colors[target_colors-1][0]} ({sorted_colors[target_colors-1][1]} pixels)")
    
    # Map all colors to nearest palette color
    color_mapping = {}
    
    for color, count in sorted_colors:
        if color in palette_colors:
            # Already in palette
            color_mapping[color] = color
        else:
            # Find nearest palette color
            color_array = np.array(color, dtype=np.int32)
            distances = np.sqrt(np.sum((palette_array - color_array) ** 2, axis=1))
            nearest_idx = np.argmin(distances)
            # Convert back to plain tuple of ints
            nearest_color = tuple(int(v) for v in palette_array[nearest_idx])
            color_mapping[color] = nearest_color
    
    # Show some examples of merged colors
    merged_count = 0
    print(f"\nExample color merges:")
    for color, count in sorted_colors[target_colors:target_colors+5]:
        if color in color_mapping and color_mapping[color] != color:
            merged_count += 1
            print(f"  {color} ({count} pixels) → {color_mapping[color]}")
    
    print(f"\nMerged {len(sorted_colors) - target_colors} rare colors into {target_colors} common colors")
    
    return color_mapping


def apply_palette_mapping(img_array, color_mapping):
    """
    Apply a color mapping to an image.
    
    Args:
        img_array: numpy array of image
        color_mapping: dict mapping old colors to new colors
    
    Returns:
        new numpy array with mapped colors
    """
    output_array = img_array.copy()
    height, width = img_array.shape[:2]
    
    for y in range(height):
        for x in range(width):
            # Convert to native Python int for proper tuple comparison
            old_color = tuple(int(v) for v in img_array[y, x])
            if old_color in color_mapping:
                output_array[y, x] = color_mapping[old_color]
    
    return output_array


def downscale_smart(input_path, target_width, target_height, 
                   sampling_method='mode', palette_path=None,
                   auto_palette=False, target_colors=None, 
                   pre_reduce=False, reduction_method='frequency',
                   double_reduce=False, output_path=None):
    """
    Intelligently downscale an interpolated upscale back to pixel-perfect form.
    
    Args:
        input_path: Path to input image
        target_width: Target width in pixels
        target_height: Target height in pixels
        sampling_method: 'mode', 'median', 'center', or 'mean'
        palette_path: Optional path to palette image for color snapping
        auto_palette: If True, extract palette from input image
        target_colors: Optional target number of colors for palette reduction
        pre_reduce: If True, apply palette reduction BEFORE downscaling (can give better results)
        reduction_method: 'frequency' (default), 'kmeans', or 'hybrid'
        double_reduce: If True, apply second reduction to half the colors after first reduction
        output_path: Optional output path (defaults to input_downscaled_METHOD.png)
    
    Returns:
        Path to output image
    """
    # Load input image
    print(f"Loading {input_path}...")
    input_img = Image.open(input_path).convert('RGB')
    input_array = np.array(input_img)
    
    input_width, input_height = input_img.size
    print(f"Input size: {input_width} × {input_height}")
    print(f"Target size: {target_width} × {target_height}")
    
    # Apply pre-reduction if requested
    if target_colors and pre_reduce:
        print(f"\n*** PRE-REDUCTION MODE ***")
        print(f"Reducing palette BEFORE downscaling...")
        print(f"Using {reduction_method} reduction method")
        
        if reduction_method == 'kmeans':
            color_mapping = reduce_palette_kmeans(input_array, target_colors)
        elif reduction_method == 'hybrid':
            color_mapping = reduce_palette_hybrid(input_array, target_colors)
        else:  # frequency
            color_mapping = reduce_palette_smart(input_array, target_colors)
        
        input_array = apply_palette_mapping(input_array, color_mapping)
        
        # Show final color count
        pre_reduced_colors = count_colors_in_image(input_array)
        print(f"Pre-reduced input now has {len(pre_reduced_colors)} unique colors")
        print(f"*** Starting downscale with cleaned palette ***\n")
    
    # Calculate scale factors
    x_scale, y_scale = calculate_scale_factors(
        (input_width, input_height),
        (target_width, target_height)
    )
    print(f"Scale factors: X={x_scale:.2f}×, Y={y_scale:.2f}×")
    
    # Load or extract palette if needed
    palette = None
    if palette_path:
        print(f"Loading palette from {palette_path}...")
        palette_img = Image.open(palette_path).convert('RGB')
        palette = extract_palette_from_image(np.array(palette_img))
        print(f"Loaded {len(palette)} colors from palette")
    elif auto_palette:
        print("Extracting palette from input image...")
        palette = extract_palette_from_image(input_array)
        print(f"Extracted {len(palette)} unique colors")
    
    # Choose sampling function
    sampling_functions = {
        'mode': sample_mode,
        'median': sample_median,
        'center': sample_center,
        'mean': sample_mean_rounded
    }
    
    if sampling_method not in sampling_functions:
        raise ValueError(f"Unknown sampling method: {sampling_method}")
    
    sample_func = sampling_functions[sampling_method]
    print(f"Using sampling method: {sampling_method}")
    
    # Create output array
    output_array = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    
    # Process each target pixel
    print("Downscaling...")
    for y in range(target_height):
        if y % 20 == 0:
            print(f"  Processing row {y}/{target_height}...")
        
        for x in range(target_width):
            # Get bounds of this pixel's block in source image
            x_start, y_start, x_end, y_end = get_pixel_block_bounds(
                x, y, x_scale, y_scale
            )
            
            # Ensure we don't go out of bounds
            x_end = min(x_end, input_width)
            y_end = min(y_end, input_height)
            
            # Extract the block
            block = input_array[y_start:y_end, x_start:x_end]
            
            # Sample the color
            if block.size > 0:
                color = sample_func(block)
                
                # Snap to palette if provided
                if palette:
                    color = find_nearest_palette_color(color, palette)
                
                output_array[y, x] = color
    
    # Create output image
    output_img = Image.fromarray(output_array, 'RGB')
    
    # Apply palette reduction if requested (and not already done as pre-reduction)
    if target_colors and not pre_reduce:
        print(f"\nApplying palette reduction to {target_colors} colors...")
        print(f"Using {reduction_method} reduction method")
        
        if reduction_method == 'kmeans':
            color_mapping = reduce_palette_kmeans(output_array, target_colors)
        elif reduction_method == 'hybrid':
            color_mapping = reduce_palette_hybrid(output_array, target_colors)
        else:  # frequency
            color_mapping = reduce_palette_smart(output_array, target_colors)
        
        output_array = apply_palette_mapping(output_array, color_mapping)
        output_img = Image.fromarray(output_array, 'RGB')
        
        # Show final color count
        final_colors = count_colors_in_image(output_array)
        print(f"Final image has {len(final_colors)} unique colors")
    
    # Apply double reduction if requested (Paul's special feature!)
    if target_colors and double_reduce:
        second_target = target_colors // 2
        print(f"\n🎨 DOUBLE REDUCTION ACTIVATED 🎨")
        print(f"Applying second reduction: {target_colors} → {second_target} colors")
        print(f"Using {reduction_method} reduction method")
        
        if reduction_method == 'kmeans':
            color_mapping = reduce_palette_kmeans(output_array, second_target)
        elif reduction_method == 'hybrid':
            color_mapping = reduce_palette_hybrid(output_array, second_target)
        else:  # frequency
            color_mapping = reduce_palette_smart(output_array, second_target)
        
        output_array = apply_palette_mapping(output_array, color_mapping)
        output_img = Image.fromarray(output_array, 'RGB')
        
        # Show final color count after double reduction
        final_colors = count_colors_in_image(output_array)
        print(f"After double reduction: {len(final_colors)} unique colors")
    
    # Determine output path
    if output_path is None:
        input_path_obj = Path(input_path)
        if target_colors:
            suffix = f"_pre{target_colors}c" if pre_reduce else f"_{target_colors}c"
            if double_reduce:
                suffix += f"x2"  # Add marker for double reduction
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_downscaled_{sampling_method}{suffix}.png"
        else:
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_downscaled_{sampling_method}.png"
    
    # Save
    print(f"Saving to {output_path}...")
    output_img.save(output_path, 'PNG')
    print("Done!")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Smart pixel art downscaler - recovers pristine pixels from interpolated upscales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic downscale using mode (most common color)
  python pixel_art_downscaler.py input.png 320 200
  
  # Use median sampling instead
  python pixel_art_downscaler.py input.png 320 200 --method median
  
  # Snap colors to a palette image
  python pixel_art_downscaler.py input.png 320 200 --palette original.png
  
  # Auto-extract and use palette from input
  python pixel_art_downscaler.py input.png 320 200 --auto-palette
  
  # Reduce to specific number of colors (cleans up artifacts)
  python pixel_art_downscaler.py input.png 320 200 --colors 16
  
  # Apply palette reduction BEFORE downscaling (often better results)
  python pixel_art_downscaler.py input.png 320 200 --colors 16 --pre-reduce
  
  # Use k-means for better color diversity (preserves rare colors like yellow hair)
  python pixel_art_downscaler.py input.png 320 200 --colors 16 --pre-reduce --reduction kmeans
  
  # Hybrid: keep most common colors + cluster the rest
  python pixel_art_downscaler.py input.png 320 200 --colors 32 --pre-reduce --reduction hybrid
  
  # Paul's double reduction: 32 colors, then reduce to 16
  python pixel_art_downscaler.py input.png 320 200 --colors 32 --reduction kmeans --double-reduce
  
  # Specify output path
  python pixel_art_downscaler.py input.png 320 200 -o output.png

Sampling methods:
  mode   - Most common color in each block (best for clean recovery)
  median - Median color (good for reducing artifacts)
  center - Center pixel only (fast, works if upscale was centered)
  mean   - Average color rounded (can help with variations)
        """
    )
    
    parser.add_argument('input', help='Input image path')
    parser.add_argument('width', type=int, help='Target width')
    parser.add_argument('height', type=int, help='Target height')
    parser.add_argument('--method', '-m', 
                       choices=['mode', 'median', 'center', 'mean'],
                       default='mode',
                       help='Sampling method (default: mode)')
    parser.add_argument('--palette', '-p',
                       help='Path to palette image for color snapping')
    parser.add_argument('--auto-palette', '-a',
                       action='store_true',
                       help='Auto-extract palette from input image')
    parser.add_argument('--colors', '-c', type=int,
                       metavar='N',
                       help='Target number of colors (reduces palette by merging similar rare colors into common ones)')
    parser.add_argument('--reduction', '-r',
                       choices=['frequency', 'kmeans', 'hybrid'],
                       default='frequency',
                       help='Palette reduction method: frequency (keep most common), kmeans (preserve diversity), hybrid (balanced)')
    parser.add_argument('--pre-reduce', '-pr',
                       action='store_true',
                       help='Apply palette reduction BEFORE downscaling (often gives cleaner results)')
    parser.add_argument('--double-reduce', '-dr',
                       action='store_true',
                       help="Paul's special feature: apply second reduction to half the colors (e.g., 32→16)")
    parser.add_argument('--output', '-o',
                       help='Output path (default: input_downscaled_METHOD.png)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # Validate palette file if provided
    if args.palette and not Path(args.palette).exists():
        print(f"Error: Palette file not found: {args.palette}")
        return 1
    
    try:
        downscale_smart(
            args.input,
            args.width,
            args.height,
            sampling_method=args.method,
            palette_path=args.palette,
            auto_palette=args.auto_palette,
            target_colors=args.colors,
            pre_reduce=args.pre_reduce,
            reduction_method=args.reduction,
            double_reduce=args.double_reduce,
            output_path=args.output
        )
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())