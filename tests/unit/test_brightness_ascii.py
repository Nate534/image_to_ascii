import pytest
from PIL import Image
from image_to_ascii.implementations.brightness_converter import convert_image_to_ascii_brightness

def test_brightness_ascii_output_shape():
    """Test that the ASCII output has correct width and height."""
    img = Image.new("L", (80, 40))
    ascii_art = convert_image_to_ascii_brightness(img, 80)
    lines = ascii_art.split("\n")

    # Aspect ratio correction uses 0.55, so expected height = round(40 / 80 * 80 * 0.55)
    expected_height = max(1, round(80 * (40 / 80) * 0.55))
    assert len(lines) == expected_height
    assert all(len(line) == 80 for line in lines)

def test_brightness_ascii_dark_to_light():
    """Test that black pixels map to dark chars and white pixels to light chars."""
    dark_img = Image.new("L", (10, 10), 0)    # all black
    light_img = Image.new("L", (10, 10), 255)  # all white

    dark_ascii = convert_image_to_ascii_brightness(dark_img, 10)
    light_ascii = convert_image_to_ascii_brightness(light_img, 10)

    # Dark image should only contain the darkest character '@'
    assert set(dark_ascii.replace("\n", "")) == {"@"}

    # Light image should only contain the lightest character ' '
    assert set(light_ascii.replace("\n", "")) == {" "}

def test_brightness_ascii_mixed_image():
    """Test a gradient image maps to multiple characters."""
    gradient_img = Image.new("L", (12, 12))
    for x in range(12):
        for y in range(12):
            gradient_img.putpixel((x, y), int((x / 11) * 255))

    ascii_art = convert_image_to_ascii_brightness(gradient_img, 12)
    chars_in_output = set(ascii_art.replace("\n", ""))

    # Should contain more than 1 character
    assert len(chars_in_output) > 1
