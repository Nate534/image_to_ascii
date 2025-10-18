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
from PIL import Image


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
    
    # Convert to numpy array
    pixels = np.array(img)
    
    # Example: Simple brightness mapping (replace with your algorithm)
    ascii_lines = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = pixels[y, x]
            char_index = int((brightness / 255.0) * (len(chars) - 1))
            line.append(chars[char_index])
        ascii_lines.append(''.join(line))
    
    return '\n'.join(ascii_lines)


# Optional: Add any helper functions your algorithm needs
def your_helper_function(data):
    """
    Document your helper functions too!
    """
    pass