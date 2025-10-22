from PIL.Image import Image
from .method import Filter
import numpy as np

def cvt_scale(img:Image,mode:Filter)->Image:
    #img = np.array(img)
    
    cvt=lambda r,g,b: 0.299*r + 0.587*g + 0.114*b
    match mode:
        case Filter.LIGHTNESS:
            cvt=lambda r,g,b: (max(r,g,b)+min(r,g,b))/2 

        case Filter.AVERAGE:
           cvt=lambda r,g,b: (r+g+b)/3
            
     
            
        
    (height,width)=img.size
    for y in range(height):
        for x in range(width):
            r,g,b=img.getpixel((y,x))
            px=int(cvt(r,g,b))
            img.putpixel((y,x),(px,px,px))
    return img

