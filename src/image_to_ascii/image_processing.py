from PIL import Image
from .implementations.method import Filter


def load_image(path):
    img = Image.open(path).convert("L")
    return img


def resize_image(img, width):
    aspect = img.height / img.width
    height = int(width * aspect / 2)
    return img.resize((width, height))
