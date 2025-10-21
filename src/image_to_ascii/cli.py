import argparse
import sys
import os
import time
from .image_processing import load_image
from .output import save_ascii
from .implementations.base_converter import convert_image_to_ascii
from .implementations.cnn_converter import convert_image_to_ascii_cnn
from .implementations.brightness_converter import convert_image_to_ascii_brightness

ALLOWED_EXT = ["jpeg", "jpg", "png", "webp"]

def print_green(data, end="\n", file=sys.stdout):
    print(f"\033[92m{data}\033[00m", end=end, file=file)

def print_red(data, end="\n", file=sys.stderr):
    print(f"\033[91m{data}\033[00m", end=end, file=file)

def multi_batch(dir_path, width, method="pca", dithering="none"):
    output_dir = 'ascii/'
    lsdir = os.listdir(dir_path)
    dir_len = len(lsdir)
    os.system("clear")
    begin_timestamp = time.perf_counter()

    for index, img_path in enumerate(lsdir):
        image_name = os.path.splitext(img_path)[0]
        extension = img_path.split(".")[-1].lower()

        if extension in ALLOWED_EXT:
            full_image_path = os.path.join(dir_path, img_path)
            img = load_image(full_image_path)

            if method == 'cnn':
                ascii_art = convert_image_to_ascii_cnn(img, width)
            elif method == 'brightness':
                ascii_art = convert_image_to_ascii_brightness(img, width, dithering=dithering)
            else:
                ascii_art = convert_image_to_ascii(img, width, dithering=dithering)

            output_path = os.path.join(output_dir, image_name + ".txt")
            os.makedirs(output_dir, exist_ok=True)
            save_ascii(ascii_art, output_path)
            print_green(f'[{index+1}/{dir_len}] ASCII art saved to {output_path}')

    end_timestamp = time.perf_counter()
    delta = end_timestamp - begin_timestamp
    delta = f"{delta:.2f}s" if delta > 1 else f"{(delta*1000):.2f}ms"
    print_green(delta, end="")
    print(f" taken to process {dir_len} images")

def single_process(input_file, output_file, width, method="pca", dithering="none"):
    input_path = input_file  
    output_dir = 'ascii/'
    extension = input_file.split(".")[-1].lower()
    begin_timestamp = time.perf_counter()

    if extension in ALLOWED_EXT:
        output_path = os.path.join(output_dir, output_file)
        os.makedirs(output_dir, exist_ok=True)

        img = load_image(input_path)

        if method == 'cnn':
            ascii_art = convert_image_to_ascii_cnn(img, width)
        elif method == 'brightness':
            ascii_art = convert_image_to_ascii_brightness(img, width, dithering=dithering)
        else:
            ascii_art = convert_image_to_ascii(img, width, dithering=dithering)

        save_ascii(ascii_art, output_path)
        print_green(f'ASCII art saved to {output_path}')

    end_timestamp = time.perf_counter()
    delta = end_timestamp - begin_timestamp
    delta = f"{delta:.2f}s" if delta > 1 else f"{(delta*1000):.2f}ms"
    print_green(delta, end="")
    print(f" taken to process 1 image")

def main():
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', help='Input image file')
    input_group.add_argument('--dir', help='Input folder path containing images')
    parser.add_argument('--output', required=True, help='Output text file')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    parser.add_argument(
        '--method',
        choices=['pca', 'cnn', 'brightness'],
        default='pca',
        help='ASCII conversion method'
    )
    parser.add_argument(
        '--dithering',
        choices=['none', 'floyd', 'atkinson'],
        default='none',
        help='Dithering method'
    )

    args = parser.parse_args()

    try:
        if args.input:
            single_process(args.input, args.output, args.width, method=args.method, dithering=args.dithering)
        elif args.dir:
            multi_batch(args.dir, args.width, method=args.method, dithering=args.dithering)
    except Exception as e:
        print_red(f'Error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
