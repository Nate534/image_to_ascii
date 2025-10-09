import numpy as np
from src.image_to_ascii.symbol_selection import select_symbol

def test_select_symbol():
    block = np.ones((8, 8)) * 255
    symbol = select_symbol(block)
    assert symbol in ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']