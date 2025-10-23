"""
EA-based ASCII converter.

This uses a simple evolutionary approach to select ASCII symbols that best
approximate blocks of the image. Intended as a demonstration; parameters
(population size, generations, mutation rate) can be tuned for quality.
"""

import numpy as np
from PIL import Image, ImageDraw
from ..models.ascii_symbols import chars  # Make sure you have a chars list somewhere

def get_char_features(char, size=8):
    """Return a flattened numpy array representing the character's 'image'."""
    img = Image.new("L", (size, size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((size//2, size//2), char, fill=0, anchor="mm")
    pixels = np.array(img)
    return pixels.flatten().astype(np.float64)

# Precompute features for all ASCII symbols
char_features = {c: get_char_features(c) for c in chars}

def select_symbol_ea(block, population_size=30, generations=20, mutation_rate=0.1):
    """Select the best ASCII symbol for a block using a simple evolutionary search."""
    block_flat = block.flatten().astype(np.float64)
    # Initialize population randomly
    population = np.random.choice(chars, population_size)
    for _ in range(generations):
        fitness = []
        for c in population:
            feature = char_features[c]
            dist = np.linalg.norm(block_flat - feature[:len(block_flat)])
            fitness.append(dist)
        fitness = np.array(fitness)
        best_idx = np.argmin(fitness)
        best_char = population[best_idx]
        # Reproduce: mutate
        new_population = np.random.choice(chars, population_size)
        new_population[0] = best_char  # keep best
        population = new_population
    return best_char

def convert_image_to_ascii_ea(img, width, population_size=30, generations=20, mutation_rate=0.1):
    """Convert an image to ASCII using the EA method."""
    # resize preserving aspect ratio
    aspect = img.height / img.width
    width = max(1, width)
    height = max(1, int(width * aspect / 2))  # ensure height is at least 1
    img_resized = img.resize((width, height)).convert("L")
    pixels = np.array(img_resized)

    ascii_art = []
    for y in range(height):
        row = []
        for x in range(width):
            block = pixels[y:y+1, x:x+1]
            symbol = select_symbol_ea(
                block,
                population_size=population_size,
                generations=generations,
                mutation_rate=mutation_rate
            )
            row.append(symbol)
        ascii_art.append("".join(row))
    return "\n".join(ascii_art)
