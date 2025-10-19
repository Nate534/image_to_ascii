from PIL import Image
from image_to_ascii.implementations.cnn_converter import convert_image_to_ascii_cnn

def test_cnn_ascii_output_shape():
    img = Image.new('L', (80, 40))
    ascii_art = convert_image_to_ascii_cnn(img, 80)
    lines = ascii_art.split('\n')
    assert len(lines) > 0
    assert all(len(line) == 80 for line in lines)
