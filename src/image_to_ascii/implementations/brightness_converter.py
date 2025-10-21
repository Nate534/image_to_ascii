"""
Brightness-based ASCII converter with optional dithering.
Maps pixel brightness (0–255) to ASCII characters using linear interpolation.
"""

import numpy as np
from PIL import Image
from ..dithering import apply_dithering  

CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']

def convert_image_to_ascii_brightness(img: Image.Image, width: int, dithering: str = "none") -> str:
    """
    Convert a PIL image to ASCII art using pixel brightness.

    Args:
        img (PIL.Image): Input image.
        width (int): Target ASCII width.
        dithering (str): Dithering method: "none", "floyd", or "atkinson".

    Returns:
        str: ASCII art string.
    """
    gray = img.convert("L")

    aspect_ratio = gray.height / gray.width
    new_height = max(1, round(width * aspect_ratio * 0.55))
    resized = gray.resize((width, new_height))

    pixels = np.array(resized, dtype=float)

    min_px, max_px = pixels.min(), pixels.max()
    if max_px != min_px:
        pixels = (pixels - min_px) / (max_px - min_px) * 255
    else:
        pixels.fill(max_px)  # uniform image

    if dithering != "none":
        pixels = apply_dithering(pixels, method=dithering)

    scale = len(CHARS) - 1
    ascii_lines = [
        ''.join(CHARS[int(px / 255 * scale)] for px in row)
        for row in pixels
    ]

    return "\n".join(ascii_lines)


###### --- optional inline test ---
# if __name__ == "__main__":
    # from PIL import ImageDraw

    # img = Image.new("L", (50, 50), 0)
    # draw = ImageDraw.Draw(img)
    # draw.rectangle([5, 5, 45, 45], fill=255)

    # ascii_output = convert_image_to_ascii_brightness(img, width=40, dithering="floyd")
    # print(ascii_output)
