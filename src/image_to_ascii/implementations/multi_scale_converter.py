
import numpy as np
import cv2 as cv
from PIL.Image import Image
from PIL import Image as baseImage

PYRAMID_LVL=4

def convert_image_to_ascii_MultiScale(img:Image):
    chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
    aspect = img.height / img.width
    height,width=img.shape
    pixels = np.array(img)
    full = {}

    for i in range(PYRAMID_LVL):
        if i!=0:
            width/=2
            aspect = img.height / img.width
            height = int(width * aspect / 2)
            img=Guassian_blurred(img)
            img = img.resize((width, height))
            pixels = np.array(img)
        ascii_lines=[]

        for y in range(height):
            line = []
            for x in range(width):
                brightness = pixels[y, x]
                char_index = int((brightness / 255.0) * (len(chars) - 1))
                line.append(chars[char_index])
            ascii_lines.append(''.join(line))
        full[width]='\n'.join(ascii_lines)
        
    return full

def Guassian_blurred(img:Image):
    arried =np.array(Image,dtype=np.uint8)
    blurred =cv.GaussianBlur(arried,(5,5),0)
    return baseImage.fromarray(blurred)