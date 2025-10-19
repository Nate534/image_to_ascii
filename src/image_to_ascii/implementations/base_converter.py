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
from PIL import Image,ImageFilter


def get_char_pca(char, size=8):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((size//2, size//2), char, fill=0, anchor='mm')
    pixels = np.array(img)
    return compute_pca_features(pixels)

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
    edge =  ['@', '#', 'X', '*'] 
    # Resize image maintaining aspect ratio
    aspect = img.height / img.width
    height = int(width * aspect / 2)

    img = img.resize((width, height))
    edge_layer=img.copy()
    edge_layer.filter(ImageFilter.BLUR())
    # Convert to numpy array
    
    pixels = np.array(img)
    pixelated_edge=np.array(edge_layer)

    edges=pixel_gradient(pixelated_edge)
    threshold=np.percentile(edges,90)
    # Example: Simple brightness mapping (replace with your algorithm)
    ascii_lines = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = pixels[y, x]
            
            if edges[y,x]>threshold:
                char_index = int((edges[y,x] / 255.0) * (len(edge) - 1))
                line.append("=")
            else:
                char_index = int((brightness / 255.0) * (len(chars) - 1))
                line.append(chars[char_index])
                #line.append("1")

        ascii_lines.append(''.join(line))
    
    return '\n'.join(ascii_lines)


def pixel_gradient(pixelated:np.ndarray)->np.ndarray:
    gx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    gy=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    
    image_pad = np.pad(pixelated,((1,1),(1,1)),mode="constant",constant_values=0)

    rows,cols=pixelated.shape

    empty_x=np.zeros_like(pixelated)
    empty_y=np.zeros_like(pixelated)
    edges=np.zeros_like(pixelated)
    direction=np.zeros_like(pixelated)

    for x in range(rows):
        for y in range(cols):
            section=image_pad[x:x+3,y:y+3]
            empty_x[x,y] = np.sum(section * gx)
            empty_y[x,y] = np.sum(section * gy)
            if empty_x[x,y]>
            edges[x,y] = np.sqrt(empty_x[x,y]**2 + empty_y[x,y]**2)

    edge_layer=(edges/edges.max()*255).astype(np.uint8)

    return edge_layer



    
# Optional: Add any helper functions your algorithm needs
def your_helper_function(data):
    """
    Document your helper functions too!
    """
    pass
def compute_pca_features(image_block):
    flat = image_block.flatten().astype(np.float64)
    mean = np.mean(flat)
    centered = flat - mean
    cov = np.outer(centered, centered) / (len(centered) - 1)
    eigenvals, eigenvecs = np.linalg.eig(cov)
    idx = np.argsort(eigenvals)[::-1]
    return eigenvals[idx], eigenvecs[:, idx]

char_features = {c: get_char_pca(c) for c in chars}

def select_symbol(block):
    block_flat = block.flatten().astype(np.float64)
    if len(block_flat) == 1:
        return chars[0]
    mean = np.mean(block_flat)
    centered = block_flat - mean
    if len(centered) <= 1:
        return chars[0]
    cov = np.outer(centered, centered) / (len(centered) - 1)
    eigenvals, eigenvecs = np.linalg.eig(cov)
    idx = np.argsort(eigenvals)[::-1]
    block_vals = eigenvals[idx]
    block_vecs = eigenvecs[:, idx]
    min_dist = float('inf')
    best_char = chars[0]
    for char in chars:
        char_vals, char_vecs = char_features[char]
        dist = np.sqrt(np.sum((block_vals - char_vals)**2) + np.sum((block_vecs[:, 0] - char_vecs[:, 0])**2))
        if dist < min_dist:
            min_dist = dist
            best_char = char
    return best_char

def convert_image_to_ascii(img, width):
    aspect = img.height / img.width
    height = int(width * aspect / 2)
    img_resized = img.resize((width, height)).convert('L')
    pixels = np.array(img_resized)

    ascii_art = []
    for y in range(0, height, 1):
        row = ''.join(select_symbol(pixels[y:y+1, x:x+1]) for x in range(width))
        ascii_art.append(row)
    return '\n'.join(ascii_art)
