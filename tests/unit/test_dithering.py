import unittest
import numpy as np
from src.image_to_ascii.dithering import floyd_steinberg_dither, atkinson_dither

class TestDithering(unittest.TestCase):

    def setUp(self):
        self.img = np.linspace(0, 255, 25, dtype=np.uint8).reshape((5,5))

    def test_floyd_steinberg_output_range(self):
        """Floyd-Steinberg output should stay within 0-255"""
        result = floyd_steinberg_dither(self.img)
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 255))

    def test_atkinson_output_range(self):
        """Atkinson output should stay within 0-255"""
        result = atkinson_dither(self.img)
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 255))

    def test_floyd_steinberg_changes_image(self):
        """Floyd-Steinberg should alter the original image"""
        result = floyd_steinberg_dither(self.img)
        self.assertFalse(np.array_equal(result, self.img))

    def test_atkinson_changes_image(self):
        """Atkinson should alter the original image"""
        result = atkinson_dither(self.img)
        self.assertFalse(np.array_equal(result, self.img))

if __name__ == "__main__":
    unittest.main()
