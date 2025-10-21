

import numpy as np
from PIL import Image,ImageFilter


def convert_image_to_ascii(img: Image.Image, width: int) -> str:
    chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
    
    aspect = img.height / img.width
    height = int(width * aspect / 2)
    img = img.resize((width, height))
    edge_layer=img.copy()
    edge_layer=edge_layer.filter(ImageFilter.EDGE_ENHANCE_MORE)
  
    pixels = np.array(img)
    pixelated_edge=np.array(edge_layer,dtype=np.float32)

    edges,dir=pixel_gradient(pixelated_edge)
    threshold=np.percentile(edges,85)
    ascii_lines = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = pixels[y, x]
            if edges[y,x]>threshold:
                line.append(dir[y,x])
            else:
                line.append(" ")
        ascii_lines.append(''.join(line))
    
    return '\n'.join(ascii_lines)
def pixel_gradient(pixelated:np.ndarray):
    gx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    gy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    
    image_pad = np.pad(pixelated,((1,1),(1,1)),mode="constant",constant_values=0)

    rows,cols=pixelated.shape

    empty_x=np.zeros_like(pixelated)
    empty_y=np.zeros_like(pixelated)
    edges=np.zeros_like(pixelated)
    direction=np.zeros_like(pixelated,dtype=str)

    for x in range(rows):
        for y in range(cols):
            section=image_pad[x:x+3,y:y+3]
            empty_x[x,y] = np.sum(section * gx)
            empty_y[x,y] = np.sum(section * gy)
            direction[x,y]=line_variation(empty_x[x,y],empty_y[x,y])
            # direction[x,y]=edge_direction(empty_x[x,y],empty_y[x,y])

            edges[x,y] = np.sqrt(empty_x[x,y]**2 + empty_y[x,y]**2)

    edge_layer=(edges/edges.max()*255).astype(np.uint8)
    direction=clean(direction)
    return edge_layer,direction

def clean(nparr :np.ndarray)->np.ndarray:
    for x in range(len(nparr)):
        for y in range(len(nparr[x])):
            if (x ==0 or y==0)or(x==(len(nparr)-1) or y==(len(nparr[x])-1)):
                nparr[x][y]=" "
    return nparr

def edge_direction(x,y):
    tanratio=np.arctan2(y,x)
    degree=np.degrees(tanratio)%180
    if 0<=degree<45:
        return "|"
        
    elif 45<=degree<90:
        return "/"
        
    elif 90<=degree<135:
        return "-" 
    elif 135<=degree<180:
        return "\\"
    
def line_variation(x,y):
   # print(x.max())
    tanratio=np.arctan2(y,x)
    char_map = ['|', '!', 'I', 'l','\\', 'Y', 'X','-', '_', '=','/', 'Z', 'N','|', '1', 'i', 'L','/', 'n', 'z','-', '~', '=','\\', 'x', 'K', 'k','|', '!', 'I', 'l']

    line_index = int((np.degrees(tanratio)%360/ 360.0) * (len(char_map) - 1))
    return char_map[line_index]