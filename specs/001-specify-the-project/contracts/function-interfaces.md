# Function Interfaces for Image to ASCII Generator

## Overview
This document describes the key function interfaces for the CLI application. Since this is a command-line tool, interfaces are defined as function signatures rather than HTTP endpoints.

## Core Functions

### load_image(path: str) -> Image
- **Description**: Loads an image from the given file path and converts it to grayscale.
- **Parameters**:
  - path: String path to the image file (e.g., 'image.jpg')
- **Returns**: PIL Image object in grayscale mode
- **Errors**: Raises IOError if file not found or format unsupported

### image_to_ascii(img: Image, width: int = 80) -> str
- **Description**: Converts a grayscale image to ASCII art string using advanced math for symbol selection.
- **Parameters**:
  - img: PIL Image object
  - width: Desired width of ASCII output (default 80)
- **Returns**: Multi-line string representing the ASCII art
- **Errors**: Raises ValueError if width is invalid

### save_ascii(ascii_art: str, path: str) -> None
- **Description**: Saves the ASCII art to a text file.
- **Parameters**:
  - ascii_art: String of ASCII art
  - path: Output file path (e.g., 'output.txt')
- **Returns**: None
- **Errors**: Raises IOError if write fails

## CLI Entry Point
- Command: `python -m image_to_ascii.cli --input <path> --output <path> --width <int>`
- Actions map to the above functions in sequence.