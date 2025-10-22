from PIL import Image as ImageF
from PIL.Image import Image
from .method import Filter
import numpy as np

def cvt_scale(img:Image,mode:Filter)->Image:
    
    img = img.convert("RGB")
    arr = np.asarray(img, dtype=float)

    
    gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]

    if mode == Filter.AVERAGE:
        gray = arr.mean(axis=2)
    elif mode == Filter.LIGHTNESS:
        gray = (arr.max(axis=2) + arr.min(axis=2)) / 2

    gray = np.clip(gray, 0, 255).astype(np.uint8)
    return ImageF.fromarray(gray, mode="L")