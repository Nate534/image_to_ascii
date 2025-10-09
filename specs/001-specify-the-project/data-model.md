# Data Model for Image to ASCII Generator

## Entities

### Image
- **Description**: Represents the input image file.
- **Fields**:
  - format: String (e.g., 'JPEG', 'PNG')
  - dimensions: Tuple (width: int, height: int)
  - pixel_data: NumPy array of grayscale values (0-255)
- **Relationships**: Converted to ASCII Art.
- **Validation Rules**:
  - Format must be supported (JPEG, PNG, etc.).
  - Dimensions must be positive integers.
  - Pixel data must be a valid 2D array.

### ASCII Art
- **Description**: Represents the output text-based representation.
- **Fields**:
  - symbols: List of strings (rows of ASCII characters)
  - dimensions: Tuple (width: int, height: int)
  - layout: String (the full ASCII art as multi-line string)
- **Relationships**: Generated from Image.
- **Validation Rules**:
  - Symbols must be valid ASCII characters.
  - Dimensions must match the number of characters in layout.
  - Layout must be a valid string without invalid characters.

## State Transitions
- N/A (stateless conversion process).