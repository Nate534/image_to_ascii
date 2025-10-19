import argparse
import sys
import os
from .image_processing import load_image
from .output import save_ascii
from .implementations.base_converter import convert_image_to_ascii
from .implementations.cnn_converter import convert_image_to_ascii_cnn

def main():
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument('--output', required=True, help='Output text file')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    parser.add_argument('--method', choices=['pca', 'cnn'], default='pca', help='ASCII conversion method')
    args = parser.parse_args()

    try:
        input_path = os.path.join('images', args.input)
        output_dir = 'ascii'
        output_path = os.path.join(output_dir, args.output)
        os.makedirs(output_dir, exist_ok=True)

        img = load_image(input_path)

        if args.method == 'cnn':
            ascii_art = convert_image_to_ascii_cnn(img, args.width)
        else:
            ascii_art = convert_image_to_ascii(img, args.width)

        save_ascii(ascii_art, output_path)
        print(f'ASCII art saved to {output_path}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
