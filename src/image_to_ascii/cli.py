import argparse
import sys
from .image_processing import load_image
from .ascii_conversion import image_to_ascii
from .output import save_ascii

def main():
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output text file')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    args = parser.parse_args()
    
    try:
        input_path = 'images/' + args.input
        output_path = 'ascii/' + args.output
        img = load_image(input_path)
        ascii_art = image_to_ascii(img, args.width)
        save_ascii(ascii_art, output_path)
        print(f'ASCII art saved to {output_path}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()