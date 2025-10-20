import argparse
import sys
import os
from .image_processing import load_image
from .output import save_ascii
from .implementations.base_converter import convert_image_to_ascii
from .implementations.cnn_converter import convert_image_to_ascii_cnn
from .implementations.edged_converter import convert_image_to_ascii as citae
import time

ALLOWED_EXT=["jpeg","jpg","png","webp"]

def print_green(data,end="\n",file=sys.stdout):
    print(f"\033[92m{data}\033[00m",end=end,file=file)

def print_red(data,end="\n",file=sys.stdout):
    print(f"\033[91m{data}\033[00m",end=end,file=file)

def multi_batch(dir,width,func):
    output_dir = 'ascii/'
    lsdir=os.listdir(dir)
    dir_len=len(lsdir)
    os.system("clear")
    begin_timestamp=time.perf_counter()
    
    for index,img_path in enumerate(lsdir):
        image_name=img_path.split(".")[0]
        extension=img_path.split(".")[-1]

        if extension in ALLOWED_EXT:
            full_image_path = os.path.join(dir, img_path)
            img = load_image(full_image_path)
            ascii_art = func(img, width)
            output_path= os.path.join(output_dir, image_name+".txt")
            os.makedirs(output_dir, exist_ok=True)
            save_ascii(ascii_art, output_path)
            print_green(f'[{index+1}/{dir_len}] ASCII art saved to {output_path}')
            
    end_timestamp=time.perf_counter()
    delta=(end_timestamp-begin_timestamp)
    delta= f"{delta:.2f}s" if delta>1 else f"{(delta*1000):.2f}ms"
    print_green(delta,end="")
    print(f" taken to process {dir_len} images")


def single_process(input,output,width,func):
    input_path = 'images/' + input 
    output_dir = 'ascii/'
    extension=input.split(".")[-1]
    begin_timestamp=time.perf_counter()

    if extension in ALLOWED_EXT:
        output_path = os.path.join(output_dir, output)
        os.makedirs(output_dir, exist_ok=True)

        img = load_image(input_path)
        ascii_art = func(img, width)
        save_ascii(ascii_art, output_path)
        print_green(f'ASCII art saved to {output_path}')

    end_timestamp=time.perf_counter()
    delta=(end_timestamp-begin_timestamp)
    delta= f"{delta:.2f}s" if delta>1 else f"{(delta*1000):.2f}ms"
    print_green(delta,end="")
    print(f" taken to process 1 images")


def main():
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    input_group=parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', help='Input image file')
    input_group.add_argument('--dir', help='Input folder path containing images')
    parser.add_argument('--output', required=True, help='Output text file')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    parser.add_argument("--outlined",type=int,default=0,choices=[1,0],help="draws an edge contour around the image")
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
    
        if args.outlined==1:
            func=citae #renamed convert_image_to_ascii for edge detection
        else:
            func=convert_image_to_ascii

        save_ascii(ascii_art, output_path)
        if args.input:
            single_process(args.input,args.output,args.width,func)
        elif args.dir:
            multi_batch(args.dir,args.width,func)

    except Exception as e:
        print_red(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
