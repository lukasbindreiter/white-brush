from typing import Tuple

import cv2
import numpy as np


def rgb_to_hsv(color: np.ndarray) -> np.ndarray:
    """
    Convert a color from the RGB colorspace to the HSV colorspace

    >>> rgb_to_hsv(np.array([10, 20, 30], np.uint8))
    array([105, 170, 30])

    Args:
        color: Color as numpy array. Can either have shape (X, Y, 3)
            if it is a whole image, (N, 3) if it is a list of colors
            or just (3) if it is a single color.
            The dtype of the array needs to be uint8

    Returns:
        The converted color in a numpy array the same shape as the
        given array

    """
    return __convert_color__(color, cv2.COLOR_RGB2HSV)


def hsv_to_rgb(color):
    """
    Convert a color from the HSV colorspace to the RGB colorspace

    >>> hsv_to_rgb(np.array([105, 170, 30], np.uint8))
    array([10, 20, 30])

    Args:
        color: Color as numpy array. Can either have shape (X, Y, 3)
            if it is a whole image, (N, 3) if it is a list of colors
            or just (3) if it is a single color.
            The dtype of the array needs to be uint8

    Returns:
        The converted color in a numpy array the same shape as the
        given array

    """
    return __convert_color__(color, cv2.COLOR_HSV2RGB)


def rgb_to_gray(color: np.ndarray) -> np.ndarray:
    """
    Convert a color from the RGB colorspace to a grayscale image

    >>> rgb_to_gray(np.array([34, 35, 36], np.uint8))
    array([35])

    Args:
        color: Color as numpy array. Can either have shape (X, Y, 3)
            if it is a whole image, (N, 3) if it is a list of colors
            or just (3) if it is a single color.
            The dtype of the array needs to be uint8

    Returns:
        The converted color in a numpy array

    """
    return __convert_color__(color, cv2.COLOR_RGB2GRAY, n_target_channels=1)


def gray_to_rgb(color: np.ndarray) -> np.ndarray:
    """
    Convert a grayscale color to a RGB image

    >>> gray_to_rgb(np.array([34], np.uint8))
    array([34, 34, 34])

    Args:
        color: Color as numpy array. Can either have shape (X, Y) if
            it is a whole image, or (N) if it is a list of grayscale
            colors. In that case, N can also be 1

    Returns:
        The converted color in a numpy array
    """
    return __convert_color__(color, cv2.COLOR_GRAY2RGB, n_src_channels=1)


def mask_to_rgb(mask: np.ndarray,
                bg_color: Tuple[int, int, int] = (255, 255, 255),
                fg_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Convert a 2D boolean mask into an RGB image

    This is done by replacing the pixels which are False in the mask
    with the background color and the pixels which are True with the
    foreground color

    Args:
        mask: Boolean numpy array of shape (X, Y)
        bg_color: Color substituted for False values in the mask
            By default this is white
        fg_color: Color substituded for True values in the mask
            By default this is black

    Returns:
        RGB Image of shape (X, Y, 3)
    """
    bg_color = np.asarray(bg_color).astype(np.uint8)
    fg_color = np.asarray(fg_color).astype(np.uint8)
    rgb = np.empty(mask.shape + (3,), np.uint8)
    rgb[:, :] = bg_color
    rgb[mask] = fg_color
    return rgb


def __convert_color__(color, conversion_code, n_src_channels=3,
                      n_target_channels=3):
    assert color.dtype == np.uint8
    # color needs to be of shape (X, Y, color_values) for the opencv cvtColor
    # functions. Therefore if it is not in that shape, reshape it first
    # and then restore the original shape later on
    target_shape = list(color.shape)
    if n_src_channels == 1 and color.size > 1:
        target_shape.append(n_target_channels)
    else:
        target_shape[-1] = n_target_channels

    if n_src_channels == 1:
        assert color.ndim <= 2, "Single channel color cannot be 3D"
    else:
        # if the input is for example a list of RGB colors,
        # it will have shape (N, 3) which is two dimensional
        # cvtColor expects it to be an image, so reshape it to (N, 1, 3)
        if color.ndim != 3:
            color = color.reshape(-1, 1, n_src_channels)

    return np.squeeze(
        cv2.cvtColor(color, conversion_code).reshape(*target_shape))
