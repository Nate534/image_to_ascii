import numpy as np
from .image_processing import resize_image
from .symbol_selection import select_symbol
from .dithering import apply_dithering  # make sure dithering.py is in the same package


def image_to_ascii(img, width, dithering="none"):
    """
    Convert a PIL image to ASCII using block-based symbol selection.

    Args:
        img: PIL.Image
        width: int, target ASCII width
        dithering: str, optional, one of "none", "floyd", "atkinson"
                   applies dithering before ASCII conversion
    Returns:
        str: ASCII art
    """
    
    img = resize_image(img, width)

    
    pixels = np.array(img)

    # Apply dithering if requested
    if dithering != "none":
        pixels = apply_dithering(pixels, method=dithering)

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


#### --- optional inline test ---
if __name__ == "__main__":
    image_to_ascii()
    # from PIL import Image

    # img = Image.open("test.jpg").convert("L")
    # ascii_art_none = image_to_ascii(img, width=80)
    # ascii_art_floyd = image_to_ascii(img, width=80, dithering="floyd")
    # ascii_art_atkinson = image_to_ascii(img, width=80, dithering="atkinson")

    # print("=== No Dithering ===")
    # print(ascii_art_none)
    # print("\n=== Floyd-Steinberg Dithering ===")
    # print(ascii_art_floyd)
    # print("\n=== Atkinson Dithering ===")
    # print(ascii_art_atkinson)
