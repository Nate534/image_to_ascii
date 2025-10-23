import argparse
import sys
import os
import time
import webbrowser
from pathlib import Path
from PIL import Image, ImageOps
from .image_processing import load_image
from .output import save_ascii
from .implementations.base_converter import convert_image_to_ascii, convert_image_to_ascii_old
from .implementations.cnn_converter import convert_image_to_ascii_cnn
from .web_view import generate_gallery_html

ALLOWED_EXT=["jpeg","jpg","png","webp"]
THUMBS_DIRNAME = "thumbnails"
ASCII_DIRNAME = "ascii"

def print_green(data,end="\n",file=sys.stdout):
    print(f"\033[92m{data}\033[00m",end=end,file=file)

def print_red(data,end="\n",file=sys.stdout):
    print(f"\033[91m{data}\033[00m",end=end,file=file)

def safe_filename(st: str):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in st)

def make_thumbnail(img_path: str, thumb_path: str, max_size=(240, 240)):
    with Image.open(img_path) as im:
        im = ImageOps.exif_transpose(im)
        im.thumbnail(max_size, Image.LANCZOS)
        rgb = im.convert("RGB")
        rgb.save(thumb_path, format="JPEG", quality=85)

def human_time(seconds: float):
    if seconds < 1.0:
        return f"{seconds*1000:.0f}ms"
    return f"{seconds:.2f}s"

def multi_batch(dir_path, width, output_dir="ascii", web_view=False, method="pca", specific_files=None):
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        print_red(f"Input directory not found: {dir_path}")
        return

    output_dir = Path(output_dir)
    ascii_out = output_dir / ASCII_DIRNAME
    thumbs_out = output_dir / THUMBS_DIRNAME
    ascii_out.mkdir(parents=True, exist_ok=True)
    thumbs_out.mkdir(parents=True, exist_ok=True)

    # Filter entries based on specific_files if provided in command
    if specific_files:
        entries = []
        for filename in specific_files:
            file_path = dir_path / filename
            if file_path.is_file():
                entries.append(file_path)
            else:
                print_red(f"File not found: {filename}")
        entries = sorted(entries)
    else:
        entries = sorted(dir_path.iterdir())
    
    processed = 0
    begin_ts = time.perf_counter()
    gallery_items = []

    for entry in entries:
        if not entry.is_file():
            continue
        ext = entry.suffix.lower().lstrip(".")
        if ext not in ALLOWED_EXT:
            continue

        try:
            start = time.perf_counter()
            img = load_image(str(entry))
            if method == "cnn":
                ascii_art = convert_image_to_ascii_cnn(img, width)
            else:
                ascii_art = convert_image_to_ascii_old(img, width)
            # derive ascii dims
            lines = ascii_art.splitlines()
            aw = len(lines[0]) if lines else 0
            ah = len(lines)
            proc_time = human_time(time.perf_counter() - start)

            out_name = entry.stem + ".txt"
            out_path = ascii_out / out_name
            save_ascii(ascii_art, str(out_path))

            # thumbnail
            thumb_name = safe_filename(entry.stem) + ".jpg"
            thumb_path = thumbs_out / thumb_name
            make_thumbnail(str(entry), str(thumb_path))

            gallery_items.append({
                "filename": entry.name,
                "orig_w": img.width,
                "orig_h": img.height,
                "ascii_w": aw,
                "ascii_h": ah,
                "proc_time": proc_time,
                "thumb_rel": os.path.join(THUMBS_DIRNAME, thumb_name),
                "ascii_rel": os.path.join(ASCII_DIRNAME, out_name),
                "ascii_text": ascii_art
            })

            processed += 1
            print_green(f"[{processed}] ASCII art saved to {out_path}")
        except Exception as e:
            print_red(f"Failed: {entry.name} : {e}")

    end_ts = time.perf_counter()
    delta = end_ts - begin_ts
    timing = f"{delta:.2f}s" if delta >= 1 else f"{(delta*1000):.2f}ms"
    print_green(f"{timing} taken to process {processed} images", end="")

    if web_view:
        html_path = output_dir / "gallery.html"
        generate_gallery_html(gallery_items, str(html_path))
        try:
            webbrowser.open_new_tab(str(html_path.resolve()))
            print_green(f"\nOpened gallery at {html_path}")
        except Exception:
            print_green(f"\nGallery written to {html_path} (open manually)")

def single_process(input_path, output_path, width, method="pca", web_view=False):
    input_path = Path(input_path)
    if not input_path.is_file():
        print_red(f"Input file not found: {input_path}")
        return

    ext = input_path.suffix.lower().lstrip(".")
    if ext not in ALLOWED_EXT:
        print_red(f"Unsupported file extension: .{ext}")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    begin_ts = time.perf_counter()
    try:
        img = load_image(str(input_path))
        if method == "cnn":
            ascii_art = convert_image_to_ascii_cnn(img, width)
        else:
            ascii_art = convert_image_to_ascii_old(img, width)
        save_ascii(ascii_art, str(output_path))
        print_green(f"ASCII art saved to {output_path}")

        if web_view:
            # Generate gallery HTML for a single image
            gallery_items = []
            lines = ascii_art.splitlines()
            aw = len(lines[0]) if lines else 0
            ah = len(lines)
            thumb_name = safe_filename(input_path.stem) + ".jpg"
            thumb_path = output_path.parent / thumb_name
            make_thumbnail(str(input_path), str(thumb_path))

            gallery_items.append({
                "filename": input_path.name,
                "orig_w": img.width,
                "orig_h": img.height,
                "ascii_w": aw,
                "ascii_h": ah,
                "proc_time": "N/A",
                "thumb_rel": thumb_name,
                "ascii_rel": output_path.name,
                "ascii_text": ascii_art
            })

            html_path = output_path.parent / "gallery.html"
            generate_gallery_html(gallery_items, str(html_path))
            try:
                webbrowser.open_new_tab(str(html_path.resolve()))
                print_green(f"\nOpened gallery at {html_path}")
            except Exception:
                print_green(f"\nGallery written to {html_path} (open manually)")
    except Exception as e:
        print_red(f"Failed to process {input_path.name} : {e}")
    end_ts = time.perf_counter()
    delta = end_ts - begin_ts
    timing = f"{delta:.2f}s" if delta >= 1 else f"{(delta*1000):.2f}ms"
    print_green(f"{timing} taken to process 1 image", end="")

def main():
    """Command-line interface for image-to-ASCII conversion."""
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    input_group=parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', help='Comma-separated list of image filenames or "all" to process all images')
    input_group.add_argument('--dir', help='Input folder path containing images')
    parser.add_argument('--input-dir', help='Directory to read images from (used with --input)')
    parser.add_argument('--output', help='Output text file (for single image) or output directory (for batch)')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    parser.add_argument('--method', choices=['pca', 'cnn'], default='pca', help='ASCII conversion method')
    parser.add_argument("--web-view", action="store_true", help="Generate an HTML gallery and open it in a browser after batch processing")
    args = parser.parse_args()

    # Validate argument combinations
    if args.input_dir and args.dir:
        parser.error("--input-dir cannot be used with --dir (use --input in combination with --input-dir)")

    try:
        if args.dir:
            # previous: --dir flag
            out_dir = args.output if args.output else ASCII_DIRNAME
            multi_batch(args.dir, args.width, out_dir, web_view=args.web_view, method=args.method)
        elif args.input:
            # new: --input flag
            input_dir = args.input_dir if args.input_dir else "."
            input_dir = Path(input_dir)
            
            if not input_dir.is_dir():
                print_red(f"Input directory not found: {input_dir}")
                sys.exit(1)
            
            if args.input.lower() == "all":
                # Process all images in the directory
                out_dir = args.output if args.output else ASCII_DIRNAME
                multi_batch(str(input_dir), args.width, out_dir, web_view=args.web_view, method=args.method)
            else:
                # Parsing comma separated filenames
                filenames = [f.strip() for f in args.input.split(',') if f.strip()]
                
                if not filenames:
                    print_red("No valid filenames provided (use comma separated filenames)")
                    sys.exit(1)
                
                # Checking if single file or multiple files
                if len(filenames) == 1:
                    # Single file
                    if not args.output:
                        parser.error("--output is required when processing a single image")
                    
                    input_path = input_dir / filenames[0]
                    single_process(str(input_path), args.output, args.width, method=args.method, web_view=args.web_view)
                else:
                    # Batch mode with specific files
                    out_dir = args.output if args.output else ASCII_DIRNAME
                    multi_batch(str(input_dir), args.width, out_dir, web_view=args.web_view, method=args.method, specific_files=filenames)
    except Exception as e:
        print_red(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
