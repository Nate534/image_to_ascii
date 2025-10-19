"""
Template for creating new ASCII converter implementations.

This file serves as a template and example for contributors who want to add
new ASCII conversion algorithms. Copy this structure when creating your own
implementation.

Example usage:
1. Copy this file to a new name (e.g., brightness_converter.py)
2. Implement your conversion algorithm
3. Add mathematical documentation
4. Test with sample images
5. Submit as a pull request!
"""

import numpy as np
from PIL import Image,ImageFilter,ImageDraw



def convert_image_to_ascii(img: Image.Image, width: int) -> str:
    """
    Template function for converting an image to ASCII art.
    
    Replace this with your own implementation!
    
    Args:
        img: PIL Image object (grayscale)
        width: Target width in characters
        
    Returns:
        ASCII art as string
        
    Mathematical approach:
        Describe your algorithm here, including:
        - What mathematical concepts you use
        - Any formulas or equations
        - References to papers or resources
        
    Example:
        For brightness-based conversion:
        1. Calculate average brightness: avg = mean(pixel_values)
        2. Map to character index: idx = int((avg / 255) * (len(chars) - 1))
        3. Return corresponding character: chars[idx]
    """
    # Your implementation goes here
    chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
    
    # Resize image maintaining aspect ratio
    aspect = img.height / img.width
    height = int(width * aspect / 2)

    img = img.resize((width, height))
    edge_layer=img.copy()
    #edge_layer=edge_layer.filter(ImageFilter.BLUR)
    # Convert to numpy array
    
    pixels = np.array(img)
    pixelated_edge=np.array(edge_layer,dtype=np.float32)

    edges,dir=pixel_gradient(pixelated_edge)
    threshold=np.percentile(edges,80)
   
    # Example: Simple brightness mapping (replace with your algorithm)
    ascii_lines = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = pixels[y, x]
            if edges[y,x]>threshold:
                line.append(dir[y,x])
            else:
                char_index = int((brightness / 255.0) * (len(chars) - 1))
                line.append(chars[char_index])
               

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
            direction[x,y]=edge_direction(empty_x[x,y],empty_y[x,y])

            edges[x,y] = np.sqrt(empty_x[x,y]**2 + empty_y[x,y]**2)

    edge_layer=(edges/edges.max()*255).astype(np.uint8)

    return edge_layer,direction
def edge_direction(x,y):
    tanratio=np.arctan2(y,x)
    degree=np.degrees(tanratio)%180
    if 0<=degree<45:
        return "-" 
    elif 45<=degree<90:
        return "/"
        
    elif 90<=degree<135:
        return "|"
    elif 135<=degree<180:
        return "\\"




    
# Optional: Add any helper functions your algorithm needs
def your_helper_function(data):
    """
    Document your helper functions too!
    """
    pass
