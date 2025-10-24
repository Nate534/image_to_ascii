from ..implementations.method import Filter
from PIL import Image, ImageOps
import sys
import os
import webbrowser
from ..implementations.base_converter import convert_image_to_ascii_old
from ..implementations.cnn_converter import convert_image_to_ascii_cnn
from ..implementations.edged_converter import convert_image_to_ascii_outlined

from ..web_view import generate_gallery_html
from ..image_processing import load_image
from ..output import save_ascii

from pathlib import Path
import time

ALLOWED_EXT = ["jpeg", "jpg", "png", "webp"]
THUMBS_DIRNAME = "thumbnails"
ASCII_DIRNAME = "ascii"


def safe_filename(st: str):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in st)


def human_time(seconds: float):
    if seconds < 1.0:
        return f"{seconds * 1000:.0f}ms"
    return f"{seconds:.2f}s"


def safe_filename(st: str):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in st)


def make_thumbnail(img_path: str, thumb_path: str, max_size=(240, 240)):
    with Image.open(img_path) as im:
        im = ImageOps.exif_transpose(im)
        im.thumbnail(max_size, Image.LANCZOS)
        rgb = im.convert("RGB")
        rgb.save(thumb_path, format="JPEG", quality=85)


def print_green(data, end="\n", file=sys.stdout):
    print(f"\033[92m{data}\033[00m", end=end, file=file)


def print_red(data, end="\n", file=sys.stdout):
    print(f"\033[91m{data}\033[00m", end=end, file=file)


def multi_batch(
    dir_path,
    width,
    mode: Filter = Filter.LUMINANCE,
    output_dir="ascii",
    web_view=False,
    method="pca",
    specific_files=None,
):
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
        print(entry)
        if not entry.is_file():
            continue
        ext = entry.suffix.lower().lstrip(".")
        if ext not in ALLOWED_EXT:
            continue

        try:
            start = time.perf_counter()
            img = load_image(str(entry), mode)
            if method == "cnn":
                ascii_art = convert_image_to_ascii_cnn(img, width)
            elif method == "edge":
                ascii_art = convert_image_to_ascii_outlined(img, width)
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

            gallery_items.append(
                {
                    "filename": entry.name,
                    "orig_w": img.width,
                    "orig_h": img.height,
                    "ascii_w": aw,
                    "ascii_h": ah,
                    "proc_time": proc_time,
                    "thumb_rel": os.path.join(THUMBS_DIRNAME, thumb_name),
                    "ascii_rel": os.path.join(ASCII_DIRNAME, out_name),
                    "ascii_text": ascii_art,
                }
            )

            processed += 1
            print_green(f"[{processed}] ASCII art saved to {out_path}")
        except Exception as e:
            print_red(f"Failed: {entry.name} : {e}")

    end_ts = time.perf_counter()
    delta = end_ts - begin_ts
    timing = f"{delta:.2f}s" if delta >= 1 else f"{(delta * 1000):.2f}ms"
    print_green(f"{timing} taken to process {processed} images", end="")

    if web_view:
        html_path = output_dir / "gallery.html"
        generate_gallery_html(gallery_items, str(html_path))
        try:
            webbrowser.open_new_tab(str(html_path.resolve()))
            print_green(f"\nOpened gallery at {html_path}")
        except Exception:
            print_green(f"\nGallery written to {html_path} (open manually)")


def single_process(
    input_path,
    output_path,
    width,
    mode: Filter = Filter.LUMINANCE,
    method="pca",
    web_view=False,
):
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
        img = load_image(str(input_path), mode)

        if method == "cnn":
            ascii_art = convert_image_to_ascii_cnn(img, width)

        elif method == "edge":
            ascii_art = convert_image_to_ascii_outlined(img, width)
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

            gallery_items.append(
                {
                    "filename": input_path.name,
                    "orig_w": img.width,
                    "orig_h": img.height,
                    "ascii_w": aw,
                    "ascii_h": ah,
                    "proc_time": "N/A",
                    "thumb_rel": thumb_name,
                    "ascii_rel": output_path.name,
                    "ascii_text": ascii_art,
                }
            )

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
    timing = f"{delta:.2f}s" if delta >= 1 else f"{(delta * 1000):.2f}ms"
    print_green(f"{timing} taken to process 1 image", end=" ")
