"""
Brightness-based ASCII converter

Maps pixel brightness (0–255) to ASCII characters using a simple linear scale.
Acts as a lightweight alternative to PCA or CNN converters.
"""

import numpy as np
from PIL import Image
from ..models.ascii_symbols import chars  

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']

def convert_image_to_ascii_brightness(img, width):
    aspect = img.height / img.width
    height = int(width * aspect / 2)
    img_resized = img.resize((width, height)).convert('L')
    pixels = np.array(img_resized)

    ascii_art = []
    for row in pixels:
        line = ""
        for px in row:
            idx = round((px / 255) * (len(chars) - 1))
            line += chars[idx]
        ascii_art.append(line)
    return "\n".join(ascii_art)
