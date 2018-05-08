import numpy as np


def color_sample(img: np.ndarray, p: float = 0.05) -> np.ndarray:
    """
    Get a representative color sample of the given image.

    Returns a subset of the color values of the given image which has a size of roughly the given percentage.

    Args:
        img: The image of shape (X, Y, 3) for which to extract a color_sample
        p: The percentage of pixels to sample

    Returns: Color sample of shape (N, 3)
    """
    ravelled = img.reshape(-1, 3)
    # for 5%, take every 20th value, for 10% every 10th, etc...
    every_nth = int(1/p)
    return ravelled[::every_nth, :]
