import os

from white_brush.io import read_image


def get_test_images():
    """
    Generator over all images in the `test_images` directory

    Usage example:
    >>> for img_name, img in get_test_images():
    >>>    print(img_name)

    Returns: Generator
    """
    for image in os.listdir("test_images"):
        yield image, read_image(os.path.join("test_images", image))
