from PIL import Image

def enhance_contrast(img):
    pixels = list(img.getdata())
    min_val = min(pixels)
    max_val = max(pixels)
    if max_val == min_val:
        return img  
    stretched = [(int((p - min_val) / (max_val - min_val) * 255)) for p in pixels]
    new_img = Image.new('L', img.size)
    new_img.putdata(stretched)
    return new_img


def load_image(path, enhance=False):
    img = Image.open(path).convert('L')
    if enhance:
        img = enhance_contrast(img)
    return img

def resize_image(img, width):
    aspect = img.height / img.width
    height = int(width * aspect / 2)
    return img.resize((width, height))

def batch_processing():
    pass