import cv2
import numpy as np


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
    # color can either be of shape (X, Y, 3) if it is an image
    # or just shape (3,) if it is a single color
    orig_shape = color.shape
    if color.ndim == 1 and color.size == 3:
        color = color.reshape(1, 1, 3)
    return cv2.cvtColor(color, conversion_code).reshape(*orig_shape)
