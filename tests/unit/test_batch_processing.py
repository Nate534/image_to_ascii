from image_to_ascii.cli import multi_batch
from pathlib import Path


def test_multi_batch():
    read_dir = "timages/"
    out_dir = "tascii/"
    multi_batch(read_dir, 50, output_dir=out_dir)


def test_multi_batch():
    test_images_dir = Path("test_images")
    test_out_image = Path("test_ascii")

    assert test_images_dir.exists()

    multi_batch(
        dir_path=test_images_dir,
        width=80,
        output_dir=test_out_image,
    )

    ascii_dir = test_out_image / "ascii"
    assert ascii_dir.exists()

    ascii_files = list(ascii_dir.glob("*.txt"))
    total_input_images = len(list(test_images_dir.glob("*")))

    assert len(ascii_files) <= total_input_images, "all image not fully bieng generated"
