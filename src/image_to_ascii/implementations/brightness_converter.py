"""
Brightness-based ASCII converter
Maps pixel brightness (0–255) to ASCII characters using linear interpolation.
Characters ordered from darkest to lightest: ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
This version resizes the image to the target width while maintaining aspect ratio.
"""

import numpy as np
from PIL import Image

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']

def convert_image_to_ascii_brightness(img: Image.Image, width: int) -> str:
    """
    Convert a PIL image to ASCII art using pixel brightness.

    Args:
        img (PIL.Image): Input image.
        width (int): Target ASCII width.

    Returns:
        str: ASCII art string.
    """
    gray = img.convert("L")

    aspect_ratio = gray.height / gray.width
    new_height = max(1, round(width * aspect_ratio * 0.55))
    
    # Resize the image
    resized = gray.resize((width, new_height))

    pixels = np.array(resized, dtype=float)

    min_px, max_px = pixels.min(), pixels.max()
    if max_px != min_px:
        pixels = (pixels - min_px) / (max_px - min_px) * 255
    else:
        pixels.fill(max_px)  # uniform image

    # Map pixels to ASCII characters
    scale = len(chars) - 1
    ascii_lines = [
        ''.join(chars[int(px / 255 * scale)] for px in row)
        for row in pixels
    ]

    return "\n".join(ascii_lines)


# --- inline test ---
if __name__ == "__main__":
    # from PIL import ImageDraw

    # img = Image.new("L", (100, 100), 0)
    # draw = ImageDraw.Draw(img)
    # draw.rectangle([10, 10, 90, 90], fill=255)

    # ascii_output = convert_image_to_ascii_brightness(img, width=50)
    # print(ascii_output)
