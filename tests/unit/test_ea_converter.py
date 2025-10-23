import numpy as np
from PIL import Image
from image_to_ascii.implementations.ea_converter import convert_image_to_ascii_ea

def test_ea_converter_returns_string(tmp_path):
    # make a small grayscale image
    img = Image.new("L", (8, 8), color=128)
    ascii_art = convert_image_to_ascii_ea(img, width=8)
    assert isinstance(ascii_art, str)
    # ensure correct width in output
    lines = ascii_art.splitlines()
    assert all(len(line) == 8 for line in lines)

def test_ea_converter_handles_blank_image():
    img = Image.new("L", (4, 4), color=255)
    result = convert_image_to_ascii_ea(img, width=4)
    assert isinstance(result, str)
    # expect repeated same symbol, not empty
    assert len(result.strip()) > 0

def test_ea_converter_tiny_image():
    img = Image.new("L", (1, 1), color=0)
    result = convert_image_to_ascii_ea(img, width=1)
    assert len(result) >= 1
