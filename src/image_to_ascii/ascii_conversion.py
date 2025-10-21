import numpy as np
from .image_processing import resize_image
from .symbol_selection import select_symbol
from .dithering import apply_dithering  

def image_to_ascii(img, width, dither=False):
    img = resize_image(img, width)

    if dither:
        img = apply_dithering(img)

    pixels = np.array(img)
    ascii_height = img.height
    ascii_width = width
    block_h = img.height // ascii_height
    block_w = img.width // ascii_width
    ascii_img = []

    for y in range(ascii_height):
        row = []
        for x in range(ascii_width):
            block = pixels[y*block_h:(y+1)*block_h, x*block_w:(x+1)*block_w]
            if block.size == 0:
                row.append(' ')
                continue
            symbol = select_symbol(block)
            row.append(symbol)
        ascii_img.append(''.join(row))

    return '\n'.join(ascii_img)
