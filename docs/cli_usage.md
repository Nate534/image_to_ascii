# CLI Usage Feature

## What it is
The CLI usage feature provides a command-line interface to run the image to ASCII converter.

## How it works
1. Parses command-line arguments using argparse.
2. Calls the image loading, conversion, and saving modules.
3. Handles errors and provides feedback.

## Diagram
```
Command Line: python -m src.image_to_ascii.main --input image.jpg --output ascii.txt --width 80
       |
       v
   Parse Arguments
       |
       v
   Load Image --> Convert to ASCII --> Save to File
       |
       v
   Print Success Message or Error
```

## Usage Examples
- Basic conversion: python -m src.image_to_ascii.main --input photo.png --output art.txt
- Custom width: python -m src.image_to_ascii.main --input image.jpg --output ascii.txt --width 100