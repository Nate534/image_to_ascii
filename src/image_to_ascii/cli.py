import argparse
import sys
from pathlib import Path
from .implementations.method import Filter
from .implementations.network.streamer import run_server
import asyncio


# I Moved The rest of the function to ./utils/process file
# for better readability

from .utils.process import print_red
from .utils.process import single_process, multi_batch
from .utils.process import ASCII_DIRNAME


def main():
    parser = argparse.ArgumentParser(description="Convert image to ASCII art")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input",
        help='Comma-separated list of image filenames or "all" to process all images',
    )
    input_group.add_argument("--dir", help="Input folder path containing images")
    parser.add_argument(
        "--input-dir", help="Directory to read images from (used with --input)"
    )
    parser.add_argument(
        "--output",
        help="Output text file (for single image) or output directory (for batch)",
    )
    parser.add_argument("--width", type=int, default=80, help="Width of ASCII art")
    parser.add_argument(
        "--method",
        choices=["pca", "cnn", "edge"],
        default="pca",
        help="ASCII conversion method",
    )
    parser.add_argument(
        "--web-view",
        action="store_true",
        help="Generate an HTML gallery and open it in a browser after batch processing (only for --dir)",
    )
    parser.add_argument(
        "--mode",
        choices=[choice.name for choice in Filter],
        default=Filter.LUMINANCE.name,
        help="Grayscale conversion method used",
    )
    parser.add_argument(
        "--web-stream",
        action="store_true",
        help="stream the webcam to ascii over websocket",
    )

    args = parser.parse_args()

    # Validate argument combinations
    if args.input_dir and args.dir:
        parser.error(
            "--input-dir cannot be used with --dir (use --input in combination with --input-dir)"
        )

    elif args.web_stream:
        try:
            print("... starting ")
            asyncio.run(run_server())
        except KeyboardInterrupt:
            print("Closing Stream Server...")
            return

    try:
        if args.dir:
            # previous: --dir flag
            out_dir = args.output if args.output else ASCII_DIRNAME
            multi_batch(
                args.dir,
                args.width,
                out_dir,
                web_view=args.web_view,
                method=args.method,
            )
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
                multi_batch(
                    str(input_dir),
                    args.width,
                    out_dir,
                    web_view=args.web_view,
                    method=args.method,
                )
            else:
                # Parsing comma separated filenames
                filenames = [f.strip() for f in args.input.split(",") if f.strip()]

                if not filenames:
                    print_red(
                        "No valid filenames provided (use comma separated filenames)"
                    )
                    sys.exit(1)

                # Checking if single file or multiple files
                if len(filenames) == 1:
                    # Single file
                    if not args.output:
                        parser.error(
                            "--output is required when processing a single image"
                        )

                    input_path = input_dir / filenames[0]
                    single_process(
                        str(input_path),
                        args.output,
                        args.width,
                        method=args.method,
                        web_view=args.web_view,
                    )
                else:
                    # Batch mode with specific files
                    out_dir = args.output if args.output else ASCII_DIRNAME
                    multi_batch(
                        str(input_dir),
                        args.width,
                        out_dir,
                        web_view=args.web_view,
                        method=args.method,
                        specific_files=filenames,
                    )
    except Exception as e:
        print_red(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
