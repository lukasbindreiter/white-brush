import cv2
import numpy as np
import webcolors


def rgb_to_hsv(color: np.ndarray) -> np.ndarray:
    """
    Convert a color from the RGB colorspace to the HSV colorspace

    >>> rgb_to_hsv(np.array([10, 20, 30]))
    array([105, 170, 30])

    Args:
        color: Color as numpy array. Can either have shape (X, Y, 3)
            if it is a whole image, or just have three elements if it
            is a single color. The dtype of the array needs to be uint8

    Returns:
        The converted color in a numpy array the same shape as the
        given array

    """
    return __convert_color__(color, cv2.COLOR_RGB2HSV)


def hsv_to_rgb(color):
    """
    Convert a color from the HSV colorspace to the RGB colorspace

    >>> hsv_to_rgb(np.array([105, 170, 30]))
    array([10, 20, 30])

    Args:
        color: Color as numpy array. Can either have shape (X, Y, 3)
            if it is a whole image, or just have three elements if it
            is a single color. The dtype of the array needs to be uint8

    Returns:
        The converted color in a numpy array the same shape as the
        given array

    """
    return __convert_color__(color, cv2.COLOR_HSV2RGB)


def __convert_color__(color, conversion_code):
    assert color.dtype == np.uint8
    # color needs to be of shape (X, Y, 3) for the opencv cvtColorexception
    # functions. Therefore if it is not in that shape, reshape it first
    # and then restore the original shape later on
    orig_shape = color.shape
    if color.ndim != 3:
        color = color.reshape(-1, 1, 3)
    return cv2.cvtColor(color, conversion_code).reshape(*orig_shape)


def parse_color(color):
    """
    Parses the given color text to rgb values in format (255,255,255).

    Args:
        color: color text to be parsed in format 'red', '#728599', and 255,255,255

    Returns:
        Returns the parsed color as rgb value or None if not parseable.
    """
    try:
        color = webcolors.name_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        color = webcolors.hex_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        data = color.split(",")
        return int(data[0]), int(data[1]), int(data[2])
    except Exception:
        pass

    return None
