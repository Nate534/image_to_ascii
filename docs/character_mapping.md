# Character Mapping Feature

## What it is
The character mapping feature selects the best ASCII character for each block of the image based on statistical moments to match the visual density and shape.

## How it works
1. Precomputes statistical moments for each ASCII character.
2. For each image block, computes its moments.
3. Calculates the Euclidean distance between the block's moments and each character's moments.
4. Selects the character with the smallest distance.

## Diagram
```
Image Block
       |
       v
   Compute Moments (mu00, mu10, etc.)
       |
       v
   Compare to Precomputed Char Moments
       |
       v
   Select Char with Min Distance
       |
       v
   ASCII Character
```

| Character | Density | Example Moments |
|-----------|---------|------------------|
| @ | High | mu00: 45, mu10: 2.1 |
| # | Medium | mu00: 30, mu10: 1.8 |
| . | Low | mu00: 5, mu10: 0.5 |