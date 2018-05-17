import cv2
import numpy as np
import os


def read_image(filename: str):
    """
    Read an image from disk

    Read an image from disk and return it as matrix of size
    (width, height, 3) in the RGB Format.

    Args:
        filename: The image file to read

    Returns: Three dimensional numpy array.

    """
    img = cv2.imread(filename)

    if img is None:
        if os.path.exists(filename):
            raise OSError(f'"{filename}" is not a valid image file.')
        else:
            raise FileNotFoundError(f'No such file or directory: "{filename}"')

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def write_image(file_name: str, img: np.ndarray):
    """
    Write an image to disk

    The format is based on the extension provided in the filename

    Args:
        file_name: The name of the image file that will be created
            If the specified file is within a directory which does not
            exist, that directory will be created
        img: The image to write, in RGB Format
    """

    dirs = os.path.dirname(file_name)
    if len(dirs) > 0:
        os.makedirs(dirs, exist_ok=True)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(file_name, img)
