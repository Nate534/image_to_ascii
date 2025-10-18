# ASCII Conversion Implementations

This directory contains different algorithms for converting images to ASCII art. Each implementation is a standalone Python file that can be used independently.

## Current Implementations

### pca_converter.py
The original implementation using Principal Component Analysis (PCA) to match image blocks with ASCII characters based on their eigenvalue signatures.

**Mathematical Approach:**
- Computes PCA features for each ASCII character
- Analyzes image blocks using eigenvalue decomposition
- Matches blocks to characters using Euclidean distance in eigenspace

## Contributing New Implementations

Want to add your own ASCII conversion algorithm? Here's how:

### 1. Use the Template
Copy `base_converter.py` and rename it to `your_algorithm_converter.py`

### 2. Implement Your Algorithm
Replace the template function with your conversion logic:

```python
def convert_image_to_ascii(img: Image.Image, width: int) -> str:
    # Your algorithm here
    pass
```

### 3. Document Your Math
Include detailed documentation about:
- Mathematical concepts used
- Formulas and equations
- Algorithm complexity
- References to papers/resources

### 4. Test Thoroughly
- Test with various image types
- Verify output quality
- Check edge cases (empty images, single pixels, etc.)

## Implementation Ideas

Check out [HACKTOBERFEST_ISSUES.md](../../../HACKTOBERFEST_ISSUES.md) for specific algorithms to implement:

- **brightness_converter.py**: Simple brightness-to-character mapping
- **edge_converter.py**: Edge detection based ASCII art
- **dithering_converter.py**: Floyd-Steinberg dithering
- **frequency_converter.py**: Frequency domain analysis
- **texture_converter.py**: Local Binary Pattern matching
- **neural_converter.py**: CNN-based character selection
- **wavelet_converter.py**: Wavelet transform analysis

## File Structure

Each implementation should be self-contained:

```python
"""
Your Algorithm Name - Brief Description

Detailed explanation of your mathematical approach.
"""

import numpy as np
from PIL import Image

def convert_image_to_ascii(img: Image.Image, width: int) -> str:
    """Main conversion function."""
    # Your implementation
    pass

def helper_function():
    """Any helper functions you need."""
    pass
```

## Testing Your Implementation

Create a simple test script:

```python
from PIL import Image
from your_converter import convert_image_to_ascii

# Load test image
img = Image.open('test.jpg').convert('L')

# Convert to ASCII
ascii_art = convert_image_to_ascii(img, 80)

# Save result
with open('output.txt', 'w') as f:
    f.write(ascii_art)
```

## Mathematical Resources

- **Linear Algebra**: NumPy documentation
- **Image Processing**: PIL/Pillow documentation  
- **Computer Vision**: OpenCV tutorials
- **Signal Processing**: SciPy documentation
- **Machine Learning**: Scikit-learn guides

Happy coding! 🎨