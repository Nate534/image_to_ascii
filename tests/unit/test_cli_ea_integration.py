import unittest
from PIL import Image
from image_to_ascii.implementations.ea_converter import convert_image_to_ascii_ea


class TestEAConverter(unittest.TestCase):
    def test_returns_string(self):
        """EA converter should return ASCII art as a string of expected width."""
        img = Image.new("L", (8, 8), color=128)
        ascii_art = convert_image_to_ascii_ea(img, width=8)

        self.assertIsInstance(ascii_art, str, "Output should be a string")
        lines = ascii_art.splitlines()
        self.assertTrue(all(len(line) == 8 for line in lines), "Each line should match target width")

    def test_handles_blank_image(self):
        """EA converter should handle uniform images without empty output."""
        img = Image.new("L", (4, 4), color=255)
        result = convert_image_to_ascii_ea(img, width=4)

        self.assertIsInstance(result, str, "Output should be a string")
        self.assertGreater(len(result.strip()), 0, "Output should not be empty")

    def test_tiny_image(self):
        """EA converter should work even for 1x1 images."""
        img = Image.new("L", (1, 1), color=0)
        result = convert_image_to_ascii_ea(img, width=1)

        self.assertGreaterEqual(len(result), 1, "Output should contain at least one character")


if __name__ == "__main__":
    unittest.main()
