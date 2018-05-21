import os
from typing import Tuple, Iterator

import numpy as np

from white_brush.io import read_image


def get_test_image() -> Tuple[str, np.ndarray]:
    """
    Return the name and the data of the first image in the `test_images`
    directory

    Usage example:
    >>> img_name, img = get_test_image()
    >>> img_name
    "01.png"

    Returns:
         name and data of the image

    """
    return next(get_test_images())


def get_test_images() -> Iterator[Tuple[str, np.ndarray]]:
    """
    Iterate over all images in the `test_images` directory

    Usage example:
    >>> for img_name, img in get_test_images():
    >>>    print(img_name)

    Returns:
        Generator over all images in the `test_images` directory

    """
    for image in os.listdir("test_images"):
        if image.startswith("."):
            continue
        yield image, read_image(os.path.join("test_images", image))
