import numpy as np
from PIL import Image, ImageDraw

chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

char_features = {}

for char in chars:
    char_features[char] = get_char_pca(char)

def get_char_pca(char, size=8):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((size//2, size//2), char, fill=0, anchor='mm')
    pixels = np.array(img)
    return compute_pca_features(pixels)

def compute_pca_features(image_block):
    flat = image_block.flatten().astype(np.float64)
    mean = np.mean(flat)
    centered = flat - mean
    cov = np.dot(centered, centered) / (len(centered) - 1)
    eigenvals, eigenvecs = np.linalg.eig(cov)
    idx = np.argsort(eigenvals)[::-1]
    return eigenvals[idx], eigenvecs[:, idx]

def select_symbol(block):
    block_flat = block.flatten().astype(np.float64)
    mean = np.mean(block_flat)
    centered = block_flat - mean
    cov = np.dot(centered, centered) / (len(centered) - 1)
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