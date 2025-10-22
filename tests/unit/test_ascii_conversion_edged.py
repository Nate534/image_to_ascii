from PIL import Image
from image_to_ascii.implementations.edged_converter import convert_image_to_ascii

def test_image_to_ascii():
    img = Image.new('L', (80, 40))
    res = convert_image_to_ascii(img, 80)
    lines = res.split('\n')
    assert len(lines) > 0
    assert all(len(line) == 80 for line in lines)

