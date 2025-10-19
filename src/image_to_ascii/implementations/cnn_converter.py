"""
CNN-based ASCII converter - Placeholder Implementation
"""

import numpy as np
from PIL import Image
import torch
from ..ascii_symbols import chars
from .models.cnn_model import load_model

PATCH_SIZE = 8  

def convert_image_to_ascii_cnn(img, width, model_path=None):
    """
    Convert a grayscale image to ASCII using CNN model inference.
    Works patch-by-patch (PATCH_SIZE x PATCH_SIZE).
    """
    model = load_model(model_path)

    # Resize image proportionally so width is as requested
    aspect = img.height / img.width
    height = int(width * aspect / PATCH_SIZE) * PATCH_SIZE
    img_resized = img.resize((width * PATCH_SIZE, height))
    img_resized = img_resized.convert('L')  # grayscale

    pixels = np.array(img_resized)
    ascii_art = []

    # Process image in PATCH_SIZE blocks
    for y in range(0, pixels.shape[0], PATCH_SIZE):
        line = ""
        for x in range(0, pixels.shape[1], PATCH_SIZE):
            patch = pixels[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            
            if patch.shape != (PATCH_SIZE, PATCH_SIZE):
                temp = np.ones((PATCH_SIZE, PATCH_SIZE)) * 255
                temp[:patch.shape[0], :patch.shape[1]] = patch
                patch = temp

            
            tensor_patch = torch.tensor(patch, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0

            
            with torch.no_grad():
                output = model(tensor_patch)
                predicted_idx = output.argmax(dim=1).item()
                line += chars[predicted_idx]

        ascii_art.append(line)

    return "\n".join(ascii_art)
