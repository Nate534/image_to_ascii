# Image Loading Feature

## What it is
The image loading feature is responsible for loading an image from a specified file path and preparing it for ASCII conversion by converting it to grayscale.

## How it works
1. Opens the image file using PIL (Pillow).
2. Converts the image to grayscale mode ('L') to simplify processing.
3. Returns the grayscale image object for further use.

## Diagram
```
Input File (e.g., photo.jpg)
       |
       v
   PIL.open() --> Grayscale Conversion
       |
       v
   Grayscale Image Object
```