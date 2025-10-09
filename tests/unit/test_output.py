import os
from src.image_to_ascii.output import save_ascii, print_ascii

def test_save_ascii():
    ascii_art = 'test'
    save_ascii(ascii_art, 'test.txt')
    assert os.path.exists('test.txt')
    with open('test.txt', 'r') as f:
        assert f.read() == 'test'
    os.remove('test.txt')