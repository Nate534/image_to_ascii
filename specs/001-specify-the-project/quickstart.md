# Quickstart Guide for Image to ASCII Generator

## Installation
1. Ensure Python 3.8+ is installed.
2. Install dependencies: `pip install Pillow numpy`
3. Clone or download the project code.

## Usage
Run the converter from the command line:
```
python -m src.image_to_ascii.cli --input path/to/image.jpg --output output.txt --width 80
```

## Example
Convert a sample image:
```
python -m src.image_to_ascii.cli --input sample.png --width 100
```
This will print the ASCII art to the console.

## Features
- Supports JPEG, PNG images.
- Adjustable output width.
- Saves to file or displays in terminal.
- Uses advanced math for symbol selection.

For more details, see the docs/ folder for per-feature explanations.