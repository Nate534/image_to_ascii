import numpy as np

def floyd_steinberg_dither(image_array: np.ndarray) -> np.ndarray:
    """Apply Floyd–Steinberg dithering to a grayscale image array (0–255)."""
    arr = image_array.astype(float) / 255.0
    h, w = arr.shape
    for y in range(h):
        for x in range(w):
            old_pixel = arr[y, x]
            new_pixel = round(old_pixel)
            arr[y, x] = new_pixel
            error = old_pixel - new_pixel
            if x + 1 < w:
                arr[y, x + 1] += error * 7 / 16
            if y + 1 < h:
                if x > 0:
                    arr[y + 1, x - 1] += error * 3 / 16
                arr[y + 1, x] += error * 5 / 16
                if x + 1 < w:
                    arr[y + 1, x + 1] += error * 1 / 16
    arr = np.clip(arr * 255, 0, 255)
    return arr.astype(np.uint8)


def atkinson_dither(image_array: np.ndarray) -> np.ndarray:
    """Apply Atkinson dithering to a grayscale image array (0–255)."""
    arr = image_array.astype(float) / 255.0
    h, w = arr.shape
    for y in range(h):
        for x in range(w):
            old_pixel = arr[y, x]
            new_pixel = round(old_pixel)
            arr[y, x] = new_pixel
            error = (old_pixel - new_pixel) / 8
            # Diffuse error according to Atkinson matrix
            for dx, dy in [(1,0), (2,0), (-1,1), (0,1), (1,1), (0,2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    arr[ny, nx] += error
    arr = np.clip(arr * 255, 0, 255)
    return arr.astype(np.uint8)


def apply_dithering(image_array: np.ndarray, method: str = "none") -> np.ndarray:
    """Wrapper to select dithering method."""
    if method == "floyd":
        return floyd_steinberg_dither(image_array)
    elif method == "atkinson":
        return atkinson_dither(image_array)
    else:
        return image_array
