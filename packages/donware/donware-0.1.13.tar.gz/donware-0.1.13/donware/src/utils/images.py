from pathlib import Path
from PIL import Image
import numpy as np


def trim_white_margins(dir_from: Path, dir_to: Path, white_tolerance: int = 10):
    """
    Trims white margins from images in a directory, makes white pixels transparent, and saves the cropped images to a new directory.

    Parameters:
    dir_from (Path): The source directory containing the images to be processed.
    dir_to (Path): The target directory where the processed images will be saved.
    white_tolerance (int): The tolerance level for white color detection (default is 10).

    Example:
    >>> from pathlib import Path
    >>> trim_white_margins(Path('input_images'), Path('output_images'), white_tolerance=15)

    Input:
    - A directory 'input_images' containing images with white margins.

    Output:
    - A directory 'output_images' containing images with white margins cropped and white pixels made transparent.
    """

    assert dir_from.is_dir(), f"Directory '{dir_from}' not found."
    dir_from, dir_to = Path(dir_from), Path(dir_to)
    dir_to.mkdir(parents=True, exist_ok=True)

    for image_path in list(dir_from.glob("*.png")) + list(dir_from.glob("*.jpg")) + list(dir_from.glob("*.jpeg")):
        image = Image.open(image_path).convert("RGBA")
        img_array = np.array(image)
        non_white_pixels = np.where(
            np.all(img_array[:, :, :3] >= [255 - white_tolerance] * 3, axis=-1) & (img_array[:, :, 3] != 0) == False
        )

        if non_white_pixels[0].size == 0:
            y_min, y_max = 0, 0
            x_min, x_max = 0, 0
        else:
            y_min, y_max = non_white_pixels[0].min(), non_white_pixels[0].max()
            x_min, x_max = non_white_pixels[1].min(), non_white_pixels[1].max()

        cropped_img = img_array[y_min : y_max + 1, x_min : x_max + 1]
        white_areas = np.all(cropped_img[:, :, :3] >= [255 - white_tolerance] * 3, axis=-1)
        cropped_img[white_areas, 3] = 0
        cropped_image = Image.fromarray(cropped_img, "RGBA")
        cropped_image.save(dir_to / image_path.name)
