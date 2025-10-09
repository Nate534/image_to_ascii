from PIL import Image
from src.image_to_ascii.ascii_conversion import image_to_ascii

def test_image_to_ascii():
    img = Image.new('L', (80, 40))
    ascii_art = image_to_ascii(img, 80)
    assert len(ascii_art) == 40
    assert all(len(line) == 80 for line in ascii_art.split('\n'))