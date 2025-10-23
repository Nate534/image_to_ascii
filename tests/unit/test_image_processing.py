import pytest
from PIL import Image
import numpy as np
from image_to_ascii.image_processing import load_image, resize_image


def test_load_image():
    img = Image.new("RGB", (10, 10), color="red")
    img.save("test.jpg")
    loaded = load_image("test.jpg")
    assert loaded.mode == "L"
    assert loaded.size == (10, 10)


def test_resize_image():
    img = Image.new("L", (20, 10))
    resized = resize_image(img, 80)
    assert resized.size[0] == 80
    assert resized.size[1] == 20
