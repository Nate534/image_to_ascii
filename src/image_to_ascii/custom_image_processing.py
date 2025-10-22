from PIL import Image
from .implementations.method import Filter
from .implementations.mode_converter import cvt_scale


def load_image(path,mode:Filter):
    img = Image.open(path).convert("RGB")
    ret=cvt_scale(img,mode)
    
    return ret


