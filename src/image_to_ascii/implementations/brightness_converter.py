"""
Brightness-based ASCII converter
Maps pixel brightness (0–255) to ASCII characters using a simple linear scale.
Automatically rescales image brightness so the full ASCII range is used.
Handles uniform black or white images correctly.
"""

import numpy as np
from PIL import Image
from ..models.ascii_symbols import chars  

# ASCII character set (dark → light)
chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']

def convert_image_to_ascii_brightness(img, width):
    """
    Convert a PIL image to ASCII art using brightness mapping.

    Args:
        img: PIL.Image object
        width: target width of ASCII art

    Returns:
        str: ASCII art as a single string
    """
    aspect = img.height / img.width
    height = int(width * aspect / 2)  # divide by 2 for character height
    img_resized = img.resize((width, height)).convert('L')

    pixels = np.array(img_resized, dtype=float)

    min_px, max_px = pixels.min(), pixels.max()
    if max_px > min_px:
        pixels = (pixels - min_px) / (max_px - min_px) * 255
    else:
        # all pixels same: map to lightest or darkest char
        if min_px == 255:
            pixels = np.full_like(pixels, 255)  # all white
        else:
            pixels = np.zeros_like(pixels)      # all black

    ascii_art = []
    for row in pixels:
        line = ""
        for px in row:
            idx = round((px / 255) * (len(chars) - 1))
            line += chars[idx]
        ascii_art.append(line)

    return "\n".join(ascii_art)
