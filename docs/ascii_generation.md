# ASCII Generation Feature

## What it is
The ASCII generation feature divides the resized image into a grid of blocks and generates the ASCII art by selecting symbols for each block.

## How it works
1. Resizes the image to the desired width, maintaining aspect ratio.
2. Divides the image into a grid based on the ASCII dimensions.
3. For each block in the grid, calls the symbol selection to get the character.
4. Assembles the characters into rows and joins them into a multi-line string.

## Diagram
```
Resized Image (e.g., 80x40 pixels)
       |
       v
   Divide into Grid (80 columns, 40 rows)
       |
       v
   For each Block:
   |   |
   |   v
   | Select Symbol
   |   |
   |   v
   | Character
   |
   v
Assemble into ASCII String
```